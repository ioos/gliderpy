"""
Some convenience functions to help visualize glider data.
"""

import warnings


try:

    import cartopy.crs as ccrs
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
except ModuleNotFoundError as err:
    warnings.warn("gliderpy requires matplotlib and cartopy for plotting.")
    raise err


def plot_track(df):
    """
    Plots a track of glider path coloured by temperature
    :return: figures, axes
    """

    x = df["longitude (degrees_east)"]
    y = df["latitude (degrees_north)"]
    dx, dy = 2, 4

    fig, ax = plt.subplots(
        figsize=(9, 9), subplot_kw={"projection": ccrs.PlateCarree()}
    )
    ax.scatter(x, y, c=None, s=25, alpha=0.25, edgecolor="none")
    ax.coastlines("10m")
    ax.set_extent([x.min() - dx, x.max() + dx, y.min() - dy, y.max() + dy])
    return fig, ax


def plot_transect(df, var, **kw):
    """
    Makes a scatter plot of depth vs time coloured by a user defined variable
    :param var: variable to colour the scatter plot
    :return: figure, axes
    """
    cmap = kw.get("cmap", None)

    fig, ax = plt.subplots(figsize=(17, 2))
    cs = ax.scatter(
        df.index,
        df["depth (m)"],
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
    ax.set_ylabel("Depth (m)")
    return fig, ax
