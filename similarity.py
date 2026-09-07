import numpy as np
from core.rag.embedder import embed_documents

textes = [
    "Le délai d'exécution du marché est de 90 jours.",
    "Les travaux doivent être achevés dans un délai de trois mois.",
    "Le prix unitaire de la ramette de papier est de 45 DH."
]

vecteurs = embed_documents(textes)

def similarite_cosinus(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("Phrase 1 vs 2 (sens proche) :", similarite_cosinus(vecteurs[0], vecteurs[1]))
print("Phrase 1 vs 3 (sens différent) :", similarite_cosinus(vecteurs[0], vecteurs[2]))