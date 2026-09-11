import uuid
from sqlalchemy.orm import Session
from models.db_models import FichierGenere


def create_fichier_genere(
    db: Session,
    dossier_id: uuid.UUID,
    type_fichier: str,
    chemin: str
) -> FichierGenere:
    """
    Enregistre un fichier généré (résumé, synthèse...) en base.
    """
    fichier = FichierGenere(
        dossier_id=dossier_id,
        type_fichier=type_fichier,
        chemin=chemin
    )
    db.add(fichier)
    db.flush()
    return fichier


def get_by_dossier_id(
    db: Session,
    dossier_id: uuid.UUID
) -> list[FichierGenere]:
    """
    Liste tous les fichiers générés pour un dossier.
    """
    return (
        db.query(FichierGenere)
        .filter(FichierGenere.dossier_id == dossier_id)
        .all()
    )


def get_by_id(
    db: Session,
    fichier_id: uuid.UUID
) -> FichierGenere | None:
    """
    Récupère un fichier généré par son id (pour le téléchargement).
    """
    return (
        db.query(FichierGenere)
        .filter(FichierGenere.id == fichier_id)
        .first()
    )