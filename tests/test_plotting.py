"""Test transect."""

from pathlib import Path

import pytest

from gliderpy.fetchers import GliderDataFetcher
from gliderpy.plotting import plot_track, plot_transect

root = Path(__file__).parent


@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_track():
    """Image comparison test for plot_track."""
    glider_grab = GliderDataFetcher()

    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()
    # Generate the plot
    fig, ax = plot_track(df)

    # Return the figure for pytest-mpl to compare
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_transect():
    glider_grab = GliderDataFetcher()

    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()
    # Generate the plot
    fig, ax = plot_transect(df, "temperature")

    # Return the figure for pytest-mpl to compare
    return fig
