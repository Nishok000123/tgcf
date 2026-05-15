import os
import subprocess
from importlib import resources

import tgcf.web_ui as wu
from tgcf.config import CONFIG


def main():
    resource = resources.files(wu).joinpath("0_👋_Hello.py")
    os.environ["STREAMLIT_THEME_BASE"] = CONFIG.theme
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    with resources.as_file(resource) as path:
        if not path.is_file():
            raise FileNotFoundError(f"Web UI entrypoint not found at {path}")
        try:
            subprocess.run(["streamlit", "run", str(path)], check=True)
        except FileNotFoundError as err:
            raise RuntimeError("streamlit command not found in PATH") from err
        except subprocess.CalledProcessError as err:
            raise RuntimeError(
                f"streamlit failed to start web UI (exit code {err.returncode})"
            ) from err
