# repository
SHELL = /bin/bash
NAME ?= ramoloss
ARCH ?= $(shell uname -m)
VERSION := $(shell git describe --abbrev=0)

# docker-compose
DC  := $(shell type -p docker-compose)
DC_BUILD_ARGS := --pull --force-rm
DC_RUN_ARGS := -d --no-build
DC_FILE := docker-compose.yml

# docker
#REGISTRY ?= docker.io
REGISTRY ?= ghcr.io
REPOSITORY ?= ramoloss

# image
IMAGE_bot=${NAME}-bot:${VERSION}
IMAGE_REGISTRY_bot=${REGISTRY}/${REGISTRY_USERNAME}/${IMAGE_bot}


export

all:
	@echo "Usage: NAME=ramoloss make deploy | build | \
	up | down | test | check | push | pull "


# check var or config
check-var-%:
	@: $(if $(value $*),,$(error $* is undefined))
	@echo ${$*}

check-config:
	${DC} -f ${DC_FILE} config

check-config-quiet:
	${DC} -f ${DC_FILE} config -q

# build all or one service
build: check-config-quiet
	echo ${VERSION}
	${DC} -f ${DC_FILE} build ${DC_BUILD_ARGS}

build-%:
	@echo "# start $*"
	${DC} -f ${DC_FILE} build ${DC_BUILD_ARGS} $*

# up all or one service
up: check-config-quiet
	@if [ -z "${DISCORD_TOKEN}" ] ; \
	then echo "ERROR: DISCORD_TOKEN \
	not defined" ; exit 1 ; fi
	${DC} -f ${DC_FILE} up ${DC_RUN_ARGS}

up-%: check-config-quiet
	${DC} -f ${DC_FILE} up ${DC_RUN_ARGS} $*

# down all or one service
down:
	${DC} -f ${DC_FILE} down

down-%:
	${DC} -f ${DC_FILE} down $*

# test
test: test-container
test-%:
	@echo "# test $*"
	bash tests/test-$*.sh

# push
push: push-bot

push-%:
	@if [ -z "${REGISTRY}" -a -z "${REGISTRY_USERNAME}" ] ; \
	then echo "ERROR: REGISTRY and REGISTRY_USERNAME \
	not defined" ; exit 1 ; fi
	docker tag ${IMAGE_$*} ${IMAGE_REGISTRY_$*}
	docker push ${IMAGE_REGISTRY_$*}

pull: pull-bot

pull-%:
	@if [ -n "${REGISTRY_TOKEN}" -a -n "${REGISTRY_LOGIN}" ] ;\
	then echo ${REGISTRY_TOKEN} | docker login ${REGISTRY} \
	--username ${REGISTRY_LOGIN} --password-stdin ; fi
	docker pull ${REGISTRY}/${REGISTRY_LOGIN}/${NAME}-$*:latest
	docker tag ${REGISTRY}/${REGISTRY_LOGIN}/${NAME}-$*:latest ${NAME}-$*:latest

deploy: pull up

