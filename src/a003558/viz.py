import matplotlib.pyplot as plt
import numpy as np


def plot_basis(save_path: str | None = None, show: bool = True, title: str | None = None):
    """Plot de standaardbasis in het vlak."""
    fig, ax = plt.subplots()
    ax.quiver([0, 0], [0, 0], [1, 0], [0, 1], angles="xy", scale_units="xy", scale=1, color=["r", "g"])
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_aspect("equal")
    if title:
        ax.set_title(title)
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def plot_cycle(points, save_path: str | None = None, show: bool = True, title: str | None = None):
    """Plot een gesloten cyclus van punten in het vlak."""
    pts = np.array(points)
    fig, ax = plt.subplots()
    ax.plot(pts[:, 0], pts[:, 1], "o-", lw=1.5)
    ax.set_aspect("equal")
    if title:
        ax.set_title(title)
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig
