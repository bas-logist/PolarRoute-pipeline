#!/bin/bash

set -e

# CopernicusMarine Credentials - use environment variables as priority, then copernicus credentials file format, fall back on old user and password files
if [[ -n "$COPERNICUSMARINE_SERVICE_USERNAME" ]] && [[ -n "$COPERNICUSMARINE_SERVICE_PASSWORD" ]] || [ -f "$COPERNICUS_CREDENTIALS_FILE" ]; then
    copernicusmarine login --check-credentials-valid
elif [ -f "$COPERNICUS_FILE_USERNAME" ] && [ -f "$COPERNICUS_FILE_PASSWORD" ]; then
    COPERNICUS_USER=$(< "${COPERNICUS_FILE_USERNAME}")
    COPERNICUS_PASSWORD=$(< "${COPERNICUS_FILE_PASSWORD}")

    copernicusmarine login \
    --username "$COPERNICUS_USER" \
    --password "$COPERNICUS_PASSWORD"
else
    echo "ERROR - Username and password not found for copernicusmarine. Please log in using copernicusmarine login \
        or set COPERNICUSMARINE_SERVICE_USERNAME and COPERNICUSMARINE_SERVICE_PASSWORD environment variables."
    exit 1
fi
