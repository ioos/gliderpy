import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import palettable
from palettable.cmocean.sequential import Thermal_20

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
    cs = ax.scatter(
        x, y, c=df["temperature (Celsius)"], s=50, alpha=0.5, edgecolor="none"
    )
    cbar = fig.colorbar(
        cs, orientation="vertical", fraction=0.1, shrink=0.9, extend="both"
    )
    ax.coastlines("10m")
    ax.set_extent([x.min() - dx, x.max() + dx, y.min() - dy, y.max() + dy])
    return fig, ax

def plot_transect(df,var):
    """
    Makes a scatter plot of depth vs time coloured by a user defined variable
    :param var: variable to colour the scatter plot
    :return: figure, axes
    """
    cmap = Thermal_20.mpl_colormap
        
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