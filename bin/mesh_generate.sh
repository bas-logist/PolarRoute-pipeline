#!/bin/bash

set -e

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Extract config name from name of config file
mesh_config_file_only=$(basename ${MESH_CONFIG_FULLPATH})
mesh_name=${mesh_config_file_only%".config.json"}

# Set up output directory
output_dir = "${OUTPUTS}/${mesh_name}/${date}"
mkdir -p ${output_dir}

output_name="${mesh_name}.mesh.json"

# Necessary because MeshiPhi 'create_mesh' prepends current workdir to every 'folder' in 
# the mesh configs, even if you provide a full path
ln -s ${DATASTORE} ./datastore

# Create the mesh
echo "Generating $mesh_name mesh"
create_mesh ${MESH_CONFIG_FULLPATH} -o ${output_dir}/${output_name}

# Copy file into most_recent directory to be picked up by next script
mkdir -p ${MOST_RECENT}
cp ${output_dir}/${output_name} ${MOST_RECENT}/${output_name}

# Remove the symlink safely
unlink ./datastore