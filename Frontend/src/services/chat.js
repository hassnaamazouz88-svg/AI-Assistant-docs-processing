const API_URL = "http://localhost:8000"

export async function envoyerMessage(dossierId, question, conversationId = null) {
  const response = await fetch(`${API_URL}/dossiers/${dossierId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, conversation_id: conversationId }),
  })

  if (!response.ok) {
    const erreur = await response.json()
    throw new Error(erreur.detail || "Erreur lors de l'envoi du message")
  }
  return response.json()
}


export async function getConversations(dossierId) {
  const response = await fetch(`${API_URL}/dossiers/${dossierId}/conversations`)
  if (!response.ok) throw new Error("Erreur lors de la récupération des conversations")
  return response.json()
}


export async function getHistorique(conversationId) {
  const response = await fetch(`${API_URL}/dossiers/conversations/${conversationId}/messages`)
  if (!response.ok) throw new Error("Erreur lors de la récupération de l'historique")
  return response.json()
}