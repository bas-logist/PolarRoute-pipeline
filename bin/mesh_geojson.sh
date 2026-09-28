# !/bin/bash

set -e

# Get absolute path of pipeline directory and scripts directory
pipeline_directory=$PIPELINE_DIRECTORY

# Extract mesh name from name of mesh file
mesh_output=$1
mesh_output_file=$(basename $mesh_output)
mesh_name=${mesh_output_file%".json"}

# Work within source file directory
directory_name=$( echo $(readlink -f $1) | rev | cut --complement -d '/' -f 1 | rev )

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Set up log file names
log_directory="${pipeline_directory}/logs/${mesh_name}_${date}"

## Export meshes
# GeoJSON
echo "Exporting mesh into GeoJSON"
export_mesh -v ${directory_name}/${mesh_name}.json GEOJSON \
            -o ${directory_name}/${mesh_name}.geojson \
            >> ${log_directory}.out \
            2>>${log_directory}.err
