#!/bin/bash

set -e

# Compress all files in most_recent folder
gzip -f ${MOST_RECENT}/outputs/most_recent/*.json
gzip -f ${MOST_RECENT}/outputs/most_recent/*.geojson
