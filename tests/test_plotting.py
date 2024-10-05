"""Test transect."""

import matplotlib as mpl

mpl.use("agg")  # Use the "agg" backend

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest

from gliderpy.fetchers import GliderDataFetcher
from gliderpy.plotting import plot_cast, plot_track, plot_transect, plot_ts

root = Path(__file__).parent


@pytest.fixture
def glider_data():
    """Fixture to load whoi_406-20160902T1700."""
    glider_grab = GliderDataFetcher()
    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    return glider_grab.to_pandas()


@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_track(glider_data):
    """Test plot_track accessor."""
    fig, ax = plot_track(glider_data)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_transect(glider_data):
    """Test plot_transect accessor."""
    fig, ax = plot_transect(glider_data, var="temperature", cmap="viridis")
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_transect_multiple_figures(glider_data):
    """Test plot_transect in subplots."""
    fig, (ax0, ax1) = plt.subplots(
        figsize=(15, 9),
        nrows=2,
        sharex=True,
        sharey=True,
    )
    glider_data.plot_transect(var="temperature", ax=ax0, cmap="viridis")
    glider_data.plot_transect(var="salinity", ax=ax1, cmap="cividis")

    assert ax0.get_ylabel() == "pressure"
    assert ax1.get_ylabel() == "pressure"

    assert ax0.get_xlim() == ax1.get_xlim()
    assert ax0.get_ylim() == ax1.get_ylim()

    cbar0 = ax0.collections[0].colorbar
    cbar1 = ax1.collections[0].colorbar

    assert cbar0.cmap.name == "viridis"
    assert cbar1.cmap.name == "cividis"

    assert cbar0.ax.get_ylabel() == "temperature"
    assert cbar1.ax.get_ylabel() == "salinity"

    return fig


def test_plot_transect_size(glider_data):
    """Test plot_transect args."""
    fig, ax = plt.subplots(figsize=(15, 9))
    glider_data.plot_transect(var="temperature")
    np.testing.assert_array_equal(fig.get_size_inches(), np.array([15.0, 9.0]))


@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_cast(glider_data):
    """Test plot_cast accessor."""
    fig, ax = plot_cast(glider_data, 0, var="temperature", color="blue")
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_ts(glider_data):
    """Test plot_ts accessor."""
    fig, ax = plot_ts(glider_data, 0)
    return fig