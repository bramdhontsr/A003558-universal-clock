# tools/generate_octahedron.py
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Kleurpalet (8 velden + as)
COLORS = {
    "cyan": "#00BCD4", "blue": "#1E88E5", "purple": "#7E57C2", "magenta": "#EC407A",
    "green": "#43A047", "yellow": "#FDD835", "orange": "#FB8C00", "red": "#E53935",
    "pink": "#F48FB1", "grey": "#9E9E9E", "chartreuse": "#7FFF00",
}

# Octaëder: 6 punten, 8 driehoeksvlakken
V = np.array([
    [ 1, 0, 0], [-1, 0, 0],
    [ 0, 1, 0], [ 0,-1, 0],
    [ 0, 0, 1], [ 0, 0,-1],
], dtype=float)

FACES = [
    [0,2,4], [2,1,4], [1,3,4], [3,0,4],  # boven (z=+)
    [2,0,5], [1,2,5], [3,1,5], [0,3,5],  # onder (z=-)
]
FIELDS = ["cyan","blue","purple","magenta","green","yellow","orange","red"]

def rot_xyz(ax, ay, az):
    cx, sx = np.cos(ax), np.sin(ax)
    cy, sy = np.cos(ay), np.sin(ay)
    cz, sz = np.cos(az), np.sin(az)
    Rx = np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])
    Ry = np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])
    Rz = np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
    return Rz @ Ry @ Rx

def project(points, R=None, scale=1.0):
    P = points.copy()
    if R is not None:
        P = (R @ P.T).T
    # orthografisch: drop z
    return P[:,:2] * scale

def draw(save_dir="exports", angle=(0.9, 0.6, 0.3), scale=2.2):
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    R = rot_xyz(*angle)
    pts2 = project(V, R=R, scale=scale)

    fig = plt.figure(figsize=(8,8), dpi=160)
    ax = plt.gca()
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    # As-lijnen (roze–grijs–chartreuse)
    r = 3.2
    ax.plot([-r, r],[0,0], lw=1.2, color=COLORS["grey"])
    ax.plot([-r, 0],[-r, r], lw=1.0, color=COLORS["pink"])
    ax.plot([0, r],[-r, r],  lw=1.0, color=COLORS["chartreuse"])

    # Dieptevolgorde (painter’s algorithm): sorteer vlakken op gemiddelde z na rotatie
    P3 = (R @ V.T).T
    zmean = [np.mean(P3[f,2]) for f in FACES]
    order = np.argsort(zmean)  # back-to-front

    # Vlakken
    for i in order:
        face = FACES[i]
        poly = pts2[face]
        patch = Polygon(poly, closed=True, facecolor=COLORS[FIELDS[i]], edgecolor="#222", linewidth=1.0, alpha=0.95)
        ax.add_patch(patch)

    # Randen (dunner, daaroverheen)
    edges = {(min(a,b), max(a,b)) for tri in FACES for a,b in zip(tri, tri[1:]+tri[:1])}
    for (a,b) in edges:
        ax.plot([pts2[a,0], pts2[b,0]], [pts2[a,1], pts2[b,1]], color="#111", lw=1.2)

    ax.text(0, -r*1.05, "Octaëder — 8 vlakken ↔ 8 velden", ha="center", va="top", fontsize=10, color="#555")

    for ext in ("png","svg"):
        out = Path(save_dir)/f"octahedron_8fields.{ext}"
        plt.savefig(out, bbox_inches="tight", pad_inches=0.1)
        print(f"Saved {out.resolve()}")

if __name__ == "__main__":
    draw()
