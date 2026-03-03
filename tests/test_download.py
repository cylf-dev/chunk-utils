"""Tests for chunk_utils.download module."""

import io
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from chunk_utils.download import download_cog

URLOPEN = "chunk_utils.download.urllib.request.urlopen"


def _fake_response(data: bytes) -> MagicMock:
    """Build a mock that acts as a urllib response context manager."""
    resp = MagicMock()
    resp.__enter__ = lambda s: io.BytesIO(data)
    resp.__exit__ = MagicMock(return_value=False)
    return resp


class TestDownloadCog:
    def test_downloads_to_explicit_path(self, tmp_path: Path) -> None:
        content = b"fake tiff content"
        output = tmp_path / "my_image.tif"

        with patch(URLOPEN, return_value=_fake_response(content)):
            download_cog("https://example.com/image.tif", output)

        assert output.exists()
        assert output.read_bytes() == content

    def test_extracts_filename_from_url(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        content = b"fake tiff content"
        monkeypatch.chdir(tmp_path)

        with patch(URLOPEN, return_value=_fake_response(content)):
            download_cog("https://example.com/data/scene.tif")

        assert (tmp_path / "scene.tif").exists()
        assert (tmp_path / "scene.tif").read_bytes() == content

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        output = tmp_path / "a" / "b" / "c" / "file.tif"

        with patch(URLOPEN, return_value=_fake_response(b"data")):
            download_cog("https://example.com/file.tif", output)

        assert output.exists()

    def test_empty_filename_in_url_raises(self) -> None:
        with pytest.raises(ValueError, match="Cannot extract filename"):
            download_cog("https://example.com/")
