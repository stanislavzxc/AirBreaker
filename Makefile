.PHONY: dev test lint format

dev: lint test
	sudo ./env/bin/uvicorn main:app --reload --host 0.0.0.0 --port 5000

test:
	python -m pytest

lint:
	ruff check .
	
format:
	ruff check --fix .