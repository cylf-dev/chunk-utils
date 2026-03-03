# chunk-utils

A toolkit for extracting and converting test data chunks from Cloud Optimized GeoTIFFs (COGs). Usable as both a CLI and a Python library.

## Install

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## CLI usage

After installing, the `chunk-utils` command is available:

```bash
chunk-utils --help
```

### Download a COG from a public URL

```bash
chunk-utils download https://example.com/image.tif
```

### Convert a local COG to Zarr v3

```bash
chunk-utils to-zarr image.tif image.zarr
chunk-utils to-zarr image.tif image.zarr --codec zstd --level 3
chunk-utils to-zarr image.tif image.zarr --chunks 1024 1024
```

### Print TIFF metadata

```bash
chunk-utils metadata image.tif
```

### Extract a single tile as raw bytes

```bash
chunk-utils extract-tile image.tif 0
```

## Library usage

chunk-utils can also be used as a Python library. All public functions are available from the top-level `chunk_utils` package:

```python
from pathlib import Path
from chunk_utils import cog_metadata, cog_to_zarr, describe_bytes, download_cog, extract_tile

# Download a COG
download_cog("https://example.com/image.tif", Path("image.tif"))

# Inspect metadata
for name, value in cog_metadata(Path("image.tif")):
    print(f"{name}: {value}")

# Extract a raw tile (compressed bytes as stored in the TIFF)
tile_bytes = extract_tile(Path("image.tif"), tile_index=0)

# Print size and SHA-256 hash
describe_bytes(tile_bytes)

# Convert a COG to Zarr v3
cog_to_zarr(Path("image.tif"), Path("image.zarr"))
cog_to_zarr(Path("image.tif"), Path("image.zarr"), codec="zstd", level=3)
```

## Acknowledgements

Partially supported by NASA-IMPACT VEDA project
