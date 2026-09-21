const API_URL = "http://localhost:8000"

export async function getDossiers() {
  const response = await fetch(`${API_URL}/dossiers/`)
  if (!response.ok) throw new Error("Erreur lors de la récupération des dossiers")
  return response.json()
}

export async function getDossier(dossierId) {
  const response = await fetch(`${API_URL}/dossiers/${dossierId}`)
  if (!response.ok) throw new Error("Erreur lors de la récupération du dossier")
  return response.json()
}

export async function uploadDossier(nom, files) {
  const formData = new FormData()
  formData.append("nom", nom)
  for (const file of files) {
    formData.append("files", file)
  }

  const response = await fetch(`${API_URL}/dossiers/`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    const erreur = await response.json()
    throw new Error(erreur.detail || "Erreur lors de l'upload")
  }
  return response.json()
}

export async function lancerIngestion(dossierId) {
  const response = await fetch(`${API_URL}/dossiers/${dossierId}/ingest`, {
    method: "POST",
  })
  if (!response.ok) {
    const erreur = await response.json()
    throw new Error(erreur.detail || "Erreur lors du lancement de l'ingestion")
  }
  return response.json()
}
