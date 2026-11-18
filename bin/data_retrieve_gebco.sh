#!/bin/bash

# Substitute the current year into GEBCO_URL_PATTERN to create this years' download link
# Download the GEBCO file with some leeway for retries

# Activate virtual environment
source ${ENV_ACTIVATE_PATH}

# Get the current date
current_year=$(date +%Y)

# Skip downloading if we already have a processed GEBCO this year
processed_gebco=${PROCESSED_OUTPUT_DIRECTORY}/${PROCESSED_OUTPUT_FILENAME_PREFIX}_${current_year}.nc
if test -f ${processed_gebco}; then
    echo "A processed GEBCO file for this year already exists at "${processed_gebco}"- skipping download"
    exit(0)
fi

# wget retries and timeouts
retries=3
timeout=20

# Set source of files to retrieve
download_url=$(echo "$GEBCO_URL_PATTERN" | sed "s/CURRENTYEAR/$current_year/g")
echo Preparing to download GEBCO data from: $download_url

raw_output_filename=${RAW_OUTPUT_FILENAME_PREFIX}_${current_year}.nc
echo "Preparing to download GEBCO data to path: "${RAW_OUTPUT_DIRECTORY}"/"${raw_output_filename} 

# Retrieve the files
if ! wget -r -nv -nc -nd -np -nH --tries=${retries} --timeout=${timeout} -e robots=off "${download_url}" \
-P ${RAW_OUTPUT_DIRECTORY}/ -O ${output_raw_filename}; then
    echo "GEBCO data file for "${current_year}" failed to download from "${download_url}" to "${RAW_OUTPUT_DIRECTORY}"/"${raw_output_filename}
fi

