import pytest

from requests.exceptions import HTTPError

from gliderpy.fetchers import GliderDataFetcher


@pytest.fixture
@pytest.mark.web
def glider_grab():
    g = GliderDataFetcher()
    g.dataset_id = "whoi_406-20160902T1700"
    yield g


def test_variables(glider_grab):
    expected = [
        "depth",
        "latitude",
        "longitude",
        "salinity",
        "temperature",
        "time",
    ]
    assert sorted(glider_grab.fetcher.variables) == sorted(expected)
