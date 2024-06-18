"""Test transect."""

import cmcrameri
import pytest
import matplotlib.pyplot as plt
from pathlib import Path
from gliderpy.plotting import plot_track
from gliderpy.plotting import plot_transect
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
def test_plot_transect_multiple_figures():
    glider_grab = GliderDataFetcher()

    glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
    df = glider_grab.to_pandas()

    # Generate the plot
    fig, (ax0, ax1) = plt.subplots(figsize=(15, 9), nrows=2, sharex=True,sharey=True)    
    df.plot_transect(var="temperature", ax=ax0)  
    df.plot_transect(var="salinity", ax=ax1, cmap=cmcrameri.cm.davos)

    # Return the figure for pytest-mpl to compare
    return fig
