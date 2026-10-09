import os
import logging
import argparse

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAXIMUM_LOGFILE_QTY = 100
MAXIMUM_LOGDIR_SIZE = 2*1024*1024*1024 #Size in bytes
DESCRIPTION = "Check and manage the pipeline logs directory"
VERSION = "0.0.1"

# Determine root of pipeline directory
pipeline_directory = os.getenv("PIPELINE_DIRECTORY")

# Determine the logs directory
logs_directory = os.path.join(pipeline_directory, "logs")


def check_directory_exists(input_directory: list):
    """
    Check that the logs directory exists
    """
    output_directory = None

    if not os.path.isdir(input_directory):
        logger.warning("Directory %s is not a directory (or doesn't exist).", input_directory)
        logger.warning("No logs management will be performed.")
    else:
        output_directory = input_directory

    return output_directory


def check_logs_dir(logsdir, quantity, size, newest):
    """
    Check the files of the logs directory and make a list of
    all files that exceed the maximum quantity or overall size.
    """
    files_to_delete = []
    running_file_count = 0
    running_size_bytes = 0
    name_of_dir = logsdir
  
    # Storing list of all files 
    # in the given directory in list_of_files 
    list_of_files = filter( lambda x: os.path.isfile 
                       (os.path.join(name_of_dir, x)), 
                        os.listdir(name_of_dir) ) 

    # Sort list of file names by modified time; newest first
    # if the 'newest' flag is True then the list is ordered the opossite way
    list_of_files = sorted( list_of_files, 
                        key =  lambda x: os.stat 
                       (os.path.join(name_of_dir, x)).st_mtime, 
                        reverse=(not(newest)))

    # Iterate over sorted list of file names and
    # record all files which fall outside maximum quantity or overall size 
    for name_of_file in list_of_files:
        running_file_count += 1
        running_size_bytes += os.stat(os.path.join(name_of_dir, name_of_file)).st_size
        if running_file_count > quantity or running_size_bytes > size:
            files_to_delete.append(os.path.join(name_of_dir, name_of_file))
    
    return files_to_delete


def delete_files(filepaths: list):
    """
    Delete each file in the list of filepaths provided
    """
    logger.info("Cleaning up logs directory")
    if len(filepaths) == 0:
        logger.info("No log file limits exceeded")
    
    for filepath in filepaths:
        try:
            os.remove(filepath)
            logger.info("Deleting file: %s", str(filepath))
        except Exception as e:
            logger.error("Unable to delete file %s", str(filepath))

def main():
    """
    Manage the pipeline log directory by restricting its maximum size,
    this is achieved by deleting the OLDEST logs when the file quantity or total size is exceeded.
    This entry point relies on $PIPELINE_DIRECTORY being available in the environment
    """
        
    parser = argparse.ArgumentParser(description=DESCRIPTION + ' v' + VERSION)
    parser.add_argument("-q", "--max-quantity", help="Maximum number of files permitted in logs directory", action="store", dest='quantity', default=MAXIMUM_LOGFILE_QTY)
    parser.add_argument("-t", "--max-total-size", help="Maximum total permitted size of the logs directory in bytes", action="store", dest='size', default=MAXIMUM_LOGDIR_SIZE)
    parser.add_argument("-d", "--logs-directory", help="Override default logs directory, deafult= ./logs/", action="store", dest='logsdir', default=logs_directory)
    parser.add_argument("-n", "--newest-first", help="Delete files newest first", action="store_true", dest='newest', default=False)
    args = parser.parse_args()


    # Now kick off main

    logsdir = check_directory_exists(args.logsdir)
    if logsdir is not None:
        files_to_delete = check_logs_dir(logsdir, args.quantity, args.size, args.newest)

        delete_files(files_to_delete)
    

if __name__ == "__main__":
    main()