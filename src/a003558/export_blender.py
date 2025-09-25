def export_label_spheres_obj(out_dir: str | None = None,
                             basename: str = "labels",
                             *,
                             labels: Iterable[str] | None = None,
                             radius: float = 0.2,
                             spacing: float = 1.0,
                             path: str | None = None) -> str:
    """
    Schrijf een simpele multi-group OBJ met per label een klein 'sphere proxy' (hier cube).
    Retourneert het volledige pad naar het geschreven .obj-bestand.

    Parameters
    ----------
    out_dir : str | None
        Doelmap (genegeerd als `path` is meegegeven).
    basename : str
        Basisnaam zonder extensie (genegeerd als `path` is meegegeven).
    labels : Iterable[str] | None
        Labels; default = ["A","B","C"].
    radius : float
        Kubus-half-edge (sphere proxy schaal).
    spacing : float
        Afstand tussen opeenvolgende labels langs x-as.
    path : str | None
        Volledig pad naar het te schrijven .obj (heeft prioriteit boven out_dir/basename).
    """

    # --- Bepaal uitpad één keer en wijzig het daarna nergens meer ---
    if path is not None:
        out_path = os.path.abspath(path)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    else:
        out_dir_eff = "." if out_dir is None else out_dir
        os.makedirs(out_dir_eff, exist_ok=True)
        out_path = os.path.join(out_dir_eff, f"{basename}.obj")
    # ----------------------------------------------------------------

    if labels is None:
        labels = ["A", "B", "C"]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Label spheres (cube proxies)\n")
        vx = 0
        for lab in labels:
            # simpele cube centered at (vx,0,0)
            half = radius
            verts = [
                (vx - half, -half, -half),
                (vx + half, -half, -half),
                (vx + half,  half, -half),
                (vx - half,  half, -half),
                (vx - half, -half,  half),
                (vx + half, -half,  half),
                (vx + half,  half,  half),
                (vx - half,  half,  half),
            ]
            # schrijf group voor elk label
            f.write(f"g {lab}\n")
            for v in verts:
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            # faces met lokale indices; we houden een offset bij per cube
            # maar omdat OBJ absolute vertex-indices verwacht, moeten we tracken hoeveel vertices we al hebben.
            # Eenvoudig: tel regels in dit bestand is onhandig; houd een teller buiten de lus.
            # We kunnen i0 baseren op hoeveel labels we al hadden * 8.
            # Om dat te doen, berekenen we de index offset uit de positie van dit label.
            idx0 = (vx // spacing) if spacing != 0 else 0  # aantal stappen; werkt als labels lineair op x met spacing
            try:
                idx0 = int(idx0)
            except Exception:
                idx0 = 0
            base = idx0 * 8
            # maar bovenstaande zou niet kloppen als spacing niet integer-delen van vx is.
            # Betere aanpak: we houden een eigen teller bij op basis van de lab-iteratie.
            # Daarom herschrijven we dit netter: we bepalen het aantal al-geschreven labels via enumerate.

    # Nettere implementatie mét correcte face-indices:
def export_label_spheres_obj(out_dir: str | None = None,
                             basename: str = "labels",
                             *,
                             labels: Iterable[str] | None = None,
                             radius: float = 0.2,
                             spacing: float = 1.0,
                             path: str | None = None) -> str:
    if path is not None:
        out_path = os.path.abspath(path)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    else:
        out_dir_eff = "." if out_dir is None else out_dir
        os.makedirs(out_dir_eff, exist_ok=True)
        out_path = os.path.join(out_dir_eff, f"{basename}.obj")

    if labels is None:
        labels = ["A", "B", "C"]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Label spheres (cube proxies)\n")
        half = radius
        # geometrie van één cube (8 vertices, 6 faces)
        cube_verts = [
            (-half, -half, -half),
            ( half, -half, -half),
            ( half,  half, -half),
            (-half,  half, -half),
            (-half, -half,  half),
            ( half, -half,  half),
            ( half,  half,  half),
            (-half,  half,  half),
        ]
        cube_faces = [
            (1, 2, 3, 4),  # bottom
            (5, 6, 7, 8),  # top
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 4, 8, 7),
            (4, 1, 5, 8),
        ]
        vcount = 0
        for i, lab in enumerate(labels):
            x = i * spacing
            f.write(f"g {lab}\n")
            for vx, vy, vz in cube_verts:
                f.write(f"v {x + vx:.6f} {vy:.6f} {vz:.6f}\n")
            # faces met offset
            base = vcount
            for a, b, c, d in cube_faces:
                f.write(f"f {base+a} {base+b} {base+c} {base+d}\n")
            vcount += 8

    return out_path
