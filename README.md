# aidcam-tools

Small, dependency-light Python utilities for working with dental 3D
files and evaluating AI dental CAD methods.

Released under MIT by the [AID·CAM](https://aid-cam.com) team.

---

## Why this exists

Public benchmarks for AI dental CAD are slowly emerging — but
standardized tooling to use them isn't. `aidcam-tools` is our small
contribution: a set of plain Python scripts that we found ourselves
writing for our own crown-generation work, packaged so anyone else
working on dental ML can skip writing them too.

This repo is intentionally narrow. It contains no model code, no AID·CAM
proprietary architecture, and no clinical data. It is dental file
plumbing — the boring useful kind.

## What's included

| Module | What it does |
|--------|--------------|
| `aidcam_tools.mesh_to_pointcloud` | Load STL/OBJ/PLY meshes via trimesh; uniformly sample N points from the surface; save to `.npz`. |
| `aidcam_tools.metrics` | Chamfer distance (L1, L2), symmetric Hausdorff distance, per-tooth-class breakdown for FDI numbering. |
| `aidcam_tools.fdi` | FDI tooth-numbering helpers: quadrant, position, is_molar, is_anterior, opposite, contralateral. |
| `aidcam_tools.eval_intellident` | Evaluation harness for the public 78-case margin-line benchmark from Intellident Dentaire (CBM 2025). |

## Install

```bash
pip install -e .
```

Requires Python ≥ 3.10. Dependencies: `numpy`, `trimesh`, `scipy`.

## Examples

### Convert a dental mesh to a point cloud

```bash
aidcam-mesh-to-pc input_prep.stl prep_points.npz --n-points 10240
```

### Compare two crown meshes

```python
import numpy as np
from aidcam_tools.metrics import chamfer_l2, hausdorff

a = np.load("crown_a.npz")["points"]
b = np.load("crown_b.npz")["points"]

print(f"Chamfer L2: {chamfer_l2(a, b):.4f} mm")
print(f"Hausdorff: {hausdorff(a, b):.4f} mm")
```

### Work with FDI tooth numbers

```python
from aidcam_tools.fdi import is_molar, opposite, quadrant

is_molar(16)       # True
opposite(11)       # 41  (upper right central → lower right central)
quadrant(35)       # 3   (lower-left quadrant)
```

### Evaluate predicted margin lines against the Intellident benchmark

```bash
git clone https://github.com/intellident-ai/public-datasets
aidcam-eval-intellident \
  --benchmark public-datasets/ \
  --predictions my_predictions/ \
  --output report.json
```

## License

MIT. See `LICENSE`.

## Citation

If you use these utilities in published work, a citation is appreciated
but not required:

```
@software{aidcam_tools_2026,
  author       = {AID·CAM},
  title        = {aidcam-tools: utilities for AI dental CAD},
  year         = {2026},
  url          = {https://github.com/AID-CAM/aidcam-tools},
}
```

## Contributing

Issues and pull requests welcome. The scope of this repo is intentionally
narrow — utility scripts for dental ML. We're not looking to grow it
into a full framework. If your contribution fits the "small dependency-
light tools" bar, please open an issue first to discuss.

## Maintainers

- [@crosswi](https://github.com/crosswi) — Cameron Cross, AID·CAM
- [@massimovenezia](https://github.com/massimovenezia) — Massimo Venezia, AID·CAM

For questions, contact [info@aid-cam.com](mailto:info@aid-cam.com).
