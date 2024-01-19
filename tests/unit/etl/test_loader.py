import logging
import os

import pytest


import pandas as pd

from gbs.etl.loader import Loader


class TestLoader:
    """Test the Loader class."""

    def test_final(self):
        """test final method of the Loader class."""

        df = Loader.final()

        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] > 0
        assert df.shape[1] > 0
