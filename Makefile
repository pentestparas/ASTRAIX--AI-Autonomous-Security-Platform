.PHONY: help up down build logs test lint format clean install dev-backend dev-frontend

# Default target
help:
	@echo "AstraIX Security Analyst - Development Commands"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make build       - Build all Docker images"
	@echo "  make logs        - View logs from all services"
	@echo "  make clean       - Remove containers, volumes, and images"
	@echo ""
	@echo "Development Commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make dev-backend - Start backend dev server"
	@echo "  make dev-frontend - Start frontend dev server"
	@echo "  make dev         - Start both dev servers (requires tmux)"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test        - Run all tests"
	@echo "  make test-backend - Run backend tests"
	@echo "  make test-frontend - Run frontend tests"
	@echo "  make test-coverage - Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint        - Run all linters"
	@echo "  make lint-backend - Run backend linters"
	@echo "  make lint-frontend - Run frontend linters"
	@echo "  make format      - Format all code"
	@echo "  make format-backend - Format backend code"
	@echo "  make format-frontend - Format frontend code"
	@echo ""
	@echo "Database:"
	@echo "  make migrate     - Run database migrations"
	@echo "  make migrate-create - Create new migration"
	@echo "  make db-shell    - Open database shell"

# Docker Commands
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

clean:
	docker-compose down -v --rmi all --remove-orphans

# Development
install: install-backend install-frontend

install-backend:
	cd backend && python -m venv .venv && .venv/bin/pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

dev:
	@echo "Starting both dev servers... (use tmux or run separately)"
	@echo "Backend: make dev-backend"
	@echo "Frontend: make dev-frontend"

# Testing
test: test-backend test-frontend

test-backend:
	cd backend && .venv/bin/pytest -v --tb=short

test-frontend:
	cd frontend && npm run test

test-coverage:
	cd backend && .venv/bin/pytest --cov=app --cov-report=html --cov-report=term
	cd frontend && npm run test:coverage

# Linting
lint: lint-backend lint-frontend

lint-backend:
	cd backend && .venv/bin/ruff check .
	cd backend && .venv/bin/mypy app

lint-frontend:
	cd frontend && npm run lint

# Formatting
format: format-backend format-frontend

format-backend:
	cd backend && .venv/bin/ruff format .
	cd backend && .venv/bin/ruff check --fix .

format-frontend:
	cd frontend && npm run format

# Database
migrate:
	cd backend && .venv/bin/alembic upgrade head

migrate-create:
	@read -p "Migration message: " msg; \
	cd backend && .venv/bin/alembic revision --autogenerate -m "$$msg"

db-shell:
	docker-compose exec postgres psql -U postgres -d astraix

# CI/CD Simulation
ci: lint test
	@echo "CI pipeline passed!"

# Generate OpenAPI spec
openapi:
	cd backend && .venv/bin/python -c "from app.main import app; import json; print(json.dumps(app.openapi(), indent=2))" > openapi.json

# Security scanning
security-scan:
	cd backend && .venv/bin/bandit -r app
	cd frontend && npm audit