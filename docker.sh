#!/bin/bash

docker build -t basicfs -f Dockerfile .
docker run --hostname localhost -p 9090:9090 -p 9091:9091 -p 9092:9092 --name basicfs --rm basicfs bash -c "cd tmp/ && ./testsetup.sh"

