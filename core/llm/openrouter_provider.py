import httpx

from config.settings import settings
from core.llm.llm_client import LLMClient


OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterProvider(LLMClient):
    """
    Implémentation du client LLM utilisant OpenRouter.

    Utilise le mécanisme natif de "model fallbacks" d'OpenRouter :
    plutôt que de réessayer le même modèle plusieurs fois, on fournit
    une liste de modèles nommés et fiables, par ordre de priorité.
    OpenRouter essaie automatiquement le suivant de la liste si le
    précédent échoue (rate limit, indisponibilité, refus de
    modération).

    On évite volontairement l'alias "openrouter/free", qui peut
    router vers n'importe quel modèle gratuit disponible, y compris
    des modèles non conversationnels totalement inadaptés.
    """

    def __init__(
        self,
        model: str | list[str],
        api_key: str | None = None
    ):
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.models = [model] if isinstance(model, str) else model

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY est introuvable dans les variables "
                "d'environnement."
            )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 1000
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "models": self.models,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            response = httpx.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload,
                timeout=60.0,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"Erreur OpenRouter ({exc.response.status_code}) : "
                f"{exc.response.text}"
            ) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(
                f"Impossible de contacter OpenRouter : {exc}"
            ) from exc

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"Réponse OpenRouter inattendue : {data}"
            ) from exc