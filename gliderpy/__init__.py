"""Easier access to glider data."""

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

from .plotting import plot_track
from .plotting import plot_transect
from .fetchers import GliderDataFetcher


__all__ = [
    "GliderDataFetcher",
    "plot_track",
    "plot_transect",
]