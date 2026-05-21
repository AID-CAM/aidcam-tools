"""Convert a dental mesh file (STL/OBJ/PLY) to a uniformly sampled point cloud.

CLI:
    aidcam-mesh-to-pc input.stl output.npz --n-points 10240
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import trimesh


def mesh_to_pointcloud(mesh_path: str | Path, n_points: int = 10240, seed: int | None = 0) -> np.ndarray:
    """Load a mesh and uniformly sample n_points from its surface.

    Args:
        mesh_path: Path to an STL, OBJ, or PLY file.
        n_points: Number of points to sample (default 10240, matches the AID·CAM
            crown-generation model's context size).
        seed: Random seed for reproducibility. Pass None for non-deterministic sampling.

    Returns:
        Array of shape (n_points, 3) with sampled point coordinates in the mesh's units.

    Raises:
        FileNotFoundError: if mesh_path does not exist.
        ValueError: if the mesh contains no faces.
    """
    mesh_path = Path(mesh_path)
    if not mesh_path.exists():
        raise FileNotFoundError(f"Mesh file not found: {mesh_path}")

    mesh = trimesh.load(mesh_path, force="mesh")
    if not hasattr(mesh, "faces") or len(mesh.faces) == 0:
        raise ValueError(f"Loaded object from {mesh_path} contains no faces")

    rng = np.random.default_rng(seed)
    points, _ = trimesh.sample.sample_surface_even(mesh, n_points, seed=int(rng.integers(0, 2**31 - 1)))
    return np.asarray(points, dtype=np.float32)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a dental mesh (STL/OBJ/PLY) to a point cloud (.npz)."
    )
    parser.add_argument("input", type=Path, help="Input mesh file (STL, OBJ, PLY).")
    parser.add_argument("output", type=Path, help="Output .npz file (contains array 'points').")
    parser.add_argument(
        "--n-points",
        type=int,
        default=10240,
        help="Number of points to sample (default: 10240).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed for reproducibility (default: 0).",
    )
    args = parser.parse_args()

    points = mesh_to_pointcloud(args.input, n_points=args.n_points, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output, points=points)
    print(f"Sampled {len(points):,} points from {args.input} → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
