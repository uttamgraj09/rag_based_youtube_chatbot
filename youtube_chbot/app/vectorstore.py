from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def create_vectorstore(transcript: str) -> FAISS:
    """
    Create FAISS vector store from transcript text.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", "!", "?"]
    )

    documents = splitter.create_documents([transcript])

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

