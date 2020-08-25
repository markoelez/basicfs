#!/bin/bash

# setup volume servers

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

PORT=9091 VOLUME=/tmp/v1 ./volume &
PORT=9092 VOLUME=/tmp/v2 ./volume &

# start master

PORT=9090 DB=/tmp/db REPLICAS=2 ./master localhost:9091,localhost:9092

