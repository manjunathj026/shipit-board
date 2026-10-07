# Small official Python base image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy only the code the app needs (tests stay out of the image)
COPY app.py config.py ./
COPY templates ./templates

# Security: never run as root inside the container
RUN useradd --create-home appuser
USER appuser

# The pipeline passes these in at build time; they show on the UI
ARG APP_VERSION=dev
ARG GIT_SHA=local
ENV APP_VERSION=${APP_VERSION} \
    GIT_SHA=${GIT_SHA}

EXPOSE 8000

# One worker so the in-memory notes stay consistent (more on this later)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "app:app"]
