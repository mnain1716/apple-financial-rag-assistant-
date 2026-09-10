import streamlit as st
from pathlib import Path
import html

from src.rag_pipeline import generate_answer


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Apple Financial Intelligence",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM DARK THEME
# ============================================================

st.markdown("""
<style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #0d0f0e;
        color: #e7e9e5;
    }

    .block-container {
        max-width: 1160px;
        padding-top: 1.4rem;
        padding-bottom: 2.5rem;
    }

    /* Normal Streamlit text */
    .stMarkdown,
    .stCaption,
    label {
        color: #c5cbc4 !important;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        padding: 1.1rem 0 1.35rem;
        border-bottom: 1px solid #2a302c;
        margin-bottom: 1.1rem;
    }

    .hero-title {
        color: #f3f4ef;
        font-family: Georgia, serif;
        font-size: 2.2rem;
        font-weight: 500;
        letter-spacing: 0;
        margin-bottom: 0.3rem;
    }

    .hero-subtitle {
        color: #929b93 !important;
        font-size: 0.9rem;
        margin: 0;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    .metric-card {
        background: #121513;
        padding: 0.85rem 0.95rem;
        border-radius: 6px;
        border: 1px solid #29312c;
        min-height: 78px;
    }

    .metric-label {
        color: #7f8b82 !important;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
        letter-spacing: 0.04em;
    }

    .metric-value {
        color: #e8ece5 !important;
        font-size: 1.1rem;
        font-weight: 600;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        color: #e8ece5 !important;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.65rem;
        border-left: 2px solid #b8d477;
        padding-left: 0.65rem;
    }


    /* ========================================================
       USER QUESTION
       ======================================================== */

    .user-question {
        background: #151916;
        color: #e7ebe4 !important;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        border: 1px solid #303932;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .user-question * {
        color: #f3f4f6 !important;
    }


    /* ========================================================
       AI ANSWER
       ======================================================== */

    .answer-card {
        background: #111412;
        color: #dce1da !important;
        padding: 1rem 1.1rem;
        border-radius: 6px;
        border: 1px solid #2b332d;
        margin-bottom: 1rem;
    }

    .answer-label {
        color: #8f9a90 !important;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.7rem;
    }


    /* ========================================================
       SOURCE CARD
       ======================================================== */

    .source-card {
        background: #151916;
        padding: 0.85rem;
        border-radius: 5px;
        border: 1px solid #303932;
        margin-bottom: 0.8rem;
    }

    .source-title {
        color: #e8ece5 !important;
        font-weight: 700;
    }

    .source-meta {
        color: #929b93 !important;
        font-size: 0.88rem;
        margin-top: 0.3rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background: #111412 !important;
        border-right: 1px solid #29312c;
    }

    [data-testid="stSidebar"] * {
        color: #c8cec7 !important;
    }

    [data-testid="stSidebar"] .stButton button {
        color: #ffffff !important;
    }


    /* ========================================================
       SIDEBAR INFO BOX
       ======================================================== */

    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: #171b18 !important;
        border: 1px solid #303932 !important;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] section {
        background: #151916 !important;
        border: 1px dashed #465047 !important;
        border-radius: 6px !important;
    }

    [data-testid="stFileUploader"] section * {
        color: #d1d5db !important;
    }

    [data-testid="stFileUploader"] button {
        color: #ffffff !important;
        background: #1e251f !important;
        border: 1px solid #465047 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 5px !important;
        font-weight: 600 !important;
        min-height: 2.4rem;
        border: 1px solid #465047 !important;
    }


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    div[data-baseweb="input"] {
        background: #111412 !important;
        border-radius: 5px !important;
        border: 1px solid #3a443c !important;
    }

    div[data-baseweb="input"] input {
        color: #edf1eb !important;
        background: transparent !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #788379 !important;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {
        background: #121513 !important;
        border: 1px solid #303932 !important;
        border-radius: 5px !important;
    }

    [data-testid="stExpander"] summary {
        color: #e5e7eb !important;
    }

    [data-testid="stExpander"] summary span {
        color: #e5e7eb !important;
    }


    /* ========================================================
       CODE / RETRIEVED EVIDENCE
       ======================================================== */

    [data-testid="stCode"] {
        border-radius: 5px !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #69736b !important;
        font-size: 0.78rem;
        padding-top: 2rem;
        line-height: 1.7;
    }

    .eyebrow {
        color: #b8d477;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .chat-label {
        color: #8f9a90;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        margin-top: 1.1rem;
        margin-bottom: 0.35rem;
    }


</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# HERO HEADER
# ============================================================

# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
<div class="hero">
<div class="eyebrow">Research workspace</div>
<div class="hero-title">Apple Financial Intelligence</div>
<p class="hero-subtitle">Search Apple financial filings with grounded source attribution.</p>
</div>
""",
    unsafe_allow_html=True
)

# ============================================================
# KNOWLEDGE BASE METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Documents</div>
        <div class="metric-value">3 Apple Filings</div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Pages indexed</div>
        <div class="metric-value">281 Pages</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Text chunks</div>
        <div class="metric-value">1,350</div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Retrieval</div>
        <div class="metric-value">FAISS + Cosine</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Controls")

    st.markdown("### Knowledge base")

    st.info(
        "Apple financial filings covering fiscal years "
        "2023, 2024 and 2025."
    )

    st.caption(
        "Embedding model: all-MiniLM-L6-v2"
    )

    st.caption(
        "Vector database: FAISS"
    )

    st.caption(
        "LLM: Gemini"
    )

    st.divider()

    st.markdown("### Add document")

    uploaded_file = st.file_uploader(
        "Upload an Apple financial PDF",
        type=["pdf"],
        help="Upload a PDF to add it to the knowledge base."
    )

    if uploaded_file is not None:

        st.success(
            f"Selected: {uploaded_file.name}"
        )

        st.caption(
            f"File size: {uploaded_file.size / 1024:.1f} KB"
        )

        if st.button(
            "Add to knowledge base",
            use_container_width=True,
            type="primary"
        ):

            from src.indexer import rebuild_index

            documents_folder = Path(__file__).resolve().parent / "data" / "documents"

            documents_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            file_path = (
                documents_folder /
                uploaded_file.name
            )

            try:

                with open(
                    file_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                with st.spinner(
                    "Processing document and rebuilding index..."
                ):

                    pages, chunks = rebuild_index()

                st.success(
                    "Knowledge base updated successfully!"
                )

                st.caption(
                    f"{pages} pages • {chunks} chunks indexed"
                )

            except Exception as e:

                st.error(
                    f"Indexing failed: {e}"
                )

    st.divider()

    st.markdown("### Session")

    if st.button(
        "Clear Conversation",
        use_container_width=True
    ):

        st.session_state.chat_history = []

        st.rerun()

    st.divider()

    st.caption(
        "🔒 Answers are generated only from the indexed "
        "Apple financial documents."
    )


# ============================================================
# QUESTION AREA
# ============================================================

st.markdown(
    '<div class="section-title">Ask a question</div>',
    unsafe_allow_html=True
)


question = st.text_input(
    "Financial question",
    placeholder="Example: What was Apple's total net sales in 2025?",
    label_visibility="collapsed"
)


ask_col, hint_col = st.columns([1, 5])


with ask_col:

    ask_button = st.button(
        "Ask",
        type="primary",
        use_container_width=True
    )


with hint_col:

    st.caption(
        "Ask about revenue, iPhone sales, Mac sales, Services, "
        "or other information contained in the indexed reports."
    )


# ============================================================
# RAG QUERY
# ============================================================

if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a financial question first."
        )

    else:

        with st.spinner(
            "Searching financial documents and generating a grounded answer..."
        ):

            try:

                answer, sources = generate_answer(
                    question
                )

                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "sources": sources
                })

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# ============================================================
# CONVERSATION
# ============================================================

if st.session_state.chat_history:

    st.markdown(
        '<div class="section-title">Conversation</div>',
        unsafe_allow_html=True
    )

    for chat in reversed(st.session_state.chat_history):

        # ----------------------------------------------------
        # USER QUESTION
        # ----------------------------------------------------

        st.markdown('<div class="chat-label">Question</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="user-question">{html.escape(chat["question"])}</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # AI ANSWER
        # ----------------------------------------------------

        st.markdown('<div class="chat-label">Answer</div>', unsafe_allow_html=True)
        st.markdown('<div class="answer-card">', unsafe_allow_html=True)
        st.markdown(
            chat["answer"]
        )
        st.markdown('</div>', unsafe_allow_html=True)


        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        if chat["sources"]:

            with st.expander(
                f"Sources and retrieved evidence "
                f"({len(chat['sources'])} chunks)"
            ):

                for i, source in enumerate(
                    chat["sources"],
                    start=1
                ):

                    st.markdown(
                        f"**Source {i}**"
                    )

                    st.write(
                        f"📄 **Document:** {source['source']}"
                    )

                    st.write(
                        f"📖 **Page:** {source['page']}"
                    )

                    st.write(
                        f"🎯 **Cosine Similarity:** "
                        f"{source['similarity']:.4f}"
                    )

                    st.markdown(
                        "**Retrieved evidence:**"
                    )

                    st.code(
                        source["text"],
                        language=None
                    )

                    st.divider()


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    Apple Financial Document Intelligence
    • FAISS
    • Sentence Transformers
    • Gemini
    • Streamlit

    <br>

    Grounded answers with document-level source attribution

</div>
""", unsafe_allow_html=True)