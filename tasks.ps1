# tasks.ps1 — veilige task runner (Windows/PowerShell)
# Gebruik:
#   .\tasks.ps1 help           # toon overzicht
#   .\tasks.ps1 check          # snelle omgeving-check
#   .\tasks.ps1 serve          # lokale webserver voor ./web
#   .\tasks.ps1 build          # bouw wheel + sdist in ./dist
#   .\tasks.ps1 release        # upload naar PyPI (met $env:PYPITOKEN)
#   .\tasks.ps1 deploy-web     # publiceer ./web naar gh-pages (via ghp-import; veilig)
#   .\tasks.ps1 viz            # (optioneel) run tools\generate_lemniscate.py
#   .\tasks.ps1 viz-oct        # (optioneel) run tools\generate_octahedron.py
#   .\tasks.ps1 viz-all        # (optioneel) beide visuals
#   .\tasks.ps1 bump patch     # bump {patch|minor|major}, commit + tag
# Let op: GEEN "all"-task, om per-ongeluk alles-in-één te vermijden.

param(
  [Parameter(Position=0)]
  [ValidateSet("help","check","serve","build","release","deploy-web","viz","viz-oct","viz-all","bump")]
  [string]$Task = "help",
  [Parameter(Position=1)]
  [string]$Arg = ""
)

function _ensure-venv {
  if (-not (Test-Path ".\.venv")) {
    Write-Host "(tip) activeer je venv: python -m venv .venv; .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
  }
}

function _require-file($path) {
  if (-not (Test-Path $path)) { throw "Bestand ontbreekt: $path" }
}

switch ($Task) {

  "help" {
    @"
Taken:
  check        - omgeving controleren (python/pip/a003558/git)
  serve        - lokale server op http://localhost:8000 (map: web)
  build        - python distributies bouwen naar ./dist
  release      - upload ./dist/* naar PyPI (zet eerst `$env:PYPITOKEN`)
  deploy-web   - publiceer ./web veilig naar gh-pages (ghp-import)
  viz          - tools\generate_lemniscate.py uitvoeren (optioneel)
  viz-oct      - tools\generate_octahedron.py uitvoeren (optioneel)
  viz-all      - beide visuals genereren (optioneel)
  bump X       - versie ophogen (X = patch|minor|major), commit + tag

Opzettelijk GEEN 'all'-task om fouten in de pipeline te voorkomen.
"@ | Write-Host
    break
  }

  "check" {
    try { python -V } catch { Write-Host "python niet gevonden" -ForegroundColor Yellow }
    try { pip -V } catch { Write-Host "pip niet gevonden" -ForegroundColor Yellow }
    python -c "import sys; print('sys.version:', sys.version)"
    python -c "import importlib; 
try:
 m=importlib.import_module('a003558'); print('a003558:', getattr(m,'__version__','n/a'))
except Exception as e:
 print('a003558 not importable:', e)"
    git remote -v
    git branch -vv
    git status -s
    break
  }

  "serve" {
    if (-not (Test-Path "web")) { throw "Map 'web' ontbreekt." }
    python -m http.server -d web 8000
    break
  }

  "build" {
    _ensure-venv
    python -m pip install --upgrade pip build
    python -m build
    Get-ChildItem dist
    break
  }

  "release" {
    _ensure-venv
    if (-not (Test-Path "dist")) {
      Write-Host "Geen ./dist gevonden; eerst build uitvoeren..." -ForegroundColor Yellow
      python -m pip install --upgrade pip build
      python -m build
    }
    python -m pip install --upgrade twine

    $files = Get-ChildItem -Path "dist" -File | ForEach-Object { $_.FullName }
    if (-not $files -or $files.Count -eq 0) { throw "Geen distributiebestanden in ./dist" }

    if ($env:PYPITOKEN) {
      # Stille upload met token
      python -m twine upload --non-interactive -u __token__ -p $env:PYPITOKEN @files
    } else {
      Write-Host "Geen PYPITOKEN gevonden; Twine zal interactief om je token vragen." -ForegroundColor Yellow
      python -m twine upload @files
    }
    break
  }

  "deploy-web" {
    # Veilig publiceren via ghp-import (wijzigt je werkboom NIET)
    if (-not (Test-Path "web")) { throw "Map 'web' ontbreekt." }

    python -m pip install --upgrade ghp-import

    # Optioneel: neem exports op in de site (kopie naar web/exports)
    if (Test-Path "exports") {
      New-Item -ItemType Directory -Path "web\exports" -ErrorAction SilentlyContinue | Out-Null
      robocopy exports web\exports /E | Out-Null
    }

    # Eenvoudige index redirect als die ontbreekt
    if (-not (Test-Path "web\index.html") -and (Test-Path "web\lemniscate.html")) {
      '<!doctype html><meta http-equiv="refresh" content="0; url=lemniscate.html">' | Out-File web\index.html -Encoding UTF8 -NoNewline
    }

    # Publiceer ALLEEN de map web/ naar gh-pages
    ghp-import -n -p -m "Publish website" web
    Write-Host "Gepubliceerd naar gh-pages. Controleer GitHub → Settings → Pages." -ForegroundColor Green
    break
  }

  "viz" {
    _ensure-venv
    _require-file "tools\generate_lemniscate.py"
    python tools\generate_lemniscate.py
    break
  }

  "viz-oct" {
    _ensure-venv
    _require-file "tools\generate_octahedron.py"
    python tools\generate_octahedron.py
    break
  }

  "viz-all" {
    _ensure-venv
    if (Test-Path "tools\generate_lemniscate.py") { python tools\generate_lemniscate.py }
    if (Test-Path "tools\generate_octahedron.py")  { python tools\generate_octahedron.py  }
    break
  }

  "bump" {
    if ($Arg -notin @("patch","minor","major")) {
      Write-Host "Gebruik: .\tasks.ps1 bump {patch|minor|major}" -ForegroundColor Yellow
      break
    }
    if (-not (Test-Path "pyproject.toml")) { throw "pyproject.toml ontbreekt in de root." }
    $content = Get-Content pyproject.toml -Raw
    if ($content -notmatch 'version\s*=\s*"(.*?)"') { throw "Kon 'version = ""x.y.z""' niet vinden in pyproject.toml." }
    $ver = [Version]$matches[1]
    switch ($Arg) {
      "patch" { $new = "{0}.{1}.{2}" -f $ver.Major, $ver.Minor, ($ver.Build + 1) }
      "minor" { $new = "{0}.{1}.{2}" -f $ver.Major, ($ver.Minor + 1), 0 }
      "major" { $new = "{0}.{1}.{2}" -f ($ver.Major + 1), 0, 0 }
    }
    $newContent = $content -replace "version\s*=\s*""$($ver)""", "version = ""$new"""
    Set-Content pyproject.toml $newContent -Encoding UTF8
    git add pyproject.toml
    git commit -m "Bump version to $new"
    git tag "v$new"
    Write-Host "Bumped to $new. Vergeet niet: git push && git push --tags" -ForegroundColor Green
    break
  }
}
