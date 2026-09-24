# !/bin/bash

set -e

# Extract mesh name from name of mesh file
mesh_output=$1
mesh_output_file=$(basename $mesh_output)
mesh_name=${mesh_output_file%".mesh.json"}

# Extract vessel name from name of config file
vessel_config=$2
vessel_config_file=$(basename $vessel_config)
vessel_name=${vessel_config_file%".config.json"}

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Where to source and store the most_recent meshes
input_directory="${PIPELINE_DIRECTORY}/inputs"
output_directory="${PIPELINE_DIRECTORY}/outputs/${mesh_name}_${vessel_name}/${date}"
mkdir -p $output_directory

# Set up log file names
log_directory="${PIPELINE_DIRECTORY}/logs/${mesh_name}_${date}"

### Run PolarRoute
# Build mesh done externally so just copy it over
cp $mesh_output $output_directory/

# Simulate vehicle
echo "Simulating $vessel_name vessel for $mesh_name"
add_vehicle ${vessel_config} ${output_directory}/${mesh_name}.mesh.json \
            -o ${output_directory}/${mesh_name}_${vessel_name}.vessel.json \
            >> ${log_directory}.out \
            2>>${log_directory}.err

# Copy output back to most recent folder
cp ${output_directory}/${mesh_name}_${vessel_name}.vessel.json \
   ${PIPELINE_DIRECTORY}/outputs/most_recent/${mesh_name}_${vessel_name}.vessel.json
