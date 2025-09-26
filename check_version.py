import re, pathlib

t = pathlib.Path("pyproject.toml").read_text(encoding="utf-8")
m = re.search(r'^\s*version\s*=\s*"(\d+\.\d+\.\d+)"', t, re.M)
print("version =", m.group(1) if m else "NOT FOUND")
