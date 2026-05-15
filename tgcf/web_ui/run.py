import os
import subprocess
from importlib import resources

import tgcf.web_ui as wu
from tgcf.config import CONFIG


def main():
    path = resources.files(wu).joinpath("0_👋_Hello.py")
    os.environ["STREAMLIT_THEME_BASE"] = CONFIG.theme
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    subprocess.run(["streamlit", "run", str(path)], check=False)
