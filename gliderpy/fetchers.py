from typing import Optional

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
            dataset_ids = dataset_ids.append(
                pd.read_csv(url)["Dataset ID"], ignore_index=True
            )
            dataset_ids_uniq = dataset_ids.str.split(";", expand=True).stack().unique()
        self.dataset_ids = pd.read_csv(url)["Dataset ID"]
        return self.dataset_ids
