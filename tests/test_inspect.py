"""Tests for chunk_utils.inspect module."""

from hashlib import sha256
from pathlib import Path

import pytest

from chunk_utils.inspect import cog_metadata, describe_bytes, extract_tile


class TestCogMetadata:
    def test_returns_list_of_tuples(self, tiled_tiff: Path) -> None:
        result = cog_metadata(tiled_tiff)
        assert isinstance(result, list)
        assert len(result) > 0
        for name, _value in result:
            assert isinstance(name, str)

    def test_contains_expected_tags(self, tiled_tiff: Path) -> None:
        result = cog_metadata(tiled_tiff)
        tag_names = {name for name, _ in result}
        assert "ImageWidth" in tag_names
        assert "ImageLength" in tag_names
        assert "TileWidth" in tag_names
        assert "TileLength" in tag_names

    def test_image_dimensions(self, tiled_tiff: Path) -> None:
        result = dict(cog_metadata(tiled_tiff))
        assert result["ImageWidth"] == 32
        assert result["ImageLength"] == 16


class TestExtractTile:
    def test_returns_bytes(self, tiled_tiff: Path) -> None:
        raw = extract_tile(tiled_tiff, 0)
        assert isinstance(raw, bytes)
        assert len(raw) > 0

    def test_tile_index_1_returns_bytes(self, tiled_tiff: Path) -> None:
        raw = extract_tile(tiled_tiff, 1)
        assert isinstance(raw, bytes)
        assert len(raw) > 0

    def test_different_tiles_differ(self, tiled_tiff: Path) -> None:
        tile0 = extract_tile(tiled_tiff, 0)
        tile1 = extract_tile(tiled_tiff, 1)
        assert tile0 != tile1

    def test_out_of_range_raises(self, tiled_tiff: Path) -> None:
        with pytest.raises(IndexError, match="out of range"):
            extract_tile(tiled_tiff, 99)

    def test_negative_index_raises(self, tiled_tiff: Path) -> None:
        with pytest.raises(IndexError, match="out of range"):
            extract_tile(tiled_tiff, -1)

    def test_writes_to_output_path(self, tiled_tiff: Path, tmp_path: Path) -> None:
        output = tmp_path / "tile_output"
        raw = extract_tile(tiled_tiff, 0, output_path=output)
        assert output.exists()
        assert output.read_bytes() == raw

    def test_creates_parent_dirs(self, tiled_tiff: Path, tmp_path: Path) -> None:
        output = tmp_path / "sub" / "dir" / "tile"
        extract_tile(tiled_tiff, 0, output_path=output)
        assert output.exists()


class TestDescribeBytes:
    def test_prints_size_and_hash(self, capsys: pytest.CaptureFixture[str]) -> None:
        describe_bytes(b"hello world")
        captured = capsys.readouterr()
        assert "size:" in captured.out
        assert "MiB" in captured.out
        assert "sha256:" in captured.out

    def test_hash_is_correct(self, capsys: pytest.CaptureFixture[str]) -> None:
        data = b"deterministic test data"
        expected_hash = sha256(data).hexdigest()
        describe_bytes(data)
        captured = capsys.readouterr()
        assert expected_hash in captured.out

    def test_size_is_correct(self, capsys: pytest.CaptureFixture[str]) -> None:
        data = b"\x00" * (2**20)  # exactly 1 MiB
        describe_bytes(data)
        captured = capsys.readouterr()
        assert "1.000 MiB" in captured.out
