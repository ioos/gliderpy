import pytest
import numpy as np

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

# testing the data type for each column
# this was adapted from How to Validate Your DataFrames with Pytest by Data Products
# https://plainenglish.io/blog/how-to-validate-your-dataframes-with-pytest-b238d2891d12
@pytest.fixture
def glider_data_type() -> dict[str, np.dtype]:
    """
    Get the data type of glider df
    :return: a dict of column name and its respective dtype 
    """
    glider_grab = GliderDataFetcher()
    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()
    glider_dtype_dict = df.dtypes.to_dict()
    return glider_dtype_dict

def test_glider_data_type(glider_data_type: callable):
    """
    Test the data type of glider data against the schema data type
    """
    glider_data_schema = {'latitude': np.dtype('float64'),
                        'longitude': np.dtype('float64'),
                        'pressure': np.dtype('float64'),
                        'profile_id': np.dtype('int64'),
                        'salinity': np.dtype('float64'),
                        'temperature': np.dtype('float64'),
                        'dataset_url': np.dtype('O')}
    assert glider_data_type == glider_data_schema
