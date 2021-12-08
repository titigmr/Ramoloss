#!/bin/bash
set -e

make build
make up
make test
make pytest
make down