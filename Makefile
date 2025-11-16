.PHONY: help dev-build dev-up dev-down dev-logs dev-shell dev-migrate prod-build prod-up prod-down prod-logs prod-shell prod-migrate clean backup

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)OpenSpace Docker Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make dev-build       - Build development containers"
	@echo "  make dev-up          - Start development environment"
	@echo "  make dev-down        - Stop development environment"
	@echo "  make dev-logs        - View development logs"
	@echo "  make dev-shell       - Access Django shell (dev)"
	@echo "  make dev-bash        - Access bash in web container (dev)"
	@echo "  make dev-migrate     - Run migrations (dev)"
	@echo "  make dev-superuser   - Create superuser (dev)"
	@echo ""
	@echo "$(GREEN)Production:$(NC)"
	@echo "  make prod-build      - Build production containers"
	@echo "  make prod-up         - Start production environment"
	@echo "  make prod-down       - Stop production environment"
	@echo "  make prod-logs       - View production logs"
	@echo "  make prod-shell      - Access Django shell (prod)"
	@echo "  make prod-bash       - Access bash in web container (prod)"
	@echo "  make prod-migrate    - Run migrations (prod)"
	@echo "  make prod-superuser  - Create superuser (prod)"
	@echo ""
	@echo "$(GREEN)Maintenance:$(NC)"
	@echo "  make backup          - Backup production database"
	@echo "  make clean           - Clean up containers and volumes"
	@echo "  make ps              - Show running containers"
	@echo "  make restart-dev     - Restart development environment"
	@echo "  make restart-prod    - Restart production environment"

# =============================================================================
# DEVELOPMENT COMMANDS
# =============================================================================

dev-build: ## Build development containers
	@echo "$(BLUE)Building development containers...$(NC)"
	docker-compose -f docker-compose.dev.yml build

dev-up: ## Start development environment
	@echo "$(GREEN)Starting development environment...$(NC)"
	docker-compose -f docker-compose.dev.yml up -d
	@echo "$(GREEN)✅ Development environment is running!$(NC)"
	@echo "Access at: http://localhost:8000"

dev-down: ## Stop development environment
	@echo "$(YELLOW)Stopping development environment...$(NC)"
	docker-compose -f docker-compose.dev.yml down

dev-logs: ## View development logs
	docker-compose -f docker-compose.dev.yml logs -f

dev-logs-web: ## View web logs only (dev)
	docker-compose -f docker-compose.dev.yml logs -f web

dev-logs-celery: ## View celery logs only (dev)
	docker-compose -f docker-compose.dev.yml logs -f celery

dev-shell: ## Access Django shell (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py shell

dev-bash: ## Access bash in web container (dev)
	docker-compose -f docker-compose.dev.yml exec web bash

dev-migrate: ## Run migrations (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations
	docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

dev-superuser: ## Create superuser (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

dev-test: ## Run tests (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py test

dev-collectstatic: ## Collect static files (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput

restart-dev: ## Restart development environment
	@echo "$(YELLOW)Restarting development environment...$(NC)"
	docker-compose -f docker-compose.dev.yml restart
	@echo "$(GREEN)✅ Development environment restarted!$(NC)"

# =============================================================================
# PRODUCTION COMMANDS
# =============================================================================

prod-build: ## Build production containers
	@echo "$(BLUE)Building production containers...$(NC)"
	docker-compose -f docker-compose.prod.yml build

prod-up: ## Start production environment
	@echo "$(GREEN)Starting production environment...$(NC)"
	docker-compose -f docker-compose.prod.yml up -d
	@echo "$(GREEN)✅ Production environment is running!$(NC)"

prod-down: ## Stop production environment
	@echo "$(YELLOW)Stopping production environment...$(NC)"
	docker-compose -f docker-compose.prod.yml down

prod-logs: ## View production logs
	docker-compose -f docker-compose.prod.yml logs -f

prod-logs-web: ## View web logs only (prod)
	docker-compose -f docker-compose.prod.yml logs -f web

prod-logs-celery: ## View celery logs only (prod)
	docker-compose -f docker-compose.prod.yml logs -f celery

prod-logs-nginx: ## View nginx logs only (prod)
	docker-compose -f docker-compose.prod.yml logs -f nginx

prod-shell: ## Access Django shell (prod)
	docker-compose -f docker-compose.prod.yml exec web python manage.py shell

prod-bash: ## Access bash in web container (prod)
	docker-compose -f docker-compose.prod.yml exec web bash

prod-migrate: ## Run migrations (prod)
	docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

prod-superuser: ## Create superuser (prod)
	docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

prod-collectstatic: ## Collect static files (prod)
	docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

restart-prod: ## Restart production environment
	@echo "$(YELLOW)Restarting production environment...$(NC)"
	docker-compose -f docker-compose.prod.yml restart
	@echo "$(GREEN)✅ Production environment restarted!$(NC)"

# =============================================================================
# DATABASE COMMANDS
# =============================================================================

db-shell-dev: ## Access PostgreSQL (dev)
	docker-compose -f docker-compose.dev.yml exec db psql -U postgres -d openspace

db-shell-prod: ## Access PostgreSQL (prod)
	docker-compose -f docker-compose.prod.yml exec db psql -U openspace_user -d openspace_prod

backup: ## Backup production database
	@echo "$(BLUE)Creating database backup...$(NC)"
	@mkdir -p backups
	docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U openspace_user openspace_prod | gzip > backups/backup_$$(date +%Y%m%d_%H%M%S).sql.gz
	@echo "$(GREEN)✅ Backup created in backups/ directory$(NC)"

restore: ## Restore database from backup (provide BACKUP_FILE=/path/to/backup.sql.gz)
	@echo "$(YELLOW)Restoring database from $(BACKUP_FILE)...$(NC)"
	gunzip < $(BACKUP_FILE) | docker-compose -f docker-compose.prod.yml exec -T db psql -U openspace_user openspace_prod
	@echo "$(GREEN)✅ Database restored!$(NC)"

# =============================================================================
# MAINTENANCE COMMANDS
# =============================================================================

ps: ## Show running containers
	@echo "$(BLUE)Development:$(NC)"
	@docker-compose -f docker-compose.dev.yml ps 2>/dev/null || echo "Not running"
	@echo ""
	@echo "$(BLUE)Production:$(NC)"
	@docker-compose -f docker-compose.prod.yml ps 2>/dev/null || echo "Not running"

stats: ## Show container resource usage
	docker stats

clean: ## Clean up containers and volumes
	@echo "$(YELLOW)This will remove all containers and volumes!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose -f docker-compose.dev.yml down -v; \
		docker-compose -f docker-compose.prod.yml down -v; \
		docker system prune -af --volumes; \
		echo "$(GREEN)✅ Cleanup complete!$(NC)"; \
	else \
		echo "$(YELLOW)Cleanup cancelled$(NC)"; \
	fi

prune: ## Remove unused Docker resources
	docker system prune -af

# =============================================================================
# SETUP COMMANDS
# =============================================================================

setup: ## Initial setup (create directories, copy env files)
	@echo "$(BLUE)Setting up project...$(NC)"
	mkdir -p nginx/conf.d nginx/ssl media staticfiles backups
	chmod +x entrypoint.dev.sh entrypoint.prod.sh 2>/dev/null || true
	@if [ ! -f .env.dev ]; then \
		cp .env.dev.example .env.dev 2>/dev/null || echo "Create .env.dev manually"; \
	fi
	@if [ ! -f .env.prod ]; then \
		cp .env.prod.example .env.prod 2>/dev/null || echo "Create .env.prod manually"; \
	fi
	@echo "$(GREEN)✅ Setup complete!$(NC)"

# =============================================================================
# UTILITY COMMANDS
# =============================================================================

update-deps: ## Update Python dependencies
	docker-compose -f docker-compose.dev.yml exec web pip install -r requirements.txt

generate-secret-key: ## Generate new SECRET_KEY
	@python3 -c "from django.core.management.utils import get_random_secret_key; print('SECRET_KEY=' + get_random_secret_key())"

generate-fernet-key: ## Generate new FERNET_KEY
	@python3 -c "from cryptography.fernet import Fernet; print('FERNET_KEY=' + Fernet.generate_key().decode())"

# Default target
.DEFAULT_GOAL := help