# ==========================================
# Bookstore - Django + Docker + Poetry
# ==========================================

# Variables
COMPOSE=docker compose
WEB=$(COMPOSE) exec web
MANAGE=$(WEB) python manage.py

.DEFAULT_GOAL := help

# ==========================================
# Help
# ==========================================

.PHONY: help

help:
	@echo.
	@echo ========== Bookstore ==========
	@echo.
	@echo Development
	@echo   make build            Build containers
	@echo   make up               Start containers
	@echo   make down             Stop containers
	@echo   make restart          Restart containers
	@echo   make logs             Show logs
	@echo.
	@echo Django
	@echo   make migrate
	@echo   make makemigrations
	@echo   make createsuperuser
	@echo   make shell
	@echo   make dbshell
	@echo   make collectstatic
	@echo.
	@echo Testing
	@echo   make test
	@echo   make coverage
	@echo.
	@echo Quality
	@echo   make lint
	@echo   make format
	@echo.
	@echo Utilities
	@echo   make bash
	@echo   make seed
	@echo   make clean
	@echo.

# ==========================================
# Docker
# ==========================================

.PHONY: build

build:
	$(COMPOSE) build

.PHONY: up

up:
	$(COMPOSE) up -d

.PHONY: down

down:
	$(COMPOSE) down

.PHONY: restart

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d

.PHONY: logs

logs:
	$(COMPOSE) logs -f

# ==========================================
# Django
# ==========================================

.PHONY: migrate

migrate:
	$(MANAGE) migrate

.PHONY: makemigrations

makemigrations:
	$(MANAGE) makemigrations

.PHONY: createsuperuser

createsuperuser:
	$(MANAGE) createsuperuser

.PHONY: shell

shell:
	$(MANAGE) shell

.PHONY: dbshell

dbshell:
	$(MANAGE) dbshell

.PHONY: collectstatic

collectstatic:
	$(MANAGE) collectstatic --noinput

# ==========================================
# Testing
# ==========================================

.PHONY: test

test:
	$(WEB) pytest

.PHONY: coverage

coverage:
	$(WEB) pytest --cov=. --cov-report=term-missing

# ==========================================
# Code Quality
# ==========================================

.PHONY: lint

lint:
	$(WEB) flake8 .
	$(WEB) black --check .
	$(WEB) isort . --check-only

.PHONY: format

format:
	$(WEB) black .
	$(WEB) isort .

# ==========================================
# Utilities
# ==========================================

.PHONY: bash

bash:
	$(WEB) sh

.PHONY: seed

seed:
	$(MANAGE) seed

.PHONY: clean

clean:
	$(COMPOSE) down -v
	docker system prune -f