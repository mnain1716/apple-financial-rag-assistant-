from pypdf import PdfReader
from pathlib import Path


def load_pdf(file_path):
    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            documents.append({
                "text": text.strip(),
                "page": page_number,
                "source": Path(file_path).name
            })

    return documents


def load_all_pdfs(folder_path):
    folder = Path(folder_path)

    all_documents = []

    for pdf_file in folder.glob("*.pdf"):
        print(f"Loading: {pdf_file.name}")

        documents = load_pdf(pdf_file)
        all_documents.extend(documents)

        print(f"  Pages loaded: {len(documents)}")

    return all_documents


if __name__ == "__main__":
    folder_path = "data/documents"

    documents = load_all_pdfs(folder_path)

    print("\n==============================")
    print(f"TOTAL PAGES LOADED: {len(documents)}")
    print("==============================")

    print("\nFirst document:")
    print(f"Source: {documents[0]['source']}")
    print(f"Page: {documents[0]['page']}")

    print("\nText preview:")
    print(documents[0]["text"][:1000])