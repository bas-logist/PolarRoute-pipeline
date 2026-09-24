# !/bin/bash

set -e

# Get absolute path of pipeline directory
pipeline_directory=$PIPELINE_DIRECTORY

# Get the vessel origin
origin_input_file=$pipeline_directory/configs/waypoints/sda_position_latest.csv
origin=$(head --lines=2 ${origin_input_file} | tail --lines=1)

# Get the destinations input
destinations_input_file=$pipeline_directory/configs/waypoints/standard_destinations.csv

# Set output file
output_file=$pipeline_directory/outputs/most_recent/waypoints.csv

# Write waypoints file
echo 'Writing waypoints file'
cp $destinations_input_file $output_file
echo $origin >> $output_file

cat ${output_file}
