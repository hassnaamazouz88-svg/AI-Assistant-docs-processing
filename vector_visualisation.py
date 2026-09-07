from core.rag import vector_store

dossier_id = "37e3cb7d-3acc-4057-bd54-2348fbc4df06"

collection = vector_store.get_collection()
resultat = collection.get(
    where={"dossier_id": dossier_id},
    include=["embeddings", "documents", "metadatas"],
    limit=1  # juste le premier, pour voir à quoi ça ressemble
)

print("Texte du chunk :", resultat["documents"][0][:100])
print("Dimensions du vecteur :", len(resultat["embeddings"][0]))
print("Premières valeurs :", resultat["embeddings"][0][:10])