"""
ui_theme_casewell.py — Alternate theme for AI Document Assistant

Styled after the "Casewell" reference: deep forest-green header, warm
cream/paper background, brass-gold accents, Fraunces serif headings.
A more premium, editorial feel than the Tickmark-style theme.

This is a SEPARATE file from ui_theme.py on purpose — so you can compare
both by switching one import line in app.py, without losing either version.

Usage in app.py (swap this in place of the ui_theme import to test it):
    from ui_theme_casewell import inject_theme, render_hero, render_pill
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root {
    --ink: #1F3A2E;
    --paper: #EFE9DA;
    --paper-light: #FAF7EF;
    --charcoal: #232420;
    --brass: #9C7A32;
    --brass-light: #B7924A;
    --line: #C9CDB9;

    --bg: var(--paper);
    --surface: var(--paper-light);
    --text: var(--charcoal);
    --text-soft: #55584E;
    --border: var(--line);
    --accent: var(--brass);
    --header-bg: var(--ink);
    --header-text: var(--paper-light);
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg: #171A16;
        --surface: #1F231C;
        --text: #EDEAE0;
        --text-soft: #B3B5A8;
        --border: #383C32;
        --accent: var(--brass-light);
        --header-bg: #101410;
        --header-text: #EDEAE0;
    }
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', -apple-system, sans-serif;
}

.stApp {
    background-color: var(--bg);
}

/* Hero — dark forest-green band, like the reference page's header */
.doc-hero {
    background: var(--header-bg);
    color: var(--header-text);
    padding: 34px 28px;
    margin: -1rem -1rem 24px -1rem;
    border-bottom: 3px solid var(--accent);
}

.doc-hero h1 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 600;
    font-size: 2.1rem;
    color: var(--header-text);
    margin: 0 0 10px 0;
    letter-spacing: -0.01em;
}

.doc-hero p {
    font-size: 1rem;
    color: #D9D6C7;
    margin: 0;
    max-width: 480px;
    line-height: 1.55;
}

/* File uploader — warm paper card */
[data-testid="stFileUploader"] {
    border: 1px solid var(--border);
    border-radius: 3px;
    background: var(--surface);
    padding: 6px;
}

[data-testid="stFileUploaderDropzone"] {
    background: var(--surface) !important;
}

/* Chat messages — paper cards, hairline borders, serif question text optional */
[data-testid="stChatMessage"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 14px 16px !important;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] textarea {
    background: var(--surface);
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
}

/* Pills */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 3px;
    margin-top: 6px;
    font-family: 'IBM Plex Sans', sans-serif;
}

.status-pill.ready {
    background: rgba(156, 122, 50, 0.15);
    color: var(--accent);
    border: 1px solid var(--accent);
}

.status-pill.flag {
    background: rgba(180, 60, 40, 0.12);
    color: #8F3A28;
    border: 1px solid #8F3A28;
}

.stCaption {
    display: inline-block;
    background: rgba(156, 122, 50, 0.15);
    color: var(--accent);
    padding: 3px 10px;
    border-radius: 3px;
    font-size: 0.82rem;
    border: 1px solid var(--accent);
}

div[data-testid="stAlert"] {
    background: rgba(180, 60, 40, 0.1) !important;
    border: 1px solid #8F3A28 !important;
    border-radius: 3px !important;
}

div[data-testid="stAlert"] p {
    color: #8F3A28 !important;
}
</style>
"""


def inject_theme():
    st.markdown(_CSS, unsafe_allow_html=True)


def render_hero(
    title="AI Document Assistant",
    subtitle="Upload a document and ask questions grounded in its actual content — every answer traces back to a source.",
):
    st.markdown(
        f"""
        <div class="doc-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pill(text, kind="ready"):
    st.markdown(
        f'<span class="status-pill {kind}">{text}</span>',
        unsafe_allow_html=True,
    )