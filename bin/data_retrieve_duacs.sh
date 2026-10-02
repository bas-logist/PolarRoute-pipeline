#!/bin/bash

# Download task logic:
# 1. Try to download whatever is available right now.
# 2. If a download fails then make it clear that the download
#    failed but carry on with the task.
# 3. If the task fails for any other  reason then this should
#    still  raise the appropriate errors and  halt if needed.
# 4. If any new  data is downloaded then  this should trigger
#    re-generation  of the  mesh(es),  which  is  handled  by
#    'check_datastore_manifest'.

set -e

# Create the output dir if it doesn't exist
mkdir -p "${OUTPUT_DIRECTORY}"

# Date for file formatting
current_date=$(date --utc +%Y-%m-%d)

# For each required date
for ((i = 0; i <= 3; i++)); do
    originaldate=$(date -d "$current_date -$i days" +%Y%m%d)
    date=$(date -d "$current_date -$i days" +%Y-%m-%d)
    echo "${date}"
    originalfilename="${OUTPUT_DIRECTORY}/${DUACS_ORIGINAL_PREFIX}_${originaldate}_${originaldate}.nc"
    filename="${OUTPUT_DIRECTORY}/${DUACS_PREFIX}_${date}.nc"

    # Only download if not present in the datastore
    if (test -f "$originalfilename") || (test -f "$filename"); then
        echo "$(basename "$filename") or $(basename "$originalfilename") already exists!"
    else
        # Download the data
        if ! copernicusmarine get \
            --dataset-id cmems_obs-sl_glo_phy-ssh_nrt_allsat-l4-duacs-0.125deg_P1D \
            --filter "*${DUACS_ORIGINAL_PREFIX}_${originaldate}*" \
            --output-directory "${OUTPUT_DIRECTORY}" \
            --no-directories \
            --disable-progress-bar \
            --response-fields "file_path" \
            --log-level INFO
        then
            echo DUACS global data file not found: "${filename}"
        fi
    fi
done
