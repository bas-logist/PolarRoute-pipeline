# !/bin/bash

set -e

# The purpose of this script is to obtain the vessel (SDA) latest
# position and insert it into the required csv file

#TODO: get real positions
# Extract lat and long from arguments
vessel_lat=-55.0811
vessel_lon=-51.8750

# Extract output filename
csv_output_file=${VESSEL_NAME}_position_latest.csv

# Write lat and long to output file
echo 'Updating vessel position'
mkdir -p ${WAYPOINT_DYNAMIC_CONFIGS}
echo 'Name,Lat,Long,Source,Destination' > ${WAYPOINT_DYNAMIC_CONFIGS}/$csv_output_file
echo $VESSEL_NAME,$vessel_lat,$vessel_lon,X, >> ${WAYPOINT_DYNAMIC_CONFIGS}/$csv_output_file
