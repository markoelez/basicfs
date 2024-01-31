#!/bin/bash

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# setup volume servers
PORT=9090 VOLUME=/tmp/v1 ./scripts/volume &
PORT=9091 VOLUME=/tmp/v2 ./scripts/volume &

# start master
PORT=9092 DB=/tmp/db REPLICAS=2 ./scripts/master localhost:9090,localhost:9091