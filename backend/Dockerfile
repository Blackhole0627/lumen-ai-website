# Build from the repository root (the compose file does this):
#   docker build -f backend/Dockerfile -t collections-backend .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /srv

# 1. The safety guardrails package
COPY safety-guard/pyproject.toml safety-guard/
COPY safety-guard/guardrails safety-guard/guardrails
RUN pip install ./safety-guard

# 2. Backend dependencies (cached unless requirements change)
COPY backend/requirements.txt backend/
RUN pip install -r backend/requirements.txt

# 3. Backend code
COPY backend/app backend/app
WORKDIR /srv/backend

RUN useradd --create-home appuser && mkdir -p data && chown appuser data
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
