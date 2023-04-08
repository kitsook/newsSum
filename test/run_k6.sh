#!/bin/sh
set -e

TAG_BASE="newssum"
TAG_NAME="$TAG_BASE-$(date +%s)"

docker run --rm --net=host -e K6_OUT=timescaledb=postgresql://k6:k6@localhost:5432/k6 -i xk6-output-timescaledb-k6 run --tag testid=$TAG_NAME - < k6/newssum.js