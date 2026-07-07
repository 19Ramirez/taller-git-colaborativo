# Makefile for Docker-Taller project (Windows Version)

IMAGE_NAME = ghcr.io/19ramirez/docker-taller:1.0.0
STACK_FILE = stack.yml

VPS_USER = $(VPS_USER)
VPS_HOST = $(VPS_HOST)
VPS_SSH_PORT = $(VPS_SSH_PORT)

.PHONY: all
all: help

.PHONY: help
help:
	@echo Available targets:
	@echo   build      Build Docker image locally
	@echo   push       Push image to GitHub Container Registry
	@echo   deploy     Deploy stack to VPS using your National ID
	@echo   clean      Remove local Docker images

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: push
push:
	@echo | set /p="$(GHCR_PAT)" | docker login ghcr.io -u $(GITHUB_ACTOR) --password-stdin
	docker push $(IMAGE_NAME)

.PHONY: deploy
deploy:
	@echo Copying $(STACK_FILE) to VPS...
	sshpass -p "$(VPS_PASSWORD)" ssh -p $(VPS_SSH_PORT) $(VPS_USER)@$(VPS_HOST) "cd ~/landinga && docker stack rm divisas || true && timeout /t 20 /nobreak && docker stack deploy -c $(STACK_FILE) --with-registry-auth divisas"

.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME) 2>nul || exit 0