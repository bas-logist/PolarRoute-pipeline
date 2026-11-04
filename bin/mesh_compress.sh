#!/bin/bash

set -e

# Compress all files in specified folder
if [ -f ${INPUT_DIRECTORY}/*.json ]; then
    gzip -k -f ${INPUT_DIRECTORY}/*.json
fi
