#!/bin/bash

set -e

# Get absolute path of pipeline directory and scripts directory
pipeline_directory=$PIPELINE_DIRECTORY
scripts_directory=$SCRIPTS_DIRECTORY
upload_directory=$PIPELINE_DIRECTORY/upload/

# Allow time for previous files written to disk
sleep 5

script=metadata_siis.py
vessel=SDA
all_files_list=""


# For geojson regions add files
for found in $(find ${upload_directory} -iname amsr_*_${vessel}.vessel_???????????????.geojson.gz ); 
do
    all_files_list=${all_files_list}" ${found}"
    echo ${found}
done

python $scripts_directory/$script $all_files_list
