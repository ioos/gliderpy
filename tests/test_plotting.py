"""Test transect."""

import pytest
import matplotlib.pyplot as plt

from gliderpy.plotting import plot_transect
from gliderpy.fetchers import GliderDataFetcher

@pytest.mark.mpl_image_compare
def test_plot_transect():
    glider_grab = GliderDataFetcher()

    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()
    # Generate the plot
    fig, ax = plot_transect(df, 'temperature')

    # Return the figure for pytest-mpl to compare
    return fig