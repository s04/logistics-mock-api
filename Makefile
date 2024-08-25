# Makefile for Logistics Mock API local testing

# Variables
DOCKER_IMAGE_NAME = logistics-mock-api
DOCKER_CONTAINER_NAME = logistics-mock-api-local
LOCAL_PORT = 8000

# Phony targets
.PHONY: all build run stop clean restart

# Default target
all: restart

# Build the Docker image
build:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the Docker container
run:
	docker run -d -p $(LOCAL_PORT):80 --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME)

# Stop the Docker container
stop:
	-docker stop $(DOCKER_CONTAINER_NAME)

# Remove the Docker container
clean: stop
	-docker rm $(DOCKER_CONTAINER_NAME)

# Restart: Clean, build, and run
restart: clean build run
	@echo "Container restarted and running on http://localhost:$(LOCAL_PORT)"

# Show logs
logs:
	docker logs $(DOCKER_CONTAINER_NAME)

# Enter the container shell
shell:
	docker exec -it $(DOCKER_CONTAINER_NAME) /bin/bash

# Run tests (if you have any)
test:
	# Add your test command here, for example:
	# docker exec $(DOCKER_CONTAINER_NAME) pytest

# Help
help:
	@echo "Available commands:"
	@echo "  make build    - Build the Docker image"
	@echo "  make run      - Run the Docker container"
	@echo "  make stop     - Stop the Docker container"
	@echo "  make clean    - Stop and remove the Docker container"
	@echo "  make restart  - Rebuild and restart the Docker container"
	@echo "  make logs     - Show container logs"
	@echo "  make shell    - Enter the container shell"
	@echo "  make test     - Run tests (if configured)"
	@echo "  make help     - Show this help message"