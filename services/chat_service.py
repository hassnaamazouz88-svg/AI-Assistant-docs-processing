from typing import Any
from uuid import UUID

from config.settings import settings
from core.rag.retriever import retrieve
from core.rag.prompt_builder import build_prompt
from core.llm.openrouter_provider import OpenRouterProvider


class ChatService:
    def __init__(self):
        self.llm = OpenRouterProvider(
            model=settings.OPENROUTER_MODEL,
            api_key=settings.OPENROUTER_API_KEY
        )

    def ask(
        self,
        question: str,
        dossier_id: UUID,
        history: list[dict[str, str]] | None = None,
        top_k: int = 8
    ) -> dict[str, Any]:

        # 1. Recherche des passages pertinents
        retrieved_chunks = retrieve(
            question=question,
            dossier_id=dossier_id,
            top_k=top_k
        )

        # 2. Construction du prompt
        prompt = build_prompt(
            question=question,
            retrieved_chunks=retrieved_chunks,
            history=history
        )

        # 3. Appel du LLM
        answer = self.llm.generate(
            prompt=prompt,
            temperature=0.0,
            max_tokens=1000
        )

        # 4. Préparation des sources
        sources = []
        for chunk in retrieved_chunks:
            sources.append({
                "nom_fichier": chunk.get("nom_fichier"),
                "document_id": chunk.get("document_id"),
                "chunk_index": chunk.get("chunk_index"),
                "distance": chunk.get("distance")
            })

        # 5. Retour du résultat
        return {
            "answer": answer,
            "sources": sources
        }