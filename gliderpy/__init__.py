"""Easier access to glider data."""

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

from .fetchers import GliderDataFetcher
from .plotting import plot_track, plot_transect, plot_ctd, plot_ts

__all__ = [
    "GliderDataFetcher",
    "plot_track",
    "plot_transect",
    "plot_ts",
    "plot_cast",
]
