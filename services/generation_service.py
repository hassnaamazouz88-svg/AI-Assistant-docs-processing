import os
import uuid
from sqlalchemy.orm import Session

from core.generation.content_planner import ContentPlanner
from core.generation.docx_generator import generate_docx
from core.generation.xlsx_generator import generate_xlsx
from core.generation.pdf_generator import generate_pdf
from repositories import fichier_genere_repository


GENERATEURS = {
    "docx": generate_docx,
    "xlsx": generate_xlsx,
    "pdf": generate_pdf,
}


def generate_document(
    db: Session,
    dossier_id: uuid.UUID,
    request: str,
    format: str = "docx"
) -> dict:
    """
    Orchestre la génération complète d'un document : planification
    du contenu via le LLM, génération du fichier dans le format
    demandé, puis enregistrement en base.

    Args:
        db: session SQLAlchemy
        dossier_id: id du dossier concerné
        request: la demande de génération formulée par l'utilisateur
        format: "docx", "xlsx" ou "pdf"

    Returns:
        {"fichier_id": ..., "chemin": ..., "titre": ...}
    """
    if format not in GENERATEURS:
        raise ValueError(
            f"Format non supporté : {format}. "
            f"Formats disponibles : {list(GENERATEURS.keys())}"
        )

    # 1. Planifier le contenu (recherche + LLM + validation)
    planner = ContentPlanner()
    plan = planner.plan(request=request, dossier_id=dossier_id)

    # 2. Construire le chemin de sortie
    nom_fichier = f"{uuid.uuid4()}.{format}"
    output_path = os.path.abspath(os.path.join(
        "storage", "dossiers", str(dossier_id), "generated", nom_fichier
    ))

    # 3. Générer le fichier dans le format demandé
    generateur = GENERATEURS[format]
    chemin_final = generateur(plan, output_path)

    # 4. Enregistrer en base
    fichier = fichier_genere_repository.create_fichier_genere(
        db=db,
        dossier_id=dossier_id,
        type_fichier=format,
        chemin=chemin_final
    )
    db.commit()

    return {
        "fichier_id": fichier.id,
        "chemin": chemin_final,
        "titre": plan["titre"]
    }