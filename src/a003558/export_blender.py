from __future__ import annotations
import os
from typing import Iterable, Tuple
import numpy as np

from .viz import default_basis_layout
from .viz_octa import octahedron_vertices_edges

# ---------- Kleine OBJ helper ----------

def _write_obj(
    path: str,
    verts: np.ndarray,
    edges: Iterable[Tuple[int,int]] | None = None,
    name: str = "object",
    mtl_name: str | None = None,
    vt: np.ndarray | None = None,
    groups: dict[str, list[int]] | None = None,
) -> None:
    """
    Schrijft een OBJ met vertices en (optioneel) edge-lijnen.
    edges verwijst naar 0-based vertex indices. Each edge wordt als 'l i j' geschreven.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# simple OBJ export\n")
        if mtl_name:
            f.write(f"mtllib {os.path.basename(mtl_name)}\n")
        f.write(f"o {name}\n")
        for v in verts:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        if vt is not None:
            for t in vt:
                f.write(f"vt {t[0]:.6f} {t[1]:.6f}\n")

        if groups:
            for gname, vidxs in groups.items():
                f.write(f"g {gname}\n")
                # we schrijven elk vertex als een los 'p' (point). Blender kan dit als losse puntjes tonen
                for vi in vidxs:
                    f.write(f"p {vi+1}\n")

        if edges:
            f.write("g edges\n")
            for i, j in edges:
                f.write(f"l {i+1} {j+1}\n")


def _filter_cube_edges(verts: np.ndarray) -> list[tuple[int,int]]:
    """Edges tussen hoekpunten die op precies één as van teken verschillen (Manhattanafstand == 2)."""
    E: list[tuple[int,int]] = []
    def manhattan(p, q): return np.abs(p-q).sum()
    n = len(verts)
    for i in range(n):
        for j in range(i+1, n):
            if np.isclose(manhattan(verts[i], verts[j]), 2.0):
                E.append((i, j))
    return E


# ---------- Publieke API ----------

def export_octa_cube_obj(
    out_dir: str = "exports",
    basename: str = "a003558_static",
    scale: float = 1.0,
) -> dict[str, str]:
    """
    Exporteer octaëder + kubus (octonion-basis) als aparte OBJ-bestanden, plus één gecombineerde.
    Retourneert paden van de bestanden.
    """
    V_oct, E_oct = octahedron_vertices_edges()
    V_cub, labels = default_basis_layout()

    V_oct = V_oct * scale
    V_cub = V_cub * scale

    # losse bestanden
    oct_path = os.path.join(out_dir, f"{basename}_octahedron.obj")
    cub_path = os.path.join(out_dir, f"{basename}_cube.obj")
    all_path = os.path.join(out_dir, f"{basename}_scene.obj")

    # 1) Octaëder
    _write_obj(
        oct_path,
        verts=V_oct,
        edges=E_oct,
        name="octahedron",
    )

    # 2) Kubus
    E_cub = _filter_cube_edges(V_cub)
    # zet ook labels als 'points' in een eigen groep
    groups = {"labels": list(range(len(V_cub)))}
    _write_obj(
        cub_path,
        verts=V_cub,
        edges=E_cub,
        name="octonion_cube",
        groups=groups,
    )

    # 3) Gecombineerd in één OBJ (door vertices te stapelen en indexen te shiften)
    V_all = np.vstack([V_oct, V_cub])
    shift = len(V_oct)
    E_oct_shift = E_oct
    E_cub_shift = [(i+shift, j+shift) for (i, j) in E_cub]
    groups_all = {"cube_labels": [shift + i for i in range(len(V_cub))]}

    _write_obj(
        all_path,
        verts=V_all,
        edges=E_oct_shift + E_cub_shift,
        name="octahedron_plus_cube",
        groups=groups_all,
    )

    # Tip: in Blender kun je materialen/kleuren toewijzen per object of per selectie.
    return {"octahedron": oct_path, "cube": cub_path, "combined": all_path}


def export_label_spheres_obj(
    path: str = "exports/a003558_labels.obj",
    radius: float = 0.05,
) -> str:
    """
    Eenvoudige placeholder: we schrijven alleen de 8 label-vertexposities als 'p' (points),
    zodat je in Blender ze direct ziet en kunt vervangen door 3D-tekst.
    Wil je echte bolletjes, laat me weten — dan voeg ik een low-poly UV-sphere builder toe.
    """
    V_cub, labels = default_basis_layout()
    groups = {"labels": list(range(len(V_cub)))}
    _write_obj(path, verts=V_cub, edges=None, name="label_points", groups=groups)
    return path
