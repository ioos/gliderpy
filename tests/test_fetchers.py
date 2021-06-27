import pytest

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


# As above for ifremer ERDDAP


@pytest.fixture
@pytest.mark.web
def glider_grab_ifr():
    g = GliderDataFetcher("http://www.ifremer.fr/erddap")
    g.fetcher.dataset_id = "OceanGlidersGDACTrajectories"
    yield g


def test_variables_ifr(glider_grab_ifr):
    expected = [
        "latitude",
        "longitude",
        "platform_deployment",
        "PRES",
        "PSAL",
        "TEMP",
        "time",
    ]
    assert sorted(glider_grab_ifr.fetcher.variables) == sorted(expected)
