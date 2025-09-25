from __future__ import annotations
import os
from typing import Optional, Sequence, Tuple

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (needed for 3D projection import side-effect)

BASIS_LABELS: Tuple[str, ...] = ("1", "e1", "e2", "e3", "e4", "e5", "e6", "e7")

def _cube_vertices() -> np.ndarray:
    """
    8 symmetrische punten als hoekpunten van een eenheids-kubus (±1,±1,±1).
    Dit geeft een natuurlijke, gelijkwaardige plaatsing voor de 8 basis-eenheden.
    """
    pts = []
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            for sz in (-1.0, 1.0):
                pts.append((sx, sy, sz))
    return np.array(pts, dtype=float)

def default_basis_layout(labels: Sequence[str] = BASIS_LABELS) -> Tuple[np.ndarray, Sequence[str]]:
    """
    Geeft (N×3)-coördinaten en labels terug voor de 8 basis-eenheden.

    Mapping:
      "1"  → ( +1, +1, +1 )
      "e1" → ( -1, +1, +1 )
      "e2" → ( +1, -1, +1 )
      "e3" → ( +1, +1, -1 )
      "e4" → ( -1, -1, +1 )
      "e5" → ( -1, +1, -1 )
      "e6" → ( +1, -1, -1 )
      "e7" → ( -1, -1, -1 )
    """
    # vaste, leesbare mapping (zodat labels niet ‘springen’ tussen runs)
    verts = np.array([
        (+1, +1, +1),  # 1
        (-1, +1, +1),  # e1
        (+1, -1, +1),  # e2
        (+1, +1, -1),  # e3
        (-1, -1, +1),  # e4
        (-1, +1, -1),  # e5
        (+1, -1, -1),  # e6
        (-1, -1, -1),  # e7
    ], dtype=float)
    return verts, labels

def plot_basis(save_path: Optional[str] = None, show: bool = False, title: str = "Octonion basis (cube layout)") -> plt.Figure:
    """
    Plot de 8 basis-eenheden in 3D (kubus-layout, dual aan een octaëder).
    - save_path: als gegeven, sla de figuur op (PNG/SVG, etc. afhankelijk van extensie).
    - show: True om plt.show() te doen (interactief).
    - return: matplotlib Figure (handig voor tests).
    """
    coords, labels = default_basis_layout()

    fig = plt.figure(figsize=(6, 6), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title(title)

    # punten
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], s=60, depthshade=True)

    # labels iets verschoven tekenen
    for (x, y, z), lab in zip(coords, labels):
        ax.text(x * 1.05, y * 1.05, z * 1.05, lab, fontsize=10, ha="center", va="center")

    # verbindingslijnen naar "1" (optioneel: geeft ‘ster’-structuur vanaf de scalair)
    origin_idx = 0
    for j in range(1, len(coords)):
        xs = [coords[origin_idx, 0], coords[j, 0]]
        ys = [coords[origin_idx, 1], coords[j, 1]]
        zs = [coords[origin_idx, 2], coords[j, 2]]
        ax.plot(xs, ys, zs, linewidth=1.0, alpha=0.5)

    # as-instellingen
    lim = 1.25
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150)

    if show:
        plt.show()

    return fig
