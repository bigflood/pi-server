#!/usr/bin/env bash

set -ea

HOME=/home/pi
DIST_DIR=$HOME/dist-files

echo "build.."
./build-dist.sh

WHL_FILE=`ls ./dist/*.whl | sort --version-sort | tail -1`
WHL_NAME=`basename $WHL_FILE`

echo "copy.."
ssh pi -- mkdir -p $DIST_DIR
scp $WHL_FILE pi:$DIST_DIR/

echo "install.."
ssh pi -- python3 -m pip install --user --upgrade $DIST_DIR/$WHL_NAME

echo "completed"
