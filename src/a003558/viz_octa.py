import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

def plot_octahedron_and_cube(save_path: str | None = None, show: bool = False, title: str = "Octahedron & Cube", **kwargs):
    # backward-compat shim
    if save_path is None and "savepath" in kwargs:
        save_path = kwargs.pop("savepath")

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title(title)

    # --- draw cube ---
    import numpy as np
    r = [-1, 1]
    for s, e in [
        ((r[0], r[0], r[0]), (r[1], r[0], r[0])),
        ((r[0], r[0], r[0]), (r[0], r[1], r[0])),
        ((r[0], r[0], r[0]), (r[0], r[0], r[1])),
        ((r[1], r[1], r[1]), (r[0], r[1], r[1])),
        ((r[1], r[1], r[1]), (r[1], r[0], r[1])),
        ((r[1], r[1], r[1]), (r[1], r[1], r[0])),
        ((r[0], r[1], r[0]), (r[1], r[1], r[0])),
        ((r[0], r[1], r[0]), (r[0], r[1], r[1])),
        ((r[1], r[0], r[0]), (r[1], r[1], r[0])),
        ((r[1], r[0], r[0]), (r[1], r[0], r[1])),
        ((r[0], r[0], r[1]), (r[1], r[0], r[1])),
        ((r[0], r[0], r[1]), (r[0], r[1], r[1])),
    ]:
        s = np.array(s); e = np.array(e)
        ax.plot(*zip(s, e))

    # --- draw octahedron ---
    verts = np.array([
        (1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)
    ], float)
    edges = [
        (0,2),(0,3),(0,4),(0,5),
        (1,2),(1,3),(1,4),(1,5),
        (2,4),(2,5),(3,4),(3,5),
    ]
    for i,j in edges:
        ax.plot(*zip(verts[i], verts[j]))

    ax.set_box_aspect((1,1,1))
    ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2); ax.set_zlim(-1.2,1.2)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    return fig
