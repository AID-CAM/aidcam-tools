"""Tests for distance metrics."""

import numpy as np
import pytest

from aidcam_tools.metrics import chamfer_l1, chamfer_l2, hausdorff


@pytest.fixture
def identical_clouds():
    rng = np.random.default_rng(0)
    return rng.random((100, 3))


def test_chamfer_l2_identical(identical_clouds):
    a = identical_clouds
    assert chamfer_l2(a, a) == pytest.approx(0.0, abs=1e-9)


def test_chamfer_l1_identical(identical_clouds):
    a = identical_clouds
    assert chamfer_l1(a, a) == pytest.approx(0.0, abs=1e-9)


def test_hausdorff_identical(identical_clouds):
    a = identical_clouds
    assert hausdorff(a, a) == pytest.approx(0.0, abs=1e-9)


def test_chamfer_l2_translation():
    a = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    b = a + np.array([0.0, 0.0, 1.0])
    # Each point's nearest neighbor in the other cloud is exactly 1.0 away.
    assert chamfer_l2(a, b) == pytest.approx(1.0, rel=1e-6)


def test_hausdorff_worst_case():
    a = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    b = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [5.0, 0.0, 0.0]])
    # The point [5, 0, 0] in b is 4 mm from its nearest neighbor in a.
    assert hausdorff(a, b) == pytest.approx(4.0, rel=1e-6)
