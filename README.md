# RAG System with LangChain, Qdrant, and Ollama

This is a minimal Retrieval-Augmented Generation (RAG) system that uses:
- LangChain for orchestration
- Qdrant for vector storage
- Ollama for embeddings and local LLM generation

## Setup

### Prerequisites
- Docker and Docker Compose for running Qdrant
- Python 3.8+ for running the RAG system
- Ollama installed locally with the llama3 model and nomic-embed-text model

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd test_rag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Copy the `.env.example` file to `.env` or use the provided `.env` file

4. Start Qdrant using Docker Compose:
```bash
docker-compose up -d
```

5. Pull the required Ollama models:
```bash
ollama pull llama3:8b-instruct-q4_K_M
ollama pull nomic-embed-text
```

6. Add your PDF documents to the `repository` directory.

## Usage

### Indexing Documents

To index the documents in the repository:

```bash
python main.py index
```

This will:
1. Load all PDF and TXT documents from the `repository` directory
2. Split them into chunks
3. Generate embeddings using Ollama (nomic-embed-text model)
4. Store the embeddings in Qdrant

### Querying

To query the indexed documents:

```bash
python main.py query "your question here"
```

This will:
1. Convert your question to an embedding
2. Find the most relevant chunks in Qdrant
3. Generate a response using Ollama with the context from the retrieved chunks

### Using OpenWebUI with RAG

This project now includes OpenWebUI, a web interface for interacting with Ollama models and the RAG system:

1. Start the Docker Compose setup which includes both Qdrant and OpenWebUI:
```bash
docker-compose up -d
```

2. Make sure Ollama is running on your host machine:
```bash
ollama serve
```

3. Index your documents as described above:
```bash
python main.py index
```

4. Access OpenWebUI in your browser at:
```
http://localhost:3000
```

5. In OpenWebUI:
   - The interface will automatically connect to your local Ollama instance
   - The RAG system is pre-configured to use your Qdrant collection
   - You can ask questions about your documents directly through the chat interface

## Configuration

You can configure the system by editing the `.env` file:

- `OLLAMA_BASE_URL`: URL for Ollama (default: http://localhost:11434)
- `OLLAMA_EMBEDDING_MODEL`: Ollama model to use for embeddings (default: nomic-embed-text)
- `OLLAMA_GENERATION_MODEL`: Ollama model to use for generation (default: llama3:8b-instruct-q4_K_M)
- `QDRANT_URL`: URL for Qdrant (default: http://localhost:6333)
- `QDRANT_COLLECTION_NAME`: Collection name in Qdrant (default: documents)
- `CHUNK_SIZE`: Size of text chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `REPOSITORY_PATH`: Path to the document repository (default: repository)

## Project Structure

- `main.py`: Command-line interface
- `indexer.py`: Document loading and indexing
- `rag.py`: Query processing and response generation
- `config.py`: Configuration management
- `docker-compose.yaml`: Docker Compose configuration for Qdrant and OpenWebUI
- `.env`: Environment variables
- `repository/`: Directory for storing documents

## Components

- **Ollama**: Local LLM server for embeddings and text generation
- **Qdrant**: Vector database for storing and retrieving document embeddings
- **LangChain**: Framework for building LLM applications
- **OpenWebUI**: Web interface for interacting with Ollama and the RAG system
