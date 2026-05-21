"""Distance metrics for point cloud comparison.

Common metrics in dental ML evaluation:
- Chamfer Distance (L1, L2) — average nearest-neighbor distance between two sets
- Hausdorff Distance — max nearest-neighbor distance (worst-case error)

All functions accept arrays of shape (N, 3) and (M, 3) and return distances
in the same units as the input (millimeters, by convention, for dental data).
"""

from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree


def chamfer_l1(a: np.ndarray, b: np.ndarray) -> float:
    """Symmetric mean L1 (Manhattan) Chamfer distance between two point sets.

    Args:
        a: array of shape (N, 3)
        b: array of shape (M, 3)

    Returns:
        Mean of the symmetric L1 nearest-neighbor distances, in the same units as the input.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    tree_a = cKDTree(a)
    tree_b = cKDTree(b)
    # For L1 nearest neighbor, query with p=1
    d_ab, _ = tree_b.query(a, p=1)
    d_ba, _ = tree_a.query(b, p=1)
    return float((d_ab.mean() + d_ba.mean()) / 2.0)


def chamfer_l2(a: np.ndarray, b: np.ndarray) -> float:
    """Symmetric mean L2 (Euclidean) Chamfer distance between two point sets.

    Args:
        a: array of shape (N, 3)
        b: array of shape (M, 3)

    Returns:
        Mean of the symmetric L2 nearest-neighbor distances, in the same units as the input.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    tree_a = cKDTree(a)
    tree_b = cKDTree(b)
    d_ab, _ = tree_b.query(a, p=2)
    d_ba, _ = tree_a.query(b, p=2)
    return float((d_ab.mean() + d_ba.mean()) / 2.0)


def hausdorff(a: np.ndarray, b: np.ndarray) -> float:
    """Symmetric Hausdorff distance — the worst-case nearest-neighbor distance.

    Args:
        a: array of shape (N, 3)
        b: array of shape (M, 3)

    Returns:
        Symmetric Hausdorff distance in the same units as the input.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    tree_a = cKDTree(a)
    tree_b = cKDTree(b)
    d_ab, _ = tree_b.query(a, p=2)
    d_ba, _ = tree_a.query(b, p=2)
    return float(max(d_ab.max(), d_ba.max()))
