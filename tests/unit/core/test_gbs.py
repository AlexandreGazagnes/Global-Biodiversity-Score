import pytest

from gbs.core.gbs import Gbs


@pytest.fixture
def gbs():
    """Return Gbs instance."""

    return Gbs()


class TestGbs:
    """Test Gbs class."""

    def test_init(self, gbs):
        """Test Gbs instance initialization."""

        assert gbs
