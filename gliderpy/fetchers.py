from typing import Optional

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd

from erddapy import ERDDAP


OptionalStr = Optional[str]

# This is hardcoded to the IOOS glider DAC.
# We aim to support more sources in the near future.
_server = "https://gliders.ioos.us/erddap"


class GliderDataFetcher(object):
    """
    Args:
        server: a glider ERDDAP server URL

    Attributes:
        dataset_id: a dataset unique id.
        constraints: download constraints, default None (opendap-like url)

    """

    def __init__(self):
        self.fetcher = ERDDAP(server=_server, protocol="tabledap",)
        self.fetcher.variables = [
            "depth",
            "latitude",
            "longitude",
            "salinity",
            "temperature",
            "time",
        ]
        self.fetcher.dataset_id: OptionalStr = None

    def to_pandas(self):
        """
        Fetches data from the server and reads into a pandas dataframe

        :return: pandas dataframe with datetime UTC as index
        """
        return self.fetcher.to_pandas(index_col="time (UTC)", parse_dates=True,)

    def query(self, min_lat, max_lat, min_lon, max_lon, start_time, end_time):
        """
        Takes user supplied geographical and time constraints and adds them to the query

        :param min_lat: southernmost lat
        :param max_lat: northermost lat
        :param min_lon: westernmost lon (-180 to +180)
        :param max_lon: easternmost lon (-180 to +180)
        :param start_time: start time, can be datetime object or string
        :param end_time: end time, can be datetime object or string
        :return: search query with argument constraints applied
        """
        self.fetcher.constraints = {
            "time>=": start_time,
            "time<=": end_time,
            "latitude>=": min_lat,
            "latitude<=": max_lat,
            "longitude>=": min_lon,
            "longitude<=": max_lon,
        }
        return self

    def plot_track(self):
        """
        Plots a track of glider path coloured by temperature
        :return: figures, axes
        """

        idx = self.to_pandas()
        x = idx["longitude (degrees_east)"]
        y = idx["latitude (degrees_north)"]
        dx, dy = 2, 4

        fig, ax = plt.subplots(
            figsize=(9, 9), subplot_kw={"projection": ccrs.PlateCarree()}
        )
        cs = ax.scatter(
            x, y, c=idx["temperature (Celsius)"], s=50, alpha=0.5, edgecolor="none"
        )
        cbar = fig.colorbar(
            cs, orientation="vertical", fraction=0.1, shrink=0.9, extend="both"
        )
        ax.coastlines("10m")
        ax.set_extent([x.min() - dx, x.max() + dx, y.min() - dy, y.max() + dy])
        return fig, ax

    def plot_transect(self, var):
        import matplotlib.dates as mdates

        """
        Makes a scatter plot of depth vs time coloured by a user defined variable
        :param var: variable to colour the scatter plot
        :return: figure, axes
        """

        idx = self.to_pandas()
        fig, ax = plt.subplots(figsize=(17, 2))
        cs = ax.scatter(
            idx.index, idx["depth (m)"], s=15, c=idx[var], marker="o", edgecolor="none",
        )

        ax.invert_yaxis()
        xfmt = mdates.DateFormatter("%H:%Mh\n%d-%b")
        ax.xaxis.set_major_formatter(xfmt)

        cbar = fig.colorbar(cs, orientation="vertical", extend="both")
        cbar.ax.set_ylabel(var)
        ax.set_ylabel("Depth (m)")
        return fig, ax


class DatasetList:
    """ Search servers for glider dataset ids. Defaults to the string "glider"


    Attributes:
        e: an ERDDAP server instance
        search_terms: A list of terms to search the server for. Multiple terms will be combined as AND

    """

    def __init__(self):
        self.e = ERDDAP(server="https://gliders.ioos.us/erddap", protocol="tabledap",)
        self.search_terms = ["glider"]

    def get_ids(self):
        """Search the database using a user supplied list of strings
        :return: Unique list of dataset ids
        """
        dataset_ids = pd.Series(dtype=str)
        for term in self.search_terms:
            url = self.e.get_search_url(search_for=term, response="csv")

            dataset_ids = dataset_ids.append(
                pd.read_csv(url)["Dataset ID"], ignore_index=True
            )
        self.dataset_ids = dataset_ids.str.split(";", expand=True).stack().unique()

        return self.dataset_ids
