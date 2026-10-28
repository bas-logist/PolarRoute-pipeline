#!/bin/bash

set -e

target_fullpath=${TARGET_FILE_DIRECTORY}/${MATCH_STRING}
output_fullpath=${OUTPUT_DIRECTORY}/${OUTPUT_FILENAME}

for f in ${target_fullpath}; do cat "$f"; done > ${output_fullpath}