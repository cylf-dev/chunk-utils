"""Tests for chunk_utils.convert module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import xarray as xr

from chunk_utils.convert import _make_compressor, cog_to_zarr

OPEN_RASTERIO = "chunk_utils.convert.rioxarray.open_rasterio"


class TestMakeCompressor:
    def test_numcodecs_zlib_default_level(self) -> None:
        result = _make_compressor("numcodecs.zlib", None)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_numcodecs_zlib_custom_level(self) -> None:
        result = _make_compressor("numcodecs.zlib", 9)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_zstd_default_level(self) -> None:
        result = _make_compressor("zstd", None)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_zstd_custom_level(self) -> None:
        result = _make_compressor("zstd", 3)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_none_codec_returns_none(self) -> None:
        assert _make_compressor("none", None) is None

    def test_unknown_codec_raises(self) -> None:
        with pytest.raises(KeyError):
            _make_compressor("not_a_real_codec", None)


def _make_mock_dataset() -> MagicMock:
    """Build a mock xr.Dataset with data_vars and the expected interface."""
    ds = MagicMock(spec=xr.Dataset)
    ds.data_vars = {"band_1": MagicMock()}
    return ds


class TestCogToZarr:
    def test_with_codec(self, tmp_path: Path) -> None:
        mock_ds = _make_mock_dataset()

        with patch(OPEN_RASTERIO, return_value=mock_ds):
            cog_to_zarr(
                tmp_path / "in.tif", tmp_path / "out.zarr", codec="zstd", level=3
            )

        encoding = mock_ds.to_zarr.call_args.kwargs.get("encoding")
        assert encoding is not None
        assert "band_1" in encoding
        assert "compressors" in encoding["band_1"]

    def test_with_chunks(self, tmp_path: Path) -> None:
        mock_ds = _make_mock_dataset()

        with patch(OPEN_RASTERIO, return_value=mock_ds):
            cog_to_zarr(tmp_path / "in.tif", tmp_path / "out.zarr", chunks=[512, 512])

        encoding = mock_ds.to_zarr.call_args.kwargs.get("encoding")
        assert encoding is not None
        assert encoding["band_1"]["chunks"] == [512, 512]

    def test_close_called_on_error(self, tmp_path: Path) -> None:
        mock_ds = _make_mock_dataset()
        mock_ds.to_zarr.side_effect = RuntimeError("write failed")

        with (
            patch(OPEN_RASTERIO, return_value=mock_ds),
            pytest.raises(RuntimeError, match="write failed"),
        ):
            cog_to_zarr(tmp_path / "in.tif", tmp_path / "out.zarr")

        mock_ds.close.assert_called_once()

    def test_non_dataset_raises_type_error(self, tmp_path: Path) -> None:
        with (
            patch(OPEN_RASTERIO, return_value=MagicMock(spec=[])),
            pytest.raises(TypeError, match="Expected a Dataset"),
        ):
            cog_to_zarr(tmp_path / "in.tif", tmp_path / "out.zarr")
