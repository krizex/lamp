IMAGE_LABEL := lamp
CONTAINER_PORT := 8000
HOST_DEBUG_PORT := 8000
HOST_RUN_PORT := 8001
CUR_DIR := $(shell pwd)
CONTAINER_NAME := lamp

.PHONY: build
build:
	mkdir -p _build/datatmp
	cp -r data/* _build/datatmp
	docker build -t $(IMAGE_LABEL) .
	rm -rf _build/datatmp

.PHONY: debug run stop restart
debug:
	docker run -it -p $(HOST_DEBUG_PORT):$(CONTAINER_PORT) $(IMAGE_LABEL):latest /bin/bash

run:
	docker run --name $(CONTAINER_NAME) -d --rm \
    -p 127.0.0.1:$(HOST_RUN_PORT):$(CONTAINER_PORT) \
	-v $(CUR_DIR)/data:/db:rw \
	-v /var/log:/var/log:rw \
	$(IMAGE_LABEL):latest

stop:
	docker stop $(CONTAINER_NAME)

restart: stop run
