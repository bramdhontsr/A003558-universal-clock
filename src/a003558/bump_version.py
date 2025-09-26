import re
from pathlib import Path
import sys

if len(sys.argv) != 2 or sys.argv[1] not in ("patch", "minor", "major"):
    print("Gebruik: python bump_version.py [patch|minor|major]")
    sys.exit(1)

level = sys.argv[1]

# Lees pyproject.toml
pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

match = re.search(r'version\s*=\s*"(\d+)\.(\d+)\.(\d+)"', pyproject)
if not match:
    print("Kon geen versie vinden in pyproject.toml")
    sys.exit(1)

major, minor, patch = map(int, match.groups())

if level == "patch":
    patch += 1
elif level == "minor":
    minor += 1
    patch = 0
elif level == "major":
    major += 1
    minor = 0
    patch = 0

new_version = f'{major}.{minor}.{patch}'
print(f"Nieuwe versie: {new_version}")

# Update pyproject.toml
pyproject_new = re.sub(r'version\s*=\s*"\d+\.\d+\.\d+"',
                       f'version = "{new_version}"',
                       pyproject)

Path("pyproject.toml").write_text(pyproject_new, encoding="utf-8")

# Voeg ook meteen een lege sectie in CHANGELOG.md toe
changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
insertion = f"\n## [{new_version}] - {Path().cwd().name}\n### Changed\n- ...\n"
Path("CHANGELOG.md").write_text(changelog + insertion, encoding="utf-8")

# Print git-commando's voor de gebruiker
print("\nVoer nu uit:")
print("  git add pyproject.toml CHANGELOG.md")
print(f'  git commit -m "Bump version to {new_version}"')
print(f"  git tag v{new_version}")
print(f"  git push origin main --tags")
