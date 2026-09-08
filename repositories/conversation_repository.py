import json
import uuid

from sqlalchemy import select
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
            Message.id
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
        sources_citees=sources_json
    )

    db.add(message)
    db.flush()

    return message