# !/bin/bash

set -e

# Get the vessel origin
origin_input_file=${WAYPOINT_DYNAMIC_CONFIGS}/${VESSEL_NAME}_position_latest.csv
origin=$(head --lines=2 ${origin_input_file} | tail --lines=1)

# Get the destinations input
destinations_input_file=${WAYPOINT_STATIC_CONFIGS}/standard_destinations.csv

# Set output file
output_file=${WAYPOINT_DYNAMIC_CONFIGS}/${WAYPOINT_FILE}

# Write waypoints file
echo 'Writing waypoints file'
cp $destinations_input_file $output_file
echo $origin >> $output_file

cat ${output_file}
