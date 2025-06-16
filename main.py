import argparse
from indexer import index_repository
from rag import generate_response

def main():
    """
    Point d'entrée principal pour le système RAG.
    - index : pour indexer les documents
    - query : pour interroger les documents indexés
    """
    parser = argparse.ArgumentParser(description="RAG (Retrieval-Augmented Generation) System")
    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")

    # Définir les sous-commandes
    subparsers.add_parser("index", help="Indexer les documents dans le dépôt")

    query_parser = subparsers.add_parser("query", help="Poser une question aux documents indexés")
    query_parser.add_argument("question", nargs="+", help="La question à poser")

    args = parser.parse_args()

    if args.command == "index":
        print("Indexation des documents...")
        index_repository()
        print("Indexation terminée.")

    elif args.command == "query":
        question = " ".join(args.question)
        print(f"Question : {question}")
        print("Génération de la réponse...")
        response = generate_response(question)
        print("\nRéponse :")
        print(response)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()