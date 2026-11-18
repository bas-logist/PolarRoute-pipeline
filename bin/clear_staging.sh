#!/bin/bash

set -e

# Activate virtual environment
source ${ENV_ACTIVATE_PATH}

# Just delete contents of staging
rm -r ${INPUT_DIRECTORY}/*