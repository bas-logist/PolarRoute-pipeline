#!/bin/bash

set -e

# Compress all files in most_recent folder
gzip -f ${INPUT_DIRECTORY}/*.yaml
