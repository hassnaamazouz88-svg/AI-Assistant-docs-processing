import uuid

from tasks.celery_app import celery_app
from config.database import SessionLocal
from services import ingestion_service


@celery_app.task(name="tasks.ingest_dossier_task", bind=True)
def ingest_dossier_task(self, dossier_id_str: str) -> dict:
    """
    Tâche Celery qui exécute l'ingestion complète d'un dossier
    en arrière-plan.
    """
    dossier_id = uuid.UUID(dossier_id_str)

    # Ce code tourne dans un processus séparé (le worker Celery),
    # jamais dans le processus Uvicorn — il ouvre donc sa propre
    # session DB, comme le ferait get_db() côté API.
    db = SessionLocal()

    try:
        resultat = ingestion_service.ingest_dossier(db, dossier_id)
        return resultat
    finally:
        db.close()