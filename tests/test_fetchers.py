"""Test Fetchers."""

import pytest

from gliderpy.fetchers import GliderDataFetcher
from gliderpy.servers import server_parameter_rename


@pytest.fixture()
@pytest.mark.web()
def glider_grab():
    """Create the basic query object for testing."""
    g = GliderDataFetcher()
    g.dataset_id = "whoi_406-20160902T1700"
    return g


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
    assert sorted(glider_grab.fetcher.variables) == sorted(expected)


def test_standardise_variables_ioos():
    """Check if IOOS variables are properly renamed."""
    glider_grab = GliderDataFetcher()
    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()
    variables = df.columns
    for var in variables:
        assert var in server_parameter_rename.values()
