import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration centralisée
CONFIG = {
    # Configuration d'Ollama
    "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL"),
    "OLLAMA_EMBEDDING_MODEL": os.getenv("OLLAMA_EMBEDDING_MODEL"),
    "OLLAMA_GENERATION_MODEL": os.getenv("OLLAMA_GENERATION_MODEL"),

    # Configuration de Qdrant
    "QDRANT_URL": os.getenv("QDRANT_URL"),
    "QDRANT_COLLECTION_NAME": os.getenv("QDRANT_COLLECTION_NAME"),

    # Configuration du traitement des documents
    "CHUNK_SIZE": int(os.getenv("CHUNK_SIZE", "1000")),
    "CHUNK_OVERLAP": int(os.getenv("CHUNK_OVERLAP", "200")),
    "REPOSITORY_PATH": os.getenv("REPOSITORY_PATH", "repository"),
}
