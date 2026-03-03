"""Utilities for downloading, inspecting, and converting Cloud Optimized GeoTIFFs."""

from chunk_utils.convert import cog_to_zarr
from chunk_utils.download import download_cog
from chunk_utils.inspect import cog_metadata, describe_bytes, extract_tile

try:
    from chunk_utils.__version__ import __version__, __version_tuple__
except ImportError:
    __version__ = "0.0.0"
    __version_tuple__ = ("0", "0", "0")

__all__ = [
    "__version__",
    "__version_tuple__",
    "cog_metadata",
    "cog_to_zarr",
    "describe_bytes",
    "download_cog",
    "extract_tile",
]
