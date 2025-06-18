# Système RAG avec LangChain, Qdrant et Ollama

Ceci est un système minimal de Génération Augmentée par Récupération (RAG) qui utilise :
- LangChain pour l'orchestration
- Qdrant pour le stockage vectoriel
- Ollama pour les embeddings et la génération locale de LLM

## Configuration

### Prérequis
- Docker et Docker Compose pour exécuter Qdrant
- Python 3.8+ pour exécuter le système RAG
- Ollama installé localement avec le modèle llama3 et le modèle nomic-embed-text

### Installation

1. Clonez ce dépôt :
```bash
git clone <repository-url>
cd test_rag
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez vos variables d'environnement :
   - Copiez le fichier `.env.example` vers `.env` ou utilisez le fichier `.env` fourni

4. Démarrez Qdrant avec Docker Compose :
```bash
docker-compose up -d
```

5. Téléchargez les modèles Ollama requis :
```bash
ollama pull llama3:8b-instruct-q4_K_M
ollama pull nomic-embed-text
```

6. Ajoutez vos documents PDF dans le répertoire `repository`.

## Utilisation

### Indexation des Documents

Pour indexer les documents dans le dépôt :

```bash
python main.py index
```

Cela va :
1. Charger tous les documents PDF et TXT du répertoire `repository`
2. Les diviser en morceaux
3. Générer des embeddings en utilisant Ollama (modèle nomic-embed-text)
4. Stocker les embeddings dans Qdrant

### Interrogation

Pour interroger les documents indexés :

```bash
python main.py query "votre question ici"
```

Cela va :
1. Convertir votre question en embedding
2. Trouver les morceaux les plus pertinents dans Qdrant
3. Générer une réponse en utilisant Ollama avec le contexte des morceaux récupérés


## Configuration

Vous pouvez configurer le système en modifiant le fichier `.env` :

- `OLLAMA_BASE_URL` : URL pour Ollama (par défaut : http://localhost:11434)
- `OLLAMA_EMBEDDING_MODEL` : Modèle Ollama à utiliser pour les embeddings (par défaut : nomic-embed-text)
- `OLLAMA_GENERATION_MODEL` : Modèle Ollama à utiliser pour la génération (par défaut : llama3:8b-instruct-q4_K_M)
- `QDRANT_URL` : URL pour Qdrant (par défaut : http://localhost:6333)
- `QDRANT_COLLECTION_NAME` : Nom de la collection dans Qdrant (par défaut : documents)
- `CHUNK_SIZE` : Taille des morceaux de texte (par défaut : 1000)
- `CHUNK_OVERLAP` : Chevauchement entre les morceaux (par défaut : 200)
- `REPOSITORY_PATH` : Chemin vers le dépôt de documents (par défaut : repository)

## Structure du Projet

- `main.py` : Interface en ligne de commande
- `indexer.py` : Chargement et indexation des documents
- `rag.py` : Traitement des requêtes et génération de réponses
- `config.py` : Gestion de la configuration
- `docker-compose.yaml` : Configuration Docker Compose pour Qdrant
- `.env` : Variables d'environnement
- `repository/` : Répertoire pour stocker les documents

## Composants

- **Ollama** : Serveur LLM local pour les embeddings et la génération de texte
- **Qdrant** : Base de données vectorielle pour stocker et récupérer les embeddings de documents
- **LangChain** : Framework pour construire des applications LLM
