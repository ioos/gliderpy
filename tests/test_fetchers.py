import pytest

from gliderpy.fetchers import GliderDataFetcher
from gliderpy.servers import server_parameter_rename


@pytest.fixture
@pytest.mark.web
def glider_grab():
    g = GliderDataFetcher()
    g.dataset_id = "whoi_406-20160902T1700"
    yield g


def test_variables(glider_grab):
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
    glider_grab = GliderDataFetcher()
    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()
    variables = df.columns
    for var in variables:
        assert var in server_parameter_rename.values()
