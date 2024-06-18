"""Some convenience functions to help visualize glider data."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

try:
    import cartopy.crs as ccrs
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    warnings.warn(
        "gliderpy requires matplotlib and cartopy for plotting.",
        stacklevel=1,
    )
    raise


if TYPE_CHECKING:
    import pandas as pd

from pandas_flavor import register_dataframe_method


@register_dataframe_method
def plot_track(df: pd.DataFrame) -> tuple(plt.Figure, plt.Axes):
    """Plot a track of glider path coloured by temperature.

    :return: figures, axes
    """
    x = df["longitude"]
    y = df["latitude"]
    dx, dy = 2, 4

    fig, ax = plt.subplots(
        figsize=(9, 9),
        subplot_kw={"projection": ccrs.PlateCarree()},
    )
    ax.scatter(x, y, c=None, s=25, alpha=0.25, edgecolor="none")
    ax.coastlines("10m")
    ax.set_extent([x.min() - dx, x.max() + dx, y.min() - dy, y.max() + dy])
    return fig, ax

@register_dataframe_method
def plot_transect(
    df: pd.DataFrame,
    var: str,
    ax: plt.Axes = None,
    **kw: dict,
) -> tuple(plt.Figure, plt.Axes):
    """Make a scatter plot of depth vs time coloured by a user defined
    variable.

    :param var: variable to colour the scatter plot
    :return: figure, axes
    """
    cmap = kw.get("cmap", None)

    fignums = plt.get_fignums()
    if ax is None and not fignums:
        fig, ax = plt.subplots(figsize=(17, 2))
    elif ax:
        fig = ax.get_figure()
    else:
        ax = plt.gca()
        fig = plt.gcf()

    if not ax.yaxis_inverted():
        ax.invert_yaxis()

    cs = ax.scatter(
        df.index,
        df["pressure"],
        s=15,
        c=df[var],
        marker="o",
        edgecolor="none",
        cmap=cmap,
    )

    xfmt = mdates.DateFormatter("%H:%Mh\n%d-%b")
    ax.xaxis.set_major_formatter(xfmt)

    cbar = fig.colorbar(cs, orientation="vertical", extend="both")
    cbar.ax.set_ylabel(var)
    ax.set_ylabel("pressure")

    ax.set_ylim(ax.get_ylim()[0], 0)
    
    return fig, ax


