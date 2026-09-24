import os
import logging
import argparse
import glob
import xarray

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DESCRIPTION = "Create a subset of an original DUACS NetCDF file, selecting only vgos and ugos variables"
VERSION = "0.0.1"


def check_directory_exists(input_directory: list):
    """
    Check that the duacs data directory exists
    """
    output_directory = None

    if not os.path.isdir(input_directory):
        logger.warning("Directory %s is not a directory (or doesn't exist).", input_directory)
        logger.warning("No logs management will be performed.")
    else:
        output_directory = input_directory

    return output_directory


def check_duacs_directory(duacsdir, subset_search_string):
    """
    Check the duacs directory to see if there are any original files that need
    to be subsetted. Make a list of those files
    """
    files_to_subset = []
    files_to_subset = glob.glob(os.path.join(duacsdir, subset_search_string+"*.nc"))
    
    return files_to_subset


def subset_duacs_files(filepaths: list, original_prefix: str, subset_prefix: str):
    """
    For each filepath, create the desired subsetted NetCDF file.
    """
    for infilepath in filepaths:
        infiledate = os.path.basename(infilepath).split(original_prefix + '_')[-1].split('_')[0]
        outfiledate = infiledate[:4]+'-'+infiledate[4:6]+'-'+infiledate[6:]
        outfilepath = os.path.join(os.path.dirname(infilepath), subset_prefix + "_" + outfiledate + '.nc')
        logger.info("Subsetting input file: %s", infilepath)
        logger.info("Creating output file: %s", outfilepath)

        toinclude = ['vgos', 'ugos']
        ds = xarray.open_dataset(infilepath)
        ds[toinclude].to_netcdf(outfilepath, engine='netcdf4')
        


def delete_files(filepaths: list):
    """
    Delete each file in the list of filepaths provided
    """
    logger.info("Removing any original files from duacs directory")
    if len(filepaths) == 0:
        logger.info("No original files to remove")
    
    for filepath in filepaths:
        try:
            os.remove(filepath)
            logger.info("Deleting file: %s", str(filepath))
        except Exception as e:
            logger.error("Unable to delete file %s", str(filepath))


def main():
    """
    Create a subset of an original DUACS NetCDF file, selecting only vgos and ugos variables
    """
    # get environment variables
    # note that I can't get booleans from the flow.cylc hence messing with string cases 
    DATASTORE = os.environ.get("DATASTORE")
    KEEP_ORIGINAL_DUACS = os.environ.get("KEEP_ORIGINAL_DUACS").upper()

    # the string pattern used to identify files that haven't been subsetted yet
    DUACS_ORIGINAL_PREFIX = os.environ.get("DUACS_ORIGINAL_PREFIX")
    # the prefix to attach to subsetted files
    DUACS_SUBSET_PREFIX = os.environ.get("DUACS_SUBSET_PREFIX")

    # Determine duacs data directory
    duacs_directory = os.path.join(DATASTORE, 'currents', 'duacs-nrt', 'global')

    # Find the DUACS directory and subset files which need it
    # Delete files if the config says to
    duacs_directory = check_directory_exists(duacs_directory)
    if duacs_directory is not None:
        files_to_subset = check_duacs_directory(duacs_directory, DUACS_ORIGINAL_PREFIX)
        subset_duacs_files(files_to_subset, DUACS_ORIGINAL_PREFIX, DUACS_SUBSET_PREFIX)
        if KEEP_ORIGINAL_DUACS == "FALSE":
            delete_files(files_to_subset)
    

if __name__ == "__main__":
    main()