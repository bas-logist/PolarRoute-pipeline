# !/bin/bash

set -e

# Export meshes as GeoJSON
echo "Exporting mesh into GeoJSON"
export_mesh -v ${MESH_NAME} \
            -o ${MESH_GEOJSON}