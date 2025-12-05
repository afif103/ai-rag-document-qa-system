FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Pull Ollama models
RUN ollama pull llama3.2:3b && ollama pull nomic-embed-text

# Expose ports
EXPOSE 8000 8501

# Start Ollama in background and run the app
CMD ["sh", "-c", "ollama serve & sleep 5 && uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8502 --server.address 0.0.0.0"]