def plot_basis(*args, **kwargs):
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise RuntimeError(
            "matplotlib is vereist voor visualisaties. "
            "Installeer met: pip install 'a003558[viz]'"
        ) from e

    # voorbeeldplot — vervang met je eigen code
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 4], label="basis")
    ax.legend()
    plt.show()
