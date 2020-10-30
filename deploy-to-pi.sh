#!/usr/bin/env bash

HOME=/home/pi
DIST_DIR=$HOME/dist-files
WHL_FILE=`ls ./dist/*.whl | sort | tail -1`
WHL_NAME=`basename $WHL_FILE`

echo "build.." && \
./build-dist.sh && \
echo "copy.." && \
ssh pi -- mkdir -p $DIST_DIR && \
scp $WHL_FILE pi:$DIST_DIR/ && \
echo "install.." && \
ssh pi -- python3 -m pip install --user --upgrade $DIST_DIR/$WHL_NAME && \
echo "completed"
