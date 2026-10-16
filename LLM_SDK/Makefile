VENV = .venv
PYTHON = $(VENV)/bin/python
UV = uv

SRC_DIR = src
TEST_DIR = tests

$(VENV):
		@echo "Creating virtual environment (.venv) using uv..." 
		$(UV) venv $(VENV)

venv = $(VENV)

install: $(venv)
		@echo "Installing dependencies..."
		uv synch

run: install
		@echo "Running LLM\_SDK in virtual environment..."
		$(PYTHON) -m src

debug: install
		@echo "Running LLM\_SDK in debug mode..."
		$(PYTHON) -m src --debug

clean:
		@echo "Cleaning up virtual environment and build artifacts..."
		rm -rf $(VENV)
		find . -type d -name "\_\_pycache\_\_" -exec rm -rf {} +
		find . -type d -name ".mypy\_cache" -exec rm -rf {} +
		find . -type d -name ".pytest\_cache" -exec rm -rf {} +
		find . -type d -name ".ruff\_cache" -exec rm -rf {} +
		find . -type f -name "\*.pyc" -delete
		find . -type f -name "\*.pyo" -delete

lint: install
		@echo "Running code quality checks (flake8 & mypy)..."
		$(VENV)/bin/flake8 $(SRC_DIR)
		$(VENV)/bin/mypy $(SRC_DIR) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
		@echo "Running strict code quality checks..."
		$(VENV)/bin/flake8 $(SRC_DIR)
		$(VENV)/bin/mypy $(SRC_DIR) --strict


.PHONY: all help venv install run debug test lint lint-strict clean