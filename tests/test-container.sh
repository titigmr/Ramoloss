#!/bin/bash
set -ex

active_container=$(docker ps --filter "name=bot-$NAME" -q)

if [ -z "${active_container}" ]; then
    echo "no container is running"
    exit 1
else
    echo "container bot-$NAME with id $active_container is running"
fi