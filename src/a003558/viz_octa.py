# src/a003558/viz_octa.py
from __future__ import annotations
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np
from typing import Optional


def _cube_edges(size=2.0):
    s = size / 2.0
    pts = np.array([
        [-s, -s, -s], [ s, -s, -s], [ s,  s, -s], [-s,  s, -s],
        [-s, -s,  s], [ s, -s,  s], [ s,  s,  s], [-s,  s,  s],
    ])
    edges_idx = [
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7),
    ]
    return pts, edges_idx


def _octa_edges(size=2.0):
    s = size / 2.0
    pts = np.array([
        [ 0,  0,  s],
        [ 0,  0, -s],
        [ s,  0,  0],
        [-s,  0,  0],
        [ 0,  s,  0],
        [ 0, -s,  0],
    ])
    edges_idx = [
        (0,2),(0,4),(0,3),(0,5),
        (1,2),(1,4),(1,3),(1,5),
        (2,4),(4,3),(3,5),(5,2),
    ]
    return pts, edges_idx


def _edges_to_segments(pts, edges_idx):
    return [ (pts[i], pts[j]) for (i,j) in edges_idx ]


def plot_octahedron_and_cube(savepath: Optional[str] = None, cube_size=2.0, octa_size=2.0, offset=(0.0,0.0,0.0)):
    """
    3D-wireframe van kubus + octaëder. Returnt (fig, ax). Optioneel savepath.
    """
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(projection="3d")

    c_pts, c_edges = _cube_edges(cube_size)
    o_pts, o_edges = _octa_edges(octa_size)

    # offset de octahedron, zodat ze niet exact samenvallen
    o_pts = o_pts + np.array(offset, dtype=float)

    c_segs = _edges_to_segments(c_pts, c_edges)
    o_segs = _edges_to_segments(o_pts, o_edges)

    lc1 = Line3DCollection(c_segs, colors="C0", linewidths=1.5, alpha=0.9)
    lc2 = Line3DCollection(o_segs, colors="C3", linewidths=1.5, alpha=0.9)

    ax.add_collection3d(lc1)
    ax.add_collection3d(lc2)

    all_pts = np.vstack([c_pts, o_pts])
    mins = all_pts.min(axis=0)
    maxs = all_pts.max(axis=0)
    center = (mins + maxs)/2.0
    span = float((maxs - mins).max()) * 0.6

    ax.set_xlim(center[0]-span, center[0]+span)
    ax.set_ylim(center[1]-span, center[1]+span)
    ax.set_zlim(center[2]-span, center[2]+span)
    ax.set_box_aspect((1,1,1))
    ax.set_title("Octahedron + Cube (wireframe)")

    if savepath:
        fig.savefig(savepath, dpi=150, bbox_inches="tight")
    return fig, ax
