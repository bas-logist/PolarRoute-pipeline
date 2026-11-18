#!/bin/bash

# Substitute the current year into GEBCO_URL_PATTERN to create this years' download link
# Download the GEBCO file with some leeway for retries

# Activate virtual environment
source ${ENV_ACTIVATE_PATH}

# Get the current date
current_year=$(date +%Y)

# wget retries and timeouts
retries=3
timeout=20

# Set source of files to retrieve
download_url=$(echo "$GEBCO_URL_PATTERN" | sed "s/CURRENTYEAR/$current_year/g")
echo Preparing to download GEBCO data from: $download_url

output_filename=${OUTPUT_FILENAME_PREFIX}_${current_year}.nc
echo Preparing to download GEBCO data to path: ${OUTPUT_DIRECTORY}/${output_filename} 

# Retrieve the files
if ! wget -r -nv -nc -nd -np -nH --tries=${retries} --timeout=${timeout} -e robots=off "${download_url}" \
-P ${OUTPUT_DIRECTORY}/ -O ${output_filename}; then
    echo GEBCO data file not downloaded from ${download_url} to ${OUTPUT_DIRECTORY}/${output_filename}
fi

