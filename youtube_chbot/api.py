from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ✅ THIS IS THE CORRECT IMPORT
from langchain_classic.memory.buffer import ConversationBufferMemory

from app.transcript import fetch_transcript
from app.vectorstore import create_vectorstore
from app.rag_chain import build_rag_chain
from app.utils import load_llm


app = FastAPI(
    title="YouTube RAG Chatbot",
    description="Ask questions about any YouTube video",
    version="1.0"
)


class ChatRequest(BaseModel):
    video_id: str
    question: str
    conversation_id: str


class ChatResponse(BaseModel):
    answer: str


VECTOR_CACHE = {}
MEMORY_STORE = {}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        video_id = request.video_id
        question = request.question
        conversation_id = request.conversation_id

        # Vectorstore cache
        if video_id not in VECTOR_CACHE:
            transcript = fetch_transcript(video_id)
            vectorstore = create_vectorstore(transcript)
            VECTOR_CACHE[video_id] = vectorstore
        else:
            vectorstore = VECTOR_CACHE[video_id]

        # Conversation memory
        if conversation_id not in MEMORY_STORE:
            MEMORY_STORE[conversation_id] = ConversationBufferMemory(
                return_messages=False
            )

        memory = MEMORY_STORE[conversation_id]

        llm = load_llm()
        rag_chain = build_rag_chain(vectorstore, llm, memory)

        answer = rag_chain.invoke(question)

        memory.save_context(
            {"input": question},
            {"output": answer}
        )

        return ChatResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

