def plot_basis(n: int = 12):
    """
    Eenvoudig voorbeeldplot voor de 'universele klok'.
    Vereist matplotlib; installeer met: pip install "a003558[viz]"

    Parameters
    ----------
    n : int
        Aantal punten/segmenten om te plotten (voorbeeld).
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise RuntimeError(
            "matplotlib is vereist voor visualisaties. "
            "Installeer met: pip install 'a003558[viz]'"
        ) from e

    # Voorbeelddata (placeholder) – vervang door jouw echte visualisatie
    xs = list(range(n))
    ys = [i * i for i in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, ys, label="basis")
    ax.set_title("A003558 Universal Clock – voorbeeldplot")
    ax.set_xlabel("t")
    ax.set_ylabel("f(t)")
    ax.legend()
    plt.show()
