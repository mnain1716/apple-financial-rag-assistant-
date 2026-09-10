from dotenv import load_dotenv
from google import genai
import os
import re
import streamlit as st
from src.retriever import load_vector_store, search

load_dotenv()


def _get_setting(name):
    value = os.getenv(name)
    if value:
        return value

    try:
        return st.secrets.get(name)
    except (FileNotFoundError, KeyError):
        return None


api_key = _get_setting("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. Add it to .env locally or "
        "Streamlit Cloud Secrets when deployed."
    )

client = genai.Client(api_key=api_key)
model_name = _get_setting("GEMINI_MODEL") or "gemini-3.6-flash"


# Load FAISS vector store
index, chunks = load_vector_store()


def generate_answer(question, top_k=5):

    # Retrieve relevant document chunks
    results = search(
        question,
        index,
        chunks,
        top_k=top_k
    )
    # Check whether the question contains a year
    year_match = re.search(r"\b(20\d{2})\b", question)

    if year_match:
        requested_year = year_match.group(1)

        year_found = any(
            requested_year in result["text"]
            for result in results
        )

        if not year_found:
            return (
                "I could not find sufficient information in the provided documents "
                "to answer this question.",
                []
            )
    # Prepare context
    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}, Page: {result['page']}\n"
            f"{result['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # Grounded RAG prompt
    prompt = f"""
You are an enterprise financial document assistant.

Answer the user's question ONLY using the provided document context.

IMPORTANT RULES:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the provided context does not contain enough information,
   say exactly:
   "I could not find sufficient information in the provided documents to answer this question."
4. Give a clear and concise answer.
5. Include source references using the document name and page number.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    return response.text, results


if __name__ == "__main__":

    question = "What was Apple's total net sales in 2046?"

    answer, sources = generate_answer(question)

    print("\n==============================")
    print("RAG ANSWER")
    print("==============================")

    print(answer)

    print("\n==============================")
    print("RETRIEVED SOURCES")
    print("==============================")

    for i, source in enumerate(sources, start=1):
        print(
            f"{i}. {source['source']} | "
            f"Page {source['page']} | "
            f"Cosine Similarity: {source['similarity']:.4f}"        )