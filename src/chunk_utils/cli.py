"""CLI entry point for chunk-utils."""

import argparse
import sys
from pathlib import Path

from chunk_utils.convert import cog_to_zarr
from chunk_utils.download import download_cog
from chunk_utils.inspect import cog_metadata, extract_tile


def main() -> None:
    """Entry point for the chunk-utils CLI."""
    parser = argparse.ArgumentParser(
        prog="chunk-utils",
        description=(
            "Extract and convert test data chunks from Cloud Optimized GeoTIFFs (COGs)."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── download ──
    dl_parser = subparsers.add_parser(
        "download",
        help="Download a COG file from a public HTTPS URL.",
    )
    dl_parser.add_argument(
        "url",
        help="Public HTTPS URL of the COG file.",
    )
    dl_parser.add_argument(
        "output",
        nargs="?",
        default=None,
        type=Path,
        help="Local file path to save the downloaded COG. "
        "Defaults to ./<filename from URL>.",
    )

    # ── to-zarr ──
    cz_parser = subparsers.add_parser(
        "to-zarr",
        help="Convert a local COG file to Zarr v3 format.",
    )
    cz_parser.add_argument(
        "input",
        type=Path,
        help="Path to the input COG file.",
    )
    cz_parser.add_argument(
        "output",
        type=Path,
        help="Path for the output Zarr store directory.",
    )
    cz_parser.add_argument(
        "--codec",
        choices=["zstd", "zlib", "none"],
        default=None,
        help="Compression codec for the data variable.",
    )
    cz_parser.add_argument(
        "--level",
        type=int,
        default=None,
        help="Compression level (codec-specific).",
    )
    cz_parser.add_argument(
        "--chunks",
        type=int,
        nargs="+",
        default=None,
        help="Chunk dimensions, one per spatial axis "
        "(e.g. --chunks 1024 1024 for y/x).",
    )

    # ── metadata ──
    cm_parser = subparsers.add_parser(
        "metadata",
        help="Print TIFF metadata for the first page of a COG file.",
    )
    cm_parser.add_argument(
        "input",
        type=Path,
        help="Path to the local COG file.",
    )

    # ── extract-tile ──
    et_parser = subparsers.add_parser(
        "extract-tile",
        help="Extract raw bytes of a single tile from a COG.",
    )
    et_parser.add_argument(
        "input",
        type=Path,
        help="Path to the local COG file.",
    )
    et_parser.add_argument(
        "tile_index",
        type=int,
        help="Zero-based index of the tile to extract.",
    )
    et_parser.add_argument(
        "output",
        nargs="?",
        default=None,
        type=Path,
        help="Output file path. Defaults to <tile_index> next to the COG file.",
    )

    args = parser.parse_args()

    if args.command == "download":
        download_cog(args.url, args.output)
    elif args.command == "to-zarr":
        if args.level is not None and args.codec is None:
            sys.stderr.write("Warning: --level has no effect without --codec\n")
        cog_to_zarr(
            args.input,
            args.output,
            args.codec,
            args.level,
            args.chunks,
        )
    elif args.command == "metadata":
        for name, value in cog_metadata(args.input):
            sys.stdout.write(f"{name}: {value}\n")
    elif args.command == "extract-tile":
        extract_tile(args.input, args.tile_index, args.output)
