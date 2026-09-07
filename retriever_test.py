from uuid import UUID

from services.chat_service import ChatService


DOSSIER_ID = UUID("37e3cb7d-3acc-4057-bd54-2348fbc4df06")


service = ChatService()

result = service.ask(
    question="Quelles sont les conditions pour participer à cet appel d'offres ?",
    dossier_id=DOSSIER_ID,
    history=None,
    top_k=5
)

print("\n==============================")
print("RÉPONSE")
print("==============================")

print(result["answer"])

print("\n==============================")
print("SOURCES")
print("==============================")

for source in result["sources"]:
    print(
        f"- {source['nom_fichier']} "
        f"(chunk {source['chunk_index']}, "
        f"distance={source['distance']})"
    )