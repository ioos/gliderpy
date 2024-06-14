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

    if ax is None:
        fig, ax = plt.subplots(figsize=(17, 2))
    else:
        fig = ax.figure

    cs = ax.scatter(
        df.index,
        df["pressure"],
        s=15,
        c=df[var],
        marker="o",
        edgecolor="none",
        cmap=cmap,
    )

    ax.invert_yaxis()
    xfmt = mdates.DateFormatter("%H:%Mh\n%d-%b")
    ax.xaxis.set_major_formatter(xfmt)

    cbar = fig.colorbar(cs, orientation="vertical", extend="both")
    cbar.ax.set_ylabel(var)
    ax.set_ylabel("pressure")
    return fig, ax

@register_dataframe_method
def plot_ctd(
    df: pd.DataFrame,
    var: str,
    ax: plt.Axes = None,
    color: str = None
) -> tuple:
    """Make a CTD profile plot of pressure vs property
    depending on what variable was chosen.
      
    :param var: variable to plot against pressure
    :param ax: existing axis to plot on (default: None)
    :param color: color for the plot line (default: None)
    :return: figure, axes
    """
    g = df.groupby(["longitude", "latitude"])
    profile = g.get_group((list(g.groups)[0]))

    if ax is None:
        fig, ax1 = plt.subplots(figsize=(5, 6))
        ax1.plot(profile[var], -profile["pressure"], label=var, color=color)
        ax1.set_ylabel('Pressure')
        ax1.set_xlabel(var)
        ax1.legend()
        return fig, ax1
    else:
        fig = ax.get_figure()
        ax2 = ax.twiny()  # Create a new twinned axis
        ax2.plot(profile[var], -profile["pressure"], label=var, color=color)
        ax2.set_xlabel(var)
        
        # Handle legends
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2, loc="lower center")
        
        return fig, ax2