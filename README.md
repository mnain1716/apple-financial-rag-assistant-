# 📊 Apple Financial Document Intelligence

An enterprise-focused Retrieval-Augmented Generation (RAG) assistant for answering questions from Apple's public financial reports.

The system combines document processing, semantic embeddings, FAISS vector search, retrieval, Gemini-based generation, source attribution, hallucination handling, and a Streamlit interface.

---

## 🎯 Project Overview

Organizations often need to find specific information from large financial reports and business documents.

This project builds a financial document intelligence assistant that allows users to ask natural-language questions about Apple's financial reports and receive grounded answers based only on the indexed documents.

### Selected Domain

**Financial Document Intelligence**

The financial domain was selected because annual reports contain structured and unstructured information such as:

- Revenue and net sales
- Product-wise sales
- Services revenue
- Year-over-year changes
- Financial performance information

---

## 🏢 Business Problem

Large financial reports can contain hundreds of pages, making manual information retrieval slow and inefficient.

The goal of this project is to provide a question-answering interface that retrieves relevant evidence from financial documents and generates an answer grounded in that evidence.

---

## 📚 Document Collection

The knowledge base contains public Apple financial reports for:

- 2023
- 2024
- 2025

The documents are public financial filings and are used for educational and internship-project purposes.

---

## 🏗️ System Architecture

```text
                 ┌──────────────────┐
                 │  Financial PDFs  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Document Loading │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Text Extraction  │
                          │
                          ▼
                 ┌──────────────────┐
                 │    Chunking      │
                 │ + Page Metadata  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    Embeddings    │
                 │ MiniLM-L6-v2     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   FAISS Index    │
                 └────────┬─────────┘
                          │
                          │
User Question ────────────┘
       │
       ▼
┌──────────────────┐
│ Query Embedding  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Semantic Search  │
│      Top-K       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Retrieved Context│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Gemini LLM       │
│ Grounded Prompt  │
└────────┬─────────┘
         │
         ▼
┌────────────────────────────┐
│ Answer + Source References │
└────────────────────────────┘
```

## Run Locally

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash
```

Install the pinned dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The committed `vectorstore/faiss.index` and `vectorstore/chunks.pkl` files are required at startup. The embedding model downloads automatically on first run.

## Deploy on Streamlit Community Cloud

1. Push this project to GitHub. Do not commit `.env` or any API key.
2. Create a new app at [share.streamlit.io](https://share.streamlit.io/).
3. Select the repository and branch, then set the main file to `app.py`.
4. In **Advanced settings -> Secrets**, add:

   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   GEMINI_MODEL = "gemini-3.6-flash"
   ```

5. Deploy. Streamlit Cloud installs `requirements.txt`, loads the committed vector store, and uses the secret for Gemini requests.

Uploaded PDFs and rebuilt indexes use temporary deployment storage and are not persistent across restarts.

If an API key was ever exposed outside `.env`, revoke it in Google AI Studio and create a replacement before deployment.