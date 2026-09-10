import gradio as gr

from src.rag_pipeline import generate_answer


def answer_question(question):
    if not question or not question.strip():
        return "Enter a financial question first.", ""

    try:
        answer, sources = generate_answer(question.strip())
    except Exception as error:
        return f"Something went wrong: {error}", ""

    source_text = "\n\n".join(
        f"{index}. {source['source']} | Page {source['page']} | "
        f"Similarity: {source['similarity']:.4f}\n{source['text']}"
        for index, source in enumerate(sources, start=1)
    )

    return answer, source_text


with gr.Blocks(title="Apple Financial Intelligence", theme=gr.themes.Base()) as demo:
    gr.Markdown(
        "# Apple Financial Intelligence\n"
        "Search Apple financial filings with grounded source attribution."
    )

    question = gr.Textbox(
        label="Financial question",
        placeholder="What was Apple's total net sales in 2025?",
        lines=2,
    )
    ask = gr.Button("Ask", variant="primary")

    answer = gr.Markdown(label="Answer")
    sources = gr.Textbox(label="Sources and retrieved evidence", lines=12)

    ask.click(answer_question, inputs=question, outputs=[answer, sources])
    question.submit(answer_question, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=None)
