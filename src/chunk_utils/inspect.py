"""Inspect and extract data from COG files."""

import sys
from hashlib import sha256
from pathlib import Path

import tifffile


def cog_metadata(input_path: Path) -> list[tuple[str, object]]:
    """Return TIFF tags for the first page of a COG file."""
    with tifffile.TiffFile(input_path) as tif:
        page = tif.pages.first
        return [(tag.name, tag.value) for tag in page.tags.values()]


def extract_tile(
    input_path: Path,
    tile_index: int,
    output_path: Path | None = None,
) -> bytes:
    """Extract raw bytes of a single tile from the first page of a COG.

    Returns the raw tile bytes. If output_path is provided, also writes
    them to that file.
    """
    with tifffile.TiffFile(input_path) as tif:
        page = tif.pages.first

        offsets = page.tags["TileOffsets"].value
        byte_counts = page.tags["TileByteCounts"].value

        if tile_index < 0 or tile_index >= len(offsets):
            msg = f"Tile index {tile_index} out of range [0, {len(offsets) - 1}]"
            raise IndexError(msg)

        offset = offsets[tile_index]
        count = byte_counts[tile_index]

    with input_path.open("rb") as f:
        f.seek(offset)
        raw_bytes = f.read(count)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("wb") as out:
            out.write(raw_bytes)

    return raw_bytes


def describe_bytes(b: bytes) -> None:
    """Print size and SHA-256 digest of a byte string."""
    h = sha256(b)
    sys.stdout.write(f"size: {len(b) / 2**20:.3f} MiB | sha256: {h.hexdigest()}\n")
