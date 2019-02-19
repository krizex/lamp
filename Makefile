IMAGE_LABEL := krizex/lamp
CONTAINER_PORT := 8001
HOST_DEBUG_PORT := 8000
CUR_DIR := $(shell pwd)
APP_CONTAINER_NAME := lamp
NGINX_CONTAINER_NAME := nginx
DB_CONTAINER_NAME := pg
NGINX_CONTAINER_PORT := 8000
HOST_SERVER_PORT := 8000

.PHONY: build
build:
	mkdir -p _build/datatmp
	cp -r data/* _build/datatmp
	docker build -t $(IMAGE_LABEL) --build-arg persist=_build/datatmp .
	rm -rf _build/datatmp

.PHONY: debug run-nginx stop-nginx run-lamp stop-lamp
debug:
	docker run -it --rm \
	--link $(DB_CONTAINER_NAME) \
	-p $(HOST_DEBUG_PORT):$(CONTAINER_PORT) \
	--env-file database.conf \
	-v $(CUR_DIR)/data:/persist:rw \
	$(IMAGE_LABEL):latest /bin/bash

run-lamp:
	@echo starting lamp...
	docker run --rm -d \
	--name $(APP_CONTAINER_NAME) \
	-v $(CUR_DIR)/data:/db:rw \
	-v /var/log/lamp:/var/log:rw \
	$(IMAGE_LABEL):latest

stop-lamp:
	@echo stopping lamp...
	docker stop $(APP_CONTAINER_NAME)

run-nginx:
	@echo starting nginx...
	docker run --rm -d \
	--name $(NGINX_CONTAINER_NAME) \
	--link lamp \
	-p $(HOST_SERVER_PORT):$(NGINX_CONTAINER_PORT) \
	-v $(CUR_DIR)/nginx_conf:/etc/nginx \
	-v $(CUR_DIR)/src/lamp/app/static:/var/www/static \
	nginx:stable

stop-nginx:
	@echo stopping nginx...
	docker stop $(NGINX_CONTAINER_NAME)

.PHONY: run-compose stop-compose run stop restart

run-compose:
	docker-compose up -d

stop-compose:
	docker-compose down

run: run-compose

stop: stop-compose

restart: stop run


.PHONY: run-pg stop-pg
run-pg:
	docker run --rm -d \
	--name $(DB_CONTAINER_NAME) \
	--env-file database.conf \
	-v $(CUR_DIR)/db:/var/lib/postgresql/data:rw \
	postgres:10-alpine

stop-pg:
	docker stop $(DB_CONTAINER_NAME)
