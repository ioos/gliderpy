from typing import Optional

import pandas as pd

from erddapy import ERDDAP

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

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
        return self.fetcher.to_pandas(index_col="time (UTC)", parse_dates=True,)

    def query(self, min_lat, max_lat, min_lon, max_lon, start_time, end_time):
        """Takes user supplied geographical and time constraints and adds them to the query
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
        
        idx = self.to_pandas()
        fig, ax = plt.subplots(figsize=(17, 2))
        cs = ax.scatter(
            idx.index,
            idx["depth (m)"],
            s=15,
            c=idx[var],
            marker="o",
            edgecolor="none",
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
    """

    def __init__(self):
        self.e = ERDDAP(server="https://gliders.ioos.us/erddap", protocol="tabledap",)
        self.search_terms = ["glider"]

    def get_ids(self):
        """Search the database using a user supplied list of strings
        """
        dataset_ids = pd.Series(dtype=str)
        for term in self.search_terms:
            url = self.e.get_search_url(search_for=term, response="csv")

            dataset_ids = dataset_ids.append(pd.read_csv(url)["Dataset ID"], ignore_index=True)
        self.dataset_ids = dataset_ids.str.split(';',expand=True).stack().unique()

        return self.dataset_ids
