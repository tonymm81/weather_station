# /data/ai-agent3/app/Dockerfile
FROM python:3.11-slim

# Peruspaketit
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kopioi sovellus ja mahdollinen requirements
COPY . /app

# Asenna riippuvuudet jos requirements.txt löytyy
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Ympäristömuuttujien oletukset (voi ylikirjoittaa docker-compose)
ENV DATABASE_PATH=/root/.ollama/ollama.db
ENV MODEL_PATH=/root/.ollama/models/library/qwen2.5
ENV OLLAMA_HOST=0.0.0.0:11434
ENV PYTHONUNBUFFERED=1

# Oletusportti (sovelluksesi pitäisi kuunnella tätä)
EXPOSE 11434

# Käynnistys: yritetään ensin uvicorn (ASGI), muuten python main.py
CMD ["sh", "-c", "if python -c 'import importlib,sys; importlib.import_module(\"uvicorn\")' 2>/dev/null; then uvicorn main:app --host 0.0.0.0 --port 11434; else python main.py; fi"]
