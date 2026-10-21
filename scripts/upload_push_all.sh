#!/bin/bash

# This script is the final step required to transfer data from shoreside
# to shipside via the siis-data-transfer. Prior to this step, the 'prepare
# all' step will generate/copy all relevant files to the local 'upload'
# directory.
# This script will take the file(s) prepared in UPLOAD_DIRECTORY and
# actually copy them into the /data/siis/data/xfer/... directories. In
# doing so the transfer will be initiated. The siis-data-transfer code will
# delete files from .../xfer/... once they have been synchronised over to
# shipside.

set -e

# Define specific xfer product directories
siis_MEVJ_dir="siis.meshiphi-json.s"      # (ME)shiphi with (V)essel (J)SON
siis_MEVG_dir="siis.meshiphi-geojson.s"   # (ME)shiphi with (V)essel (G)EOJSON
siis_OPRM_dir="siis.polarroute-meta.y"    # (O)perational (P)olar(R)oute (M)etadata
siis_metadata_dir="md"                    # SIIS specific metadata files

# Check that all xfer product directories exist
if !([ -d "${PUSH_DIRECTORY}/$siis_MEVJ_dir" ] && 
     [ -d "${PUSH_DIRECTORY}/$siis_MEVG_dir" ] && 
     [ -d "${PUSH_DIRECTORY}/$siis_OPRM_dir" ] &&
     [ -d "${PUSH_DIRECTORY}/$siis_metadata_dir" ]); then
    echo Unable to 'push' upload as one or more xfer product directories does not exist
    exit 1
fi

# Copy files to correct directory dependant on file type
find ${UPLOAD_DIRECTORY}/ -name "*.json.gz" -exec cp {} ${PUSH_DIRECTORY}/${siis_MEVJ_dir}/ \;
find ${UPLOAD_DIRECTORY}/ -name "*.geojson.gz" -exec cp {} ${PUSH_DIRECTORY}/$siis_MEVG_dir/ \;
find ${UPLOAD_DIRECTORY}/ -name "*.yaml.gz" -exec cp {} ${PUSH_DIRECTORY}/$siis_OPRM_dir/ \;
find ${UPLOAD_DIRECTORY}/ -name "*.json" -exec cp {} ${PUSH_DIRECTORY}/$siis_metadata_dir/ \;
