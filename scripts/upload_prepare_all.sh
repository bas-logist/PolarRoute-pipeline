#!/bin/bash

set -e

# Get absolute path of pipeline, most_recent and scripts directories
pipeline_directory=$PIPELINE_DIRECTORY
scripts_directory=$SCRIPTS_DIRECTORY
most_recent_directory=$PIPELINE_DIRECTORY/outputs/most_recent

# Allow time for previous files written to disk
sleep 5

# Detect all of the .json.gz files in the most_recent directory
# and determine their plain region names.
region_files=($(ls $most_recent_directory/*.json.gz))
json_regions=()
for region in "${region_files[@]}"
do
    end_trim=${region#${most_recent_directory}/amsr_}
    region_vessel=$(echo ${end_trim} | cut -d. -f1)
    plain_region=${region_vessel%_SDA*}
    json_regions+=(${plain_region})
done

# Make the plain region lists contain only unique regions
json_regions=($(for reg in "${json_regions[@]}"; do echo "${reg}"; done | sort -u))

echo "json   : ${json_regions[@]}"

script=upload_prepare.sh
vessel=SDA
all_files_list="upload_metadata.yaml.gz"


# For json regions add files
for region in "${json_regions[@]}"
do
    all_files_list=${all_files_list}" amsr_${region}.mesh.json.gz"
    all_files_list=${all_files_list}" amsr_${region}_${vessel}.vessel.json.gz"
done


bash $scripts_directory/$script $all_files_list
