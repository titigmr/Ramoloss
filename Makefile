# repository
SHELL = /bin/bash
NAME ?= ramoloss
ARCH ?= $(shell uname -m)
VERSION ?= $(shell git describe --tag --abbrev=0)
SERVICES := bot db log

# docker-compose
DC  := $(shell type -p docker-compose)
DC_BUILD_ARGS := --pull --force-rm
DC_RUN_ARGS := -d --no-build
DC_FILE := docker-compose.yml
DC_CONFIG_ARGS := -q
PLATFORM ?= linux/amd64

# docker
#REGISTRY ?= docker.io
REGISTRY ?= ghcr.io
REPOSITORY ?= ramoloss
REGISTRY_USERNAME ?= toto

# image
IMAGES = $(foreach srv, $(SERVICES), ${NAME}-${srv}:${VERSION})
IMAGES_REGISTRY=$(foreach im, $(IMAGE), ${REGISTRY}/${REGISTRY_USERNAME}/${im})

export

all:
	@echo "Usage: VERSION=latest make deploy | build | \
	up | down | test | check | push | pull "


# check var or config
check-var:
	@: $(if $(value $*),,$(error $* is undefined))
	@echo ${$*}

# for see configs use: `make DC_CONFIG_ARGS="" check-config`
check-config:
	${DC} -f ${DC_FILE} config ${DC_CONFIG_ARGS}

# build all or one service
build: check-config
	${DC} -f ${DC_FILE} build ${DC_BUILD_ARGS}

build-%:
	@echo "# start $*"
	${DC} -f ${DC_FILE} build ${DC_BUILD_ARGS} $*

# up all or one service
up: check-config
	@if [ -z "${DISCORD_TOKEN}" ] ; \
	then echo "ERROR: DISCORD_TOKEN \
	not defined" ; exit 1 ; fi
	${DC} -f ${DC_FILE} up ${DC_RUN_ARGS}

up-%: check-config
	${DC} -f ${DC_FILE} up ${DC_RUN_ARGS} $*

# down all or one service
down:
	${DC} -f ${DC_FILE} down

down-%:
	${DC} -f ${DC_FILE} down $*

# test container and app
test: test-container test-bot
test-%:
	@echo "# test $*"
	bash tests/test-$*.sh

# push
push: push-bot

push-%:
	@if [ -z "${REGISTRY}" -a -z "${REGISTRY_USERNAME}" ] ; \
	then echo "ERROR: REGISTRY and REGISTRY_USERNAME \
	not defined" ; exit 1 ; fi
	docker tag ${NAME}-$*:${VERSION} ${REGISTRY}/${REGISTRY_LOGIN}/${NAME}-$*:${VERSION}
	docker push ${REGISTRY}/${REGISTRY_LOGIN}/${NAME}-$*:${VERSION}

pull: pull-bot

pull-%:
	@if [ -n "${REGISTRY_TOKEN}" -a -n "${REGISTRY_LOGIN}" ] ;\
	then echo ${REGISTRY_TOKEN} | docker login ${REGISTRY} \
	--username ${REGISTRY_LOGIN} --password-stdin ; fi
	docker pull ${REGISTRY}/${REGISTRY_LOGIN}/${NAME}-$*:${VERSION}
	docker tag ${REGISTRY}/${REGISTRY_LOGIN}/${NAME}-$*:${VERSION} ${NAME}-$*:${VERSION}


deploy: VERSION=latest
deploy: pull up

