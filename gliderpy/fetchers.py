"""
Helper methods to fetch glider data from multiple ERDDAP serves

"""

from typing import Optional

import httpx
import pandas as pd
from erddapy import ERDDAP
from erddapy.erddapy import urlopen

from gliderpy.servers import (
    server_parameter_rename,
    server_select,
    server_vars,
)

OptionalStr = Optional[str]

# This defaults to the IOOS glider DAC.
_server = "https://gliders.ioos.us/erddap"


def standardise_df(df, dataset_url):
    """
    Standardise variable names in a dataset and add column for url
    """
    df.columns = df.columns.str.lower()
    df.rename(columns=dict(server_parameter_rename), inplace=True)
    df.index.rename("time", inplace=True)
    df["dataset_url"] = dataset_url
    return df


class GliderDataFetcher:
    """
    Args:
        server: a glider ERDDAP server URL

    Attributes:
        dataset_id: a dataset unique id.
        constraints: download constraints, default None (opendap-like url)

    """

    def __init__(self, server=_server):
        server = server_select(server)
        self.server = server
        self.fetcher = ERDDAP(
            server=server,
            protocol="tabledap",
        )
        self.fetcher.variables = server_vars[server]
        self.fetcher.dataset_id: OptionalStr = None
        self.datasets: Optional = None

    def to_pandas(self):
        """
        Fetches data from the server and reads into a pandas dataframe

        :return: pandas dataframe with datetime UTC as index
        """
        if type(self.datasets) is pd.Series:
            df_all = []
            for dataset_id in self.datasets:
                self.fetcher.dataset_id = dataset_id
                df = self.fetcher.to_pandas(
                    index_col="time (UTC)",
                    parse_dates=True,
                )
                dataset_url = self.fetcher.get_download_url().split("?")[0]
                df = standardise_df(df, dataset_url)
                df_all.append(df)
            return pd.concat(df_all)

        if not self.fetcher.dataset_id:
            return None

        df = self.fetcher.to_pandas(
            index_col="time (UTC)",
            parse_dates=True,
        )
        # Standardize variable names
        dataset_url = self.fetcher.get_download_url().split("?")[0]
        df = standardise_df(df, dataset_url)
        return df

    def query(self, min_lat, max_lat, min_lon, max_lon, min_time, max_time):
        """
        Takes user supplied geographical and time constraints and adds them to the query

        :param min_lat: southernmost lat
        :param max_lat: northermost lat
        :param min_lon: westernmost lon (-180 to +180)
        :param max_lon: easternmost lon (-180 to +180)
        :param min_time: start time, can be datetime object or string
        :param max_time: end time, can be datetime object or string
        :return: search query with argument constraints applied
        """
        self.fetcher.constraints = {
            "time>=": min_time,
            "time<=": max_time,
            "latitude>=": min_lat,
            "latitude<=": max_lat,
            "longitude>=": min_lon,
            "longitude<=": max_lon,
        }
        if not self.fetcher.dataset_id:
            url = self.fetcher.get_search_url(
                search_for="glider",
                response="csv",
                min_lat=min_lat,
                max_lat=max_lat,
                min_lon=min_lon,
                max_lon=max_lon,
                min_time=min_time,
                max_time=max_time,
            )
            try:
                data = urlopen(url)
            except httpx.HTTPError as err:
                raise Exception(
                    f"Error, no datasets found in supplied range. Try relaxing your constraints: {self.fetcher.constraints}",
                ) from err
                return None
            df = pd.read_csv(data)
            self.datasets = df["Dataset ID"]
            return df[["Title", "Institution", "Dataset ID"]]

        return self

    def platform(self, platform):
        """

        :param platform: platform and deployment id from ifremer
        :return: search query with platform constraint applied
        """
        self.fetcher.constraints["platform_deployment="] = platform
        return self


class DatasetList:
    """Build a glider dataset ids list.


    Attributes:
        e: an ERDDAP server instance
        TODO: search_terms: A list of terms to search the server for. Multiple terms will be combined as AND

    """

    def __init__(self, server=_server):
        self.e = ERDDAP(
            server=server,
            protocol="tabledap",
        )

    def get_ids(self):
        """Return the allDatasets list for the glider server."""
        if self.e.server == "https://gliders.ioos.us/erddap":
            self.e.dataset_id = "allDatasets"
            dataset_ids = self.e.to_pandas()["datasetID"].to_list()
            dataset_ids.remove("allDatasets")
            self.dataset_ids = dataset_ids
            return self.dataset_ids
        else:
            raise ValueError(f"The {self.e.server} does not supported this operation.")
        # TODO: List the platform_deployment variable
        # if self.e.server == "https://erddap.ifremer.fr/erddap":
        #     dataset_id = OceanGlidersGDACTrajectories
        #     platform_deployment
