# AI RAG Document Q&A System

A local AI-powered document question-answering system using RAG (Retrieval-Augmented Generation).

## Features

- PDF document processing and text extraction
- Local embeddings using Ollama
- Vector search with FAISS
- Local LLM responses with Ollama
- Confidence scoring for answers
- Streamlit web interface
- Docker deployment support
- Comprehensive security and error handling
- Session memory logging

## Quick Start

### Prerequisites

- Python 3.12+
- Ollama (for local AI models)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/afif103/ai-rag-document-qa-system.git
   cd ai-rag-document-qa-system
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and setup Ollama:**
   - Download from https://ollama.ai/
   - Pull required models:
     ```bash
     ollama pull llama3.2:3b
     ollama pull nomic-embed-text
     ```

5. **Run the application:**
   ```bash
   # Terminal 1: Start Ollama
   ollama serve

   # Terminal 2: Start backend
   uvicorn backend.main:app --reload

   # Terminal 3: Start frontend
   streamlit run frontend/app.py
   ```

6. **Access the application:**
   - Frontend: http://localhost:8502
   - Backend API: http://localhost:8001

## Setup Details

### Local Setup (without Docker)

Follow the Quick Start steps above.

### Docker Setup

1. **Build and run with Docker:**
   ```bash
   docker build -t ai-rag-system .
   docker run -p 8001:8001 -p 8502:8502 ai-rag-system
   ```

2. **Access the application:**
   - Frontend: http://localhost:8502
   - Backend API: http://localhost:8001

### Troubleshooting

- **Ollama connection issues:** Ensure `ollama serve` is running
- **Model not found:** Run `ollama pull llama3.2:3b` and `ollama pull nomic-embed-text`
- **Port conflicts:** Change ports in commands if needed
- **PDF processing fails:** Use text-based PDFs, check Ollama status

## Usage

1. **Upload a PDF:** Use the file uploader in the Streamlit interface
2. **Ask questions:** Type questions about the document content
3. **View answers:** Get AI-powered responses with confidence scores
4. **Check memory:** View conversation history in memory.txt

## Architecture

- **Backend**: FastAPI with async endpoints, RAG pipeline, security validation
- **Frontend**: Streamlit web app with file upload and Q&A interface
- **LLM**: Ollama (llama3.2:3b) for local inference
- **Embeddings**: Ollama (nomic-embed-text) for local vectorization
- **Vector Store**: FAISS for efficient similarity search
- **Document Processing**: PyPDFLoader with recursive text splitting
- **Memory**: Automatic logging of successful operations and conversations

## Development

- **Run tests:** `python test_qa.py`
- **Lint:** `ruff check . && ruff format .`
- **Type check:** `mypy .`
- **Environment:** Copy `.env.example` to `.env` and configure

## Project Structure

```
ai-rag-document-qa-system/
├── backend/
│   ├── main.py          # FastAPI backend
│   └── __init__.py
├── frontend/
│   ├── app.py           # Streamlit frontend
│   └── __init__.py
├── tools/
│   ├── rag_tools.py     # RAG utilities
│   └── __init__.py
├── config/
│   ├── .env             # Environment variables
│   └── __init__.py
├── data/                # Document storage
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Submit a pull request

## License

MIT License - see LICENSE file for details