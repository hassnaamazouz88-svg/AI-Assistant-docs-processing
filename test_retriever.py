from uuid import UUID
from core.rag.retriever import retrieve

DOSSIER_ID = UUID("2243bbeb-b81d-40fc-aa23-e8abb9900349")

results = retrieve(
    question="Quels sont les critères demandés dans cet appel d'offres ?",
    dossier_id=DOSSIER_ID,
    top_k=5
)

print(f"\nNombre de résultats : {len(results)}\n")
for i, result in enumerate(results, start=1):
    print("=" * 70)
    print(f"Résultat #{i} — {result['nom_fichier']} (chunk {result['chunk_index']}, distance {result['distance']:.3f})")
    print(result["text"][:200])