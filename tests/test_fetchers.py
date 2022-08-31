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
        "pressure",
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
        "PRES",
        "PSAL",
        "TEMP",
        "time",
    ]
    assert sorted(glider_grab_ifr.fetcher.variables) == sorted(expected)


def test_standardise_variables_ioos():
    glider_grab = GliderDataFetcher()
    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()
    variables = df.columns
    for var in variables:
        assert var in server_parameter_rename.values()


def test_standardise_variables_ifremer():
    glider_grab = GliderDataFetcher("http://www.ifremer.fr/erddap")
    glider_grab.fetcher.dataset_id = "OceanGlidersGDACTrajectories"
    glider_grab.query(-90, 90, -180, 180, "2015-09-20", "2015-09-27")
    df = glider_grab.to_pandas()
    variables = df.columns
    for var in variables:
        assert var in server_parameter_rename.values()


@pytest.mark.xfail
def test_standardise_variables_uncabled():
    glider_grab = GliderDataFetcher(
        "https://erddap-uncabled.oceanobservatories.org/uncabled/erddap"
    )
    glider_grab.fetcher.dataset_id = (
        "CP05MOAS-GL336-02-FLORTM000-flort_m_glider_"
        "instrument-telemetered-deployment0005-tabledap"
    )
    df = glider_grab.to_pandas()
    variables = df.columns
    for var in variables:
        assert var in server_parameter_rename.values()
