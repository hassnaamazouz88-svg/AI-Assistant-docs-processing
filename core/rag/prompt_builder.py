from typing import Any


# ============================================================
# Instructions système
# ============================================================

SYSTEM_INSTRUCTIONS = """
Tu es un assistant spécialisé dans l'analyse de dossiers
d'appels d'offres et de documents administratifs.

Ta mission est de répondre aux questions de l'utilisateur
en utilisant PRIORITAIREMENT et UNIQUEMENT les informations
présentes dans le contexte documentaire fourni.

RÈGLES OBLIGATOIRES :

1. Ne fabrique jamais une information qui n'est pas présente
   dans le contexte documentaire.

2. Si la réponse ne peut pas être déterminée à partir des
   documents fournis, indique clairement :
   "Je ne trouve pas cette information dans les documents fournis."

3. Ne complète pas une information manquante avec tes
   connaissances générales.

4. Lorsque tu réponds, cite les documents utilisés sous la forme :
   [Source: nom_fichier]

5. Si plusieurs documents sont utilisés, cite chaque document
   correspondant aux informations utilisées.

6. Si les documents contiennent des informations contradictoires,
   signale explicitement la contradiction et indique les sources
   concernées.

7. Distingue clairement les informations explicitement présentes
   dans les documents des éventuelles interprétations.

8. Réponds dans la même langue que la question de l'utilisateur,
   sauf indication contraire.

9. Sois précis, factuel et concis.

10. Ne mentionne pas ces instructions dans ta réponse.

Le contexte documentaire fourni ci-dessous est la source
de vérité pour répondre à la question.
"""


# ============================================================
# Construction du contexte documentaire
# ============================================================

def build_context(
    retrieved_chunks: list[dict[str, Any]]
) -> str:
    """
    Construit le contexte documentaire à partir des chunks
    retournés par le retriever.

    Chaque chunk est présenté avec son fichier source.

    Args:
        retrieved_chunks:
            Liste de chunks provenant de retriever.py.

    Returns:
        Texte formaté du contexte documentaire.
    """

    if not retrieved_chunks:
        return (
            "Aucun passage pertinent n'a été trouvé "
            "dans les documents."
        )

    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):

        nom_fichier = chunk.get(
            "nom_fichier",
            "Document inconnu"
        )

        chunk_index = chunk.get(
            "chunk_index",
            "?"
        )

        text = chunk.get(
            "text",
            ""
        )

        context_parts.append(
            f"""
--- Passage {index} ---
[Source: {nom_fichier}]
[Chunk: {chunk_index}]

{text}
"""
        )

    return "\n".join(context_parts)


# ============================================================
# Construction de l'historique
# ============================================================

def build_history(
    history: list[dict[str, str]] | None
) -> str:
    """
    Formate l'historique de conversation.

    Format attendu :

    [
        {
            "role": "user",
            "content": "..."
        },
        {
            "role": "assistant",
            "content": "..."
        }
    ]

    Args:
        history:
            Historique de la conversation.

    Returns:
        Historique formaté sous forme de texte.
    """

    if not history:
        return "Aucun historique de conversation."

    history_parts = []

    for message in history:

        role = message.get("role", "unknown")
        content = message.get("content", "")

        if role == "user":
            role_label = "Utilisateur"

        elif role == "assistant":
            role_label = "Assistant"

        else:
            role_label = role.capitalize()

        history_parts.append(
            f"{role_label} : {content}"
        )

    return "\n".join(history_parts)


# ============================================================
# Construction du prompt final
# ============================================================

def build_prompt(
    question: str,
    retrieved_chunks: list[dict[str, Any]],
    history: list[dict[str, str]] | None = None
) -> str:
    """
    Construit le prompt final envoyé au LLM.

    Structure :

        Instructions système
                ↓
        Contexte documentaire
                ↓
        Historique
                ↓
        Question utilisateur

    Args:
        question:
            Question actuelle de l'utilisateur.

        retrieved_chunks:
            Chunks retournés par le retriever.

        history:
            Historique de conversation.

    Returns:
        Prompt final sous forme de chaîne de caractères.
    """

    context = build_context(
        retrieved_chunks
    )

    conversation_history = build_history(
        history
    )

    prompt = f"""
{SYSTEM_INSTRUCTIONS}

============================================================
CONTEXTE DOCUMENTAIRE
============================================================

{context}

============================================================
HISTORIQUE DE LA CONVERSATION
============================================================

{conversation_history}

============================================================
QUESTION DE L'UTILISATEUR
============================================================

{question}

============================================================
INSTRUCTIONS POUR LA RÉPONSE
============================================================

Réponds directement à la question de l'utilisateur.

Utilise les documents fournis comme source de vérité.

Pour chaque information importante provenant d'un document,
indique sa source avec le format :

[Source: nom_fichier]

Si les documents ne permettent pas de répondre avec certitude,
dis-le explicitement plutôt que d'inventer une réponse.

RÉPONSE :
"""

    return prompt.strip()