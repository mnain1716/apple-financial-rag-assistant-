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
                 └────────┬─────────┘
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