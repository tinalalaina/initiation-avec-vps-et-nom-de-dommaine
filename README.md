# utilisateur-avec-react-vite-et-django-et-postgresql-otp

## Local (sans Docker)
```bash
git clone <repo>
cd frontend
npm install
npm run dev
```

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Objectif VPS (Docker Hub + Docker Compose)
- `frontend` => image Docker `gasy-frontend`
- `backend` => image Docker `gasy-backend`
- `postgresql` => conteneur PostgreSQL sur le VPS
- un seul `docker-compose.vps.yml` sur le VPS pour lancer les 3 services

> Le frontend et le backend peuvent être dans **2 repositories GitHub différents**. Sur le VPS, on utilise uniquement les images Docker Hub.

## 1) Build et push des images vers Docker Hub

### Frontend (dans le repo frontend)
```bash
docker build -t <dockerhub_user>/gasy-frontend:latest -f frontend/Dockerfile frontend
docker push <dockerhub_user>/gasy-frontend:latest
```

### Backend (dans le repo backend)
```bash
docker build -t <dockerhub_user>/gasy-backend:latest -f backend/Dockerfile backend
docker push <dockerhub_user>/gasy-backend:latest
```

## 2) Déploiement sur le VPS

Copier sur le VPS:
- `docker-compose.vps.yml`
- `.env.vps` (copié depuis `.env.vps.example` puis adapté)

```bash
cp .env.vps.example .env.vps
# puis éditer les valeurs (images, mot de passe postgres, secret django)
```

Lancer la stack:
```bash
docker compose --env-file .env.vps -f docker-compose.vps.yml up -d
```

Vérifier:
```bash
docker compose --env-file .env.vps -f docker-compose.vps.yml ps
docker compose --env-file .env.vps -f docker-compose.vps.yml logs -f
```

## Fichiers ajoutés pour Docker
- `frontend/Dockerfile`
- `frontend/nginx.conf`
- `frontend/.dockerignore`
- `frontend/.env.example`
- `backend/Dockerfile`
- `backend/.dockerignore`
- `docker-compose.vps.yml`
- `.env.vps.example`

## Notes
- En production, le frontend appelle l'API via `/api` (reverse proxy Nginx vers le service `backend`).
- En local, vous pouvez conserver `VITE_API_URL=http://127.0.0.1:8000/api` via `frontend/.env`.
