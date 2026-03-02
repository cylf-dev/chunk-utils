# chunk-utils

A CLI utility for extracting and converting test data chunks from Cloud Optimized GeoTIFFs (COGs).

## Install

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

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

## Acknowledgements

Partially supported by NASA-IMPACT VEDA project
