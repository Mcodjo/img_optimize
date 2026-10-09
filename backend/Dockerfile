FROM python:3.11-slim

# FFmpeg est requis pour l'optimisation vidéo et la fusion audio/vidéo de yt-dlp.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py optimize_images.py video_processor.py video_downloader.py ./

RUN useradd --create-home appuser
USER appuser

# Render injecte $PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
