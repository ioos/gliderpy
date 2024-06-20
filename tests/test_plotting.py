"""Test transect."""

import matplotlib
matplotlib.use('agg')  # Use the 'agg' backend

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from gliderpy.plotting import plot_track, plot_transect
from gliderpy.fetchers import GliderDataFetcher

root = Path(__file__).parent

@pytest.fixture
def glider_data():
    glider_grab = GliderDataFetcher()
    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()
    return df

@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_track(glider_data):
    # Generate the plot
    fig, ax = plot_track(glider_data)
    # Return the figure for pytest-mpl to compare
    return fig

@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_transect(glider_data):
    # Generate the plot
    fig, ax = plot_transect(glider_data, 'temperature', cmap='viridis')
    # Return the figure for pytest-mpl to compare
    return fig

@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_transect_multiple_figures(glider_data):
    # Generate the plot with multiple figures
    fig, (ax0, ax1) = plt.subplots(figsize=(15, 9), nrows=2, sharex=True, sharey=True)
    glider_data.plot_transect(var="temperature", ax=ax0, cmap='viridis')
    glider_data.plot_transect(var="salinity", ax=ax1, cmap='cividis')
    # Return the figure for pytest-mpl to compare
    return fig

def test_plot_transect_size(glider_data):
    # Generate the plot with a specific size
    fig, ax = plt.subplots(figsize=(15, 9))
    glider_data.plot_transect(var="temperature")
    np.testing.assert_array_equal(fig.get_size_inches(), np.array([15.,  9.]))

