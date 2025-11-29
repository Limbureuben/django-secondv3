FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

FROM base AS production

ENV DJANGO_ENVIRONMENT=production \
    DJANGO_SETTINGS_MODULE=openspace.settings

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY --chown=nobody:nogroup . .

RUN mkdir -p /app/staticfiles /app/media /app/logs && \
    chmod +x /app/entrypoint.sh && \
    chown -R nobody:nogroup /app

RUN python manage.py collectstatic --noinput --clear

USER nobody

EXPOSE 8099

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8099/admin/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "openspace.wsgi:application", \
     "--bind", "0.0.0.0:8099", \
     "--workers", "4", \
     "--threads", "2", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--timeout", "120", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]