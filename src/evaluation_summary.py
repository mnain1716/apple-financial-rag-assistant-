import pandas as pd


def create_summary():

    df = pd.read_csv("data/evaluation_results.csv")

    total_questions = len(df)

    successful_answers = (
        df["generated_answer"] != "ERROR"
    ).sum()

    retrieval_success = (
        df["source_found"] == True
    ).sum()

    api_errors = (
        df["generated_answer"] == "ERROR"
    ).sum()

    retrieval_rate = (
        retrieval_success / total_questions
    ) * 100

    answer_rate = (
        successful_answers / total_questions
    ) * 100

    print("\n==============================")
    print("RAG EVALUATION SUMMARY")
    print("==============================")

    print(f"Total Questions: {total_questions}")
    print(f"Successful Answers: {successful_answers}")
    print(f"Retrieved Sources: {retrieval_success}")
    print(f"Retrieval Success Rate: {retrieval_rate:.1f}%")
    print(f"Answer Generation Rate: {answer_rate:.1f}%")
    print(f"API/Generation Errors: {api_errors}")

    print("==============================")


if __name__ == "__main__":
    create_summary()