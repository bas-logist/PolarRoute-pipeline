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
echo 'Name,Lat,Long,Source,Destination' > ${OUTPUTS}/configs/waypoints/$csv_output_file
echo $VESSEL_NAME,$vessel_lat,$vessel_lon,X, >> ${OUTPUTS}/configs/waypoints/$csv_output_file
