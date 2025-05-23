"""Easier access to glider data."""

import pandas as pd
from pandas_flavor import register_dataframe_method

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

from .fetchers import GliderDataFetcher
from .plotting import plot_cast, plot_track, plot_transect, plot_ts

__all__ = [
    "GliderDataFetcher",
    "plot_cast",
    "plot_track",
    "plot_transect",
    "plot_ts",
]


def _num_profiles(df: pd.DataFrame) -> int:
    """Compute the number of unique glider pofiles."""
    return len(df[["latitude", "longitude"]].value_counts())


def _days(df: pd.DataFrame) -> pd.Timedelta:
    """Compute the glider days."""
    return df.index.dropna()[-1].ceil("D") - df.index.dropna()[0].floor("D")


def _deployment_lat(df: pd.DataFrame) -> dict:
    """Return the glider deployment latitude."""
    return df["latitude"].to_list()[0]


def _deployment_lon(df: pd.DataFrame) -> dict:
    """Return the glider deployment longitude."""
    return df["longitude"].to_list()[0]


@register_dataframe_method
def summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return the summary for a set of gliders."""
    summ = {
        "num_profiles": _num_profiles(df),
        "days": _days(df),
        "deployment_lat": _deployment_lat(df),
        "deployment_lon": _deployment_lon(df),
    }

    return pd.Series(summ)
