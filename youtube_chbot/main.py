from app.transcript import fetch_transcript
from app.vectorstore import create_vectorstore
from app.rag_chain import build_rag_chain
from app.utils import load_llm


def run(video_id: str, question: str):
    transcript = fetch_transcript(video_id)
    vectorstore = create_vectorstore(transcript)
    llm = load_llm()

    rag_chain = build_rag_chain(vectorstore, llm)
    answer = rag_chain.invoke(question)

    return answer


if __name__ == "__main__":
    video_id = "Gfr50f6ZBvo"
    question = "Is aliens discussed in this video?"

    response = run(video_id, question)
    print("\nAnswer:\n", response)

