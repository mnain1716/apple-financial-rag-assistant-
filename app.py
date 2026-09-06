import streamlit as st
from pathlib import Path

from src.rag_pipeline import generate_answer
from src.indexer import rebuild_index

st.set_page_config(
    page_title="Apple Financial RAG Assistant",
    page_icon="📊",
    layout="wide"
)


# -----------------------------
# Session State
# -----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -----------------------------
# Header
# -----------------------------

st.title("📊 Apple Financial Document Intelligence")

st.caption(
    "Enterprise RAG Assistant powered by "
    "FAISS + Sentence Transformers + Gemini"
)

st.divider()


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚙️ Controls")

    st.write("### 📚 Knowledge Base")

    st.write(
        "Apple financial reports from 2023, 2024 and 2025."
    )
    st.divider()


    st.write("### 📄 Upload Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success(
            f"Selected: {uploaded_file.name}"
        )

        st.caption(
            f"Size: {uploaded_file.size / 1024:.1f} KB"
        )

        if st.button(
            "📥 Add to Knowledge Base",
            use_container_width=True
        ):

            documents_folder = Path("data/documents")

            documents_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            file_path = documents_folder / uploaded_file.name

            with open(file_path, "wb") as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            st.success(
                f"{uploaded_file.name} added successfully!"
            )

            with st.spinner(
                "Updating knowledge base..."
            ):

                try:

                    pages, chunks = rebuild_index()

                    st.success(
                        f"Knowledge base updated! "
                        f"{pages} pages and {chunks} chunks indexed."
                    )

                except Exception as e:

                    st.error(
                        f"Indexing failed: {e}"
                    )

# -----------------------------
# Question Input
# -----------------------------

question = st.text_input(
    "Ask a question about Apple's financial reports:",
    placeholder="Example: What was Apple's total net sales in 2025?"
)


if st.button("Ask AI", type="primary"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:

                answer, sources = generate_answer(question)

                # Save conversation
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "sources": sources
                })

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# -----------------------------
# Conversation History
# -----------------------------

if st.session_state.chat_history:

    st.divider()

    st.subheader("💬 Conversation")


    for chat in st.session_state.chat_history:

        st.markdown(
            f"**🧑 You:** {chat['question']}"
        )

        st.markdown(
            f"**🤖 Assistant:** {chat['answer']}"
        )

        if chat["sources"]:

            with st.expander("📚 View Sources & Retrieved Evidence"):

                for i, source in enumerate(
                    chat["sources"],
                    start=1
                ):

                    st.markdown(
                        f"### Source {i}"
                    )

                    st.write(
                        f"**Document:** {source['source']}"
                    )

                    st.write(
                        f"**Page:** {source['page']}"
                    )

                    st.write(
                        f"**Cosine Similarity:** "
                        f"{source['similarity']:.4f}"
                    )

                    st.markdown(
                        "**Retrieved text:**"
                    )

                    st.code(
                        source["text"],
                        language=None
                    )

                    st.divider()
# -----------------------------
# Footer
# -----------------------------

st.caption(
    "This assistant answers only from the indexed "
    "Apple financial documents."
)