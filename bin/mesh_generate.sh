#!/bin/bash

set -e

# Symlinking necessary, because the config files specify their resource paths relative to 
# a directory called 'datastore'. Search an environment config for 'folder' to
# see an example.
ln -s ${DATASTORE} ./datastore

# Create the mesh
echo "Generating mesh: "${OUTPUT_FILENAME}
create_mesh ${MESH_CONFIG_FULLPATH} -o ${OUTPUT_DIRECTORY}/${OUTPUT_FILENAME}

# Copy file into checkpoint directory, in case a partial pipeline is run later
cp ${OUTPUT_DIRECTORY}/${OUTPUT_FILENAME} ${CHECKPOINT_DIRECTORY}/${OUTPUT_FILENAME}

# Remove the symlink safely
unlink ./datastore