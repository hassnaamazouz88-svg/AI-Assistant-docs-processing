from core.rag import vector_store
from core.rag.embedder import embed_query

dossier_id = "2243bbeb-b81d-40fc-aa23-e8abb9900349"

collection = vector_store.get_collection()
resultat = collection.get(where={"dossier_id": dossier_id})
print(f"Nombre de chunks indexés : {len(resultat['ids'])}")

question = "Quel est l'objet du marché ?"
vecteur_question = embed_query(question)

resultats_recherche = vector_store.search(
    dossier_id=dossier_id,
    query_embedding=vecteur_question,
    top_k=5
)

for doc, distance, metadata in zip(
    resultats_recherche["documents"][0],
    resultats_recherche["distances"][0],
    resultats_recherche["metadatas"][0]
):
    print(f"\n[{metadata['nom_fichier']}, distance: {distance:.3f}]")
    print(doc[:200])