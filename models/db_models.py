import uuid
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Dossier(Base):
    __tablename__ = "dossiers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    statut: Mapped[str] = mapped_column(String(50), nullable=False, default="en_attente")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relations : un dossier a plusieurs documents / conversations / fichiers générés
    documents: Mapped[list["Document"]] = relationship(
        back_populates="dossier", cascade="all, delete-orphan"
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="dossier", cascade="all, delete-orphan"
    )
    fichiers_generes: Mapped[list["FichierGenere"]] = relationship(
        back_populates="dossier", cascade="all, delete-orphan"
    )


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    dossier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dossiers.id"), nullable=False
    )
    nom_fichier: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    statut_traitement: Mapped[str] = mapped_column(
        String(50), nullable=False, default="en_attente"
    )
    chemin_stockage: Mapped[str] = mapped_column(String(500), nullable=True)

    dossier: Mapped["Dossier"] = relationship(back_populates="documents")


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    dossier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dossiers.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    dossier: Mapped["Dossier"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    contenu: Mapped[str] = mapped_column(Text, nullable=False)
    sources_citees: Mapped[str] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")


class FichierGenere(Base):
    __tablename__ = "fichiers_generes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    dossier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dossiers.id"), nullable=False
    )
    type_fichier: Mapped[str] = mapped_column(String(50), nullable=True)
    chemin: Mapped[str] = mapped_column(String(500), nullable=True)

    dossier: Mapped["Dossier"] = relationship(back_populates="fichiers_generes")