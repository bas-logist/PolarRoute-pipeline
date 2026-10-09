# !/bin/bash

set -e

# Get the vessel origin
origin=$(head --lines=2 ${VESSEL_ORIGIN_FULLPATH} | tail --lines=1)

# Write waypoints file
echo 'Writing waypoints file'
cp ${WAYPOINT_INPUT_FULLPATH} ${WAYPOINT_OUTPUT_FULLPATH}
echo $origin >> ${WAYPOINT_OUTPUT_FULLPATH}

cat ${WAYPOINT_OUTPUT_FULLPATH}
