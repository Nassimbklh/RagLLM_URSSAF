from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from qdrant_client import QdrantClient
from config import CONFIG

def generate_response(query: str) -> str:
    """
    Générer une réponse à une requête en utilisant RAG:
    1. Convertir la requête en embedding en utilisant Ollama
    2. Rechercher des morceaux pertinents dans Qdrant
    3. Générer une réponse en utilisant Ollama avec le contexte des morceaux récupérés

    Args:
        query: La question de l'utilisateur

    Returns:
        La réponse générée
    """
    # Générer l'embedding pour la requête
    embeddings = OllamaEmbeddings(
        base_url=CONFIG["OLLAMA_BASE_URL"],
        model=CONFIG["OLLAMA_EMBEDDING_MODEL"]
    )
    query_vector = embeddings.embed_query(query)

    # Rechercher des morceaux pertinents dans Qdrant
    qdrant = QdrantClient(url=CONFIG["QDRANT_URL"])
    search_results = qdrant.search(
        collection_name=CONFIG["QDRANT_COLLECTION_NAME"],
        query_vector=query_vector,
        limit=5  # Récupérer les 5 morceaux les plus pertinents
    )

    # Extraire le texte des résultats de recherche
    if not search_results:
        return "Je n'ai pas trouvé d'information pertinente pour répondre à cette question."

    # Construire le contexte à partir des morceaux récupérés
    context = "\n\n".join([hit.payload["text"] for hit in search_results])

    # Créer le prompt avec le contexte et la requête
    prompt = f"""
Tu es un assistant expert. Utilise uniquement les informations du contexte pour répondre.
Si tu ne trouves pas d'information pertinente dans le contexte, indique-le clairement.

Contexte :
{context}

Question : {query}

Réponse :
"""

    # Générer la réponse en utilisant Ollama
    llm = OllamaLLM(
        base_url=CONFIG["OLLAMA_BASE_URL"],
        model=CONFIG["OLLAMA_GENERATION_MODEL"]
    )

    # Générer et retourner la réponse
    return llm.invoke(prompt)

if __name__ == "__main__":
    # Tester le système RAG
    test_query = "Quel est le sujet principal du document?"
    response = generate_response(test_query)
    print(f"Question : {test_query}")
    print(f"Réponse : {response}")
