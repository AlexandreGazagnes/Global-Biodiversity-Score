import os

import logging

import pytest

from gbs.etl.extract import Extract


@pytest.fixture
def extract():
    return Extract()


class TestExtract:
    """Test the Extract class."""

    def test_init(self, extract):
        """Test the initialization of the Extract class."""

        assert extract.base == "./"
        assert extract.folder == "data"
        assert extract.subfolder == "source"

    def test_make_folders(self, extract):
        """Test the make_folders method of the Extract class."""

        extract.make_folders()

        assert os.path.exists(
            os.path.join(
                extract.base,
                extract.folder,
                extract.subfolder,
            )
        )

    def test_clean(self, extract):
        """Test the clean method of the Extract class."""

        extract.clean()

        assert not os.path.exists(
            os.path.join(
                extract.base,
                extract.folder,
                extract.subfolder,
            )
        )

        extract.make_folders()

    def test_get_crops(self, extract):
        """Test the get_crops method of the Extract class."""

        extract.get_crops()

        assert os.path.exists(
            os.path.join(
                extract.base,
                extract.folder,
                extract.subfolder,
                "crops.csv",
            )
        )

    def test_get_country_specs(self, extract):
        """Test the get_country_specs method of the Extract class."""

        extract.get_country_specs()

        assert os.path.exists(
            os.path.join(
                extract.base,
                extract.folder,
                extract.subfolder,
                "country_specs.csv",
            )
        )

    def test_get_production(self, extract):
        """Test the get_production method of the Extract class."""

        # extract.get_production()

        # assert os.path.exists(
        #     os.path.join(
        #         extract.base,
        #         extract.folder,
        #         extract.subfolder,
        #         "production",
        #     )
        # )

        pass

    def test_curl_production(self, extract):
        """Test the _curl_production method of the Extract class."""

        extract._curl_production()

        assert os.path.exists(
            os.path.join(
                extract.base,
                extract.folder,
                extract.subfolder,
                "production.zip",
            )
        )

    def test_check_folders(self, extract):
        """Test the _check_folders method of the Extract class."""

        extract.check_files(include_production=False)

    @pytest.mark.parametrize("clean", [True, False])
    def test_get_all(self, extract, clean):
        """Test the get_all method of the Extract class."""

        extract.get_all(clean=clean, include_production=False)
