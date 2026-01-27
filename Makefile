.PHONY: run test migrate migration-create clean frontend-dev frontend-build frontend-serve frontend-clean help all

# Default target
.DEFAULT_GOAL := help

all: build docs

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

clean: frontend-clean ## Delete all generated files
	rm -f app.db

build: frontend-build ## Build database and frontend
	alembic upgrade head

run: ## Run the application
	python main.py

test: ## Run tests with coverage
	python -m pytest test -n4 --cov=backend --cov-report=term-missing

migrate: ## Apply database migrations
	alembic upgrade head

migration-create : migrate ## Create a new migration (use MESSAGE="your message")
	@if [ -z "$(MESSAGE)" ]; then \
		echo "Error: MESSAGE variable is required. Usage: make migration-create MESSAGE=\"your message\""; \
		exit 1; \
	fi
	alembic revision --autogenerate -m "$(MESSAGE)"

docs: ## Generate documentation
	make -C docs

# Frontend targets
frontend-dev: ## Run frontend development server
	$(MAKE) -C frontend dev

frontend-build: ## Build frontend for production
	$(MAKE) -C frontend build

frontend-serve: ## Preview frontend production build
	$(MAKE) -C frontend serve

frontend-clean: ## Clean frontend build artifacts
	$(MAKE) -C frontend clean
