"""Shared fixtures for chunk-utils tests."""

from pathlib import Path

import numpy as np
import pytest
import tifffile


@pytest.fixture
def tiled_tiff(tmp_path: Path) -> Path:
    """Create a minimal tiled TIFF: 32x16 uint16 with 16x16 tiles (2 tiles)."""
    path = tmp_path / "test.tif"
    data = np.arange(32 * 16, dtype=np.uint16).reshape(16, 32)
    tifffile.imwrite(path, data, tile=(16, 16))
    return path
