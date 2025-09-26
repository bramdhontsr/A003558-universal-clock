#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import subprocess
from pathlib import Path

USAGE = "Gebruik: python bump_version.py [patch|minor|major]"

def run(cmd, check=True):
    print("$", " ".join(cmd))
    r = subprocess.run(cmd, text=True, capture_output=True)
    if r.stdout:
        print(r.stdout.strip())
    if r.stderr and (check or r.returncode != 0):
        print(r.stderr.strip())
    if check and r.returncode != 0:
        sys.exit(r.returncode)
    return r

def current_branch():
    r = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return r.stdout.strip()

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("patch", "minor", "major"):
        print(USAGE)
        sys.exit(1)
    level = sys.argv[1]

    pyproj_path = Path("pyproject.toml")
    if not pyproj_path.exists():
        print("Fout: pyproject.toml niet gevonden in de huidige map.")
        sys.exit(1)

    text = pyproj_path.read_text(encoding="utf-8")
    m = re.search(r'^\s*version\s*=\s*"(\d+)\.(\d+)\.(\d+)"', text, re.M)
    if not m:
        print('Kon geen versie vinden (verwacht regel: version = "X.Y.Z").')
        sys.exit(1)

    major, minor, patch = map(int, m.groups())
    if level == "patch":
        patch += 1
    elif level == "minor":
        minor += 1
        patch = 0
    else:  # major
        major += 1
        minor = 0
        patch = 0

    new_ver = f"{major}.{minor}.{patch}"
    print("Nieuwe versie:", new_ver)

    new_text = re.sub(
        r'(^\s*version\s*=\s*")\d+\.\d+\.\d+(")',
        rf'\g<1>{new_ver}\g<2>',
        text,
        count=1,
        flags=re.M,
    )
    pyproj_path.write_text(new_text, encoding="utf-8")

    branch = current_branch() or "main"
    run(["git", "add", "pyproject.toml"])
    run(["git", "commit", "-m", f"Bump version to {new_ver}"])
    run(["git", "tag", f"v{new_ver}"])
    run(["git", "push", "origin", branch])
    run(["git", "push", "origin", "--tags"])

    print("\nKlaar! Tag gepusht. GitHub Actions draait CI en publiceert naar PyPI (met auto release notes).")

if __name__ == "__main__":
    main()
