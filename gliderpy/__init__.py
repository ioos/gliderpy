"""Easier access to glider data."""

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

from .plotting import plot_track
from .fetchers import GliderDataFetcher
from .plotting import plot_transect

__all__ = [
    "GliderDataFetcher",
    "plot_track",
    "plot_transect",
]
