# tools/generate_lemniscate.py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Kleurdefinities volgens jullie velden
COLORS = {
    "cyan": "#00BCD4",
    "blue": "#1E88E5",
    "purple": "#7E57C2",
    "magenta": "#EC407A",
    "green": "#43A047",
    "yellow": "#FDD835",
    "orange": "#FB8C00",
    "red": "#E53935",
    "pink": "#F48FB1",        # mimetisch verlangen
    "grey": "#9E9E9E",        # zelf / zelfde
    "chartreuse": "#7FFF00",  # hoop
}

# Lemniscaat van Bernoulli: (x^2 + y^2)^2 = a^2 (x^2 - y^2)
# Parametrisatie
def lemniscate_bernoulli(a=1.0, n=2000):
    t = np.linspace(0, 2*np.pi, n)
    denom = 1 + np.sin(t)**2
    x = (a*np.sqrt(2) * np.cos(t)) / denom
    y = (a*np.sqrt(2) * np.sin(t)*np.cos(t)) / denom
    return x, y

def draw(save_dir="exports", a=1.0):
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    x, y = lemniscate_bernoulli(a=a, n=4000)

    # Segmenten in 8 gelijke stukken → koppelen aan 8 velden
    fields = ["cyan","blue","purple","magenta","green","yellow","orange","red"]
    seg_len = len(x)//len(fields)

    # Basisfiguur
    fig = plt.figure(figsize=(8,8), dpi=160)
    ax = plt.gca()
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    # As (roze–grijs–chartreuse) als dunne gradient-achtige lijnen
    # We tekenen drie lagen: horizontaal (grijs), diagonaal links (roze), diagonaal rechts (chartreuse)
    r = a*1.2
    ax.plot([-r, r], [0, 0], lw=1.2, color=COLORS["grey"])
    ax.plot([-r, 0], [-r, r], lw=1.0, color=COLORS["pink"])
    ax.plot([0, r], [-r, r], lw=1.0, color=COLORS["chartreuse"])

    # Lemniscaat in 8 gekleurde segmenten
    for i, name in enumerate(fields):
        s = i*seg_len
        e = (i+1)*seg_len if i < len(fields)-1 else len(x)
        ax.plot(x[s:e], y[s:e], lw=3.0, color=COLORS[name])

    # Titeltje subtiel
    ax.text(0, -1.45*a, "The Praxis of Everything — bijzondere lus", ha="center", va="top", fontsize=10, color="#555")

    # Exporteer
    for ext in ("png","svg"):
        out = Path(save_dir)/f"lemniscate_praxis.{ext}"
        plt.savefig(out, bbox_inches="tight", pad_inches=0.1)
        print(f"Saved {out.resolve()}")

if __name__ == "__main__":
    draw()
