import os, sys, isort


import pandas as pd

from gbs.etl.urls import Urls


class Loader:
    """ """

    @classmethod
    def final(cls):
        """Load Final Df"""

        return pd.read_csv(Urls.final)
