# !/bin/bash

set -e

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Symlinking necessary, because the config files specify their resource paths relative to 
# a directory called 'datastore'. Search an environment config for 'folder' to
# see an example.
ln -s ${DATASTORE} ./datastore

### Run PolarRoute
# Simulate vehicle
echo "Simulating $vessel_name vessel for $mesh_name"
add_vehicle ${VESSEL_CONFIG_FULLPATH} ${REGION_MESH_FULLPATH} \
            -o ${OUTPUT_DIRECTORY}/${OUTPUT_FILENAME}

# Copy the final file to the 'checkpoint' directory, in case we want to
# skip steps on a future pipeline
cp ${OUTPUT_DIRECTORY}/${OUTPUT_FILENAME} ${CHECKPOINT_DIRECTORY}/${OUTPUT_FILENAME}

# Remove symlink safely
unlink ./datastore