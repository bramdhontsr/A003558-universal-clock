# src/a003558/viz.py
from __future__ import annotations
import matplotlib
matplotlib.use("Agg")  # headless voor CI/pytest
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional, Sequence


def plot_basis(savepath: Optional[str] = None, vectors: Optional[Sequence[np.ndarray]] = None):
    """
    Eenvoudige 2D-visualisatie van basisvectoren (of willekeurige pijlen).
    - Als 'vectors' None is, teken 7 stralen onder vaste hoeken.
    - Returnt (fig, ax). Als 'savepath' gegeven is, sla op.
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

    if vectors is None:
        # 7 stralen (denk aan e1..e7), unit circle
        angles = np.linspace(0, 2*np.pi, 8, endpoint=False)[1:]  # 7 pijlen
        vectors = [np.array([np.cos(a), np.sin(a)]) for a in angles]

    for v in vectors:
        v = np.asarray(v).reshape(-1)
        if v.size != 2:
            v = v[:2]
        ax.arrow(0, 0, v[0], v[1], head_width=0.05, length_includes_head=True, alpha=0.8)

    ax.add_artist(plt.Circle((0, 0), 1.0, fill=False, alpha=0.2))
    ax.set_title("Basis/stralen (schets)")
    if savepath:
        fig.savefig(savepath, dpi=150, bbox_inches="tight")
    return fig, ax
