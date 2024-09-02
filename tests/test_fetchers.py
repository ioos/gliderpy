"""Test Fetchers."""

import pytest

from gliderpy.fetchers import GliderDataFetcher
from gliderpy.servers import server_parameter_rename


@pytest.fixture
@pytest.mark.web
def glider_grab():
    """Create the basic query object for testing."""
    g = GliderDataFetcher()
    g.fetcher.dataset_id = "whoi_406-20160902T1700"
    return g, g.to_pandas()


@pytest.mark.vcr
def test_variables(glider_grab):
    """Check if expected variables are being fetched."""
    expected = [
        "latitude",
        "longitude",
        "pressure",
        "profile_id",
        "salinity",
        "temperature",
        "time",
    ]
    g, df = glider_grab
    assert sorted(g.fetcher.variables) == sorted(expected)


@pytest.mark.vcr
def test_standardise_variables(glider_grab):
    """Check if IOOS variables are properly renamed."""
    g, df = glider_grab
    variables = df.columns
    for var in variables:
        assert var in server_parameter_rename.values()
