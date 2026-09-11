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