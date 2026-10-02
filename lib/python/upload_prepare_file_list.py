import os
import gzip
import shutil
from metadata_generate import create_expected_output_filelist

INPUT_DIRECTORY = os.getenv("INPUT_DIRECTORY")
METADATA_FILE_FULLPATH = os.getenv("METADATA_FILE_FULLPATH")
REGIONS_VESSELS = os.getenv("REGIONS_VESSELS")
OUTPUT_FILE_FULLPATH = os.getenv("OUTPUT_FILE_FULLPATH")
LIST_FILENAME = os.getenv("LIST_FILENAME")


def main():
    """
    Get a list of the files we need to upload.
    Store it in a file of its own, for later pipeline steps 
    to access.
    """
    # Make a list of files we want to upload
    output_filelist = create_expected_output_filelist(INPUT_DIRECTORY, REGIONS_VESSELS, compressed=True)
    output_filelist.append(METADATA_FILE_FULLPATH)

    # Remove any central geojson files for some reason
    # Carried over from original 'upload_prepare_all.sh'
    output_filelist = [i for i in output_filelist if "central" and "geojson" not in i]

    # Clean out already-existing files from this directory
    if os.path.exists(OUTPUT_FILE_FULLPATH):
        os.remove(OUTPUT_FILE_FULLPATH)

    # Output the filelist to a file, so next pipeline steps can access it
    with open(OUTPUT_FILE_FULLPATH, "w") as list_file:
        list_file.write("\n".join(map(str, output_filelist)))

if __name__ == "__main__":
    main()