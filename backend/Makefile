.PHONY: help install test run lint format clean

help:
	@echo "Backend Development Commands"
	@echo "install    - Install dependencies"
	@echo "test       - Run all tests with coverage"
	@echo "test-fast  - Run tests without coverage"
	@echo "run        - Start development server"
	@echo "lint       - Run linting checks"
	@echo "format     - Format code with black"
	@echo "clean      - Remove cache and build files"

install:
	pip install -r requirements.txt

test:
	pytest --cov=app --cov-report=html --cov-report=term

test-fast:
	pytest -v

run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

lint:
	black --check app tests main.py
	isort --check-only app tests main.py

format:
	black app tests main.py
	isort app tests main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
