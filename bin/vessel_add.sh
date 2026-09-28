# !/bin/bash

set -e

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Make an output directory for the mesh, and create a 'most recent' location
# to send it to afterwards, if one doesn't already exist
ADD_VEHICLE_OUTPUT_PATH="${OUTPUTS}/${MESH_NAME}_${VESSEL_NAME}/${date}"
mkdir -p $ADD_VEHICLE_OUTPUT_PATH
mkdir -p $MOST_RECENT

# ?Necessary because MeshiPhi prepends current workdir to every 'folder' in 
# the mesh configs, even if you provide a full path
ln -s ${DATASTORE} ./datastore

### Run PolarRoute
# Simulate vehicle
echo "Simulating $vessel_name vessel for $mesh_name"
add_vehicle ${VESSEL_CONFIG_FULLPATH} ${REGION_MESH_FULLPATH} \
            -o ${ADD_VEHICLE_OUTPUT_PATH}/${mesh_name}_${vessel_name}.vessel.json

# Copy output up to the most recent folder
cp ${output_directory}/${REGION_MESH_NAME}_${VESSEL_NAME}.vessel.json \
   ${MOST_RECENT}/${mesh_name}_${vessel_name}.vessel.json

# Remove symlink
#unlink ./datastore