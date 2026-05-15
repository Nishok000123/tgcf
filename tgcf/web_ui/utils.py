import os
from importlib import resources
from typing import Dict, List

from streamlit.components.v1 import html

from tgcf.config import write_config
import tgcf.web_ui as wu


def get_list(string: str):
    # string where each line is one element
    my_list = []
    for line in string.splitlines():
        clean_line = line.strip()
        if clean_line != "":
            my_list.append(clean_line)
    return my_list


def get_string(my_list: List):
    string = ""
    for item in my_list:
        string += f"{item}\n"
    return string


def dict_to_list(dict: Dict):
    my_list = []
    for key, val in dict.items():
        my_list.append(f"{key}: {val}")
    return my_list


def list_to_dict(my_list: List):
    my_dict = {}
    for item in my_list:
        key, val = item.split(":")
        my_dict[key.strip()] = val.strip()
    return my_dict


def apply_theme(st, CONFIG, hidden_container):
    """Apply theme using browser's local storage"""
    if st.session_state.theme == "☀️":
        theme = "Light"
        CONFIG.theme = "light"
    else:
        theme = "Dark"
        CONFIG.theme = "dark"
    write_config(CONFIG)
    script = (
        f"<script>localStorage.setItem('stActiveTheme-/-v1', "
        f'\'{{"name":"{theme}"}}\');'
    )
    with resources.as_file(resources.files(wu).joinpath("pages")) as pages_dir:
        pages = os.listdir(pages_dir)
        for page in pages:
            script += (
                f"localStorage.setItem('stActiveTheme-/{page[4:-3]}-v1', "
                f'\'{{"name":"{theme}"}}\');'
            )
    script += "parent.location.reload()</script>"
    with hidden_container:  # prevents the layout from shifting
        html(script, height=0, width=0)


def switch_theme(st, CONFIG):
    """Display the option to change theme (Light/Dark)"""
    with st.sidebar:
        leftpad, content, rightpad = st.columns([0.27, 0.46, 0.27])
        with content:
            st.radio(
                "Theme:",
                ["☀️", "🌒"],
                horizontal=True,
                label_visibility="collapsed",
                index=CONFIG.theme == "dark",
                on_change=apply_theme,
                key="theme",
                args=[st, CONFIG, leftpad],  # or rightpad
            )


def apply_base_style(st):
    st.markdown(
        """
        <style>
            .stApp {
                background-image: radial-gradient(circle at top right, rgba(120, 119, 198, 0.16), transparent 45%),
                                  radial-gradient(circle at bottom left, rgba(52, 211, 153, 0.10), transparent 40%);
            }
            .main .block-container {
                max-width: 1000px;
                padding-top: 1.4rem;
                padding-bottom: 2rem;
            }
            div[data-testid="stExpander"] {
                border: 1px solid rgba(120, 120, 130, 0.25);
                border-radius: 14px;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
            }
            div[data-testid="stTextInput"] > div > div,
            div[data-testid="stTextArea"] textarea,
            div[data-testid="stMultiSelect"] > div {
                border-radius: 10px !important;
            }
            button[kind],
            .stButton > button {
                border-radius: 999px !important;
                font-weight: 600 !important;
            }
            .tgcf-hero {
                padding: 1rem 1.1rem;
                border: 1px solid rgba(120, 120, 130, 0.25);
                border-radius: 14px;
                background: rgba(255, 255, 255, 0.02);
                margin-bottom: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hide_st(st):
    dev = os.getenv("DEV")
    if dev:
        return
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
