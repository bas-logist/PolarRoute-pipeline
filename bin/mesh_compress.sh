#!/bin/bash

set -e

# Compress all files in specified folder
gzip -f ${INPUT_DIRECTORY}/*.json
gzip -f ${INPUT_DIRECTORY}/*.geojson
