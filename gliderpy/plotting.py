"""Some convenience functions to help visualize glider data."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

try:
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
def plot_transect(
    df: pd.DataFrame,
    var: str,
    **kw: dict,
) -> tuple(plt.Figure, plt.Axes):
    """Make a scatter plot of depth vs time coloured by a user defined
    variable.

    :param var: variable to colour the scatter plot
    :return: figure, axes
    """
    cmap = kw.get("cmap", None)

    fig, ax = plt.subplots(figsize=(17, 2))
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
