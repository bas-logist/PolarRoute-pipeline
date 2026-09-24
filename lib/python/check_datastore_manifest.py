import os
import hashlib
from datetime import datetime

# Find location of script and run all commands from there
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(BASE_DIR)

# Determine root of pipeline directory
pipeline_directory = os.getenv("PIPELINE_DIRECTORY")

# Determine datastore manifest checksum location
datastore_checksum_manifest = os.path.join(pipeline_directory, 'outputs', 'most_recent', '.datastore.md5')

# If there is no previous datastore manifest then there is no choice but to
# allow the pipeline to continue.
if not os.path.exists(datastore_checksum_manifest):
    manifest = False
else:
    manifest = True

# Determine the datastore
datastore = os.getenv("APPLICATION_DATASTORE")
if datastore is None:
    datastore = os.path.join(pipeline_directory, 'datastore')
else:
    if datastore[:2] == './':
        datastore = os.path.join(pipeline_directory, datastore[2:])
    elif datastore[0] != '/':
        datastore = os.path.join(pipeline_directory, datastore)
    else:
        pass

# Determine how deep to manifest
manifest_depth = os.getenv("DATASTORE_MANIFEST_DEPTH")
if manifest_depth is None:
    manifest_depth = 5

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

# List the n most recent files for each of the check directories
all_filepaths = []
for directory in directories_to_check:
    dirname = os.path.join(*directory)
    files = [ os.path.join(datastore, dirname, fname) for fname in os.listdir(os.path.join(datastore, dirname)) ]
    files.sort(key=os.path.getmtime)
    files = files[-(int(manifest_depth)):]
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
