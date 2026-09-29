"""
pdf_loader.py — PDF text extraction for AI Document Assistant
"""

from pypdf import PdfReader


def extract_text(uploaded_file):
    """
    Extract all text from an uploaded PDF (Streamlit's UploadedFile object
    or any file-like object pypdf can read).

    Returns the full document text as a single string, with page breaks
    marked so you can trace answers back to a page number later if you
    want to extend citations beyond chunk IDs.
    """
    reader = PdfReader(uploaded_file)
    pages_text = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages_text.append(f"[Page {page_num}]\n{text.strip()}")

    return "\n\n".join(pages_text)