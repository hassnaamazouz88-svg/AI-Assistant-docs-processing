from uuid import UUID

from core.rag.embedder import embed_query
from core.rag.vector_store import search


def retrieve(
    question: str,
    dossier_id: UUID,
    top_k: int = 8
) -> list[dict]:
    """
    Récupère les chunks les plus pertinents pour une question
    dans un dossier précis.

    Pipeline :

        question
            ↓
        embed_query()
            ↓
        vector_store.search()
            ↓
        résultats ChromaDB
            ↓
        liste de chunks normalisée

    Args:
        question: Question posée par l'utilisateur.
        dossier_id: Identifiant du dossier à interroger.
        top_k: Nombre maximum de chunks à récupérer.

    Returns:
        Liste de dictionnaires contenant notamment :

        {
            "text": "...",
            "dossier_id": "...",
            "document_id": "...",
            "nom_fichier": "...",
            "chunk_index": 0,
            "distance": 0.12
        }
    """

    # --------------------------------------------------------
    # 1. Transformer la question en embedding
    # --------------------------------------------------------

    query_embedding = embed_query(question)

    # --------------------------------------------------------
    # 2. Recherche dans ChromaDB
    # --------------------------------------------------------

    results = search(
        dossier_id=dossier_id,
        query_embedding=query_embedding,
        top_k=top_k
    )

    # --------------------------------------------------------
    # 3. Normaliser la réponse de ChromaDB
    # --------------------------------------------------------

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved_chunks = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        retrieved_chunks.append({
            "text": document,
            "dossier_id": metadata.get("dossier_id"),
            "document_id": metadata.get("document_id"),
            "nom_fichier": metadata.get("nom_fichier"),
            "chunk_index": metadata.get("chunk_index"),
            "distance": distance,
        })

    return retrieved_chunks