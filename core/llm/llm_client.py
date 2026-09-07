from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Interface générique pour un client LLM.

    Les implémentations concrètes peuvent utiliser :
    - OpenRouter
    - Ollama
    - OpenAI
    - Gemini
    - etc.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 1000
    ) -> str:
        """
        Génère une réponse à partir d'un prompt.

        Args:
            prompt: Prompt complet envoyé au LLM.
            temperature: Niveau de créativité du modèle.
            max_tokens: Nombre maximum de tokens générés.

        Returns:
            Réponse textuelle du LLM.
        """
        pass