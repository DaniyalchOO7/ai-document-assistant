"""
ui_theme.py — Custom look for AI Document Assistant

Import and call inject_theme() once near the top of app.py, right after
st.set_page_config(). Replaces the default st.title/caption with a styled
hero section that fits a "study/research assistant" identity instead of
a generic chatbot look.
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #FAF7F0;
}

.doc-hero {
    padding: 8px 0 20px;
    border-bottom: 1px solid #D8D2C2;
    margin-bottom: 24px;
}

.doc-hero h1 {
    font-family: 'Source Serif 4', serif;
    font-weight: 600;
    font-size: 2.1rem;
    color: #1C2321;
    margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}

.doc-hero p {
    font-size: 0.98rem;
    color: #4A4A44;
    margin: 0;
    max-width: 480px;
    line-height: 1.5;
}

/* File uploader — reads as a document slot, not a generic dropzone */
[data-testid="stFileUploader"] {
    border: 1px dashed #B8B09A;
    border-radius: 4px;
    background: #FFFDF8;
    padding: 4px;
}

/* Chat message bubbles */
[data-testid="stChatMessage"] {
    background: transparent;
    border-bottom: 1px solid #EDE8DA;
    padding-bottom: 14px;
    margin-bottom: 14px;
}

/* Source citation caption — the one place yellow appears */
.stCaption {
    display: inline-block;
    background: #FBE9A8;
    color: #4A3B00;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 0.78rem;
    font-weight: 500;
}
</style>
"""


def inject_theme():
    st.markdown(_CSS, unsafe_allow_html=True)


def render_hero(title="AI Document Assistant", subtitle="Upload a document and ask questions grounded in its actual content — every answer traces back to a source."):
    st.markdown(
        f"""
        <div class="doc-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )