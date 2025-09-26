import pathlib
import pytest
from a003558.viz import plot_cycle

@pytest.mark.parametrize("length", [6, 12])
def test_plot_cycle_smoke(tmp_path: pathlib.Path, length: int):
    """
    Smoke-test: plot_cycle moet figuur renderen en opslaan zonder exception.
    """
    out = tmp_path / f"cycle_{length}.png"
    fig = plot_cycle(length=length, save_path=str(out), show=False, title=f"Cycle {length}")
    assert out.exists()
    assert fig is not None
