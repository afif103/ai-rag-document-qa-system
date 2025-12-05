from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


def split_text(documents, chunk_size=500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


# create_embeddings removed, using OllamaEmbeddings


def create_vector_store(chunks, embeddings, persist_directory="./data/vector_db"):
    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=persist_directory
    )
    return vector_store


def load_vector_store(embeddings, persist_directory="./data/vector_db"):
    vector_store = Chroma(
        persist_directory=persist_directory, embedding_function=embeddings
    )
    return vector_store
