from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
import uuid

from config.database import get_db
from models.schemas import DossierResponse, ChatRequest, ChatResponse
from services import dossier_service
from services import ingestion_service
from services.chat_service import ChatService
from repositories import dossier_repository, conversation_repository


router = APIRouter(
    prefix="/dossiers",
    tags=["Dossiers"]
)


@router.post("/", response_model=DossierResponse)
async def creer_dossier(
    nom: str = Form(...),
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    dossier = await dossier_service.create_dossier_with_files(
        db=db,
        nom=nom,
        files=files
    )

    return dossier


@router.post("/{dossier_id}/ingest")
def ingerer_dossier(
    dossier_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    dossier = dossier_repository.get_by_id(db, dossier_id)

    if dossier is None:
        raise HTTPException(status_code=404, detail="Dossier introuvable")

    resultat = ingestion_service.ingest_dossier(db, dossier_id)

    return resultat


@router.post("/{dossier_id}/chat", response_model=ChatResponse)
def discuter_avec_dossier(
    dossier_id: uuid.UUID,
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    # 1. Vérifier que le dossier existe
    dossier = dossier_repository.get_by_id(
        db,
        dossier_id
    )

    if dossier is None:
        raise HTTPException(
            status_code=404,
            detail="Dossier introuvable"
        )

    # 2. Vérifier que le dossier est prêt
    if dossier.statut != "pret":
        raise HTTPException(
            status_code=400,
            detail="Le dossier n'est pas prêt pour le chat"
        )

    # 3. Récupérer ou créer la conversation
    if request.conversation_id is not None:

        conversation = conversation_repository.get_conversation(
            db,
            request.conversation_id
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation introuvable"
            )

        # Vérifier que la conversation appartient bien
        # au dossier demandé
        if conversation.dossier_id != dossier_id:
            raise HTTPException(
                status_code=400,
                detail="La conversation n'appartient pas à ce dossier"
            )

    else:

        conversation = conversation_repository.create_conversation(
            db=db,
            dossier_id=dossier_id
        )

    # 4. Charger l'historique
    history = conversation_repository.get_conversation_history(
        db=db,
        conversation_id=conversation.id
    )

    # 5. Appeler le ChatService
    chat_service = ChatService()

    resultat = chat_service.ask(
        question=request.question,
        dossier_id=dossier_id,
        history=history
    )

    # 6. Sauvegarder la question
    conversation_repository.add_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        contenu=request.question
    )

    # 7. Sauvegarder la réponse
    conversation_repository.add_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        contenu=resultat["answer"],
        sources_citees=resultat["sources"]
    )

    # 8. Valider la transaction
    db.commit()

    # 9. Retourner la réponse
    return ChatResponse(
        conversation_id=conversation.id,
        answer=resultat["answer"],
        sources=resultat["sources"]
    )

