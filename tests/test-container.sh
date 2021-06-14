#!/bin/bash
set -e

active_container=$(docker ps --filter "name=$APP_NAME" -q)

if [ -z "${active_container}" ]; then
    echo "no container is running"
    exit 1
else
    echo "container $APP_NAME with id $active_container is running"
fi