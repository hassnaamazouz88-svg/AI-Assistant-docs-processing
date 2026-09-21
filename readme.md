# Assistant IA — Analyse de dossiers d'appels d'offres

Backend FastAPI (ingestion de documents, OCR, RAG, génération de documents)
+ frontend React, orchestrés via Docker Compose.

## Prérequis

- Docker et Docker Compose installés ([docs.docker.com](https://docs.docker.com/get-docker/))
- Une clé API [PennyOCR](https://pennyocr.com/dashboard/) (gratuite, 100 pages)
- Une clé API [OpenRouter](https://openrouter.ai/settings/keys)

## Installation

1. Cloner le dépôt :

git clone <url-du-depot>
cd "AI Assistant"


2. Créer le fichier de configuration :

cp .env.example .env

   Puis ouvrir `.env` et renseigner :
   - `DB_PASSWORD` : un mot de passe de ton choix pour PostgreSQL
   - `PENNYOCR_API_KEY` : ta clé PennyOCR
   - `OPENROUTER_API_KEY` : ta clé OpenRouter

## Lancement

docker compose up --build


Premier lancement uniquement : créer les tables de la base de données
dans un second terminal, une fois les conteneurs démarrés :

docker compose exec backend python create_tables.py


## Accès à l'application

| Service | URL |
|---|---|
| Frontend (interface web) | http://localhost:5173 |
| Backend (API) | http://localhost:8000 |
| Documentation interactive de l'API | http://localhost:8000/docs |

## Arrêter l'application

docker compose down


Pour tout arrêter **et** supprimer les données (base de données,
fichiers uploadés) :

docker compose down -v


## Architecture

- `backend` — API FastAPI (upload, extraction, RAG, génération de documents)
- `worker` — worker Celery (traitement asynchrone de l'ingestion)
- `postgres` — base de données relationnelle
- `redis` — file d'attente pour Celery
- `frontend` — interface React, servie par Nginx

## Dépannage

- **Port déjà utilisé** : si `5173`, `8000` ou `5432` sont déjà occupés
  sur ta machine, modifie le port de gauche dans `docker-compose.yml`
  (ex: `"5174:80"` au lieu de `"5173:80"`).
- **Le worker ne traite rien** : vérifie que le service `redis` est bien
  démarré (`docker compose ps`).