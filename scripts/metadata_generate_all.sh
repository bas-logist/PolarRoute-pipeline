#!/bin/bash

set -e

# Get absolute path of pipeline, most_recent and scripts directories
pipeline_directory=$PIPELINE_DIRECTORY
scripts_directory=$SCRIPTS_DIRECTORY
most_recent_directory=$PIPELINE_DIRECTORY/outputs/most_recent

# Allow time for previous files written to disk
sleep 5

# Detect all of the .json  files in the most_recent directory
# and determine their plain region names.
region_files=($(ls $most_recent_directory/*.json))
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

script=metadata_generate.py
vessel=SDA
options="-dmisl"
all_files_list=""

# For json regions add files
for region in "${json_regions[@]}"
do
    all_files_list=${all_files_list}" ${pipeline_directory}/outputs/most_recent/amsr_${region}.mesh.json" # add environment meshes
    all_files_list=${all_files_list}" ${pipeline_directory}/outputs/most_recent/amsr_${region}_${vessel}.vessel.json" # add vessel meshes
done

python $scripts_directory/$script $options $all_files_list
