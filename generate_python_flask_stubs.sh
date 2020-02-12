#!/usr/bin/env bash

docker run --rm -u "$(id -u):$(id -g)" -v ${PWD}:/local openapitools/openapi-generator-cli generate -o /local/ctt-server -i /local/radonctt-openapi.yaml -g python-flask 
