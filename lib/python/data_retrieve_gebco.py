import os
from datetime import datetime, timedelta
from pathlib import Path
import logging
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEBCO_URL_PATTERN = os.getenv("GEBCO_URL_PATTERN")
GEBCO_YEAR_RECURSION = os.getenv("GEBCO_YEAR_RECURSION")
RAW_OUTPUT_FILENAME_PREFIX = os.getenv("RAW_OUTPUT_FILENAME_PREFIX")
PROCESSED_OUTPUT_DIRECTORY = os.getenv("PROCESSED_OUTPUT_DIRECTORY")
PROCESSED_OUTPUT_FILENAME_PREFIX = os.getenv("PROCESSED_OUTPUT_FILENAME_PREFIX")
RAW_OUTPUT_DIRECTORY = os.getenv("RAW_OUTPUT_DIRECTORY")


def download_gebco_for_specified_year(year: str,
                                      gebco_url_pattern: str,
                                      processed_output_filename_prefix: str,
                                      processed_output_directory: str,
                                      output_filename_prefix: str,
                                      output_directory: str,
                                      year_recursion_depth: int):
    """
    Download GEBCO file for a specified year, if it doesn't already exist.
    Construct the URL with string substitution, and retrieve the file with
    streaming/chunk writing, because it's really big.
    Try past years if you need to, up to the limit in year_recursion_depth.
    """
    processed_gebco = f"{processed_output_directory}/"\
        f"{processed_output_filename_prefix}_{year}.nc"
    if Path(processed_gebco).is_file():
        logger.info(f"A processed GEBCO file for year {year} exists "
                    f"at {processed_gebco} - skipping download")
        sys.exit()
    
    download_url = gebco_url_pattern.replace("CURRENTYEAR", str(year))
    output_filename=f"{output_filename_prefix}_{year}.nc"
    logger.info(f"Preparing to download GEBCO data from {download_url} to"
                f" {output_directory}/{output_filename}")

    timeout = 20
    retries = 3
    try:
        s = requests.Session()
        retries = Retry(
            total=retries,
            backoff_factor=0.1,
            allowed_methods={'GET'}
        )
        s.mount('https://', HTTPAdapter(max_retries=retries))
        response = requests.get(download_url, stream=True, timeout=timeout,
                                retries=retries)
        logger.info(f"Downloaded GEBCO data from {download_url} to"
                f"{output_directory}/{output_filename}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == "404":
            logger.error(f"404 error for URL {download_url} - trying earlier year")

            previous_year = datetime.datetime.strptime(year, "%Y%m")
            # try last year, if this isn't out of the range set by year_recursion_depth
            earliest_permitted_year = datetime.datetime.today().year - timedelta(
                years=int(year_recursion_depth)
                )
            if previous_year < earliest_permitted_year:
                download_gebco_for_specified_year(
                    str(previous_year.year),
                    gebco_url_pattern,
                    output_filename_prefix,
                    output_directory,
                    year_recursion_depth
                )
            else:
                logger.error(f"GEBCO file not found within time period set by "
                             f"{year_recursion_depth!r} - check URLs valid")
            
    with open(f"{RAW_OUTPUT_DIRECTORY}/{output_filename}", mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)
    logger.info(f"GEBCO data finished saving to: {RAW_OUTPUT_DIRECTORY}/{output_filename}")


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

    download_gebco_for_specified_year(
        str(current_year), 
        GEBCO_URL_PATTERN,
        PROCESSED_OUTPUT_FILENAME_PREFIX,
        PROCESSED_OUTPUT_DIRECTORY,
        RAW_OUTPUT_FILENAME_PREFIX,
        RAW_OUTPUT_DIRECTORY,
        GEBCO_YEAR_RECURSION
        )
    

if __name__ == "__main__":
    main()