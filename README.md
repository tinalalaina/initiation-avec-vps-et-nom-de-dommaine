# utilisateur-avec-react-vite-et-django-et-postgresql-otp

![Docker Frontend](https://github.com/tinalalaina/initiation-avec-vps-et-nom-de-domaine/actions/workflows/docker-frontend.yml/badge.svg)
![Docker Backend](https://github.com/tinalalaina/initiation-avec-vps-et-nom-de-domaine/actions/workflows/docker-backend.yml/badge.svg)

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



## GitHub Actions (pour voir l'indicateur Docker)

Si l'onglet **Actions** affiche seulement "Get started", c'est normal: il faut d'abord un fichier workflow dans `.github/workflows/`.

Workflows ajoutés:
- `.github/workflows/docker-frontend.yml`
- `.github/workflows/docker-backend.yml`

### Secrets à configurer dans GitHub
Dans `Settings > Secrets and variables > Actions`, ajoutez:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` (token Docker Hub, pas le mot de passe)

> `DOCKERHUB_USERNAME` doit être exactement votre namespace Docker Hub (ex: `tinalalaina`).

Ensuite:
1. poussez sur `main`/`master`, ou
2. lancez manuellement via **Actions > Docker Frontend/Backend > Run workflow**.

### Erreur GitHub Actions: `Username and password required`
Cette erreur veut dire que GitHub n'a pas trouvé les secrets Docker Hub.

Corrigez comme suit:
1. Dans Docker Hub, créez un **Access Token** (`Account settings > Personal access tokens`).
2. Dans GitHub: `Settings > Secrets and variables > Actions > New repository secret`.
3. Ajoutez exactement:
   - `DOCKERHUB_USERNAME` = votre username Docker Hub (ex: `lalainaraky`)
   - `DOCKERHUB_TOKEN` = le token Docker Hub

    Name: DOCKERHUB_USERNAME
    Secret: ton username Docker Hub (ex: lalainaraky)

    Name: DOCKERHUB_TOKEN
    Secret: le nouveau PAT Docker (Read & Write)

Ces noms doivent être exacts, car le workflow lit précisément ces clés. 


4. Re-lancez le workflow (**Actions > Docker Frontend/Backend > Re-run jobs**).

> Les workflows poussent maintenant **obligatoirement** les images sur Docker Hub. Si les secrets manquent, le job échoue avec un message explicite.

Après le premier run, vous verrez l'indicateur (badge vert/rouge) du build Docker.

## Arborescence recommandée (3 repositories GitHub)

Si vous avez **3 repositories** (`frontend`, `backend`, `infra-vps`), utilisez cette structure:

```text
# Repo 1: gasy-frontend
gasy-frontend/
├── src/
├── public/
├── package.json
├── Dockerfile
├── nginx.conf
└── .dockerignore

# Repo 2: gasy-backend
gasy-backend/
├── agriculture/
├── users/
├── manage.py
├── requirements.txt
├── Dockerfile
└── .dockerignore

# Repo 3: gasy-infra-vps
gasy-infra-vps/
├── docker-compose.vps.yml
└── .env.vps
```

> Sur le VPS, vous clonez seulement `gasy-infra-vps`, puis `docker compose` tire les images Docker Hub `frontend` et `backend`.

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


## ✅ Prochaine étape quand les images sont visibles sur Docker Hub

Si vous voyez `lalainaraky/gasy-frontend` et `lalainaraky/gasy-backend` avec les tags (`latest`, `main`, hash), la suite est:

1. Préparer le fichier d'environnement VPS:
```bash
cp .env.vps.example .env.vps
```
2. Modifier `.env.vps` avec vos vraies valeurs:
   - `FRONTEND_IMAGE=docker.io/lalainaraky/gasy-frontend:latest`
   - `BACKEND_IMAGE=docker.io/lalainaraky/gasy-backend:latest`
   - `POSTGRES_PASSWORD` fort
   - `DJANGO_SECRET_KEY` fort
   - `DJANGO_ALLOWED_HOSTS` avec votre domaine ou IP VPS (pas `*` en production)

3. Lancer les conteneurs sur le VPS:
```bash
docker compose --env-file .env.vps -f docker-compose.vps.yml up -d
```

4. Vérifier que tout tourne:
```bash
docker compose --env-file .env.vps -f docker-compose.vps.yml ps
docker compose --env-file .env.vps -f docker-compose.vps.yml logs -f backend
docker compose --env-file .env.vps -f docker-compose.vps.yml logs -f frontend
```

5. Initialiser/valider l'application:
   - tester l'URL publique du frontend
   - tester l'API via `http://<vps>/api/...`
   - créer un admin Django si nécessaire:
```bash
docker compose --env-file .env.vps -f docker-compose.vps.yml exec backend python manage.py createsuperuser
```

6. (Recommandé) Mettre un reverse proxy HTTPS (Nginx + Certbot) si vous utilisez un nom de domaine.


## 🧪 Tester en local avec les images Docker Hub (sur votre ordinateur)

Si vous avez déjà Docker Desktop / Docker Engine en local, vous pouvez tester exactement les images publiées sans VPS.

1. Créer un fichier d'environnement local:
```bash
cp .env.vps.example .env.local
```

2. Éditer `.env.local`:
- `FRONTEND_IMAGE=docker.io/lalainaraky/gasy-frontend:latest`
- `BACKEND_IMAGE=docker.io/lalainaraky/gasy-backend:latest`
- `POSTGRES_PASSWORD=mot_de_passe_local`
- `DJANGO_SECRET_KEY=cle_locale_longue`
- `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`

3. Récupérer explicitement les dernières images:
```bash
docker pull docker.io/lalainaraky/gasy-frontend:latest
docker pull docker.io/lalainaraky/gasy-backend:latest
```

4. Démarrer la stack en local:
```bash
docker compose --env-file .env.local -f docker-compose.vps.yml up -d
```

5. Vérifier le démarrage:
```bash
docker compose --env-file .env.local -f docker-compose.vps.yml ps
docker compose --env-file .env.local -f docker-compose.vps.yml logs -f backend
docker compose --env-file .env.local -f docker-compose.vps.yml logs -f frontend
```

6. Tester dans le navigateur:
- Frontend: `http://localhost`
- API (via proxy frontend): `http://localhost/api/`

7. Arrêter les conteneurs après test:
```bash
docker compose --env-file .env.local -f docker-compose.vps.yml down
```

> Si le port `80` est déjà utilisé sur votre machine, libérez-le ou adaptez temporairement le mapping `ports` du service `frontend`.

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
- Le build Docker frontend utilise `npm run build:docker` (`vite build`) pour produire l'image même si le type-check TypeScript strict échoue en CI.
- En production, le frontend appelle l'API via `/api` (reverse proxy Nginx vers le service `backend`).
- En local, vous pouvez conserver `VITE_API_URL=http://127.0.0.1:8000/api` via `frontend/.env`.
