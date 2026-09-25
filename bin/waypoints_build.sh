# !/bin/bash

set -e

# Get the vessel origin
origin_input_file=${OUTPUTS}/configs/waypoints/${VESSEL_NAME}_position_latest.csv
origin=$(head --lines=2 ${origin_input_file} | tail --lines=1)

# Get the destinations input
destinations_input_file=${OUTPUTS}/configs/waypoints/standard_destinations.csv

# Set output file
output_file=${OUTPUTS}/most_recent/waypoints.csv

# Write waypoints file
echo 'Writing waypoints file'
cp $destinations_input_file $output_file
echo $origin >> $output_file

cat ${output_file}
