IMAGE_LABEL := krizex/lamp
CONTAINER_PORT := 8001
HOST_DEBUG_PORT := 8000
CUR_DIR := $(shell pwd)
APP_CONTAINER_NAME := lamp
NGINX_CONTAINER_NAME := nginx
NGINX_CONTAINER_PORT := 8000
HOST_SERVER_PORT := 8000

.PHONY: build
build:
	mkdir -p _build/datatmp
	cp -r data/* _build/datatmp
	docker build -t $(IMAGE_LABEL) .
	rm -rf _build/datatmp

.PHONY: debug run stop restart run-nginx run-lamp
debug:
	docker run -it --rm -p $(HOST_DEBUG_PORT):$(CONTAINER_PORT) $(IMAGE_LABEL):latest /bin/bash

run-lamp:
	@echo starting lamp...
	docker run --rm --name $(APP_CONTAINER_NAME) -d \
	-v $(CUR_DIR)/data:/db:rw \
	-v /var/log:/var/log:rw \
	$(IMAGE_LABEL):latest


run-nginx:
	@echo starting nginx...
	docker run --rm -d --link lamp -p $(HOST_SERVER_PORT):$(NGINX_CONTAINER_PORT) \
	-v $(CUR_DIR)/nginx_conf:/etc/nginx \
	-v $(CUR_DIR)/src/lamp/app/static:/var/www/static \
	--name $(NGINX_CONTAINER_NAME) nginx:stable

run: run-lamp run-nginx

stop:
	@echo stopping...
	-docker stop $(APP_CONTAINER_NAME)
	-docker stop $(NGINX_CONTAINER_NAME)

restart: stop run

.PHONY: run-compose stop-compose

run-compose:
	docker-compose up -d

stop-compose:
	docker-compose down
