# Tests backend — démarrage rapide

Les tests vivent dans `backend/tests/` (découverts par `pytest.ini`) :

| Fichier | Contenu |
|---|---|
| `tests/conftest.py` | Fixtures communes (client FastAPI, images en mémoire, reset du rate limiter) |
| `tests/test_main.py` | Routes de l'API |
| `tests/test_optimize_images.py` | Moteur d'optimisation d'images |
| `tests/test_security.py` | Validation d'entrées, DoS, CORS, path traversal |
| `tests/test_download.py`, `test_video_downloader.py` | Téléchargement par URL (yt-dlp, SSRF) |
| `tests/test_video_processor.py` | Moteur vidéo (FFmpeg) |
| `tests/test_download_routes.py` | Téléchargement de résultats, ZIP sur disque, IP client |

## Lancer

```bash
cd backend
pip install -r requirements.txt -r requirements-dev.txt
pytest                      # avec couverture (seuil `--cov-fail-under` dans pytest.ini)
pytest --no-cov -m security # un sous-ensemble, sans couverture
```

Markers disponibles : `unit`, `integration`, `security`, `slow`, `edge_case`.
Détails : `tests/README.md`.
