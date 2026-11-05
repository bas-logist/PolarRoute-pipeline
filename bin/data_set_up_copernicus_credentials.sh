#!/bin/bash

set -e

# CopernicusMarine Credentials - use Copernicus credentials file format
if [ -f "$COPERNICUS_FILE_USERNAME" ] && [ -f "$COPERNICUS_FILE_PASSWORD" ]; then
    COPERNICUS_USER=$(< "${COPERNICUS_FILE_USERNAME}")
    COPERNICUS_PASSWORD=$(< "${COPERNICUS_FILE_PASSWORD}")

    # let login force overwrite to a '.copernicusmarine' file, else it will hang at the 'delete file?' prompt
    copernicusmarine login --force-overwrite \
    --credentials-file "$COPERNICUS_FILE_CREDENTIALS" \
    --username "$COPERNICUS_USER" \
    --password "$COPERNICUS_PASSWORD"
else
    echo "ERROR - Username and password not found for copernicusmarine. Please set username and password \
        files."
    exit 1
fi
