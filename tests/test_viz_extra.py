import pathlib
from a003558.viz import plot_basis, plot_cycle
from a003558.viz_octa import plot_octahedron

def test_plot_cycle_smoke(tmp_path: pathlib.Path):
    """
    Smoke-test: plot_cycle moet zonder exception werken en een figuur opslaan.
    """
    out_png = tmp_path / "cycle.png"
    fig = plot_cycle(8, save_path=str(out_png), show=False, title="Cycle Smoke")
    assert out_png.exists()
    assert fig is not None

def test_plot_octahedron_smoke(tmp_path: pathlib.Path):
    """
    Smoke-test: plot_octahedron moet zonder exception werken en een figuur opslaan.
    """
    out_png = tmp_path / "octa.png"
    fig = plot_octahedron(save_path=str(out_png), show=False)
    assert out_png.exists()
    assert fig is not None

def test_plot_basis_again(tmp_path: pathlib.Path):
    """
    Extra check van plot_basis (variant).
    """
    out_png = tmp_path / "basis2.png"
    fig = plot_basis(16, save_path=str(out_png), show=False, title="Basis Again")
    assert out_png.exists()
    assert fig is not None
