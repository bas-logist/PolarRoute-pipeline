#!/bin/bash

set -e

# Compress all files in most_recent folder
gzip -f ${MOST_RECENT}/*.yaml
