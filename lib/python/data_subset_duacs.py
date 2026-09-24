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

# Determine root of pipeline directory
pipeline_directory = os.getenv("PIPELINE_DIRECTORY")

# Determine duacs data directory
duacs_directory = os.path.join(pipeline_directory, 'datastore', 'currents', 'duacs-nrt', 'global')


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


def check_duacs_directory(duacsdir):
    """
    Check the duacs directory to see if there are any original files that need
    to be subsetted. Make a list of those files
    """
    files_to_subset = []
    files_to_subset = glob.glob(os.path.join(duacsdir, "nrt_global_allsat_phy_l4_*.nc"))
    
    return files_to_subset


def subset_duacs_files(filepaths: list):
    """
    For each filepath, create the desired subsetted NetCDF file.
    """
    for infilepath in filepaths:
        infiledate = os.path.basename(infilepath).split \
            ('nrt_global_allsat_phy_l4_')[-1].split('_')[0]
        outfiledate = infiledate[:4]+'-'+infiledate[4:6]+'-'+infiledate[6:]
        outfilepath = os.path.join(os.path.dirname(infilepath), 'duacs_nrt_'+outfiledate+'.nc')
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
        
    parser = argparse.ArgumentParser(description=DESCRIPTION + ' v' + VERSION)
    parser.add_argument("-d", "--duacs-directory", help="Override default duacs directory, default="+duacs_directory, action="store", dest='duacsdir', default=duacs_directory)
    parser.add_argument("-k", "--keep-original", help="Keep the original input file(s)", action="store_true", dest='keep', default=False)
    args = parser.parse_args()


    # Now kick off main

    duacsdir = check_directory_exists(args.duacsdir)
    if duacsdir is not None:
        files_to_subset = check_duacs_directory(duacsdir)
        subset_duacs_files(files_to_subset)
        if not args.keep:
            delete_files(files_to_subset)
    

if __name__ == "__main__":
    main()