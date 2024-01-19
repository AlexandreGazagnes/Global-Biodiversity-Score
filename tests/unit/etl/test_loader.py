import logging
import os

import pytest


import pandas as pd

from gbs.etl.loader import Loader


class TestLoader:
    """Test the Loader class."""

    def test_final(self):
        """test final"""

        df = Loader.final()

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert len(df.columns) > 0
