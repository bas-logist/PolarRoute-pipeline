#!/bin/bash

set -e

copernicus_credentials_dir="$HOME/.copernicusmarine"
copernicus_credentials_file="$copernicus_credentials_dir/.copernicusmarine-credentials"

# CopernicusMarine Credentials - use environment variables as priority, then copernicus credentials file format, fall back on old user and password files
if [[ -n "$COPERNICUSMARINE_SERVICE_USERNAME" ]] && [[ -n "$COPERNICUSMARINE_SERVICE_PASSWORD" ]] || [ -f "$copernicus_credentials_file" ]; then
    copernicusmarine login --check-credentials-valid
elif [ -f "$copernicus_credentials_dir/user" ] && [ -f "$copernicus_credentials_dir/password" ]; then
    COPERNICUS_USER=$(< "${HOME}"/.copernicusmarine/user)
    COPERNICUS_PASSWORD=$(< "${HOME}"/.copernicusmarine/password)

    copernicusmarine login \
    --username "$COPERNICUS_USER" \
    --password "$COPERNICUS_PASSWORD"
else
    echo "ERROR - Username and password not found for copernicusmarine. Please log in using copernicusmarine login \
        or set COPERNICUSMARINE_SERVICE_USERNAME and COPERNICUSMARINE_SERVICE_PASSWORD environment variables."
    exit 1
fi

