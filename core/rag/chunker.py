import re
from transformers import AutoTokenizer


# Configuration

MODEL_NAME = "LiquidAI/LFM2.5-Embedding-350M"

MAX_TOKENS = 400       # marge de sécurité sous la limite de 512 tokens
OVERLAP_TOKENS = 60    # chevauchement entre chunks


# Tokenizer LFM2.5
# ============================================================

# Le tokenizer est téléchargé automatiquement depuis Hugging Face
# lors de la première exécution, puis conservé dans le cache local.
_tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)


# Comptage des tokens
def count_tokens(text: str) -> int:
    """
    Compte le nombre de tokens en utilisant le tokenizer
    associé à LFM2.5-Embedding-350M.

    Cela permet d'utiliser la même logique de tokenisation
    que celle utilisée par le modèle d'embedding.
    """
    return len(
        _tokenizer.encode(
            text,
            add_special_tokens=True
        )
    )


# Niveau 1 : découpage structurel
def split_into_sections(text: str) -> list[str]:
    """
    Niveau 1 :
    Découpe le texte aux marqueurs de structure produits
    par text_builder.py :

        [Page X]
        [Tableau N]
        [Feuille : Nom]

    Chaque section devient une unité de départ pour
    le découpage récursif.
    """

    pattern = r'(?=\[Page \d+\]|\[Tableau \d+\]|\[Feuille : )'

    parts = re.split(pattern, text)

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


# Niveau 2 : découpage récursif
def split_recursive(
    text: str,
    max_tokens: int = MAX_TOKENS
) -> list[str]:
    """
    Niveau 2 :
    Si une section dépasse max_tokens, elle est découpée
    récursivement selon l'ordre :

        1. paragraphes
        2. lignes
        3. phrases
        4. espaces

    Le découpage descend au niveau suivant uniquement
    lorsque le niveau actuel ne permet pas d'obtenir
    des chunks suffisamment petits.
    """

    # La section tient déjà dans la limite
    if count_tokens(text) <= max_tokens:
        return [text]

    # Séparateurs du plus naturel au moins naturel
    separateurs = [
        "\n\n",   # paragraphes
        "\n",     # lignes
        ". ",     # phrases
        " "       # mots
    ]

    separateur_choisi = None

    for sep in separateurs:
        if sep in text:
            separateur_choisi = sep
            break

    # Aucun séparateur disponible
    if separateur_choisi is None:
        return [text]

    parts = text.split(separateur_choisi)

    chunks = []
    current = ""

    for part in parts:

        candidat = (
            current
            + (separateur_choisi if current else "")
            + part
        )

        # Le candidat tient dans la limite
        if count_tokens(candidat) <= max_tokens:
            current = candidat

        else:
            # Sauvegarder le chunk actuel
            if current:
                chunks.append(current)

            # Une partie individuelle est encore trop grande
            if count_tokens(part) > max_tokens:
                chunks.extend(
                    split_recursive(
                        part,
                        max_tokens
                    )
                )

                current = ""

            else:
                current = part

    # Ajouter le dernier chunk
    if current:
        chunks.append(current)

    return chunks


# ============================================================
# Overlap
# ============================================================

def add_overlap(
    chunks: list[str],
    overlap_tokens: int = OVERLAP_TOKENS,
    max_tokens: int = MAX_TOKENS
) -> list[str]:
    """
    Ajoute un chevauchement entre chunks consécutifs.

    Exemple :

        Chunk 1 : A B C D E
        Chunk 2 : F G H I J

    devient :

        Chunk 1 : A B C D E
        Chunk 2 : D E F G H I J

    L'overlap est limité afin que le chunk final
    ne dépasse pas max_tokens.
    """

    if len(chunks) <= 1:
        return chunks

    resultat = [chunks[0]]

    for i in range(1, len(chunks)):

        chunk_precedent = chunks[i - 1]
        chunk_actuel = chunks[i]

        tokens_precedents = _tokenizer.encode(
            chunk_precedent,
            add_special_tokens=False
        )

        # Déterminer combien de tokens peuvent être ajoutés
        taille_chunk_actuel = count_tokens(chunk_actuel)

        espace_disponible = max_tokens - taille_chunk_actuel

        if espace_disponible <= 0:
            resultat.append(chunk_actuel)
            continue

        overlap_effectif = min(
            overlap_tokens,
            len(tokens_precedents),
            espace_disponible
        )

        if overlap_effectif > 0:

            tokens_chevauchement = tokens_precedents[
                -overlap_effectif:
            ]

            texte_chevauchement = _tokenizer.decode(
                tokens_chevauchement,
                skip_special_tokens=True
            )

            chunk_final = (
                texte_chevauchement
                + "\n"
                + chunk_actuel
            )

        else:
            chunk_final = chunk_actuel

        # Sécurité supplémentaire
        if count_tokens(chunk_final) > max_tokens:

            # Si malgré tout le chunk dépasse la limite,
            # on conserve le chunk original.
            chunk_final = chunk_actuel

        resultat.append(chunk_final)

    return resultat


# Point d'entrée principal
def chunk_text(
    text: str,
    max_tokens: int = MAX_TOKENS,
    overlap_tokens: int = OVERLAP_TOKENS
) -> list[dict]:
    """
    Point d'entrée principal du chunking.

    Pipeline :

        Texte
          ↓
        Sections structurelles
          ↓
        Recursive splitting
          ↓
        Overlap
          ↓
        Chunks finaux

    Returns:
        Liste de dictionnaires :

        [
            {
                "text": "...",
                "tokens": 342
            },
            ...
        ]
    """

    # --------------------------------------------------------
    # Niveau 1 : découpage structurel
    # --------------------------------------------------------

    sections = split_into_sections(text)

    # --------------------------------------------------------
    # Niveau 2 : découpage récursif
    # --------------------------------------------------------

    tous_les_chunks = []

    for section in sections:

        chunks_section = split_recursive(
            section,
            max_tokens
        )

        tous_les_chunks.extend(chunks_section)

    # --------------------------------------------------------
    # Overlap
    # --------------------------------------------------------

    tous_les_chunks = add_overlap(
        tous_les_chunks,
        overlap_tokens,
        max_tokens
    )

    # --------------------------------------------------------
    # Résultat final
    # --------------------------------------------------------

    resultats = []

    for index, chunk in enumerate(tous_les_chunks):

        resultats.append({
            "text": chunk,
            "tokens": count_tokens(chunk),
            "chunk_index": index
        })

    return resultats