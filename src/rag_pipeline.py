from dotenv import load_dotenv
from google import genai
import os
import re
from src.retriever import load_vector_store, search

load_dotenv()


# Gemini client
client = genai.Client()


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
        model="gemini-3.7-flash",
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