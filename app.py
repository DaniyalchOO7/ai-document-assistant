"""
app.py — Streamlit chat UI for AI Document Assistant

Wires together: pdf_loader (extraction) -> rag (chunk + embed + retrieve)
-> llm (Gemini + grounding check).
"""

import streamlit as st
from pdf_loader import extract_text
from rag import chunk_text, build_index, retrieve, format_context
from llm import ask_with_grounding_check

st.set_page_config(page_title="AI Document Assistant", page_icon="📄")
from ui_theme import inject_theme, render_hero
inject_theme()
render_hero()

# --- Session state setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "index" not in st.session_state:
    st.session_state.index = None
if "chunks" not in st.session_state:
    st.session_state.chunks = None
if "doc_name" not in st.session_state:
    st.session_state.doc_name = None

# --- File upload + indexing ---
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None and uploaded_file.name != st.session_state.doc_name:
    with st.spinner("Reading and indexing document..."):
        text = extract_text(uploaded_file)
        chunks = chunk_text(text)
        index, chunks = build_index(chunks)

        st.session_state.index = index
        st.session_state.chunks = chunks
        st.session_state.doc_name = uploaded_file.name
        st.session_state.messages = []  # reset chat for a new document

    st.success(f"Indexed {uploaded_file.name} — {len(chunks)} chunks ready.")

# --- Chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            st.caption(f"Sources: Chunk {', '.join(str(s) for s in msg['sources'])}")
        if msg.get("grounded") is False:
            st.warning("This answer may not be fully grounded in the document.")

# --- Chat input ---
if question := st.chat_input("Ask a question about the document..."):
    if st.session_state.index is None:
        st.warning("Upload a PDF first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                retrieved = retrieve(question, st.session_state.index, st.session_state.chunks)
                context = format_context(retrieved)
                result = ask_with_grounding_check(question, retrieved, context)
                from doc_qa_metrics import log_interaction
                log_interaction(question, retrieved, result)

                st.markdown(result["answer"])
                if result["sources"]:
                    st.caption(f"Sources: Chunk {', '.join(str(s) for s in result['sources'])}")
                if not result["grounded"]:
                    st.warning("This answer may not be fully grounded in the document.")

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
            "grounded": result["grounded"],
        })