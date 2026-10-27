#!/bin/bash

# This script is the final step required to transfer data from shoreside
# to shipside via the siis-data-transfer. Prior to this step, the 'prepare
# all' step will generate/copy all relevant files to the local 'upload'
# directory.
# This script will take the file(s) prepared in the 'upload' directory and
# actually copy them into the /data/siis/data/xfer/... directories. In
# doing so the transfer will be initiated. The siis-data-transfer code will
# delete files from .../xfer/... once they have been synchronised over to
# shipside.

set -e

# Get absolute path of the pipeline, upload, and push directories
pipeline_directory=$PIPELINE_DIRECTORY
upload_directory=${PIPELINE_DIRECTORY}/upload
push_directory=${PIPELINE_DIRECTORY}/push

# Define specific xfer product directories
siis_MEVJ_dir="siis.meshiphi-json.s"      # (ME)shiphi with (V)essel (J)SON
siis_OPRM_dir="siis.polarroute-meta.y"    # (O)perational (P)olar(R)oute (M)etadata

# Check that all xfer product directories exist
if !([ -d "$push_directory/$siis_MEVJ_dir" ] && 
     [ -d "$push_directory/$siis_OPRM_dir" ] ); then
    echo Unable to 'push' upload as one or more xfer product directories does not exist
    exit 1
fi

# Copy files to correct directory dependant on file type
find $upload_directory/ -name "*.json.gz" -exec cp {} ${push_directory}/${siis_MEVJ_dir}/ \;
find $upload_directory/ -name "*.yaml.gz" -exec cp {} $push_directory/$siis_OPRM_dir/ \;
