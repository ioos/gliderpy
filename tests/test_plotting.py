"""Test transect."""

import matplotlib
matplotlib.use("agg")  # Use the "agg" backend

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pytest
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
    fig, ax = plot_transect(glider_data, "temperature", cmap="viridis")
    # Return the figure for pytest-mpl to compare
    return fig

@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_transect_multiple_figures(glider_data):
    # Generate the plot with multiple figures
    fig, (ax0, ax1) = plt.subplots(figsize=(15, 9), nrows=2, sharex=True, sharey=True)
    glider_data.plot_transect(var="temperature", ax=ax0, cmap="viridis")
    glider_data.plot_transect(var="salinity", ax=ax1, cmap="cividis")
    # Return the figure for pytest-mpl to compare
    return fig

def test_plot_transect_size(glider_data):
    # Generate the plot with a specific size
    fig, ax = plt.subplots(figsize=(15, 9))
    glider_data.plot_transect(var="temperature")
    np.testing.assert_array_equal(fig.get_size_inches(), np.array([15.,  9.]))

def test_verify_plot_transect(glider_data):
    # Create two plots with different variables and colormaps
    fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True, sharey=True)
    glider_data.plot_transect("temperature", ax=ax0, cmap="viridis")
    glider_data.plot_transect("salinity", ax=ax1, cmap="plasma")

    # Check if the y-label is named "pressure"
    assert ax0.get_ylabel() == "pressure"
    assert ax1.get_ylabel() == "pressure"

    # Since sharex=True and sharey=True, xlim and ylim should be the same
    assert ax0.get_xlim() == ax1.get_xlim()
    assert ax0.get_ylim() == ax1.get_ylim()

    # Get the colorbars
    cbar0 = ax0.collections[0].colorbar
    cbar1 = ax1.collections[0].colorbar

    # Check colormap
    assert cbar0.cmap.name == "viridis"
    assert cbar1.cmap.name == "plasma"

    #Check labels
    assert cbar0.ax.get_ylabel() == 'temperature'
    assert cbar1.ax.get_ylabel() == 'salinity'

