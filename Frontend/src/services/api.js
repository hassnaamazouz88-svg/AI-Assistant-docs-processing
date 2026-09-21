const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export async function getDossiers() {
  const response = await fetch(`${API_URL}/dossiers`)
  if (!response.ok) throw new Error("Erreur lors de la récupération des dossiers")
  return response.json()
}