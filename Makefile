.PHONY: help dev build test lint format clean migrate seed etl

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

dev: ## Start development environment
	docker-compose up -d db redis
	cd apps/api && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
	cd apps/web && npm run dev

build: ## Build all applications
	docker-compose build

test: ## Run all tests
	cd apps/api && python -m pytest
	cd apps/web && npm test

lint: ## Lint all code
	cd apps/api && ruff check . && mypy .
	cd apps/web && npm run lint

format: ## Format all code
	cd apps/api && black . && ruff format .
	cd apps/web && npm run format

clean: ## Clean up containers and volumes
	docker-compose down -v
	docker system prune -f

migrate: ## Run database migrations
	cd apps/api && alembic upgrade head

seed: ## Seed database with initial data
	cd apps/api && python -m app.seed

etl: ## Run ETL jobs
	cd apps/api && python -m app.etl.run_all

setup: ## Initial setup
	pnpm install
	make migrate
	make seed
