import json
from typing import Any
from uuid import UUID

from config.settings import settings
from core.llm.openrouter_provider import OpenRouterProvider
from core.rag.retriever import retrieve


SYSTEM_INSTRUCTIONS = """
Tu es un assistant spécialisé dans l'analyse et la synthèse
de dossiers d'appels d'offres et de documents administratifs.

Ta mission est de préparer le contenu structuré d'un document
qui sera ensuite généré automatiquement au format DOCX, XLSX
ou PDF.

RÈGLES OBLIGATOIRES :

1. Utilise UNIQUEMENT les informations présentes dans le
   contexte documentaire fourni.

2. N'invente jamais une information.

3. Ne complète jamais une information manquante avec tes
   connaissances générales.

4. Si une information n'est pas présente dans les documents,
   indique-le clairement dans le contenu.

5. Le résultat doit être retourné EXCLUSIVEMENT sous forme
   de JSON valide.

6. N'ajoute aucun texte avant ou après le JSON.

7. Respecte exactement la structure JSON demandée.

8. Réponds dans la même langue que la demande de l'utilisateur.

9. Lorsque plusieurs documents fournissent une information,
   tu peux les utiliser ensemble.

10. Si les documents contiennent des informations contradictoires,
    signale la contradiction dans le contenu concerné.

11. Le contenu doit être factuel, clair et adapté à un document
    administratif.

Le contexte documentaire fourni est la seule source de vérité.
"""


def build_generation_prompt(
    request: str,
    retrieved_chunks: list[dict[str, Any]]
) -> str:
    if not retrieved_chunks:
        context = (
            "Aucun passage pertinent n'a été trouvé "
            "dans les documents du dossier."
        )
    else:
        context_parts = []
        for index, chunk in enumerate(retrieved_chunks, start=1):
            nom_fichier = chunk.get("nom_fichier", "Document inconnu")
            chunk_index = chunk.get("chunk_index", "?")
            text = chunk.get("text", "")
            context_parts.append(
                f"""
--- Passage {index} ---
[Source: {nom_fichier}]
[Chunk: {chunk_index}]

{text}
"""
            )
        context = "\n".join(context_parts)

    prompt = f"""
{SYSTEM_INSTRUCTIONS}

============================================================
DEMANDE DE L'UTILISATEUR
============================================================

{request}

============================================================
CONTEXTE DOCUMENTAIRE
============================================================

{context}

============================================================
STRUCTURE JSON OBLIGATOIRE
============================================================

Retourne exactement un objet JSON ayant cette structure :

{{
    "titre": "Titre du document",
    "sections": [
        {{
            "titre": "Titre de la section",
            "contenu": "Contenu de la section"
        }}
    ]
}}

============================================================
CONSIGNES
============================================================

- "titre" doit être un titre pertinent pour le document.
- "sections" doit contenir les différentes parties du document.
- Chaque section doit avoir un "titre" et un "contenu".
- Le contenu doit être basé uniquement sur les passages fournis.
- Ne crée pas de section contenant des informations inventées.
- Si une information importante demandée par l'utilisateur
  n'est pas disponible, indique-le dans la section concernée.
- Ne retourne que le JSON.
- N'utilise pas de Markdown autour du JSON.
- N'ajoute pas ```json.
- N'ajoute aucun commentaire.

JSON :
"""
    return prompt.strip()


def validate_content_plan(plan: Any) -> dict[str, Any]:
    if not isinstance(plan, dict):
        raise ValueError("Le plan généré doit être un dictionnaire JSON.")
    if "titre" not in plan:
        raise ValueError("Le plan généré ne contient pas le champ 'titre'.")
    if "sections" not in plan:
        raise ValueError("Le plan généré ne contient pas le champ 'sections'.")
    if not isinstance(plan["titre"], str):
        raise ValueError("Le champ 'titre' doit être une chaîne de caractères.")
    if not isinstance(plan["sections"], list):
        raise ValueError("Le champ 'sections' doit être une liste.")

    for index, section in enumerate(plan["sections"]):
        if not isinstance(section, dict):
            raise ValueError(f"La section {index} doit être un objet JSON.")
        if "titre" not in section:
            raise ValueError(f"La section {index} ne contient pas 'titre'.")
        if "contenu" not in section:
            raise ValueError(f"La section {index} ne contient pas 'contenu'.")
        if not isinstance(section["titre"], str):
            raise ValueError(f"Le titre de la section {index} doit être une chaîne de caractères.")
        if not isinstance(section["contenu"], str):
            raise ValueError(f"Le contenu de la section {index} doit être une chaîne de caractères.")

    return plan


def _clean_json_response(response: str) -> str:
    """Retire un éventuel balisage ```json ... ``` résiduel."""
    response = response.strip()
    if response.startswith("```json"):
        response = response[7:]
    elif response.startswith("```"):
        response = response[3:]
    if response.endswith("```"):
        response = response[:-3]
    return response.strip()


class ContentPlanner:
    def __init__(self):
        self.llm = OpenRouterProvider(
            model=settings.OPENROUTER_MODELS,  # liste, plus une seule chaîne,
            api_key=settings.OPENROUTER_API_KEY
        )

    def plan(
        self,
        request: str,
        dossier_id: UUID,
        top_k: int = 8,
        max_retries: int = 3
    ) -> dict[str, Any]:
        """
        Puisque le modèle utilisé peut être routé de façon
        imprévisible (ex: "openrouter/free"), on réessaie
        plusieurs fois si le JSON échoue à parser/valider : un
        nouvel appel peut être routé vers un modèle plus adapté.
        """
        if not request.strip():
            raise ValueError("La demande de génération ne peut pas être vide.")

        retrieved_chunks = retrieve(
            question=request,
            dossier_id=dossier_id,
            top_k=top_k
        )

        prompt = build_generation_prompt(
            request=request,
            retrieved_chunks=retrieved_chunks
        )

        derniere_erreur = None

        for tentative in range(1, max_retries + 1):

            response = self.llm.generate(
                prompt=prompt,
                temperature=0.0,
                max_tokens=2000
            )

            if response is None:
                derniere_erreur = ValueError("Le LLM n'a retourné aucun contenu.")
                continue

            response = _clean_json_response(response)

            try:
                plan = json.loads(response)
            except json.JSONDecodeError:
                derniere_erreur = ValueError(
                    f"Tentative {tentative}/{max_retries} : le LLM "
                    f"n'a pas retourné un JSON valide.\nRéponse reçue :\n{response}"
                )
                continue

            try:
                plan = validate_content_plan(plan)
            except ValueError as exc:
                derniere_erreur = ValueError(
                    f"Tentative {tentative}/{max_retries} : structure invalide — {exc}"
                )
                continue

            return plan

        raise derniere_erreur