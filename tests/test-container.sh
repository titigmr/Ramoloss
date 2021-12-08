#!/bin/bash
<<<<<<< HEAD
set -ex

active_container=$(docker ps --filter "name=bot-$NAME" -q)

if [ -z "${active_container}" ]; then
    echo "no container is running"
    exit 1
else
    echo "container bot-$NAME with id $active_container is running"
=======
set +e

APP_NAME=${NAME}-bot
container=$(docker ps --filter "name=$APP_NAME" -q)
ret=0
timeout=20;
test_result=1


until [ "$timeout" -le 0 -o "$test_result" -eq "0" ] ; do
        [ ! -z $container ]
        test_result=$?
        echo "Wait $timeout seconds: ${APP_NAME} is not running";
        (( timeout-- ))
        sleep 1
done
if [ "$test_result" -gt "0" ] ; then
        ret=$test_result
        echo "ERROR: timeout with ${APP_NAME}"
        exit $ret
>>>>>>> 2e73db2c69a28863c50d9d08c1ab95b8ee9ed139
fi