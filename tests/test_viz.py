import os
import pathlib

import matplotlib
matplotlib.use("Agg")  # headless backend voor CI/pytest
import matplotlib.pyplot as plt

from a003558.viz import plot_basis

def test_plot_basis_smoke(tmp_path: pathlib.Path):
    """
    Smoke-test: de plot moet zonder exceptions renderen en een bestand kunnen wegschrijven.
    """
    out_png = tmp_path / "basis.png"
    fig = plot_basis(save_path=str(out_png), show=False, title="Test Plot")
    assert fig is not None
    plt.close(fig)

    assert out_png.exists()
    assert out_png.stat().st_size > 0
