# OpenSpace Project Instructions

## 1. Project Context & Architecture

- **Frameworks**: Django 4.2 (Backend), Graphene-Django (GraphQL), Django REST Framework (REST), Celery (Async Tasks).
- **Database**: PostgreSQL (Production/Dev), SQLite (Local fallback).
- **Infrastructure**: Docker & Docker Compose (Dev/Prod separation), Nginx (Reverse Proxy), Redis (Cache/Broker).
- **Key Components**:
  - `openspace/`: Project configuration with smart environment detection.
  - `myapp/`: Core business logic (Models, Views, Schema, Tasks).
  - `nginx/`: Web server configuration.
  - `scripts/`: Utility scripts for DB access, key generation.

## 2. Development Workflow

- **Environment Setup**:
  - Use `setup_venv.bat` for local virtualenv.
  - Use `start_dev.bat` to spin up Docker containers (Web, DB, Redis, Celery).
  - **Critical**: Environment is detected via `openspace/settings.py:detect_environment()`. Ensure `.env.dev` or `.env.prod` exists for Docker.
- **Running the App**:
  - **Docker**: `docker-compose -f docker-compose.dev.yml up --build`
  - **Local**: `python manage.py runserver` (requires local DB setup).
- **Database Management**:
  - Use `db_access.bat` or `scripts/db_access.py` for backups and connection info.
  - Migrations: `python manage.py makemigrations` & `python manage.py migrate`.

## 3. Code Style & Conventions

- **Models (`myapp/models.py`)**:
  - Use `CustomUser` (extends `AbstractUser`) for authentication.
  - `Report` model uses a custom `_generate_unique_id` method.
  - `OpenSpace` and `OpenSpaceBooking` manage facility availability.
- **GraphQL (`myapp/schema.py`)**:
  - All mutations and queries are aggregated in `schema.py`.
  - Use `graphene_django` types for model mapping.
  - Authentication via `graphql_jwt`.
- **Async Tasks (`myapp/notification_task.py`)**:
  - Use `@shared_task` decorator.
  - Tasks handle SMS notifications and booking expiration checks.
  - Scheduled via `CELERY_BEAT_SCHEDULE` in `settings.py`.

## 4. Testing & Quality Assurance

- **Current State**: `myapp/tests.py` is currently empty.
- **Guideline**:
  - **Must** add tests for new features.
  - Focus on Model methods (e.g., `Report.save()`, `_generate_unique_id`).
  - Test GraphQL mutations for permissions and logic.
  - Use `django.test.TestCase`.

## 5. Specific Patterns & Gotchas

- **Environment Detection**:
  - `settings.py` logic is complex. Always check `DJANGO_ENVIRONMENT` env var.
  - `DEBUG` is forced `False` in production.
- **SMS & Email**:
  - `sms_utils.py` handles external SMS APIs (Africa's Talking, Beem).
  - `Report` model sends emails on save (`_send_notification_email`).
- **Security**:
  - Production settings enforce SSL and secure cookies.
  - `generate_keys.py` creates secure secrets.

## 6. Common Commands

- **Start Dev**: `start_dev.bat`
- **Create Superuser**: `python manage.py createsuperuser`
- **Shell**: `python manage.py shell`
- **Celery Worker**: `celery -A openspace worker -l info`
