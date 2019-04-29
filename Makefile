IMAGE_LABEL := krizex/lamp
CONTAINER_PORT := 8000
HOST_DEBUG_PORT := 8000
CUR_DIR := $(shell pwd)
DB_CONTAINER_NAME := pg
APP_CONTAINER_NAME := lamp
DB_NAME := lamp

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
	-v /etc/localtime:/etc/localtime:ro \
	$(IMAGE_LABEL):latest /bin/bash

.PHONY: run stop restart attach

run:
	docker-compose up -d

attach:
	docker exec -it $(APP_CONTAINER_NAME) /bin/bash

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

.PHONY: backup-db restore-db
backup-db:
	$(eval cur_date := $(shell date +%Y-%m-%d_%H_%M_%S))
	docker exec $(DB_CONTAINER_NAME) pg_dump -U lamp $(DB_NAME) > data/backup/dump_$(DB_NAME)_$(cur_date).sql

restore-db:
	@if [ "x$(backup)" = x ]; then echo "No backup argument"; exit 1; fi
	docker exec $(DB_CONTAINER_NAME) dropdb -U lamp $(DB_NAME)
	docker exec $(DB_CONTAINER_NAME) createdb -U lamp $(DB_NAME)
	cat $(backup) | docker exec -i $(DB_CONTAINER_NAME) psql -U lamp -d $(DB_NAME) -a
