.PHONY: dev test lint build run_mongo

# Looking for packet manager
ifeq ($(shell which apt-get 2>/dev/null),)
    ifeq ($(shell which dnf 2>/dev/null),)
        ifeq ($(shell which pacman 2>/dev/null),)
            INSTALL_CMD = echo "Пакетный менеджер не найден. Установите зависимости вручную:"
        else
            INSTALL_CMD = sudo pacman -Syu --noconfirm
            PKGS = python python-virtualenv libpcap tcpdump
        endif
    else
        INSTALL_CMD = sudo dnf install -y
        PKGS = python3 python3-virtualenv libpcap-devel tcpdump
    endif
else
    INSTALL_CMD = sudo apt-get update && sudo apt-get install -y
    PKGS = python3 python3-venv libpcap-dev tcpdump
endif

dev: lint test run_mongo
	@echo "AirBreaker is running successfully"
	sudo ./env/bin/python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 5000 --env-file .env
	@echo "AirBreaker was stopped successfully"

test:
	./env/bin/python3 -m pytest

lint:
	./env/bin/ruff check --fix .

build: run_mongo
	@echo "Detected package manager command: $(INSTALL_CMD)"
	$(INSTALL_CMD) $(PKGS)
	
	python3 -m venv env
	./env/bin/pip install --upgrade pip
	./env/bin/pip install -r requirements.txt

run_mongo:
	sudo docker compose up -d --build
