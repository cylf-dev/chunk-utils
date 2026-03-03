"""Tests for chunk_utils.cli module."""

from unittest.mock import patch

import pytest

from chunk_utils.cli import main


class TestCliToZarr:
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


class TestCliNoCommand:
    def test_no_subcommand_exits(self) -> None:
        with (
            patch("sys.argv", ["chunk-utils"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()
        assert exc_info.value.code == 2
