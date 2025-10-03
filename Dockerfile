# syntax=docker/dockerfile:1.6

############################################################
# Frontend build stage
############################################################
FROM node:20-alpine AS frontend-builder
WORKDIR /usr/src/app/frontend

# Install dependencies first to leverage Docker layer caching
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --legacy-peer-deps

# Copy the rest of the frontend source and build the production bundle
COPY frontend/ ./
RUN npm run build

############################################################
# Backend runtime stage
############################################################
FROM python:3.11-slim AS backend
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Install system dependencies required for Python packages
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and project dependencies
RUN pip install poetry==1.7.1
COPY backend/pyproject.toml backend/poetry.lock ./
RUN poetry install --without dev --no-root

# Copy the backend application code
COPY backend/ ./

# Ensure the SQLite data directory exists by default
RUN mkdir -p /app/data

# Copy the built frontend from the previous stage and configure FastAPI to serve it
COPY --from=frontend-builder /usr/src/app/frontend/dist /app/frontend_dist
ENV FRONTEND_BUILD_DIR=/app/frontend_dist \
    PYTHONPATH=/app

EXPOSE 8000

# Run database migrations automatically before starting the server
CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
