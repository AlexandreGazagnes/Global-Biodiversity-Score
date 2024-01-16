import os
import logging
import json

from gbs.helpers import runcmd
from gbs.etl.urls import Urls


class Extract:
    """Extracts data from a source."""

    CROPS_URL = Urls.crops_url
    COUNTRY_SPECS_URL = Urls.country_specs_url
    PRODUCTION_URL = Urls.production_url
    PRODUCTION_JSON = Urls.production_json

    BASE = "./"
    FOLDER = "data"
    SUBFOLDER = "source"

    def __init__(
        self,
        base: str | None = None,
        folder: str | None = None,
        subfolder: str | None = None,
        crops_url: str | None = None,
        country_specs_url: str | None = None,
        production_url: str | None = None,
        production_json: str | None = None,
        verbose: bool = False,
    ):
        """Initializes the Extract class."""

        # data folder / subfolder
        self.base = base if base else self.BASE
        self.folder = folder if folder else self.FOLDER
        self.subfolder = subfolder if subfolder else self.SUBFOLDER

        # urls
        self.crops_url = crops_url if crops_url else self.CROPS_URL
        self.country_specs_url = (
            country_specs_url if country_specs_url else self.COUNTRY_SPECS_URL
        )
        self.production_url = (
            production_url if production_url else self.PRODUCTION_URL
        )
        self.production_json = (
            production_json if production_json else self.PRODUCTION_JSON
        )

        # verbose
        self.verbose = verbose

        # make / check folders
        self.make_folders()
        self._check_folders()

    def get_crops(self, out="crops.csv"):
        """ """

        dest = os.path.join(self.base, self.folder, self.subfolder, out)
        std_out, std_err = runcmd(f"wget -O {dest} '{self.crops_url}'")

        if not std_err:
            return dest

    def get_county_specs(
        self,
        out="country_specs.csv",
    ):
        """ """

        dest = os.path.join(self.base, self.folder, self.subfolder, out)
        std_out, std_err = runcmd(
            f"wget -O {dest} '{ self.country_specs_url}'"
        )

        if not std_err:
            return dest

    def get_production(
        self,
        out="production.zip",
        curl=True,
        unzip=True,
        mv=True,
        rename=True,
    ):
        """ """

        if curl:
            self._curl_production(out=out)
        if unzip:
            self._unzip_production()
        if mv:
            self._mv_production()
        if rename:
            self._rename_production()

        return

    def _curl_production(self, out="production.zip"):
        """ """

        dest = os.path.join(self.base, self.folder, self.subfolder, out)
        std_out, std_err = runcmd(
            f"curl --output {dest} '{self.production_url}'"
        )

        if not std_err:
            return dest

    def _unzip_production(self):
        """ """

        # TODO: make this more robust : do not use absolute path
        # dest = os.path.join(self.base, self.folder, self.subfolder)
        # fn = os.path.join(dest, out)
        # runcmd(f"unzip {fn} -d {dest}")

        std_out, std_err = runcmd(
            f"unzip ./data/source/production.zip -d ./data/source/"
        )

        if not std_err:
            return "./data/source/"

    def _mv_production(self):
        """ """

        # TODO: make this more robust : do not use absolute path

        # make data/source/production if it doesn't exist
        if not os.path.exists("data/source/production"):
            os.makedirs("data/source/production")

        # TODO: make this more robust : do not use absolute path

        # move production files to production folder
        std_out, std_err = runcmd(
            "mv ./data/source/Pr* ./data/source/production/"
        )

        if not std_err:
            return "./data/source/production/"

    def _rename_production(self):
        """ """

        # update filenames to lowercase
        path = "data/source/production/"
        pattern = "Production_Crops_Livestock_E_All_"

        # each file
        dst_list = []
        for fn in os.listdir(path):
            # clean filename
            cleaned_fn = (
                fn.replace(pattern, "")
                .lower()
                .replace("(", "")
                .replace(")", "")
            )

            # src and dst
            src_ = os.path.join(path, fn)
            dst_ = os.path.join(path, cleaned_fn)

            # do rename
            os.rename(src_, dst_)

            # add to list
            dst_list.append(dst_)

        return dst_list

    def make_folders(self):
        """Create both folders and sub folders."""

        # data folder
        folder = os.path.join(self.base, self.folder)
        if not os.path.exists(folder):
            logging.info(f"Creating data folder: {folder}")
            os.makedirs(folder)

        # data subfolder
        subfolder = os.path.join(folder, self.subfolder)
        if not os.path.exists(subfolder):
            logging.info(f"Creating data subfolder: {subfolder}")
            os.makedirs(subfolder)

    def _check_folders(self):
        """Check if the data folder and subfolder exist."""

        folder = os.path.join(self.base, self.folder)
        subfolder = os.path.join(folder, self.subfolder)

        if not (os.path.exists(folder) and os.path.exists(subfolder)):
            raise FileNotFoundError(
                f"Data folder {folder}  or subfolder {subfolder} does not exist."
            )

    def clean(self):
        """Clean up data folder."""

        os.remove(os.path.join(self.base, self.folder))

    def __repr__(self) -> str:
        return f"Extract({self.__dict__})"
