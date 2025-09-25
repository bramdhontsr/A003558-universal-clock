from __future__ import annotations
import os
from typing import Optional, Sequence, Tuple

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from .viz import BASIS_LABELS, default_basis_layout  # hergebruik labels + mapping

# --- Geometrie helpers ---

def octahedron_vertices_edges() -> Tuple[np.ndarray, list[tuple[int,int]]]:
    """
    Standaard octaëder (dual van de kubus):
    6 hoekpunten op de assen: (±1,0,0), (0,±1,0), (0,0,±1)
    Randen verbinden elke +as met de 4 orthogonale ±assen (geen antipode).
    """
    V = np.array([
        (+1, 0, 0), (-1, 0, 0),
        (0, +1, 0), (0, -1, 0),
        (0, 0, +1), (0, 0, -1)
    ], dtype=float)
    # Randen van de octaëder: handmatige lijst
    E = [
        (0,2),(0,3),(0,4),(0,5),  # +x met ±y, ±z
        (1,2),(1,3),(1,4),(1,5),  # -x met ±y, ±z
        (2,4),(2,5),(3,4),(3,5)   # ±y met ±z
    ]
    return V, E

def cube_edges_from_vertices(N: int = 8) -> list[tuple[int,int]]:
    """
    Edges voor een eenheidskubus zoals in default_basis_layout:
    Indices in default mapping:
      0: (+1,+1,+1)   1: (-1,+1,+1)   2: (+1,-1,+1)   3: (+1,+1,-1)
      4: (-1,-1,+1)   5: (-1,+1,-1)   6: (+1,-1,-1)   7: (-1,-1,-1)
    Maak edges tussen hoekpunten die op exact één coordinaat verschillen in teken.
    """
    E = []
    # brute-force: connecteer paren met Manhattan-afstand 2 (verschil exact op één as)
    # in onze ±1-coordinates betekent dat: som(|xi - yi|) == 2
    for i in range(N):
        for j in range(i+1, N):
            # We genereren edges later met coord data, maar hier kennen we de layout pas in plot
            E.append((i, j))
    return E  # we filteren ze op afstand in plot-functie

# --- Plot ---

def plot_octahedron_and_cube(
    save_path: Optional[str] = None,
    show: bool = False,
    title: str = "Octahedron (dual) & Octonion basis (cube)"
) -> plt.Figure:
    """
    Plot in 3D: octaëder (6 vertices) + duale kubus (8 vertices = basis octonions).
    """
    # data
    V_oct, E_oct = octahedron_vertices_edges()
    V_cube, labels = default_basis_layout()

    fig = plt.figure(figsize=(7.5, 7.5), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title(title)

    # --- Octahedron ---
    ax.scatter(V_oct[:,0], V_oct[:,1], V_oct[:,2], s=50, c="#2D7DD2", label="Octahedron vertices")
    for (i,j) in E_oct:
        xs = [V_oct[i,0], V_oct[j,0]]
        ys = [V_oct[i,1], V_oct[j,1]]
        zs = [V_oct[i,2], V_oct[j,2]]
        ax.plot(xs, ys, zs, color="#2D7DD2", linewidth=1.5, alpha=0.8)

    # --- Cube (octonion basis) ---
    ax.scatter(V_cube[:,0], V_cube[:,1], V_cube[:,2], s=60, c="#F46036", label="Octonion basis (cube)")
    for (x,y,z), lab in zip(V_cube, labels):
        ax.text(x*1.07, y*1.07, z*1.07, lab, fontsize=9, ha="center", va="center", color="#333333")

    # Filter en teken echte kubusranden (paren met |Δ|1 op exact één as)
    def manhattan(p, q): return np.abs(p-q).sum()
    for i in range(len(V_cube)):
        for j in range(i+1, len(V_cube)):
            if np.isclose(manhattan(V_cube[i], V_cube[j]), 2.0):  # ±1-verschil op één coord
                xs = [V_cube[i,0], V_cube[j,0]]
                ys = [V_cube[i,1], V_cube[j,1]]
                zs = [V_cube[i,2], V_cube[j,2]]
                ax.plot(xs, ys, zs, color="#F46036", linewidth=1.2, alpha=0.6)

    # As-instellingen
    lim = 1.35
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1,1,1))
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.legend(loc="upper left")

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150)

    if show:
        plt.show()

    return fig
