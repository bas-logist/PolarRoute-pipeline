# !/bin/bash

set -e

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Construct Route and output a route GeoJSON and mesh
echo "Constructing ${ROUTE_NAME} optimised route for $vessel_name in $mesh_name"
optimise_routes ${ROUTE_CONFIG_FULLPATH} ${MESH_INPUT_FULLPATH} \
                ${WAYPOINT_CONFIG_FULLPATH} \
                -p -o ${OUTPUT_FILE_FULLPATH}
