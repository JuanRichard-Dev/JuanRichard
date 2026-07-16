"""Execute one dashboard page with lightweight UI stubs for CI smoke testing."""

from __future__ import annotations

import os
import runpy
import sys
import tempfile
import types
from pathlib import Path

TARGET_PAGE = sys.argv[1]
PROJECT = Path(__file__).resolve().parents[1]
os.chdir(PROJECT)
sys.path.insert(0, str(PROJECT))
RUNTIME = tempfile.TemporaryDirectory(prefix="dashboard-smoke-")
os.environ["DATA_SOURCE"] = "local"
os.environ["DATA_LOCAL_PATH"] = str(PROJECT / "Dashboard SM CGR 2026.xlsx")
os.environ["AUTO_REFRESH_ENABLED"] = "false"
os.environ["LOCAL_RUNTIME_DIR"] = RUNTIME.name


class Context:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def markdown(self, *_args, **_kwargs):
        return None

    caption = markdown
    dataframe = markdown
    info = markdown
    warning = markdown
    success = markdown
    metric = markdown


class CacheData:
    def __call__(self, func=None, **_kwargs):
        if func is not None:
            return func
        return lambda wrapped: wrapped

    @staticmethod
    def clear() -> None:
        return None


st = types.ModuleType("streamlit")
st.session_state = {}
st.query_params = {}
st.secrets = {}
st.cache_data = CacheData()
st.fragment = lambda func=None, **_kwargs: (
    func if func is not None else (lambda wrapped: wrapped)
)
st.sidebar = Context()
st.empty = lambda: Context()
st.container = lambda *_a, **_k: Context()
st.set_page_config = lambda *_a, **_k: None
st.set_option = lambda *_a, **_k: None
st.markdown = lambda *_a, **_k: None
st.caption = lambda *_a, **_k: None
st.warning = lambda *_a, **_k: None
st.info = lambda *_a, **_k: None
st.success = lambda *_a, **_k: None
st.toast = lambda *_a, **_k: None
st.error = lambda *_a, **_k: None
st.stop = lambda: (_ for _ in ()).throw(RuntimeError("st.stop"))
st.rerun = lambda: (_ for _ in ()).throw(RuntimeError("st.rerun"))
st.plotly_chart = lambda *_a, **_k: None
st.dataframe = lambda *_a, **_k: None
st.metric = lambda *_a, **_k: None
st.columns = lambda spec, **_k: [Context() for _ in range(spec if isinstance(spec, int) else len(spec))]
st.expander = lambda *_a, **_k: Context()
st.tabs = lambda names: [Context() for _ in names]
st.button = lambda *_a, **_k: False
st.download_button = lambda *_a, **_k: False
st.toggle = lambda *_a, value=False, **_k: value
st.multiselect = lambda _label, options, *_a, key=None, default=None, **_k: st.session_state.setdefault(
    key, list(default if default is not None else options)
)


def selectbox(_label, options, index=0, key=None, **_kwargs):
    if key == "main_navigation_native_v8":
        st.session_state[key] = TARGET_PAGE
        return TARGET_PAGE
    if key is None:
        return list(options)[index]
    return st.session_state.setdefault(key, list(options)[index])


st.selectbox = selectbox
st.radio = selectbox
st.number_input = lambda _label, *_a, value=0, **_k: value
st.text_input = lambda *_a, **_k: ""
st.spinner = lambda *_a, **_k: Context()
sys.modules["streamlit"] = st


runpy.run_path(str(PROJECT / "app.py"), run_name="__main__")
