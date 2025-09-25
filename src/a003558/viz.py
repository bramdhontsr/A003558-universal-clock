import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_basis(save_path: str | None = None, show: bool = False, title: str = "Basisplot", **kwargs):
    """
    Render a simple 2D/3D basis plot (headless by default).
    """
    # backward-compat shim
    if save_path is None and "savepath" in kwargs:
        save_path = kwargs.pop("savepath")

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.plot([0, 1, 2], [0, 1, 0], lw=2)
    ax.grid(True)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    return fig