#!/bin/bash

set -e

# Activate virtual environment
source ${ENV_ACTIVATE_PATH}

# Extract names of files we need to prepare for upload, to an array
readarray -t all_files_to_copy < ${INPUT_DIRECTORY}/${FILE_LIST}

# Move metadata to staging
echo "Copy metadata from: "${INPUT_DIRECTORY}/${METADATA_FILENAME}" to: "${OUTPUT_DIRECTORY}/${METADATA_FILENAME}

cp ${INPUT_DIRECTORY}/${METADATA_FILENAME} ${OUTPUT_DIRECTORY}/${METADATA_FILENAME}

# Send mesh files to staging
for eachfile in ${all_files_to_copy[@]}
do
    #make sure to get the zipped copy not the unzipped one
    eachfile=${eachfile}".gz"
    base_name=$(basename ${eachfile})
    echo "Copy mesh file from: "${eachfile}" to: "${OUTPUT_DIRECTORY}/${base_name}
    cp ${eachfile} ${OUTPUT_DIRECTORY}/${base_name}
done
