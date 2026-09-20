.PHONY: dev test lint

dev: lint test
# 	sudo ./env/bin/uvicorn main:app --reload --host 0.0.0.0 --port 5000
	echo 0

test:
	python -m pytest

lint:
	ruff check --fix .
