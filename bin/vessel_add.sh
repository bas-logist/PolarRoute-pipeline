# !/bin/bash

set -e

# Create fullpaths from environment args provided to the script
region_mesh_fullpath="${OUTPUTS}/most_recent/${MESH_NAME}.mesh.json"
vessel_config_fullpath="${VESSEL_CONFIGS}/${VESSEL_NAME}.config.json"

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Where to store the most_recent meshes
output_directory="${OUTPUTS}/${MESH_NAME}_${VESSEL_NAME}/${date}"
mkdir -p $output_directory

# ?Necessary because MeshiPhi prepends current workdir to every 'folder' in 
# the mesh configs, even if you provide a full path
ln -s ${DATASTORE} ./datastore

### Run PolarRoute
# Build mesh done externally so just copy it over
cp ${region_mesh_fullpath} ${output_directory}/

# Simulate vehicle
echo "Simulating $vessel_name vessel for $mesh_name"
add_vehicle ${vessel_config_fullpath} ${output_directory}/${mesh_name}.mesh.json \
            -o ${output_directory}/${mesh_name}_${vessel_name}.vessel.json

# Copy output back to most recent folder
cp ${output_directory}/${mesh_name}_${vessel_name}.vessel.json \
   ${OUTPUT_DIRECTORY}/most_recent/${mesh_name}_${vessel_name}.vessel.json

# Remove symlink
#unlink ./datastore