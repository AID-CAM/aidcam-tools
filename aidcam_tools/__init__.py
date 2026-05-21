"""aidcam-tools — small Python utilities for dental 3D files and AI-CAD evaluation."""

from aidcam_tools.metrics import chamfer_l1, chamfer_l2, hausdorff
from aidcam_tools.mesh_to_pointcloud import mesh_to_pointcloud
from aidcam_tools.fdi import (
    is_molar,
    is_premolar,
    is_anterior,
    quadrant,
    opposite,
    contralateral,
)

__version__ = "0.1.0"
__all__ = [
    "chamfer_l1",
    "chamfer_l2",
    "hausdorff",
    "mesh_to_pointcloud",
    "is_molar",
    "is_premolar",
    "is_anterior",
    "quadrant",
    "opposite",
    "contralateral",
]
