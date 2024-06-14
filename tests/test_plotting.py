"""Test transect."""

import pytest
import matplotlib as mpl
from pathlib import Path
from gliderpy.plotting import plot_track
from gliderpy.plotting import plot_transect
from gliderpy.plotting import plot_ctd
from gliderpy.fetchers import GliderDataFetcher

root = Path(__file__).parent

@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_track():
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
    fig, ax = plot_transect(df, 'temperature')

    # Return the figure for pytest-mpl to compare
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=root.joinpath("baseline/"))
def test_plot_ctd():
    glider_grab = GliderDataFetcher()

    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()
    # Generate the plot
    fig, ax = plot_ctd(df, 'temperature')

    # Return the figure for pytest-mpl to compare
    return fig
