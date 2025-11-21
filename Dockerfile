# syntax=docker/dockerfile:1.6

# ---------- Base dependencies ----------
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    postgresql-client \
    netcat-traditional \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY . /app

# FIX PERMISSIONS PROPERLY
RUN chmod +x /app/entrypoint.dev.sh && chmod +x /app/entrypoint.prod.sh
RUN chmod +x /app/waitfordatabase.sh

RUN addgroup --system appuser && adduser --system --ingroup appuser appuser
RUN chown -R appuser:appuser /app

USER appuser

# ---------- Development stage ----------
FROM base AS dev
ENV DJANGO_ENVIRONMENT=development \
    DEBUG=1

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.dev.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ---------- Production build stage ----------
FROM base AS prod-build
ENV DJANGO_ENVIRONMENT=production \
    DJANGO_SETTINGS_MODULE=openspace.settings \
    SECRET_KEY=dummy_secret_for_build
RUN python manage.py collectstatic --noinput

# ---------- Production runtime stage ----------
FROM python:3.11-slim AS prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_ENVIRONMENT=production \
    DJANGO_SETTINGS_MODULE=openspace.settings

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=prod-build /app /app

RUN chmod +x /app/entrypoint.prod.sh


EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.prod.sh"]








# CMD ["sh", "-c", "gunicorn openspace.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-4} --threads ${GUNICORN_THREADS:-2} --timeout 120 --access-logfile - --error-logfile -"]




# syntax=docker/dockerfile:1.6

# # ---------- Base dependencies ----------
# FROM python:3.11-slim AS base

# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     PIP_NO_CACHE_DIR=1

# WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     curl \
#     libpq-dev \
#     netcat-traditional \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt /tmp/requirements.txt
# RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# COPY . /app
# RUN chmod +x /app/entrypoint.dev.sh /a    
# RUN addgroup --system appuser && adduser --system --ingroup appuser appuser && \
#     chown -R appuser:appuser /app

# USER appuserpp/entrypoint.prod.sh && \
#     mkdir -p /app/media /app/staticfiles /app/logs

# # ---------- Development stage ----------
# FROM base AS dev
# ENV DJANGO_ENVIRONMENT=development \
# DEBUG=1

# EXPOSE 8000
# ENTRYPOINT ["/app/entrypoint.dev.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# # ---------- Production build stage ----------
# FROM base AS prod-build
# ENV DJANGO_ENVIRONMENT=production \
#     DJANGO_SETTINGS_MODULE=openspace.settings \
#     SECRET_KEY=dummy_secret_for_build
# RUN python manage.py collectstatic --noinput

# # ---------- Production runtime stage ----------
# FROM python:3.11-slim AS prod

# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     DJANGO_ENVIRONMENT=production \
#     DJANGO_SETTINGS_MODULE=openspace.settings

# WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libpq-dev \
#     netcat-traditional \
#     && rm -rf /var/lib/apt/lists/*

# COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# COPY --from=base /usr/local/bin /usr/local/bin
# COPY --from=prod-build /app /app

# # RUN addgroup --system appuser && adduser --system --ingroup appuser appuser && \
# #     chown -R appuser:appuser /app

# # USER appuser
# EXPOSE 8000
# ENTRYPOINT ["/app/entrypoint.prod.sh"]
# CMD ["sh", "-c", "gunicorn openspace.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-4} --threads ${GUNICORN_THREADS:-2} --timeout 120 --access-logfile - --error-logfile -"]
