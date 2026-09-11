import os
from core.ingestion.pipeline import process_document

fichier_a_tester = "storage/dossiers/2243bbeb-b81d-40fc-aa23-e8abb9900349/CPS.docx"

print("Le fichier existe :", os.path.exists(fichier_a_tester))

texte = process_document(fichier_a_tester)
print(f"Longueur totale du texte : {len(texte)} caractères")
print("--- DÉBUT ---")
print(texte[:500])