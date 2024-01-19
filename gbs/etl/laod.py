import os, sys, logging

import pandas as pd

from gbs.etl.urls import Urls


class Loader:
    """Loader class for loading data into the database"""

    @classmethod
    def final(cls):
        """flaod the final csv into the database"""

        return pd.read_csv(Urls.final_csv)
