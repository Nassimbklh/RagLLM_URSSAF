from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from config import CONFIG
from pathlib import Path
import os

def load_documents():
    """
    Charger les documents depuis le répertoire du dépôt.
    Prend en charge les fichiers PDF et TXT.
    """
    documents = []
    script_dir = Path(__file__).parent.absolute()
    repository_path = script_dir / CONFIG["REPOSITORY_PATH"]

    if not repository_path.exists():
        print(f"Le répertoire du dépôt {repository_path} n'existe pas.")
        return documents

    for file_path in repository_path.rglob("*.*"):
        if file_path.suffix.lower() == ".pdf":
            print(f"Chargement du PDF : {file_path}")
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())
        elif file_path.suffix.lower() == ".txt":
            print(f"Chargement du TXT : {file_path}")
            loader = TextLoader(str(file_path))
            documents.extend(loader.load())

    return documents

def index_repository():
    """
    Indexer les documents dans le dépôt:
    1. Charger les documents
    2. Diviser en morceaux
    3. Générer des embeddings en utilisant OpenAI
    4. Stocker dans Qdrant
    """
    # Charger les documents
    docs = load_documents()
    if not docs:
        print("Aucun document trouvé à indexer.")
        return

    print(f"{len(docs)} pages de documents chargées.")


    splitter = RecursiveCharacterTextSplitter(

        chunk_size=CONFIG["CHUNK_SIZE"],
        chunk_overlap=CONFIG["CHUNK_OVERLAP"],
        separators=["\n\n", "\n", " ", ""]

    )
    chunks = splitter.split_documents(docs)

    print(f"{len(chunks)} fragments de documents créés.")


    embeddings = OllamaEmbeddings(
        base_url=CONFIG["OLLAMA_BASE_URL"],
        model=CONFIG["OLLAMA_EMBEDDING_MODEL"]
    )

    print("Génération des embeddings...")
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    # Connexion à Qdrant
    qdrant = QdrantClient(url=CONFIG["QDRANT_URL"])

    # Générer un embedding d'exemple pour déterminer la dimension du vecteur
    print("Détermination de la dimension du vecteur...")
    sample_vector = embeddings.embed_query("Texte d'exemple pour la détection de dimension")
    vector_size = len(sample_vector)
    print(f"Dimension du vecteur : {vector_size}")

    # Vérifier si la collection existe et a la bonne taille de vecteur
    collection_name = CONFIG["QDRANT_COLLECTION_NAME"]
    try:
        # Essayer d'obtenir les informations de la collection
        collection_info = qdrant.get_collection(collection_name=collection_name)
        existing_vector_size = collection_info.config.params.vectors.size

        # Si la taille du vecteur ne correspond pas, recréer la collection
        if existing_vector_size != vector_size:
            print(f"La collection existante a une dimension de vecteur de {existing_vector_size}, mais les embeddings actuels ont une dimension de {vector_size}")
            print(f"Recréation de la collection {collection_name}...")
            qdrant.delete_collection(collection_name=collection_name)
            qdrant.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            print(f"Collection recréée : {collection_name}")
        else:
            print(f"Utilisation de la collection existante : {collection_name}")
    except Exception as e:
        # La collection n'existe pas, la créer
        print(f"Création d'une nouvelle collection : {collection_name}")
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    # Générer des embeddings et créer des points
    batch_size = 100  # Traiter par lots pour éviter les problèmes de mémoire
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_metadatas = metadatas[i:i+batch_size]

        print(f"Traitement du lot {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}...")

        # Générer des embeddings pour le lot
        vectors = embeddings.embed_documents(batch_texts)

        # Créer des points
        points = []
        for j in range(len(batch_texts)):
            point = PointStruct(
                id=i + j,
                vector=vectors[j],
                payload={
                    "text": batch_texts[j],
                    "metadata": batch_metadatas[j]
                }
            )
            points.append(point)

        # Insérer dans Qdrant
        qdrant.upsert(
            collection_name=CONFIG["QDRANT_COLLECTION_NAME"],
            points=points
        )

    print(f"Indexation terminée. {len(chunks)} fragments indexés dans Qdrant.")

if __name__ == "__main__":
    index_repository()
