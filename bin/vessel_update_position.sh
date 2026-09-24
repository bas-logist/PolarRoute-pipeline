# !/bin/bash

set -e

# The purpose of this script is to obtain the vessel (SDA) latest
# position and insert it into the required csv file

# Get absolute path of pipeline directory
pipeline_directory=$PIPELINE_DIRECTORY

# Extract lat and long from arguments
vessel_lat=-55.0811
vessel_lon=-51.8750

# Extract vessel name
vessel_name=SDA

# Extract output filename
csv_output_file=sda_position_latest.csv


# Write lat and long to output file
echo 'Updating vessel position'
echo 'Name,Lat,Long,Source,Destination' > $pipeline_directory/configs/waypoints/$csv_output_file
echo $vessel_name,$vessel_lat,$vessel_lon,X, >> $pipeline_directory/configs/waypoints/$csv_output_file
