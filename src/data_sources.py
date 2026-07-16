"""Reliable data-source abstraction with AutoSync snapshots and contingency.

The dashboard never writes to the source workbook. Remote and local sources are
copied to immutable snapshots under ``.runtime/snapshots``. A workbook is only
promoted to ``.runtime/last_valid.xlsx`` after the full application parser has
accepted it.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests

try:
    import streamlit as st
except ModuleNotFoundError:  # CLI validation before UI dependencies are installed.
    class _CacheDataFallback:
        def __call__(self, func=None, **_kwargs):
            if func is not None:
                return func
            return lambda wrapped: wrapped

        @staticmethod
        def clear() -> None:
            return None

    class _StreamlitFallback:
        cache_data = _CacheDataFallback()

    st = _StreamlitFallback()

from src.runtime_config import get_int, get_setting

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOCAL_FILE = PROJECT_ROOT / "Dashboard SM CGR 2026.xlsx"
DEFAULT_GOOGLE_SHEETS_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1uvtKSQ4PmUcahUhvHEwrqfyeudb1zNto/export?format=xlsx"
)
DEFAULT_REMOTE_FILENAME = "Dashboard SM CGR 2026.xlsx"
_REMOTE_CACHE_TTL = get_int("AUTO_REFRESH_SECONDS", 120, minimum=15)


class DataSourceError(RuntimeError):
    """Raised when the configured source cannot provide a usable workbook."""


@dataclass(frozen=True)
class PreparedDataSource:
    path: Path
    source_type: str
    display_name: str
    checksum: str
    detail: str
    original_path: str = ""
    modified_at: datetime | None = None
    size_bytes: int = 0
    source_signature: tuple[int, int] = (0, 0)
    snapshot: bool = True
    fallback_used: bool = False
    checked_at: datetime | None = None
    changed_at: datetime | None = None
    etag: str = ""
    last_modified_header: str = ""


def runtime_dir() -> Path:
    configured = str(get_setting("LOCAL_RUNTIME_DIR", ".runtime")).strip() or ".runtime"
    path = Path(configured).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def snapshot_dir() -> Path:
    path = runtime_dir() / "snapshots"
    path.mkdir(parents=True, exist_ok=True)
    return path


def source_state_path() -> Path:
    return runtime_dir() / "source_state.json"


def _atomic_write_bytes(target: Path, content: bytes) -> None:
    """Write bytes atomically using a unique temporary file in the same folder.

    Streamlit can execute the script concurrently for multiple sessions/reruns.
    A fixed ``.tmp`` filename creates a race where one execution moves the file
    before another reaches ``os.replace``. A unique temporary name removes that
    collision while preserving atomic replacement semantics.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent),
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def _atomic_write_text(target: Path, content: str) -> None:
    _atomic_write_bytes(target, content.encode("utf-8"))


def _atomic_copy_file(source: Path, target: Path) -> None:
    """Copy a file and promote it atomically without shared temp filenames."""
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent),
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as destination, source.open("rb") as origin:
            shutil.copyfileobj(origin, destination)
            destination.flush()
            os.fsync(destination.fileno())
        os.replace(temporary, target)
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def quick_file_signature(path: str | Path) -> tuple[int, int]:
    """Return a lightweight local-file change signature."""
    candidate = Path(path).expanduser()
    try:
        stat = candidate.stat()
    except OSError:
        return (0, 0)
    return (int(stat.st_mtime_ns), int(stat.st_size))


def _looks_like_html(content: bytes) -> bool:
    prefix = content[:1024].lstrip().lower()
    return prefix.startswith((b"<!doctype html", b"<html", b"<head", b"<body")) or b"<html" in prefix


def _looks_like_xlsx(content: bytes) -> bool:
    if not content or not content.startswith(b"PK"):
        return False
    try:
        if not zipfile.is_zipfile(BytesIO(content)):
            return False
        with zipfile.ZipFile(BytesIO(content)) as archive:
            names = set(archive.namelist())
            return "[Content_Types].xml" in names and any(name.startswith("xl/") for name in names)
    except (OSError, zipfile.BadZipFile):
        return False


def validate_xlsx_payload(content: bytes, *, content_type: str = "") -> None:
    """Reject HTML/login responses and malformed workbook downloads."""
    normalized_type = content_type.casefold()
    if _looks_like_html(content) or "text/html" in normalized_type:
        raise DataSourceError(
            "O endereço remoto retornou HTML em vez da planilha. Isso normalmente "
            "indica página de login, falta de permissão ou erro temporário do Google."
        )
    if not content:
        raise DataSourceError("A fonte remota retornou um arquivo vazio.")
    if not _looks_like_xlsx(content):
        raise DataSourceError(
            "O conteúdo baixado não é um XLSX válido. A sincronização foi interrompida "
            "para proteger o dashboard e a última versão válida será utilizada."
        )


def _read_stable_local_file(path: Path) -> tuple[bytes, tuple[int, int], datetime]:
    """Read a file only after its metadata remains stable across the read."""
    attempts = get_int("LOCAL_READ_ATTEMPTS", 8, minimum=2)
    delay_seconds = float(get_setting("LOCAL_READ_RETRY_SECONDS", 0.5) or 0.5)
    last_error = "arquivo indisponível"

    for _attempt in range(attempts):
        try:
            before = path.stat()
            content = path.read_bytes()
            after = path.stat()
            before_signature = (int(before.st_mtime_ns), int(before.st_size))
            after_signature = (int(after.st_mtime_ns), int(after.st_size))

            if before_signature != after_signature:
                last_error = "o arquivo mudou durante a leitura"
            elif len(content) != after.st_size:
                last_error = "o tamanho lido não corresponde ao arquivo"
            else:
                validate_xlsx_payload(content)
                return content, after_signature, datetime.fromtimestamp(after.st_mtime)
        except (OSError, PermissionError, DataSourceError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        time.sleep(max(0.1, delay_seconds))

    raise DataSourceError(
        "Não foi possível obter uma cópia estável da planilha local. "
        "Aguarde a sincronização e confira a opção 'Sempre manter neste dispositivo'. "
        f"Detalhe: {last_error}"
    )


def _parse_http_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        return parsed.astimezone().replace(tzinfo=None) if parsed.tzinfo else parsed
    except (TypeError, ValueError, OverflowError):
        return None


def _read_source_state() -> dict[str, dict[str, object]]:
    path = source_state_path()
    try:
        payload = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        return payload if isinstance(payload, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _write_source_state(payload: dict[str, dict[str, object]]) -> None:
    path = source_state_path()
    _atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2))


def _record_remote_state(
    identifier: str,
    digest: str,
    *,
    checked_at: datetime,
    header_modified: datetime | None,
    size_bytes: int,
    etag: str,
    last_modified_header: str,
) -> datetime:
    state = _read_source_state()
    key = sha256(identifier.encode("utf-8")).hexdigest()[:24]
    previous = state.get(key, {}) if isinstance(state.get(key), dict) else {}
    previous_digest = str(previous.get("checksum", ""))
    previous_changed = str(previous.get("changed_at", ""))

    if previous_digest == digest and previous_changed:
        try:
            changed_at = datetime.fromisoformat(previous_changed)
        except ValueError:
            changed_at = header_modified or checked_at
    else:
        changed_at = header_modified or checked_at

    state[key] = {
        "identifier": identifier,
        "checksum": digest,
        "checked_at": checked_at.isoformat(),
        "changed_at": changed_at.isoformat(),
        "size_bytes": size_bytes,
        "etag": etag,
        "last_modified": last_modified_header,
    }
    try:
        _write_source_state(state)
    except OSError:
        pass
    return changed_at


def _save_snapshot(
    content: bytes,
    filename: str,
    *,
    source_type: str,
    display_name: str,
    detail: str,
    original_path: str = "",
    modified_at: datetime | None = None,
    source_signature: tuple[int, int] = (0, 0),
    fallback_used: bool = False,
    checked_at: datetime | None = None,
    changed_at: datetime | None = None,
    etag: str = "",
    last_modified_header: str = "",
) -> PreparedDataSource:
    validate_xlsx_payload(content)
    digest = sha256(content).hexdigest()
    suffix = Path(filename).suffix.lower() or ".xlsx"
    target = snapshot_dir() / f"dashboard-{digest[:20]}{suffix}"
    if not target.exists():
        try:
            _atomic_write_bytes(target, content)
        except OSError as exc:
            raise DataSourceError(
                "A planilha foi baixada e validada, mas o Streamlit não conseguiu "
                "gravar o snapshot local. A cópia de contingência será utilizada. "
                f"Detalhe: {type(exc).__name__}: {exc}"
            ) from exc

    effective_change = changed_at or modified_at
    return PreparedDataSource(
        path=target,
        source_type=source_type,
        display_name=display_name,
        checksum=digest,
        detail=detail,
        original_path=original_path,
        modified_at=effective_change,
        size_bytes=len(content),
        source_signature=source_signature,
        snapshot=True,
        fallback_used=fallback_used,
        checked_at=checked_at or datetime.now(),
        changed_at=effective_change,
        etag=etag,
        last_modified_header=last_modified_header,
    )


@st.cache_data(ttl=_REMOTE_CACHE_TTL, show_spinner=False)
def _download_url(url: str, bearer_token: str = "") -> tuple[bytes, dict[str, str], str]:
    headers = {
        "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream;q=0.9,*/*;q=0.5",
        "User-Agent": "SM-CGR-Dashboard-AutoSync/10.1",
    }
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    checked_at = datetime.now()
    try:
        response = requests.get(url, headers=headers, timeout=(10, 45), allow_redirects=True)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise DataSourceError(f"Falha ao baixar a planilha remota: {exc}") from exc

    selected_headers = {
        "content-type": str(response.headers.get("Content-Type", "")),
        "content-disposition": str(response.headers.get("Content-Disposition", "")),
        "etag": str(response.headers.get("ETag", "")),
        "last-modified": str(response.headers.get("Last-Modified", "")),
    }
    content = response.content
    validate_xlsx_payload(content, content_type=selected_headers["content-type"])
    return content, selected_headers, checked_at.isoformat()


@st.cache_data(ttl=300, show_spinner=False)
def _graph_access_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    try:
        response = requests.post(
            token_url,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": "https://graph.microsoft.com/.default",
                "grant_type": "client_credentials",
            },
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise DataSourceError(f"Falha ao autenticar no Microsoft Graph: {exc}") from exc
    payload = response.json()
    token = str(payload.get("access_token", ""))
    if not token:
        raise DataSourceError("O Microsoft Graph não retornou um access_token.")
    return token


def _filename_from_url(url: str) -> str:
    configured = str(get_setting("DATA_FILENAME", DEFAULT_REMOTE_FILENAME)).strip()
    if configured:
        return configured
    candidate = unquote(Path(urlparse(url).path).name)
    return candidate if candidate.lower().endswith(".xlsx") else DEFAULT_REMOTE_FILENAME


def _is_google_sheets_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.casefold().endswith("docs.google.com") and "/spreadsheets/" in parsed.path


def _prepare_local() -> PreparedDataSource:
    configured_path = str(get_setting("DATA_LOCAL_PATH", str(DEFAULT_LOCAL_FILE)))
    path = Path(configured_path).expanduser().resolve()
    if not path.exists():
        raise DataSourceError(f"Arquivo local não encontrado: {path}")

    content, signature, modified_at = _read_stable_local_file(path)
    checked_at = datetime.now()
    return _save_snapshot(
        content,
        path.name,
        source_type="local",
        display_name=path.name,
        detail=f"Origem local/OneDrive: {path}",
        original_path=str(path),
        modified_at=modified_at,
        changed_at=modified_at,
        checked_at=checked_at,
        source_signature=signature,
    )


def _prepare_url(url: str, bearer_token: str = "") -> PreparedDataSource:
    content, headers, checked_raw = _download_url(url, bearer_token)
    checked_at = datetime.fromisoformat(checked_raw)
    filename = _filename_from_url(url)
    source_type = "google_sheets" if _is_google_sheets_url(url) else "url"
    display_name = filename
    digest = sha256(content).hexdigest()
    header_modified = _parse_http_datetime(headers.get("last-modified", ""))
    changed_at = _record_remote_state(
        url,
        digest,
        checked_at=checked_at,
        header_modified=header_modified,
        size_bytes=len(content),
        etag=headers.get("etag", ""),
        last_modified_header=headers.get("last-modified", ""),
    )
    return _save_snapshot(
        content,
        filename,
        source_type=source_type,
        display_name=display_name,
        detail=("Google Sheets AutoSync" if source_type == "google_sheets" else "URL remota"),
        original_path=url,
        modified_at=changed_at,
        changed_at=changed_at,
        checked_at=checked_at,
        etag=headers.get("etag", ""),
        last_modified_header=headers.get("last-modified", ""),
    )


def _prepare_sharepoint() -> PreparedDataSource:
    tenant_id = str(get_setting("MS_TENANT_ID", ""))
    client_id = str(get_setting("MS_CLIENT_ID", ""))
    client_secret = str(get_setting("MS_CLIENT_SECRET", ""))
    drive_id = str(get_setting("MS_DRIVE_ID", ""))
    item_id = str(get_setting("MS_ITEM_ID", ""))
    missing = [
        key for key, value in {
            "MS_TENANT_ID": tenant_id,
            "MS_CLIENT_ID": client_id,
            "MS_CLIENT_SECRET": client_secret,
            "MS_DRIVE_ID": drive_id,
            "MS_ITEM_ID": item_id,
        }.items() if not value
    ]
    if missing:
        raise DataSourceError("Fonte SharePoint incompleta. Configure: " + ", ".join(missing))

    token = _graph_access_token(tenant_id, client_id, client_secret)
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/content"
    content, headers, checked_raw = _download_url(url, token)
    checked_at = datetime.fromisoformat(checked_raw)
    digest = sha256(content).hexdigest()
    identifier = f"sharepoint:{drive_id}:{item_id}"
    changed_at = _record_remote_state(
        identifier,
        digest,
        checked_at=checked_at,
        header_modified=_parse_http_datetime(headers.get("last-modified", "")),
        size_bytes=len(content),
        etag=headers.get("etag", ""),
        last_modified_header=headers.get("last-modified", ""),
    )
    return _save_snapshot(
        content,
        DEFAULT_REMOTE_FILENAME,
        source_type="sharepoint",
        display_name=f"{DEFAULT_REMOTE_FILENAME} (SharePoint)",
        detail=f"Microsoft Graph drive={drive_id} item={item_id}",
        original_path=identifier,
        modified_at=changed_at,
        changed_at=changed_at,
        checked_at=checked_at,
        etag=headers.get("etag", ""),
        last_modified_header=headers.get("last-modified", ""),
    )


def last_valid_paths() -> tuple[Path, Path]:
    return runtime_dir() / "last_valid.xlsx", runtime_dir() / "last_valid.json"


def mark_source_valid(source: PreparedDataSource) -> bool:
    """Promote the latest fully parsed workbook to the contingency copy.

    Persistence failures must not take down a dashboard that has already loaded
    valid data. ``False`` lets the interface report a non-blocking warning.
    """
    if source.fallback_used or not source.path.exists():
        return False

    target, metadata_path = last_valid_paths()

    payload = {
        "checksum": source.checksum,
        "display_name": source.display_name,
        "source_type": source.source_type,
        "detail": source.detail,
        "original_path": source.original_path,
        "modified_at": source.modified_at.isoformat() if source.modified_at else None,
        "changed_at": source.changed_at.isoformat() if source.changed_at else None,
        "checked_at": source.checked_at.isoformat() if source.checked_at else None,
        "size_bytes": source.size_bytes,
        "source_signature": list(source.source_signature),
        "etag": source.etag,
        "last_modified_header": source.last_modified_header,
        "validated_at": datetime.now().isoformat(),
    }
    try:
        _atomic_copy_file(source.path, target)
        _atomic_write_text(metadata_path, json.dumps(payload, ensure_ascii=False, indent=2))
        cleanup_snapshot_cache()
        return True
    except OSError:
        return False


def _metadata_datetime(metadata: dict[str, object], key: str, fallback: datetime) -> datetime:
    raw = metadata.get(key)
    try:
        return datetime.fromisoformat(str(raw)) if raw else fallback
    except (TypeError, ValueError):
        return fallback


def prepare_last_valid_source() -> PreparedDataSource | None:
    """Return the last workbook that passed the full application parser."""
    workbook_path, metadata_path = last_valid_paths()
    if not workbook_path.exists():
        return None
    try:
        content = workbook_path.read_bytes()
        validate_xlsx_payload(content)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    except (OSError, json.JSONDecodeError, DataSourceError):
        return None

    file_time = datetime.fromtimestamp(workbook_path.stat().st_mtime)
    modified_at = _metadata_datetime(metadata, "modified_at", file_time)
    changed_at = _metadata_datetime(metadata, "changed_at", modified_at)
    checked_at = _metadata_datetime(metadata, "checked_at", file_time)
    raw_signature = metadata.get("source_signature") or [0, 0]
    signature = (
        int(raw_signature[0]) if len(raw_signature) > 0 else 0,
        int(raw_signature[1]) if len(raw_signature) > 1 else 0,
    )
    return PreparedDataSource(
        path=workbook_path,
        source_type=str(metadata.get("source_type", "local")),
        display_name=str(metadata.get("display_name", "Última versão válida")),
        checksum=sha256(content).hexdigest(),
        detail=str(metadata.get("detail", "Cópia de contingência local")),
        original_path=str(metadata.get("original_path", "")),
        modified_at=modified_at,
        changed_at=changed_at,
        checked_at=checked_at,
        size_bytes=int(metadata.get("size_bytes", len(content))),
        source_signature=signature,
        snapshot=True,
        fallback_used=True,
        etag=str(metadata.get("etag", "")),
        last_modified_header=str(metadata.get("last_modified_header", "")),
    )



def discard_unvalidated_snapshot(source: PreparedDataSource) -> None:
    """Remove a candidate snapshot that failed the full workbook parser."""
    if source.fallback_used or not source.snapshot:
        return
    try:
        candidate = source.path.resolve()
        snapshots_root = snapshot_dir().resolve()
        if candidate.parent == snapshots_root and candidate.exists():
            candidate.unlink()
    except OSError:
        pass

def cleanup_snapshot_cache() -> None:
    """Keep only the newest configured number of immutable XLSX snapshots."""
    keep = get_int("KEEP_SOURCE_SNAPSHOTS", 6, minimum=5)
    candidates: list[tuple[int, Path]] = []
    for item in snapshot_dir().glob("dashboard-*.xlsx"):
        try:
            candidates.append((item.stat().st_mtime_ns, item))
        except OSError:
            # Another Streamlit session may have removed the same stale file.
            continue
    files = [item for _mtime, item in sorted(candidates, key=lambda entry: entry[0], reverse=True)]
    for stale_file in files[keep:]:
        try:
            stale_file.unlink()
        except OSError:
            pass


def prepare_data_source() -> PreparedDataSource:
    """Resolve the workbook based on ``DATA_SOURCE``.

    Supported values: ``google_sheets``/``url`` (default), ``local`` and
    ``sharepoint``.
    """
    source_type = str(get_setting("DATA_SOURCE", "google_sheets")).strip().casefold()
    if source_type == "local":
        return _prepare_local()
    if source_type in {"url", "google_sheets", "google", "sheets"}:
        url = str(get_setting("DATA_URL", DEFAULT_GOOGLE_SHEETS_URL)).strip() or DEFAULT_GOOGLE_SHEETS_URL
        token = str(get_setting("DATA_BEARER_TOKEN", ""))
        return _prepare_url(url, token)
    if source_type == "sharepoint":
        return _prepare_sharepoint()
    raise DataSourceError(
        f"DATA_SOURCE inválido: {source_type}. Use google_sheets, url, local ou sharepoint."
    )


def probe_data_source(source: PreparedDataSource) -> PreparedDataSource:
    """Check the configured source and return its latest validated XLSX snapshot."""
    # A fallback carries metadata from the previous valid source. The active
    # configuration may already point elsewhere, so recovery must re-resolve it.
    if source.fallback_used:
        return prepare_data_source()
    if source.source_type == "local":
        return _prepare_local()
    if source.source_type in {"google_sheets", "url"}:
        url = source.original_path or str(get_setting("DATA_URL", DEFAULT_GOOGLE_SHEETS_URL))
        return _prepare_url(url, str(get_setting("DATA_BEARER_TOKEN", "")))
    if source.source_type == "sharepoint":
        return _prepare_sharepoint()
    return prepare_data_source()
