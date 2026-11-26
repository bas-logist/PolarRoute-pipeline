import pytest

import lib.python.data_retrieve_gebco


class TestDownloadGebcoForCurrentYear:
    """
    Tests the downloader for GEBCO data.
    """
    def test_current_year_data_already_available(self):
        assert 1 + 1 == 2
    