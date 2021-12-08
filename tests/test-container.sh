#!/bin/bash
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
fi