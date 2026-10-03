.PHONY: dev test lint build

dev: lint test run_mongo
	@echo "AirBreaker is running successfully"
	sudo ./env/bin/python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 5000 --env-file .env
	@echo "AirBreaker was stopped successfully"

test:
	./env/bin/python3 -m pytest

lint:
	./env/bin/ruff check --fix .

build: run_mongo
	sudo apt install -y python3 python3-venv
	python3 -m venv env
	
	sudo apt install -y  \
	libpcap-dev \
    tcpdump 

	source env/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

run_mongo:
	sudo docker compose up -d --build