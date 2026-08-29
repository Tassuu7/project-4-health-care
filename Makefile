# AegisCare Enterprise Automation Makefile

.PHONY: help install build run test clean docker-build docker-run

help:
	@echo "AegisCare Enterprise Management Commands:"
	@echo "  make install     - Install pinned Python dependencies"
	@echo "  make build       - Validate build and execute tests"
	@echo "  make run         - Start the AegisCare web application"
	@echo "  make test        - Run automated pytest suite with coverage"
	@echo "  make clean       - Remove cached artifacts and temporary files"

install:
	pip install -r requirements.txt

build:
	python -m pytest tests/

run:
	python main.py

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -r {} + 2>/dev/null || true

docker-build:
	docker build -t aegiscare-enterprise:latest .

docker-run:
	docker run -p 8000:8000 aegiscare-enterprise:latest
