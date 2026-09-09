import streamlit as st
from pathlib import Path
import html

from src.rag_pipeline import generate_answer
from src.indexer import rebuild_index


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
        background: #0b0f14;
        color: #e5e7eb;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Normal Streamlit text */
    .stMarkdown,
    .stCaption,
    label {
        color: #e5e7eb !important;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        padding: 2.2rem 2.4rem;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            #05070a 0%,
            #111827 55%,
            #1f2937 100%
        );
        border: 1px solid #273244;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.35);
    }

    .hero-title {
        color: #ffffff;
        font-size: 2.45rem;
        font-weight: 750;
        letter-spacing: -1px;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        color: #9ca3af !important;
        font-size: 1rem;
        margin: 0;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    .metric-card {
        background: #11161d;
        padding: 1.2rem;
        border-radius: 17px;
        border: 1px solid #26303d;
        min-height: 105px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.20);
    }

    .metric-label {
        color: #8b95a5 !important;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
        letter-spacing: 0.08em;
    }

    .metric-value {
        color: #f9fafb !important;
        font-size: 1.35rem;
        font-weight: 700;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        color: #f9fafb !important;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }


    /* ========================================================
       USER QUESTION
       ======================================================== */

    .user-question {
        background: #172033;
        color: #f3f4f6 !important;
        padding: 1rem 1.2rem;
        border-radius: 15px;
        border: 1px solid #293752;
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
        background: #11161d;
        color: #e5e7eb !important;
        padding: 1.4rem 1.5rem;
        border-radius: 18px;
        border: 1px solid #26303d;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.20);
        margin-bottom: 1rem;
    }

    .answer-label {
        color: #9ca3af !important;
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
        background: #151b23;
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid #293341;
        margin-bottom: 0.8rem;
    }

    .source-title {
        color: #f9fafb !important;
        font-weight: 700;
    }

    .source-meta {
        color: #9ca3af !important;
        font-size: 0.88rem;
        margin-top: 0.3rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background: #0f141b !important;
        border-right: 1px solid #252d38;
    }

    [data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    [data-testid="stSidebar"] .stButton button {
        color: #ffffff !important;
    }


    /* ========================================================
       SIDEBAR INFO BOX
       ======================================================== */

    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: #172033 !important;
        border: 1px solid #293752 !important;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] section {
        background: #151b23 !important;
        border: 1px dashed #3b4655 !important;
        border-radius: 12px !important;
    }

    [data-testid="stFileUploader"] section * {
        color: #d1d5db !important;
    }

    [data-testid="stFileUploader"] button {
        color: #ffffff !important;
        background: #1f2937 !important;
        border: 1px solid #374151 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 11px !important;
        font-weight: 650 !important;
        min-height: 2.6rem;
    }


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    div[data-baseweb="input"] {
        background: #11161d !important;
        border-radius: 12px !important;
        border: 1px solid #303a48 !important;
    }

    div[data-baseweb="input"] input {
        color: #f9fafb !important;
        background: transparent !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #7c8797 !important;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {
        background: #11161d !important;
        border: 1px solid #293341 !important;
        border-radius: 14px !important;
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
        border-radius: 10px !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #6b7280 !important;
        font-size: 0.78rem;
        padding-top: 2.5rem;
        line-height: 1.7;
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
<div class="hero-title">🍎 Apple Financial Intelligence</div>
<p class="hero-subtitle">Enterprise RAG Assistant for grounded analysis of Apple financial reports</p>
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
        <div class="metric-label">DOCUMENTS</div>
        <div class="metric-value">3 Apple Filings</div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">KNOWLEDGE BASE</div>
        <div class="metric-value">281 Pages</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">CHUNKS</div>
        <div class="metric-value">1,350</div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">RETRIEVAL</div>
        <div class="metric-value">FAISS + Cosine</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Controls")

    st.markdown("### 📚 Knowledge Base")

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

    st.markdown("### 📄 Add Document")

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
            "📥 Add to Knowledge Base",
            use_container_width=True,
            type="primary"
        ):

            documents_folder = Path("data/documents")

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

    st.markdown("### 🧹 Session")

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
    '<div class="section-title">Ask the Financial Assistant</div>',
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
        "🔍 Ask AI",
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
        '<div class="section-title">💬 Conversation</div>',
        unsafe_allow_html=True
    )

    for chat in reversed(st.session_state.chat_history):

        # ----------------------------------------------------
        # USER QUESTION
        # ----------------------------------------------------

        st.markdown("### 🧑 You")

        st.markdown(
            f"> {chat['question']}"
        )


        # ----------------------------------------------------
        # AI ANSWER
        # ----------------------------------------------------

        st.markdown("### 🤖 AI Answer")

        st.markdown(
            chat["answer"]
        )


        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        if chat["sources"]:

            with st.expander(
                f"📚 View Sources & Retrieved Evidence "
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