from werkzeug.utils import secure_filename


from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import sys
import shutil
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from tools.rag_tools import (
    load_pdf,
    split_text,
    create_vector_store,
)
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import datetime

load_dotenv(dotenv_path="config/.env")


class QuestionRequest(BaseModel):
    question: str


app = FastAPI()

vector_store = None


def check_ollama_health():
    try:
        # Try to create embeddings to check if Ollama is running
        test_embeddings = OllamaEmbeddings(model="nomic-embed-text")
        return True, None
    except Exception as e:
        error_str = str(e).lower()
        if "model" in error_str and "not found" in error_str:
            return (
                False,
                "Model 'nomic-embed-text' not found. Run: ollama pull nomic-embed-text",
            )
        elif "connection" in error_str or "http" in error_str or "connect" in error_str:
            return False, "Ollama not running. Start with: ollama serve"
        else:
            return False, f"Ollama error: {str(e)}"


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store
    try:
        print("Starting upload")
        print(f"Received file: {file.filename}")
        # Safety: Input validation
        print("Checking filename presence")
        if not file.filename:
            print("No filename")
            raise HTTPException(status_code=400, detail="No file provided")
        print("Checking filename extension")
        if not file.filename.endswith(".pdf"):
            print("Filename does not end with .pdf")
            raise HTTPException(
                status_code=400,
                detail="Invalid filename. Only PDF files (.pdf extension) are allowed",
            )
        # if file.content_type != "application/pdf":
        #     raise HTTPException(
        #         status_code=400, detail="Invalid file type. Only PDF files are allowed"
        #     )
        print("Checking file size")
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Seek back to start
        if file_size > 10 * 1024 * 1024:
            print("File too large")
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        print("Sanitizing filename")
        safe_filename = secure_filename(file.filename)
        if not safe_filename:
            print("Invalid filename after sanitization")
            vector_store = "mock"
            return {
                "message": "PDF uploaded successfully (Invalid filename, using mock mode)"
            }

        file_path = f"data/{safe_filename}"
        print(f"Saving file to {file_path}")
        with open(file_path, "wb") as buffer:
            await file.seek(0)
            content = await file.read()
            buffer.write(content)

        print("Loading PDF")
        documents = load_pdf(file_path)
        print(f"Loaded {len(documents)} documents")

        print("Splitting text")
        chunks = split_text(documents)
        print(f"Created {len(chunks)} chunks")

        print("Creating embeddings")
        health, message = check_ollama_health()
        if not health:
            print(f"Health check failed: {message}, using mock")
            vector_store = "mock"
            return {
                "message": "PDF uploaded successfully (Ollama not available, using mock mode)"
            }
        try:
            embeddings = OllamaEmbeddings(model="nomic-embed-text")
            print("Embeddings created")
        except Exception as e:
            print(f"Embeddings creation failed: {e}, using mock")
            vector_store = "mock"
            return {
                "message": "PDF uploaded successfully (Embeddings failed, using mock mode)"
            }

        print("Creating vector store")
        try:
            vector_store = create_vector_store(chunks, embeddings)
            print("Vector store created")
        except Exception as e:
            print(f"Vector store creation failed: {e}, using mock")
            vector_store = "mock"
            return {
                "message": "PDF uploaded successfully (Vector store failed, using mock mode)"
            }

        with open("memory.txt", "a") as f:
            f.write(
                f"{datetime.datetime.now()}: Successful PDF upload: {safe_filename}\n"
            )
        return {"message": "PDF uploaded and processed successfully"}
    except Exception as e:
        print(f"Error processing PDF: {type(e).__name__}: {e}")
        if isinstance(e, HTTPException):
            detail = e.detail
        else:
            detail = f"Error processing PDF: {type(e).__name__}: {str(e)}"
        raise HTTPException(status_code=500, detail=detail)


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    if vector_store is None:
        raise HTTPException(status_code=400, detail="No document uploaded yet")

    if vector_store == "mock":
        return {
            "answer": "Ollama not running. Start with: ollama serve",
            "confidence": 0.0,
        }

    # Use Ollama for local LLM
    llm = ChatOllama(model="llama3.2:3b")

    retriever = vector_store.as_retriever()
    # Get docs with scores for confidence
    docs_with_scores = vector_store.similarity_search_with_score(request.question, k=3)
    if docs_with_scores:
        min_score = min(score for _, score in docs_with_scores)
        print(f"Min score: {min_score}")
        # Normalize score (FAISS scores are distance, lower better)
        confidence = max(
            0, 1 - min_score / 1000
        )  # Adjust normalization for high scores
    else:
        confidence = 0.0

    prompt = ChatPromptTemplate.from_template(
        "Answer the question based on the context.\nContext: {context}\nQuestion: {question}"
    )
    qa_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = qa_chain.invoke(request.question)
    with open("memory.txt", "a") as f:
        f.write(
            f"{datetime.datetime.now()}: Q: {request.question} | A: {answer} | Confidence: {confidence:.2f}\n"
        )
    return {"answer": answer, "confidence": round(confidence, 2)}
