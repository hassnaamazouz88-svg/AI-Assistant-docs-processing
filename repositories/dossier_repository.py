import uuid
from sqlalchemy.orm import Session
from models.db_models import Dossier


def create_dossier(db: Session, nom: str) -> Dossier:
    """
    Crée un nouveau dossier (pas encore commité définitivement).
    """
    dossier = Dossier(
        nom=nom
    )
    db.add(dossier)
    db.flush()
    return dossier


def get_by_id(db: Session, dossier_id: uuid.UUID) -> Dossier | None:
    """
    Récupère un dossier par son id.

    Utilisé par le service d'ingestion pour vérifier que le
    dossier existe avant de lancer le traitement.

    Args:
        db: session SQLAlchemy
        dossier_id: ID du dossier recherché

    Returns:
        Le dossier trouvé, ou None s'il n'existe pas.
    """
    return db.query(Dossier).filter(Dossier.id == dossier_id).first()

def get_all(db: Session) -> list[Dossier]:
    """Liste tous les dossiers."""
    return db.query(Dossier).order_by(Dossier.created_at.desc()).all()


def update_statut(
    db: Session,
    dossier_id: uuid.UUID,
    statut: str
) -> Dossier | None:
    """
    Met à jour le statut global d'un dossier.

    Utilisé par le service d'ingestion pour marquer le dossier
    comme "pret" une fois tous ses documents traités.

    Args:
        db: session SQLAlchemy
        dossier_id: ID du dossier à mettre à jour
        statut: nouveau statut ("pret", "en_cours", "echec", etc.)

    Returns:
        Le dossier mis à jour, ou None s'il n'existe pas.
    """
    dossier = db.query(Dossier).filter(Dossier.id == dossier_id).first()

    if dossier is None:
        return None

    dossier.statut = statut
    db.flush()
    return dossier