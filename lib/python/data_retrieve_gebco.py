import os
from datetime import datetime
from pathlib import Path
import logging
import sys
import requests

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEBCO_URL_PATTERN = os.getenv("GEBCO_URL_PATTERN")
RAW_OUTPUT_FILENAME_PREFIX = os.getenv("RAW_OUTPUT_FILENAME_PREFIX")
PROCESSED_OUTPUT_DIRECTORY = os.getenv("PROCESSED_OUTPUT_DIRECTORY")
PROCESSED_OUTPUT_FILENAME_PREFIX = os.getenv("PROCESSED_OUTPUT_FILENAME_PREFIX")
RAW_OUTPUT_DIRECTORY = os.getenv("RAW_OUTPUT_DIRECTORY")

def download_gebco_for_specified_year(year: str,
                                      gebco_url_pattern: str,
                                      output_filename_prefix: str,
                                      output_directory: str):
    """
    Download GEBCO file for a specified year.
    Construct the URL with string substitution, and retrieve the file with
    streaming/chunk writing, because it's really big.

    """
    download_url = gebco_url_pattern.replace("CURRENTYEAR", str(year))
    output_filename=f"{output_filename_prefix}_{year}.nc"
    logger.info(f"Preparing to download GEBCO data from {download_url} to"
                f" {output_directory}/{output_filename}")

    #TODO: write error-catching
    timeout = 20
    retries = 3
    try:
        response = requests.get(download_url, stream=True, timeout=timeout,
                                retries=retries)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == "404":
            logger.error(f"404 error for URL {download_url} - fall back to "
                         "previous year's GEBCO file")

    with open(f"{RAW_OUTPUT_DIRECTORY}/{output_filename}", mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)


def main():
    """
    Substitute the current year into GEBCO_URL_PATTERN to create this years'
    download link. Download the GEBCO file, with some retry/timeout options
    to give it some leeway.
    In the event of a 404, try looking for the previous year's file, in case
    this year's forecast isn't out yet.
    """
    # Get the current date
    current_year = datetime.now().year

    # Skip downloading if we already have a processed GEBCO this year
    processed_gebco = f"{PROCESSED_OUTPUT_DIRECTORY}/"\
        f"{PROCESSED_OUTPUT_FILENAME_PREFIX}_{current_year}.nc"
    if Path(processed_gebco).is_file():
        logger.info("A processed GEBCO file for this year already exists at "
                     f"{processed_gebco} - skipping download")
        sys.exit()

    try:
        download_gebco_for_specified_year(str(current_year), 
                                          GEBCO_URL_PATTERN, 
                                          RAW_OUTPUT_FILENAME_PREFIX,
                                          RAW_OUTPUT_DIRECTORY)
    except #however you capture a 404:
        logger.error(f"404 error for GEBCO URL - fall back to previous "
                     "year's GEBCO file")
        try:
            last_year
            download_gebco_for_specified_year(str(last_year), 
                                                GEBCO_URL_PATTERN, 
                                                RAW_OUTPUT_FILENAME_PREFIX,
                                                RAW_OUTPUT_DIRECTORY)
        except:


if __name__ == "__main__":
    main()