from pathlib import Path
from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


def generate_xlsx(
    content_plan: dict[str, Any],
    output_path: str | Path
) -> str:
    """
    Génère un fichier XLSX à partir d'une structure
    de contenu produite par ContentPlanner.

    Parameters
    ----------
    content_plan:
        Dictionnaire contenant le titre et les sections
        à générer.

    output_path:
        Chemin du fichier XLSX à créer.

    Returns
    -------
    str:
        Chemin du fichier XLSX généré.
    """

    # Vérification du contenu
    if not isinstance(content_plan, dict):
        raise ValueError(
            "Le contenu à générer doit être un dictionnaire."
        )

    if "titre" not in content_plan:
        raise ValueError(
            "Le contenu ne contient pas de champ 'titre'."
        )

    if "sections" not in content_plan:
        raise ValueError(
            "Le contenu ne contient pas de champ 'sections'."
        )

    titre = content_plan["titre"]
    sections = content_plan["sections"]

    if not isinstance(titre, str):
        raise ValueError(
            "Le champ 'titre' doit être une chaîne de caractères."
        )

    if not isinstance(sections, list):
        raise ValueError(
            "Le champ 'sections' doit être une liste."
        )

    # Préparer le chemin de sortie
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Créer le classeur Excel
    workbook = Workbook()

    # Feuille principale
    worksheet = workbook.active
    worksheet.title = "Synthèse"

    # Titre principal
    worksheet["A1"] = titre
    worksheet["A1"].font = Font(
        bold=True,
        size=16
    )

    # En-têtes du tableau
    worksheet["A3"] = "Section"
    worksheet["B3"] = "Contenu"

    worksheet["A3"].font = Font(bold=True)
    worksheet["B3"].font = Font(bold=True)

    # Ajouter les sections
    row = 4

    for section in sections:

        if not isinstance(section, dict):
            raise ValueError(
                "Chaque section doit être un dictionnaire."
            )

        section_title = section.get("titre")
        section_content = section.get("contenu")

        if section_title is None:
            raise ValueError(
                "Une section ne contient pas de titre."
            )

        if section_content is None:
            raise ValueError(
                f"La section '{section_title}' "
                "ne contient pas de contenu."
            )

        worksheet.cell(row=row,column=1,value=section_title)

        worksheet.cell(row=row,column=2,value=section_content)
        
        # Ajout : hauteur de ligne explicite pour éviter le glitch visuel
        worksheet.row_dimensions[row].height = 60

        row += 1

    # Mise en forme
    for current_row in worksheet.iter_rows(
        min_row=3,
        max_row=row - 1,
        min_col=1,
        max_col=2
    ):
        for cell in current_row:
            cell.alignment = Alignment(
                vertical="top",
                wrap_text=True
            )

    # Largeur des colonnes
    worksheet.column_dimensions["A"].width = 30
    worksheet.column_dimensions["B"].width = 100

    # Figer les en-têtes
    worksheet.freeze_panes = "A4"

    # Sauvegarder le fichier
    workbook.save(output_path)

    return str(output_path)