def create_chunks(documents, chunk_size=1000, overlap=200):
    chunks = []

    for document in documents:
        text = document["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text.strip(),
                    "source": document["source"],
                    "page": document["page"]
                })

            start += chunk_size - overlap

    return chunks
if __name__ == "__main__":
    from document_loader import load_all_pdfs

    documents = load_all_pdfs("data/documents")

    chunks = create_chunks(documents)

    print("\n==============================")
    print(f"TOTAL DOCUMENT PAGES: {len(documents)}")
    print(f"TOTAL CHUNKS: {len(chunks)}")
    print("==============================")

    print("\nFirst chunk:")
    print("------------------------------")
    print(chunks[0]["text"][:1000])
    print("------------------------------")
    print(f"Source: {chunks[0]['source']}")
    print(f"Page: {chunks[0]['page']}")