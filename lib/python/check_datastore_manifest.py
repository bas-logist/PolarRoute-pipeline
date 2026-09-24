import os
import hashlib
from datetime import datetime

# Get environment variables provided from flow.cylc
OUTPUTS = os.environ.get("OUTPUTS")
DATASTORE = os.environ.get("DATASTORE")
DATASTORE_MANIFEST_DEPTH = os.environ.get("DATASTORE_MANIFEST_DEPTH") 

# Determine datastore manifest checksum location
datastore_checksum_manifest = os.path.join(OUTPUTS, 'most_recent', '.datastore.md5')

# If there is no previous datastore manifest then there is no choice but to
# allow the pipeline to continue.
if not os.path.exists(datastore_checksum_manifest):
    manifest = False
else:
    manifest = True

# Determine how deep to manifest
if DATASTORE_MANIFEST_DEPTH is None:
    DATASTORE_MANIFEST_DEPTH = 5

# Determine of the datastore has been updated with new files
directories_to_check = [['currents', 'duacs-nrt', 'global'],
#                        ['wave'    , 'era5'     , 'daily'],  # temporarily removed
#                        ['wind'    , 'era5'     , 'daily'],  # temporarily removed
                        ['sic'     , 'amsr2'    , 'north'],
                        ['sic'     , 'amsr2'    , 'south']]

def calculate_checksum(filenames):
    hash = hashlib.md5()
    for file in filenames:
        hash.update(open(file, 'rb').read())
    return hash.hexdigest()

def main():
    # List the n most recent files for each of the check directories
    all_filepaths = []
    for directory in directories_to_check:
        dirname = os.path.join(*directory)
        files = [ os.path.join(DATASTORE, dirname, fname) for fname in os.listdir(os.path.join(DATASTORE, dirname)) ]
        files.sort(key=os.path.getmtime)
        files = files[-(int(DATASTORE_MANIFEST_DEPTH)):]
        all_filepaths += files

    manifest_checksum = calculate_checksum(all_filepaths)

    if manifest:
        with open(datastore_checksum_manifest, 'r') as m:
            previous_manifest = m.read()
        if previous_manifest == manifest_checksum:
            raise RuntimeError("WARNING:"+str(datetime.now())+
                            ":pipeline:Task: Check Datastore Manifest Restriction, "+
                            "NO NEW DATA PRODUCTS IN DATASTORE")
        else:
            with open(datastore_checksum_manifest, 'w') as n:
                n.write(manifest_checksum)
