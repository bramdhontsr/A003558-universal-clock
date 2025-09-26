import matplotlib.pyplot as plt
import numpy as np


def plot_octahedron(save_path: str | None = None, show: bool = True, title: str | None = None):
    """Plot een octaëder in 3D."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Definieer hoekpunten van een octaëder
    r = [-1, 1]
    vertices = [(x, 0, 0) for x in r] + [(0, y, 0) for y in r] + [(0, 0, z) for z in r]

    # Plot randen
    edges = [
        ((r[0], 0, 0), (0, r[0], 0)),
        ((r[0], 0, 0), (0, r[1], 0)),
        ((r[0], 0, 0), (0, 0, r[0])),
        ((r[0], 0, 0), (0, 0, r[1])),
        ((r[1], 0, 0), (0, r[0], 0)),
        ((r[1], 0, 0), (0, r[1], 0)),
        ((r[1], 0, 0), (0, 0, r[0])),
        ((r[1], 0, 0), (0, 0, r[1])),
        ((0, r[0], 0), (0, 0, r[0])),
        ((0, r[0], 0), (0, 0, r[1])),
        ((0, r[1], 0), (0, 0, r[0])),
        ((0, r[1], 0), (0, 0, r[1])),
    ]
    for s, e in edges:
        s = np.array(s)
        e = np.array(e)
        ax.plot(*zip(s, e), color="b")

    ax.set_box_aspect((1, 1, 1))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-1.2, 1.2)
    if title:
        ax.set_title(title)
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig
