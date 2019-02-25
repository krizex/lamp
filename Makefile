IMAGE_LABEL := krizex/lamp
CONTAINER_PORT := 8001
HOST_DEBUG_PORT := 8000
CUR_DIR := $(shell pwd)
DB_CONTAINER_NAME := pg

.PHONY: build
build:
	mkdir -p _build/datatmp
	cp -r data/* _build/datatmp
	docker build -t $(IMAGE_LABEL) --build-arg persist=_build/datatmp .
	rm -rf _build/datatmp

.PHONY: debug
debug:
	docker run -it --rm \
	--link $(DB_CONTAINER_NAME) \
	-p $(HOST_DEBUG_PORT):$(CONTAINER_PORT) \
	--env-file database.conf \
	-v $(CUR_DIR)/data:/persist:rw \
	-v $(CUR_DIR)/src:/app \
	$(IMAGE_LABEL):latest /bin/bash

.PHONY: run stop restart

run:
	docker-compose up -d

stop:
	docker-compose down

restart: stop run

.PHONY: run-pg stop-pg
run-pg:
	docker run --rm -d \
	--name $(DB_CONTAINER_NAME) \
	--env-file database.conf \
	-v /var/lamp/db:/var/lib/postgresql/data:rw \
	postgres:10-alpine

stop-pg:
	docker stop $(DB_CONTAINER_NAME)

.PHONY: push pull
push:
	docker push ${IMAGE_LABEL}

pull:
	docker pull ${IMAGE_LABEL}
