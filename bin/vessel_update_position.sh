# !/bin/bash

set -e

# The purpose of this script is to obtain the vessel (SDA) latest
# position and insert it into the required csv file

#TODO: get real positions
# Extract lat and long from arguments
vessel_lat=-55.0811
vessel_lon=-51.8750

# Write lat and long to output file
echo 'Updating vessel position'
echo 'Name,Lat,Long,Source,Destination' > ${VESSEL_POSITION_OUTPUT_FULLPATH}
echo $VESSEL_NAME,$vessel_lat,$vessel_lon,X, >> ${VESSEL_POSITION_OUTPUT_FULLPATH}
