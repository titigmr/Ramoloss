SHELL = /bin/bash
APP := bot
APP_NAME := ramoloss

# docker-compose
DC  := $(shell type -p docker-compose)
DC_BUILD_ARGS := --pull --no-cache --force-rm
DC_RUN_ARGS := -d --no-build
DC_FILE := docker-compose.yml

export


all:
	@echo "Usage: make build | up | down | test | check"


# check var or config
check-var-%:
	@: $(if $(value $*),,$(error $* is undefined))

check-config:
	${DC} -f ${DC_FILE} config -q

# build all or one service
build: check-config
	${DC} -f ${DC_FILE} build ${DC_BUILD_ARGS}

build-%:
	@echo "# start $*"
	${DC} -f ${DC_FILE} build ${DC_BUILD_ARGS}  $*

# up all or one service
up: check-config
	${DC} -f ${DC_FILE} up ${DC_RUN_ARGS}

up-%: check-config
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
	./tests/test-$*.sh