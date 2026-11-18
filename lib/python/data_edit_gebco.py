import os
import xarray as xr
import logging
from pathlib import Path
import sys

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INPUT_FULLPATH = os.getenv("INPUT_FULLPATH")
OUTPUT_FULLPATH = os.getenv("OUTPUT_FULLPATH")
KEEP_VARS = os.getenv("KEEP_VARS")


def open_dataset_with_error_handling(file_path: str, file_descriptor: str):
    """
    Just open the provided filepath with xarray and return it as a dataset.
    Log potential errors.
    """
    try:
        output = xr.open_dataset(file_path)
        return output
    except FileNotFoundError as e:
        logger.critical(f"GEBCO {file_descriptor} file does not exist: {file_path}.\
                        Please address this to resume pipeline functioning")
        logger.critical(e)
        sys.exit()
    except ValueError as e:
        logger.critical(f"GEBCO {file_descriptor} file is not a valid NC file: {file_path}.\
                        Please address this to resume pipeline functioning")
        logger.critical(e)
        sys.exit


def main():
    """
    GEBCO netCDF files need editing before use, as MeshiPhi can't handle 'extra' variables.
    If a GEBCO processed file doesn't already exist, open the raw netCDF dataset, and
    drop unnecessary values from the dataset. Write the final result to a file.
    If a GEBCO processed file DOES exist, check that it only has the desired variables.
    Raise warnings otherwise.
    """
    # Check an output doesn't exist for this year already. If it does and 
    # passes sense checks around columns, then skip it.
    output_file = Path(OUTPUT_FULLPATH)
    if output_file.is_file():
        logger.info(f"A GEBCO processed file {output_file} already exists,\
                     checking that it doesn't have unexpected values")
        output_dataset = open_dataset_with_error_handling(OUTPUT_FULLPATH, "processed")
        output_dataset_vars = [i.name for i in output_dataset.data_vars]
        if set(output_dataset_vars) != set(KEEP_VARS):
            # the processed file is missing necessary columns, or has invalid ones
            logger.critical("GEBCO processed file has invalid columns. " \
            "Please address this to resume pipeline functioning")
            sys.exit()
    else:
        # Processed output doesn't exist yet - create it by dropping columns from the raw input
        dataset = open_dataset_with_error_handling(INPUT_FULLPATH, "raw")
        dataset_vars = [i.name for i in dataset.data_vars]
        remove_vars = list(set(dataset_vars) - set(KEEP_VARS))
        dataset = dataset.drop_vars(remove_vars)
        dataset.to_netcdf(OUTPUT_FULLPATH)

if __name__ == "__main__":
    main()
