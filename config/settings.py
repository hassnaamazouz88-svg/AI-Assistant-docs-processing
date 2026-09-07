import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        # Charger le fichier .env
        load_dotenv()

        # Lire les variables
        self.DB_USER = os.getenv("DB_USER", None)
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", None)
        self.DB_HOST = os.getenv("DB_HOST", None)
        self.DB_PORT = os.getenv("DB_PORT", None)
        self.DB_NAME = os.getenv("DB_NAME", None)
        
        self.PENNYOCR_API_KEY = os.getenv("PENNYOCR_API_KEY", None)
        
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", None)
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", None)
        




# Une seule instance, créée une fois, au niveau du module (pas indentée dans la classe)
settings = Config()


