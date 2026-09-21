"""Sincroniza uma planilha XLSX local com um arquivo no Google Drive.

Uso recomendado no PC Windows:
    python sync_excel_to_drive.py

O processo fica ativo, verifica o arquivo a cada intervalo e só envia quando o
conteúdo realmente mudou. A leitura exige que tamanho e data de modificação
permaneçam estáveis, evitando publicar um XLSX parcialmente salvo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
import time
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Any

import requests
try:
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account
except ModuleNotFoundError:  # Allows local validation to report a useful setup error.
    Request = None  # type: ignore[assignment]
    service_account = None  # type: ignore[assignment]

SCOPES = ["https://www.googleapis.com/auth/drive"]
DRIVE_UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files"
DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"
XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

logger = logging.getLogger("google_drive_sync")


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def load_service_account() -> service_account.Credentials:
    if service_account is None or Request is None:
        raise RuntimeError("Instale as dependências com: pip install -r requirements.txt")
    raw_json = env("GOOGLE_SERVICE_ACCOUNT_JSON")
    json_path = env("GOOGLE_SERVICE_ACCOUNT_FILE")
    if raw_json:
        try:
            info = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON não contém JSON válido.") from exc
        return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    if json_path:
        path = Path(json_path).expanduser()
        if not path.exists():
            raise RuntimeError(f"Arquivo de credenciais não encontrado: {path}")
        return service_account.Credentials.from_service_account_file(str(path), scopes=SCOPES)
    raise RuntimeError("Configure GOOGLE_SERVICE_ACCOUNT_FILE ou GOOGLE_SERVICE_ACCOUNT_JSON.")


def auth_headers() -> dict[str, str]:
    credentials = load_service_account()
    credentials.refresh(Request())
    return {"Authorization": f"Bearer {credentials.token}"}


def validate_xlsx(data: bytes) -> None:
    if not data or not data.startswith(b"PK"):
        raise RuntimeError("O arquivo local não parece ser um XLSX válido.")
    try:
        with zipfile.ZipFile(BytesIO(data)) as archive:
            names = set(archive.namelist())
            if "[Content_Types].xml" not in names or not any(n.startswith("xl/") for n in names):
                raise RuntimeError("O XLSX não contém a estrutura esperada do Excel.")
            bad = archive.testzip()
            if bad:
                raise RuntimeError(f"O XLSX está corrompido; entrada inválida: {bad}")
    except zipfile.BadZipFile as exc:
        raise RuntimeError("O arquivo local está corrompido ou ainda está sendo salvo.") from exc


def read_stable_file(path: Path, attempts: int = 8, delay: float = 0.5) -> tuple[bytes, str]:
    last_error = "arquivo indisponível"
    for _ in range(attempts):
        try:
            before = path.stat()
            data = path.read_bytes()
            after = path.stat()
            if (before.st_mtime_ns, before.st_size) != (after.st_mtime_ns, after.st_size):
                last_error = "o arquivo mudou durante a leitura"
            elif len(data) != after.st_size:
                last_error = "o tamanho lido não corresponde ao arquivo"
            else:
                validate_xlsx(data)
                return data, hashlib.sha256(data).hexdigest()
        except (OSError, RuntimeError) as exc:
            last_error = str(exc)
        time.sleep(delay)
    raise RuntimeError(f"Não foi possível ler uma versão estável de {path}: {last_error}")


def find_or_create_file(headers: dict[str, str], name: str, folder_id: str) -> str:
    configured_id = env("GOOGLE_DRIVE_FILE_ID")
    if configured_id:
        response = requests.get(
            f"{DRIVE_FILES_URL}/{configured_id}",
            params={"fields": "id,name,mimeType"}, headers=headers, timeout=30,
        )
        response.raise_for_status()
        return configured_id

    query = f"name = '{name.replace(chr(39), chr(92) + chr(39))}' and trashed = false"
    if folder_id:
        query += f" and '{folder_id}' in parents"
    response = requests.get(
        DRIVE_FILES_URL,
        params={"q": query, "pageSize": 10, "fields": "files(id,name,mimeType,modifiedTime)"},
        headers=headers, timeout=30,
    )
    response.raise_for_status()
    files = response.json().get("files", [])
    if files:
        return str(files[0]["id"])

    metadata: dict[str, Any] = {"name": name, "mimeType": XLSX_MIME}
    if folder_id:
        metadata["parents"] = [folder_id]
    response = requests.post(
        DRIVE_UPLOAD_URL,
        params={"uploadType": "resumable", "fields": "id"},
        headers={**headers, "Content-Type": "application/json; charset=UTF-8"},
        json=metadata, timeout=30,
    )
    response.raise_for_status()
    location = response.headers.get("Location")
    if not location:
        raise RuntimeError("O Google Drive não retornou a URL de upload.")
    return _upload_bytes(location, headers, b"", create=True)


def _upload_bytes(url: str, headers: dict[str, str], data: bytes, *, create: bool = False) -> str:
    if create:
        # The resumable session is completed by the real upload in sync_file;
        # this branch is intentionally unreachable for normal creation.
        raise RuntimeError("Sessão de upload criada sem conteúdo.")
    response = requests.patch(
        url, params={"uploadType": "media", "fields": "id,modifiedTime,size"},
        headers={**headers, "Content-Type": XLSX_MIME}, data=data, timeout=120,
    )
    response.raise_for_status()
    return str(response.json().get("id", ""))


def sync_file(path: Path, state_path: Path) -> bool:
    data, digest = read_stable_file(path)
    previous = state_path.read_text(encoding="utf-8").strip() if state_path.exists() else ""
    if previous == digest:
        logger.info("Sem alteração: %s", path)
        return False

    headers = auth_headers()
    file_id = env("GOOGLE_DRIVE_FILE_ID")
    if not file_id:
        # Search/create is handled without resumable upload to keep the setup simple.
        name = env("GOOGLE_DRIVE_FILE_NAME", path.name)
        folder_id = env("GOOGLE_DRIVE_FOLDER_ID")
        query = f"name = '{name.replace(chr(39), chr(92) + chr(39))}' and trashed = false"
        if folder_id:
            query += f" and '{folder_id}' in parents"
        response = requests.get(DRIVE_FILES_URL, params={"q": query, "pageSize": 10, "fields": "files(id)"}, headers=headers, timeout=30)
        response.raise_for_status()
        found = response.json().get("files", [])
        if found:
            file_id = str(found[0]["id"])
        else:
            metadata: dict[str, Any] = {"name": name, "mimeType": XLSX_MIME}
            if folder_id:
                metadata["parents"] = [folder_id]
            response = requests.post(DRIVE_FILES_URL, params={"fields": "id"}, headers={**headers, "Content-Type": "application/json"}, json=metadata, timeout=30)
            response.raise_for_status()
            file_id = str(response.json()["id"])
    _upload_bytes(f"{DRIVE_UPLOAD_URL}/{file_id}", headers, data)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(digest, encoding="utf-8")
    logger.info("Sincronizado no Google Drive: %s (sha256=%s)", file_id, digest[:12])
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="Executa uma verificação e encerra")
    parser.add_argument("--interval", type=int, default=int(env("SYNC_INTERVAL_SECONDS", "600")), help="Intervalo em segundos")
    args = parser.parse_args()
    source = Path(env("LOCAL_XLSX_PATH", "Dashboard SM CGR 2026.xlsx")).expanduser().resolve()
    state = Path(env("SYNC_STATE_FILE", str(source.parent / ".google_drive_sync.sha256"))).expanduser()
    logging.basicConfig(level=getattr(logging, env("LOG_LEVEL", "INFO").upper(), logging.INFO), format="%(asctime)s %(levelname)s %(message)s")
    if not source.exists():
        logger.error("Arquivo não encontrado: %s", source)
        return 2
    while True:
        try:
            sync_file(source, state)
        except Exception:
            logger.exception("Falha na sincronização; o próximo ciclo tentará novamente")
        if args.once:
            return 0
        time.sleep(max(60, args.interval))


if __name__ == "__main__":
    sys.exit(main())
