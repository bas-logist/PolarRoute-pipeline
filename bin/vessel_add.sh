# !/bin/bash

set -e

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Necessary because MeshiPhi config files give the path from a 'datastore' directory in the
# current working directory
ln -s ${DATASTORE} ./datastore

### Run PolarRoute
# Simulate vehicle
echo "Simulating $vessel_name vessel for $mesh_name"
add_vehicle ${VESSEL_CONFIG_FULLPATH} ${REGION_MESH_FULLPATH} \
            -o ${OUTPUT_FILE_FULLPATH}

# Remove symlink
unlink ./datastore