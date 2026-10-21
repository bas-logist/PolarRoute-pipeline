# !/bin/bash

# N.B. 'export_mesh' is from the MeshiPhi tool, so everything must
# be set up in a MeshiPhi compatible way

set -e

# MeshiPhi tools prepend the current workdir to the -v path, so we need
# to make symlinks instead of using full paths directly
ln -s ${MESH_FULLPATH} ./${MESH_NAME}

# Export meshes as GeoJSON
echo "Exporting mesh into GeoJSON"
export_mesh -v ./${MESH_NAME} \
            -o ${OUTPUT_GEOJSON}

# Safely remove symlink now the work is done
unlink ./${MESH_NAME}