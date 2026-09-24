#!/bin/bash

# Download task logic:
# 1. Try to download whatever is available right now.
# 2. If a download fails then make it clear that the download failed but carry on with the task.
# 3. If the task fails for any other reason then this should still raise the appropriate errors and halt if needed.
# 4. If any new data is downloaded then this should trigger re-generation of the mesh(es), which is handled by
#    'check_datastore_manifest'.

set -e

# Get absolute path of pipeline directory
pipeline_directory=$PIPELINE_DIRECTORY

# Get the current date
current_date=$(date --utc +%Y%m%d)

# Where to save AMSR data
save_directory="$pipeline_directory/datastore/sic/amsr2"

# wget retries and timeouts
retries=3
timeout=20

# Loop to generate the last three days' dates,
# then generate and download a link
for ((i = 1; i <= 3; i++)); do
	# Subtract the days from the current date
	date=$(date -d "$current_date -$i days" +%Y%m%d)
	# Get the year 
	year=$(date -d "$current_date -$i days" +%Y)
	
	# Set source of files to retrieve
	north_file="https://seaice.uni-bremen.de/data/amsr2/asi_daygrid_swath/n6250/netcdf/${year}/asi-AMSR2-n6250-${date}-v5.4.nc"
	south_file="https://seaice.uni-bremen.de/data/amsr2/asi_daygrid_swath/s6250/netcdf/${year}/asi-AMSR2-s6250-${date}-v5.4.nc"

	# Retrieve the files
	if ! wget -r -nv -nc -nd -np -nH --tries=${retries} --timeout=${timeout} -e robots=off "${north_file}" -P $save_directory/north/ &> /dev/null; then
		echo AMSRv2 north data file not found: ${north_file}
	fi
	if ! wget -r -nv -nc -nd -np -nH --tries=${retries} --timeout=${timeout} -e robots=off "${south_file}" -P $save_directory/south/ &> /dev/null; then
		echo AMSRv2 south data file not found: ${south_file}
	fi
	
done
