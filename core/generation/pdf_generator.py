import subprocess
import os

from core.generation.docx_generator import generate_docx


def generate_pdf(content_plan: dict, output_path: str) -> str:
    """
    Génère un PDF à partir d'une structure de contenu, en passant
    par une génération DOCX intermédiaire convertie ensuite via
    LibreOffice.
    """
    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    docx_temp_path = os.path.join(output_dir, "_temp_generation.docx")
    generate_docx(content_plan, docx_temp_path)

    result = subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            docx_temp_path
        ],
        capture_output=True,
        text=True,
        timeout=60
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Échec de la conversion en PDF.\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    base_name = os.path.splitext(os.path.basename(docx_temp_path))[0]
    pdf_genere = os.path.join(output_dir, f"{base_name}.pdf")

    # os.replace() au lieu de os.rename() : écrase silencieusement
    # le fichier de destination s'il existe déjà (comportement
    # cohérent entre Windows et Linux/Mac, contrairement à rename)
    os.replace(pdf_genere, output_path)

    # Nettoyage du DOCX temporaire
    if os.path.exists(docx_temp_path):
        os.remove(docx_temp_path)

    return output_path



def convert_to_pdf(file_path: str) -> str:
    """
    Convertit un fichier Office existant (docx, xlsx...) en PDF via
    LibreOffice, sans passer par un content_plan — utilisé pour
    prévisualiser un fichier déjà généré, sans le regénérer depuis
    zéro.

    Args:
        file_path: chemin du fichier à convertir

    Returns:
        Le chemin du PDF résultant.
    """
    file_path = os.path.abspath(file_path)
    output_dir = os.path.dirname(file_path)

    result = subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            file_path
        ],
        capture_output=True,
        text=True,
        timeout=60
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Échec de la conversion en PDF pour prévisualisation.\n"
            f"stderr: {result.stderr}"
        )

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    return os.path.join(output_dir, f"{base_name}.pdf")


def get_or_create_preview_pdf(file_path: str) -> str:
    """
    Retourne le chemin d'un PDF d'aperçu pour un fichier docx/xlsx
    donné — le convertit via LibreOffice uniquement s'il n'a pas
    déjà été converti auparavant (mise en cache simple sur disque).

    Le cache est basé sur le nom du fichier source : si celui-ci
    change de contenu sans changer de nom, le cache ne sera pas
    invalidé automatiquement (limite acceptée pour cette V1 — les
    fichiers générés ont un nom unique par uuid.uuid4(), donc ce
    cas ne se produit jamais en pratique dans ce projet).

    Args:
        file_path: chemin du fichier source (docx ou xlsx)

    Returns:
        Le chemin du PDF d'aperçu (existant ou nouvellement créé).
    """
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.dirname(os.path.abspath(file_path))
    chemin_pdf_cache = os.path.join(output_dir, f"{base_name}.pdf")

    # Le cache existe déjà : on le réutilise directement
    if os.path.exists(chemin_pdf_cache):
        return chemin_pdf_cache

    # Sinon, on convertit une première fois
    return convert_to_pdf(file_path)