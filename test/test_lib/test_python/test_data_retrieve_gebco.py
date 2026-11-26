import logging
import pytest
from unittest.mock import patch

from lib.python.data_retrieve_gebco import *

LOGGER = logging.getLogger(__name__)

class TestDownloadGebcoForCurrentYear:
    """
    Tests the downloader for GEBCO data.
    """
    def test_already_exists(self, caplog):
        """
        CASE: A processed GEBCO file already exists for the year provided.
        EXPECT: The function exits, and logs an INFO message to tell us that a file wasn't needed.
        """
        current_year = "2026"
        gebco_url_pattern = "https://data.ceda.ac.uk/bodc/gebco/global/gebco_CURRENTYEAR/sub_ice_topography_bathymetry/netcdf/GEBCO_CURRENTYEAR_sub_ice.nc"
        processed_output_filename_prefix = "gebco_global"
        processed_output_directory =  "./bathymetry/gebco"
        raw_output_filename_prefix = "gebco_raw_download"
        raw_output_directory = "./test"
        gebco_year_recursion = 2

        caplog.set_level(logging.DEBUG)
        # catch the sys.exit
        with pytest.raises(SystemExit) as output, patch("pathlib.Path.is_file", autospec=True):
            # mock the file-opening so that it shows as existing
            #with patch("pathlib.Path.exists", autospec=True):
            download_gebco_for_specified_year(
                current_year, 
                gebco_url_pattern,
                processed_output_filename_prefix,
                processed_output_directory,
                raw_output_filename_prefix,
                raw_output_directory,
                gebco_year_recursion
                )

        # check the program exited
        assert output.type == SystemExit

        # check that the exit was due to the file already existing
        expected_filename = f"{processed_output_directory}/{processed_output_filename_prefix}_{current_year}.nc"
        expected_log = f"A processed GEBCO file for year 2026 exists at {expected_filename} - skipping download"
        
        assert expected_log in caplog.text

    def test_downloads_ok_if_file_exists(self, caplog):
        """
        CASE: the GEBCO URL for the current year exists (we've mocked it). 
        EXPECT: the function tries to run requests, logs a message to say the download worked,
        then writes out to a file.
        """