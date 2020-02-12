#!/usr/bin/env bash

CURRENT_DIR=$(pwd)
SH_DIR=$(dirname "$0")

cd $SH_DIR/ctt-server
virtualenv .
source bin/activate
pip install --no-cache -r requirements.txt
python -m openapi_server

cd $CURRENT_DIR
