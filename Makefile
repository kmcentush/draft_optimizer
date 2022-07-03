.PHONY: install
install:
	python -m pip install pip --upgrade
	pip install -r requirements-dev.txt --upgrade
	pre-commit install
	pip install -r requirements.txt --upgrade
	pip install -e . --upgrade --no-deps

.PHONY: format
format:
	isort . --profile black --line-length=120
	mypy . --ignore-missing-imports
	black . --line-length=120
	flake8 . --max-line-length=120 --ignore=E203 --exclude=__init__.py

.PHONY: pytest
pytest:
	pytest --cov-report term-missing --cov=draft_optimizer tests/
