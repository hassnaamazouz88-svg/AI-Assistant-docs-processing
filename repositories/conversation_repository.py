import json
import uuid
from datetime import datetime

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from models.db_models import Conversation, Message


def create_conversation(
    db: Session,
    dossier_id: uuid.UUID
) -> Conversation:
    conversation = Conversation(
        dossier_id=dossier_id
    )

    db.add(conversation)
    db.flush()

    return conversation


def get_conversation(
    db: Session,
    conversation_id: uuid.UUID
) -> Conversation | None:
    statement = select(Conversation).where(
        Conversation.id == conversation_id
    )

    return db.scalar(statement)


def get_conversations_by_dossier(
    db: Session,
    dossier_id: uuid.UUID
) -> list[Conversation]:
    statement = (
        select(Conversation)
        .where(Conversation.dossier_id == dossier_id)
        .order_by(Conversation.created_at.desc())
    )

    return list(db.scalars(statement).all())


def get_conversation_history(
    db: Session,
    conversation_id: uuid.UUID
) -> list[dict[str, str]]:
    statement = (
        select(Message)
        .where(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.created_at,
            # `Message.id` est un UUID aléatoire : l'utiliser comme
            # départage mélangeait l'ordre des messages ayant le même
            # created_at (deux messages insérés dans la même
            # transaction, avant le correctif ci-dessus). `ctid` reflète
            # l'ordre physique réel d'insertion des lignes côté
            # PostgreSQL, ce qui corrige aussi l'affichage des anciennes
            # conversations déjà enregistrées avec ce bug.
            text("messages.ctid")
        )
    )

    messages = db.scalars(statement).all()

    history = []

    for message in messages:
        history.append({
            "role": message.role,
            "content": message.contenu
        })

    return history


def add_message(
    db: Session,
    conversation_id: uuid.UUID,
    role: str,
    contenu: str,
    sources_citees: list[dict] | None = None
) -> Message:
    sources_json = None

    if sources_citees:
        sources_json = json.dumps(
            sources_citees,
            ensure_ascii=False
        )

    message = Message(
        conversation_id=conversation_id,
        role=role,
        contenu=contenu,
        sources_citees=sources_json,
        # Fixé explicitement ici plutôt que de compter sur le
        # server_default : en PostgreSQL, now() renvoie l'heure de
        # DÉBUT DE TRANSACTION, donc identique pour tous les messages
        # insérés dans le même commit (question + réponse). Le tri
        # utilisait alors l'UUID (aléatoire) comme départage, ce qui
        # mélangeait parfois question et réponse au rechargement de
        # l'historique. datetime.utcnow() donne à chaque message un
        # horodatage réellement croissant.
        created_at=datetime.utcnow()
    )

    db.add(message)
    db.flush()

    return message