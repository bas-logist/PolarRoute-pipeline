# !/bin/bash

set -e

mesh_name = ${MOST_RECENT}/${mesh_name}_${vessel_name}.vessel.json

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Where to store the meshes
output_directory="${OUTPUT_DIRECTORY}/${mesh_name}_${vessel_name}/${date}"
mkdir -p $output_directory

# Construct Route and output a route GeoJSON and mesh
echo "Constructing $route_name optimised route for $vessel_name in $mesh_name"
optimise_routes ${route_config} ${output_directory}/${mesh_name}_${vessel_name}.vessel.json ${waypoints} \
                -p -o ${output_directory}/${mesh_name}_${vessel_name}_${route_name}.route.json

# Copy to most_recent directory
cp ${output_directory}/${mesh_name}_${vessel_name}_${route_name}.route.json \
   ${MOST_RECENT}/${mesh_name}_${vessel_name}_${route_name}.route.json

cp ${output_directory}/${mesh_name}_${vessel_name}_${route_name}.route.geojson \
   ${MOST_RECENT}/${mesh_name}_${vessel_name}_${route_name}.route.geojson