#!/usr/bin/env bash

cp -R ctt-server /tmp/$(date '+%Y-%m-%d_%H%M%S')-ctt-server

docker run --rm -u "$(id -u):$(id -g)" -v ${PWD}:/local openapitools/openapi-generator-cli generate -o /local/ctt-server -i /local/radonctt-openapi.yaml -g python-flask 
