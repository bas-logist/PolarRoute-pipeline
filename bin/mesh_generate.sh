#!/bin/bash

set -e

# Local pipeline directory
pipeline_directory=$PIPELINE_DIRECTORY

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Extract config name from name of config file
mesh_config=$1
mesh_config_file=$(basename $mesh_config)
mesh_name=${mesh_config_file%".config.json"}

# Set up output directory
output_directory="${pipeline_directory}/outputs"
output_name="${mesh_name}.mesh.json"
mkdir -p $output_directory/${mesh_name}/${date}


# Set up log file names
log_directory="${pipeline_directory}/logs"

# Create the mesh
echo "Generating $mesh_name mesh"
create_mesh ${mesh_config} -o ${output_directory}/${mesh_name}/${date}/${output_name} \
            >> ${log_directory}/${mesh_name}_${date}.out \
            2>> ${log_directory}/${mesh_name}_${date}.err

# Copy file into most_recent directory to be picked up by next script
mkdir -p ${pipeline_directory}/outputs/most_recent
cp ${output_directory}/${mesh_name}/${date}/${output_name} ${output_directory}/most_recent/${output_name}
