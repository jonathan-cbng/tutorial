.PHONY: dev build serve clean help all test

# Default target
.DEFAULT_GOAL := help

all: build

help: ## Show this help message
	@echo "Available frontend targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

dev: ## Run development server
	npm run dev

build: ## Build for production
	npm run build

serve: ## Preview production build
	npm run serve

clean: ## Delete build artifacts
	rm -rf dist node_modules

test:
	npm run test
