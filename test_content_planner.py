from uuid import UUID
from core.generation.content_planner import ContentPlanner

DOSSIER_ID = UUID("2243bbeb-b81d-40fc-aa23-e8abb9900349")

planner = ContentPlanner()
plan = planner.plan(
    request="Génère un résumé du marché avec l'objet, le montant, et le délai d'exécution",
    dossier_id=DOSSIER_ID
)

print("--- TITRE ---")
print(plan["titre"])
print("\n--- SECTIONS ---")
for section in plan["sections"]:
    print(f"\n### {section['titre']}")
    print(section["contenu"])