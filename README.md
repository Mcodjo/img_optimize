# Pixora : Optimiseur d'Images et Videos

**Pixora** est une application web moderne pour compresser et convertir vos images et videos sans compromis sur la qualite. Optimise pour le SEO et la performance web.

## Outils disponibles

| Page | Route | Role |
| :--- | :--- | :--- |
| Hub | `/app` | Point d'entree vers les outils |
| Images | `/app/images` | Compression / conversion (WebP, AVIF, JPEG, PNG), limite 1 Mo, renommage SEO |
| Videos | `/app/videos` | Transcodage H.264 / H.265 / VP9 / AV1, resolution, FPS |
| Telechargement | `/app/download` | Recupere une video depuis une URL (yt-dlp) puis l'optimise ou la conserve |
| Signature | `/app/sign` | Watermark texte ou logo, qualite maximale |
| Lissage | `/app/smooth` | Lissage d'image, qualite maximale |
| Securite | `/security` | Page de presentation securite |

Un service separe (`pdf-repair-service/`) analyse et repare les PDF.

---

## Sommaire
1. [Utilisation](#utilisation)
2. [Formats supportes](#formats-supportes)
3. [Architecture Technique](#architecture-technique)
4. [Installation Locale](#installation-locale)
5. [API & Endpoints](#api--endpoints)
6. [Configuration](#configuration)
7. [Deploiement](#deploiement)
8. [Securite & Confidentialite](#securite--confidentialite)

---

## Structure du depot

```
backend/               API FastAPI (+ Dockerfile, tests/)
frontend/              React + Vite + Tailwind (public/ : favicon, logo, image de partage)
pdf-repair-service/    Service d'analyse et de reparation de PDF
branding/              Logos maitres (symbole, logo complet) et references graphiques
scripts/               Outils manuels : tests, benchmark, smoke test de signature
doc/                   Architecture, API, securite, runbook, ADR, diagrammes, archive/
render.yaml            Blueprint de deploiement Render
```

---

## Utilisation

1. **Glissez-deposez** vos images (JPG, PNG, WebP, AVIF) et/ou videos (MP4, WebM, AVI, MOV, MKV).
2. **Choisissez le format** de sortie pour les images (WebP, AVIF, JPEG, PNG).
3. **Configurez le codec** pour les videos (H.264, H.265, VP9, AV1).
4. **Ajustez la qualite** : CRF pour les videos, qualite 0-100 pour les images.
5. **Lancez l'optimisation** et suivez la progression en temps reel (SSE).
6. **Telechargez** le fichier ZIP contenant tous vos assets optimises.

---

## Formats supportes

### Images

| Format | Avantages | Recommandation |
| :--- | :--- | :--- |
| **WebP** | Excellent rapport qualite/poids, 96%+ navigateurs. | **Defaut** pour le web moderne. |
| **AVIF** | Compression superieure au WebP (+30% gain). | Performance maximale. |
| **JPEG** | Compatibilite universelle. | Impressions, vieux systemes. |
| **PNG** | Transparence sans perte. | Logos, graphiques transparents. |

### Videos

| Codec | Avantages | Extension |
| :--- | :--- | :--- |
| **H.264** | Universel, compatible 98% navigateurs. | .mp4 |
| **H.265/HEVC** | -50% vs H.264, qualite superieure. | .mp4 |
| **VP9** | WebM natif, excellent pour le web. | .webm |
| **AV1** | Compression maximale, futur du web. | .webm |

Parametres video disponibles :
- **CRF** (15-51) : niveau de qualite (plus bas = meilleur)
- **Resolution** : 4K, 1080p, 720p, 480p, 360p, originale
- **FPS max** : limiter le nombre d'images par seconde

---

## Architecture Technique

- **Frontend** : React 18 + Vite 6 + Tailwind CSS 3 (Glassmorphism), React Router, SSE natif
- **Backend** (`backend/`) : FastAPI + Pillow (images) + FFmpeg (videos) + yt-dlp (telechargement)
- **Service PDF** (`pdf-repair-service/`) : FastAPI, analyse et reparation de PDF
- **Deploiement** : Backend (Docker) et service PDF sur Render, Frontend sur Vercel (`render.yaml`)
- **Analytics** : Vercel Analytics (anonyme)

### Detection automatique des formats
Le frontend interroge dynamiquement le backend (`/api/formats`, `/api/video/formats`) pour savoir quels formats et codecs sont reels supportes. Les formats non disponibles sont automatiquement masques.

---

## Installation Locale

### Pre requis
- Python 3.11+
- Node.js 18+
- FFmpeg (pour l'optimisation video)

### 1. Cloner le projet
```bash
git clone https://github.com/Africatech25/img_optimize.git
cd img_optimize
```

### 2. Configurer le Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
Le backend tournera sur `http://localhost:8000` (le proxy Vite `/api` pointe dessus).

### 3. Configurer le Frontend
```bash
cd ../frontend
npm install
npm run dev
```
Le frontend sera accessible sur `http://localhost:5173`.

---

## API & Endpoints

| Methode | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check (AVIF, FFmpeg, yt-dlp) |
| `GET` | `/api/formats` | Formats image disponibles |
| `GET` | `/api/video/formats` | Codecs video disponibles |
| `POST` | `/api/optimize` | Lancer un traitement ; `mode` = `optimize_image`, `optimize_video`, `sign` ou `smooth` |
| `POST` | `/api/download` | Telecharger une video depuis une URL (YouTube, TikTok, ...) puis l'optimiser |
| `GET` | `/api/download/platforms` | Plateformes de telechargement supportees |
| `GET` | `/api/progress/{id}` | SSE - progression en temps reel |
| `GET` | `/api/job/{id}` | Statut d'un job |
| `GET` | `/api/download/{id}` | Telecharger le fichier ZIP |
| `GET` | `/api/download/{id}/{filename}` | Telecharger un fichier resultat (uniquement ceux traites avec succes) |
| `GET` | `/api/download-zip/{id}` | Forcer le telechargement ZIP |
| `DELETE` | `/api/cleanup/{id}` | Nettoyer les fichiers d'un job |

Le service PDF expose `/api/pdf/repair`, `/validate`, `/info`, `/smart-repair` et `/analyze`.

### Limites
- **Upload** : 50 MB par fichier, 50 fichiers par requete (ecrits sur disque par blocs)
- **ZIP** : 1 Go cumule maximum (generation sur disque)
- **Jobs concurrents** : 20 maximum
- **Rate limiting** : 10 requetes/minute sur `/api/optimize` et `/api/download`
- **Retention** : jobs auto-nettoyes apres 24h

---

## Configuration

Creer un fichier `.env` dans `backend/` (voir `.env.example`) :

| Variable | Defaut | Description |
| :--- | :--- | :--- |
| `PORT` | 8000 | Port du serveur backend |
| `CORS_ORIGINS` | `http://localhost:5173` | Domaines CORS autorises |
| `MAX_UPLOAD_SIZE_MB` | 50 | Taille max par fichier upload |
| `MAX_FILES_PER_REQUEST` | 50 | Fichiers max par requete |
| `MAX_ZIP_SIZE_MB` | 1024 | Taille cumulee max d'un ZIP |
| `MAX_CONCURRENT_JOBS` | 20 | Jobs max simultanes |
| `MAX_DOWNLOAD_SIZE_MB` | 500 | Taille max d'une video telechargee par URL |
| `DOWNLOAD_ALLOWED_DOMAINS` | liste interne | Domaines autorises pour `/api/download` (separes par des virgules) |
| `TRUSTED_PROXY_COUNT` | 0 | Nombre de proxys devant l'app (1 sur Render) pour lire l'IP client dans `X-Forwarded-For` |

---

## Deploiement

### Backend (Render)
Le blueprint `render.yaml` deploie le backend via `backend/Dockerfile` (FFmpeg n'est pas installable
par `apt-get` dans un build Python natif sur Render) et le service PDF en environnement Python.
Verifiez `TRUSTED_PROXY_COUNT=1` et `CORS_ORIGINS` dans les variables d'environnement.

`yt-dlp` est epingle dans `backend/requirements.txt` : le mettre a jour regulierement, les
plateformes cassent souvent les anciennes versions.

### Frontend (Vercel)
1. Connecter le repo GitHub
2. Root directory : `frontend`
3. Variable d'env : `VITE_API_URL` (URL de votre API Render)

---

## Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest            # tests/ + couverture (seuil dans pytest.ini)
```

Le service PDF a ses propres tests dans `pdf-repair-service/`. Guide detaille : `backend/tests/README.md`.

---

## Documentation

`doc/` : architecture, API, donnees, securite (`SECURITY_AUDIT_2025-01.md`), performance, runbook,
backlog, ADR et diagrammes Draw.io (MERISE / UML).

---

## Securite & Confidentialite

- **CORS restreint** : seuls les domaines configures sont autorises
- **Rate limiting** : protection contre les abus
- **Validation des fichiers** : taille (plafond applique pendant la lecture), extension, prefixe (injection prevention)
- **Anti-SSRF** : telechargement par URL limite a une liste de domaines, IP internes refusees
- **Zip Slip protection** : securite sur les archives ZIP
- **Path traversal protection** : validation des noms de fichiers
- **Nettoyage auto** : fichiers temporaires supprimes apres 24h

---

**Developpe par Maurice CODJO**
