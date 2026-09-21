const API_URL = "http://localhost:8000"

export async function getFichiersGeneres(dossierId) {
  const response = await fetch(`${API_URL}/dossiers/${dossierId}/fichiers-generes`)
  if (!response.ok) throw new Error("Erreur lors de la récupération des fichiers générés")
  return response.json()
}

export async function genererDocument(dossierId, demande, format = "docx", conversationId = null) {
  const response = await fetch(`${API_URL}/dossiers/${dossierId}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ demande, format, conversation_id: conversationId }),
  })

  if (!response.ok) {
    const erreur = await response.json()
    throw new Error(erreur.detail || "Erreur lors de la génération du document")
  }
  return response.json()
}

export function urlTelechargement(fichierId) {
  return `${API_URL}/dossiers/fichiers-generes/${fichierId}/download`
}

export function urlApercu(fichierId) {
  return `${API_URL}/dossiers/fichiers-generes/${fichierId}/preview`
}
