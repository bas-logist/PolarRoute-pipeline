#!/bin/bash

set -e

# Local pipeline directory
pipeline_directory=$PIPELINE_DIRECTORY

# Compress all files in most_recent folder
gzip -f ${pipeline_directory}/outputs/most_recent/*.json
