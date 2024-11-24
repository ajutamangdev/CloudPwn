SHELL := /bin/bash

# Tools and Directories
LINTER = pylint
BLACK = black
FLAKE8 = flake8
AUDITER = bandit
TYPECHECKER = mypy
TARGET_DIR = cloudpwn
VENV_DIR = .venv
PYTHON_VERSION = python3.12

.DEFAULT_GOAL := help

# Targets
.PHONY: all clean setup install lint format flake8 audit typecheck help

all: clean format lint flake8 audit typecheck ## Run all quality checks

clean: ## Clean up build artifacts and Python caches
	@rm -rf __pycache__ .pytest_cache
	@find . -name '*.pyc' -exec rm -r {} +
	@find . -name '__pycache__' -exec rm -r {} +
	@rm -rf build dist
	@find . -name '*.egg-info' -type d -exec rm -r {} +

setup: ## Set up the virtual environment and install dependencies
	@echo "Creating virtual environment at: $(VENV_DIR)"
	@$(PYTHON_VERSION) -m venv $(VENV_DIR)
	@echo "Upgrading pip..."
	@source $(VENV_DIR)/bin/activate && pip install --upgrade pip
	@echo "Installing dependencies..."
	@source $(VENV_DIR)/bin/activate && pip install -e .
	@echo -e "\n✅🎉 Done.\n"
	@echo "➡️ For Linux/MacOs source $(VENV_DIR)/bin/activate"
	@echo "➡️ For Windows source $(VENV_DIR)/Scripts/activate"
	@echo "➡️  python3 cloudpwn/main.py"

install: setup ## Install the project and dependencies

lint: ## Run pylint on the target directory
	$(LINTER) $(TARGET_DIR)

format: ## Format Python files with Black and AutoPEP8
	$(BLACK) .

flake8: ## Run flake8 for code style checking
	$(FLAKE8) $(TARGET_DIR)

audit: ## Audit the codebase for security issues with Bandit
	$(AUDITER) -r $(TARGET_DIR)

typecheck: ## Run static type checks with mypy
	$(TYPECHECKER) $(TARGET_DIR)

help: ## Show this help message
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

