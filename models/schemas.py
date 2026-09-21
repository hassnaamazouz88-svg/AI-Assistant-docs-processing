from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: UUID
    nom_fichier: str
    statut_traitement: str

    model_config = ConfigDict(from_attributes=True)


class DossierResponse(BaseModel):
    id: UUID
    nom: str
    statut: str
    documents: list[DocumentResponse]

    model_config = ConfigDict(from_attributes=True)


class ConversationResponse(BaseModel):
    id: UUID
    dossier_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FichierGenereResponse(BaseModel):
    id: UUID
    dossier_id: UUID
    type_fichier: str | None = None
    titre: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    question: str
    conversation_id: UUID | None = None


class ChatResponse(BaseModel):
    conversation_id: UUID
    answer: str
    sources: list[dict]
    
    
class GenerationRequest(BaseModel):
    demande: str
    format: str = "docx"
    conversation_id: UUID | None = None