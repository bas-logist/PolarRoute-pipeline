import os
import gzip
import shutil

LIST_OF_FILES = os.getenv("LIST_OF_FILES")
INPUT_DIRECTORY = os.getenv("INPUT_DIRECTORY")
METADATA_FILENAME = os.getenv("METADATA_FILENAME")
OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY") 
OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME")

def main():
    """
    Get a list of the files we need to upload.
    Store it in a file of its own, for later pipeline steps 
    to access.
    """
    # Make a list of files we want to upload
    with open(f"{INPUT_DIRECTORY}/{LIST_OF_FILES}") as f:
        output_filelist = f.read().splitlines()
    output_filelist.append(f"{INPUT_DIRECTORY}/{METADATA_FILENAME}")

    # Clean out already-existing files from this directory
    if os.path.exists(f"{OUTPUT_DIRECTORY}/{OUTPUT_FILENAME}"):
        os.remove(f"{OUTPUT_DIRECTORY}/{OUTPUT_FILENAME}")

    # Output the filelist to a file, so next pipeline steps can access it
    with open(f"{OUTPUT_DIRECTORY}/{OUTPUT_FILENAME}", "w") as list_file:
        list_file.write("\n".join(map(str, output_filelist)))

if __name__ == "__main__":
    main()