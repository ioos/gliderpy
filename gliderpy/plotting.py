"""Some convenience functions to help visualize glider data."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

try:
    import cartopy.crs as ccrs
    import gsw
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    import numpy as np

except ModuleNotFoundError:
    warnings.warn(
        "gliderpy requires matplotlib and cartopy for plotting.",
        stacklevel=1,
    )


if TYPE_CHECKING:
    import pandas as pd

from pandas_flavor import register_dataframe_method


@register_dataframe_method
def plot_track(df: pd.DataFrame) -> tuple[plt.Figure, plt.Axes]:
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
) -> tuple[plt.Figure, plt.Axes]:
    """Make a scatter plot of depth vs time coloured by a user defined
    variable.

    :param var: variable to colour the scatter plot
    :return: figure, axes
    """
    cmap = kw.get("cmap")

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


@register_dataframe_method
def plot_cast(
    df: pd.DataFrame,
    profile_number: int,
    var: str,
    ax: plt.Axes = None,
    color: str | None = None,
) -> tuple[plt.Figure, plt.Axes]:
    """Make a CTD profile plot of pressure vs property
    depending on what variable was chosen.

    :param profile_number: profile number of CTD
    :param var: variable to plot against pressure
    :param ax: existing axis to plot on (default: None)
    :param color: color for the plot line (default: None)
    :return: figure, axes
    """
    g = df.groupby(["longitude", "latitude"])
    profile = g.get_group(list(g.groups)[profile_number])

    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 6))
    else:
        fig = ax.get_figure()

    ax.plot(profile[var], profile["pressure"], label=var, color=color)
    ax.set_ylabel("Pressure")
    ax.set_xlabel(var)
    ax.invert_yaxis()

    return fig, ax


@register_dataframe_method
def plot_ts(
    df: pd.DataFrame,
) -> tuple[plt.Figure, plt.Axes]:
    """Make a TS diagram for all profiles in the DataFrame.

    :return: figure, axes
    """
    df["sa"] = gsw.conversions.SA_from_SP(
        df["salinity"],
        df["pressure"],
        df["longitude"],
        df["latitude"],
    )

    df["ct"] = gsw.conversions.CT_from_t(
        df["sa"],
        df["temperature"],
        df["pressure"],
    )

    g = df.groupby(["longitude", "latitude"])

    fig, ax = plt.subplots(figsize=(10, 10))

    for _name, group in g:
        sc = plt.scatter(
            group["sa"],
            group["ct"],
            c=group["pressure"],
            cmap="plasma_r",
            s=30,
        )

    plt.xlabel("Absolute Salinity(g/kg)")
    plt.ylabel("Conservative Temperature (°C)")
    cbar = plt.colorbar(sc)
    cbar.set_label("Pressure (dbar)")

    # Define salinity and temperature grids
    salinity_grid = np.linspace(df["sa"].min() - 5, df["sa"].max() + 5, 100)
    temperature_grid = np.linspace(df["ct"].min() - 5, df["ct"].max() + 5, 100)
    sal, temp = np.meshgrid(salinity_grid, temperature_grid)
    sigma = gsw.sigma0(sal, temp)

    contours = plt.contour(
        sal,
        temp,
        sigma,
        levels=np.arange(20, 30, 1),
        colors="grey",
        linestyles="--",
    )

    plt.clabel(contours, inline=True, fmt="%1.1f", fontsize=8, colors="black")

    return fig, ax
