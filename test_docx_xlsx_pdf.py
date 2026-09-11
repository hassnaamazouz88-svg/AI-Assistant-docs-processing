from uuid import UUID
from core.generation.content_planner import ContentPlanner
from core.generation.docx_generator import generate_docx
from core.generation.xlsx_generator import generate_xlsx
from core.generation.pdf_generator import generate_pdf

DOSSIER_ID = UUID("2243bbeb-b81d-40fc-aa23-e8abb9900349")

planner = ContentPlanner()
plan = planner.plan(
    request="Génère un résumé du marché avec l'objet, le montant, et le délai d'exécution",
    dossier_id=DOSSIER_ID
)

chemin_docx = generate_docx(plan, "storage/generated_test/resume.docx")
chemin_xlsx = generate_xlsx(plan, "storage/generated_test/resume.xlsx")
chemin_pdf = generate_pdf(plan, "storage/generated_test/resume.pdf")

print("DOCX :", chemin_docx)
print("XLSX :", chemin_xlsx)
print("PDF :", chemin_pdf)