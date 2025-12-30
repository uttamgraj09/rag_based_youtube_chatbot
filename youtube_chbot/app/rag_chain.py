from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough
)

# ✅ CORRECT import for YOUR environment
from langchain_classic.memory.buffer import ConversationBufferMemory


def build_rag_chain(vectorstore, llm, memory: ConversationBufferMemory):
    """
    Build a RAG chain with conversation memory.
    """

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "lambda_mult": 0.7}
    )

    prompt = PromptTemplate(
        input_variables=["context", "question", "chat_history"],
        template="""
You are a helpful assistant answering questions about a YouTube video.

Rules:
- Use ONLY the provided context from the transcript.
- If the answer is not present, say: "This was not discussed in the video."
- Be concise and factual.

Chat history:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
"""
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
            "chat_history": RunnableLambda(
                lambda _: memory.load_memory_variables({})["history"]
            )
        })
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

