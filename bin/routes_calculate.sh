# !/bin/bash

set -e

# Get absolute path of pipeline directory
pipeline_directory=$PIPELINE_DIRECTORY

# Extract mesh name from name of mesh file
mesh_output=$1
mesh_output_file=$(basename $mesh_output)
mesh_name=${mesh_output_file%".vessel.json"}

# Extract vessel name from name of mesh file
vessel_name=$(echo ${mesh_name} | rev | cut -d '_' -f 1 | rev)
# Cut the vessel name from the mesh name
mesh_name=${mesh_name%"_"${vessel_name}}

# Extract route name from name of config file
route_config=$2
route_config_file=$(basename $route_config)
route_name=${route_config_file%".config.json"}

# Human readable variable for waypoints file
waypoints=$3

# Date for indexing
date=$(date --utc +"%Y-%m-%d")

# Where to source and store the most_recent meshes
output_directory="${pipeline_directory}/outputs/${mesh_name}_${vessel_name}/${date}"
mkdir -p $output_directory

# Set up log file names
log_directory="${pipeline_directory}/logs/${mesh_name}_${date}"

# Construct Route and output a route GeoJSON and mesh
echo "Constructing $route_name optimised route for $vessel_name in $mesh_name"
optimise_routes ${route_config} ${output_directory}/${mesh_name}_${vessel_name}.vessel.json ${waypoints} \
                -p -o ${output_directory}/${mesh_name}_${vessel_name}_${route_name}.route.json \
                >> ${log_directory}.out \
                2>>${log_directory}.err

# Copy to most_recent directory outside of date directory
cp ${output_directory}/${mesh_name}_${vessel_name}_${route_name}.route.json \
   ${pipeline_directory}/outputs/most_recent/${mesh_name}_${vessel_name}_${route_name}.route.json

cp ${output_directory}/${mesh_name}_${vessel_name}_${route_name}.route.geojson \
   ${pipeline_directory}/outputs/most_recent/${mesh_name}_${vessel_name}_${route_name}.route.geojson