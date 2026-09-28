#!/bin/bash

set -e

# Local pipeline directory
pipeline_directory=$PIPELINE_DIRECTORY

# Extract filenames to copy
all_files_to_copy=$@

# Date for indexing
date=$(date --utc +"_%Y%m%dT%H%M%S")
echo $date

# Set up input directory
input_directory="${MOST_RECENT}"

# Set up output directory
output_directory="${pipeline_directory}/upload"
mkdir -p $output_directory

# remove any previous gz and json files in upload
rm -f ${output_directory}/*.gz
rm -f ${output_directory}/*.json

# Decompress and recompress files to upload directory with unique datetime
for eachfile in $all_files_to_copy
do
    if [[ $eachfile == *".geojson.gz"* ]]; then
        file_name=${eachfile%".geojson.gz"}
        echo $file_name.geojson
        gzip -dcf ${input_directory}/${eachfile} >${output_directory}/${file_name}${date}.geojson
        gzip -f ${output_directory}/${file_name}${date}.geojson

    elif [[ $eachfile == *".json.gz"* ]]; then
        file_name=${eachfile%".json.gz"}
        echo $file_name.json
        gzip -dcf ${input_directory}/${eachfile} >${output_directory}/${file_name}${date}.json
        gzip -f ${output_directory}/${file_name}${date}.json

    elif [[ $eachfile == *".yaml.gz"* ]]; then
        file_name=${eachfile%".yaml.gz"}
        echo $file_name.yaml
        gzip -dcf ${input_directory}/${eachfile} >${output_directory}/${file_name}${date}.yaml
        yaml_file=${output_directory}/${file_name}${date}.yaml
        # Leave the metadata yaml unzipped as the next step needs to correct the unique filenames

    fi
done

# Correct the filenames inside the metadata yaml file
echo "Correcting unique filenames in metadata yaml"
for eachfile in $all_files_to_copy
do
    if [[ $eachfile == *".geojson.gz"* ]]; then
        file_name=${eachfile%".geojson.gz"}
        echo $file_name${date}.geojson
        replace_command='s/'${file_name}'.geojson/'${file_name}${date}'.geojson/g'
        sed -i -e ${replace_command} ${yaml_file}

    elif [[ $eachfile == *".json.gz"* ]]; then
        file_name=${eachfile%".json.gz"}
        echo $file_name${date}.json
        replace_command='s/'${file_name}'.json/'${file_name}${date}'.json/g'
        sed -i -e ${replace_command} ${yaml_file}
    
    fi
done

# Re-zip the corrected metadata yaml file
gzip -f ${yaml_file}
