"""Tests for chunk_utils.cli module."""

from pathlib import Path
from unittest.mock import patch

import pytest

from chunk_utils.cli import main


class TestCliDownload:
    def test_download_with_url_only(self) -> None:
        with (
            patch("sys.argv", ["chunk-utils", "download", "https://example.com/f.tif"]),
            patch("chunk_utils.cli.download_cog") as mock,
        ):
            main()
            mock.assert_called_once_with("https://example.com/f.tif", None)

    def test_download_with_output(self, tmp_path: Path) -> None:
        out = str(tmp_path / "out.tif")
        with (
            patch(
                "sys.argv",
                ["chunk-utils", "download", "https://example.com/f.tif", out],
            ),
            patch("chunk_utils.cli.download_cog") as mock,
        ):
            main()
            mock.assert_called_once_with("https://example.com/f.tif", Path(out))


class TestCliToZarr:
    def test_basic_to_zarr(self) -> None:
        with (
            patch("sys.argv", ["chunk-utils", "to-zarr", "in.tif", "out.zarr"]),
            patch("chunk_utils.cli.cog_to_zarr") as mock,
        ):
            main()
            mock.assert_called_once_with(
                Path("in.tif"), Path("out.zarr"), None, None, None
            )

    def test_to_zarr_with_codec_and_level(self) -> None:
        with (
            patch(
                "sys.argv",
                [
                    "chunk-utils",
                    "to-zarr",
                    "in.tif",
                    "out.zarr",
                    "--codec",
                    "zstd",
                    "--level",
                    "3",
                ],
            ),
            patch("chunk_utils.cli.cog_to_zarr") as mock,
        ):
            main()
            mock.assert_called_once_with(
                Path("in.tif"), Path("out.zarr"), "zstd", 3, None
            )

    def test_to_zarr_with_chunks(self) -> None:
        with (
            patch(
                "sys.argv",
                [
                    "chunk-utils",
                    "to-zarr",
                    "in.tif",
                    "out.zarr",
                    "--chunks",
                    "1024",
                    "1024",
                ],
            ),
            patch("chunk_utils.cli.cog_to_zarr") as mock,
        ):
            main()
            mock.assert_called_once_with(
                Path("in.tif"), Path("out.zarr"), None, None, [1024, 1024]
            )

    def test_level_without_codec_warns(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        with (
            patch(
                "sys.argv",
                ["chunk-utils", "to-zarr", "in.tif", "out.zarr", "--level", "5"],
            ),
            patch("chunk_utils.cli.cog_to_zarr"),
        ):
            main()
            captured = capsys.readouterr()
            assert "level has no effect without --codec" in captured.err


class TestCliMetadata:
    def test_metadata_prints_tags(self, capsys: pytest.CaptureFixture[str]) -> None:
        tags = [("ImageWidth", 256), ("ImageLength", 256)]
        with (
            patch("sys.argv", ["chunk-utils", "metadata", "image.tif"]),
            patch("chunk_utils.cli.cog_metadata", return_value=tags),
        ):
            main()
            captured = capsys.readouterr()
            assert "ImageWidth: 256" in captured.out
            assert "ImageLength: 256" in captured.out


class TestCliExtractTile:
    def test_extract_tile_default_output(self) -> None:
        with (
            patch(
                "sys.argv",
                ["chunk-utils", "extract-tile", "data/image.tif", "0"],
            ),
            patch("chunk_utils.cli.extract_tile") as mock,
        ):
            main()
            mock.assert_called_once_with(Path("data/image.tif"), 0, Path("data/0"))

    def test_extract_tile_explicit_output(self) -> None:
        with (
            patch(
                "sys.argv",
                ["chunk-utils", "extract-tile", "image.tif", "0", "tile_0.bin"],
            ),
            patch("chunk_utils.cli.extract_tile") as mock,
        ):
            main()
            mock.assert_called_once_with(Path("image.tif"), 0, Path("tile_0.bin"))


class TestCliNoCommand:
    def test_no_subcommand_exits(self) -> None:
        with (
            patch("sys.argv", ["chunk-utils"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()
        assert exc_info.value.code == 2
