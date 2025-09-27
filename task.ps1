# tasks.ps1 - eenvoudige task runner voor Windows/PowerShell
# Gebruik:
#   .\tasks.ps1 help
#   .\tasks.ps1 viz            # lemniscaat (PNG+SVG)
#   .\tasks.ps1 viz-oct        # octaëder (PNG+SVG)
#   .\tasks.ps1 viz-all        # beide visuals
#   .\tasks.ps1 serve          # lokale server op ./web (http://localhost:8000)
#   .\tasks.ps1 serve-live     # idem, met hint naar /lemniscate-live.html
#   .\tasks.ps1 clean          # ruim ./dist ./build ./exports op
#   .\tasks.ps1 build          # bouw wheel + sdist in ./dist
#   .\tasks.ps1 release        # upload naar PyPI (env PYPITOKEN of interactief)
#   .\tasks.ps1 deploy-web     # publiceer ./web (+ ./exports) naar gh-pages
#   .\tasks.ps1 publish-pages  # viz-all + deploy-web
#   .\tasks.ps1 check          # snelle health check van omgeving
#   .\tasks.ps1 bump patch     # bump semver (patch/minor/major), commit + tag

param(
  [Parameter(Position=0)]
  [string]$Task = "help",
  [Parameter(Position=1)]
  [string]$Arg = ""     # gebruikt door bv. bump (patch/minor/major)
)

function _ensure-venv {
  if (-not (Test-Path ".\.venv")) {
    Write-Host ">> (Tip) Activeer je virtualenv: python -m venv .venv; .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
  }
}

function _require-file($path) {
  if (-not (Test-Path $path)) { throw "Vereist bestand ontbreekt: $path" }
}

switch ($Task.ToLower()) {

  # --- Visuals ---
  "viz" {
    _ensure-venv
    _require-file "tools\generate_lemniscate.py"
    Write-Host ">> Generating lemniscate visual to ./exports ..." -ForegroundColor Cyan
    python tools/generate_lemniscate.py
    break
  }

  "viz-oct" {
    _ensure-venv
    _require-file "tools\generate_octahedron.py"
    Write-Host ">> Generating octahedron visual to ./exports ..." -ForegroundColor Cyan
    python tools/generate_octahedron.py
    break
  }

  "viz-all" {
    _ensure-venv
    if (Test-Path "tools\generate_lemniscate.py") {
      Write-Host ">> Lemniscaat..." -ForegroundColor Cyan
      python tools/generate_lemniscate.py
    } else {
      Write-Host "!! tools/generate_lemniscate.py ontbreekt" -ForegroundColor Yellow
    }
    if (Test-Path "tools\generate_octahedron.py") {
      Write-Host ">> Octaëder..." -ForegroundColor Cyan
      python tools/generate_octahedron.py
    } else {
      Write-Host "!! tools/generate_octahedron.py ontbreekt" -ForegroundColor Yellow
    }
    Write-Host ">> Done." -ForegroundColor Green
    break
  }

  # --- Server ---
  "serve" {
    Write-Host ">> Starting local static server at http://localhost:8000 (./web)" -ForegroundColor Cyan
    python -m http.server -d web 8000
    break
  }

  "serve-live" {
    Write-Host ">> Starting local static server at http://localhost:8000 (./web)" -ForegroundColor Cyan
    Write-Host "   Open: http://localhost:8000/lemniscate-live.html" -ForegroundColor DarkCyan
    python -m http.server -d web 8000
    break
  }

  # --- Clean/Build/Release ---
  "clean" {
    Write-Host ">> Cleaning ./dist ./build ./exports ..." -ForegroundColor Cyan
    Remove-Item -Recurse -Force dist, build, exports -ErrorAction SilentlyContinue
    break
  }

  "build" {
    _ensure-venv
    Write-Host ">> Building wheel + sdist into ./dist ..." -ForegroundColor Cyan
    python -m pip install --upgrade pip build
    python -m build
    Write-Host ">> Done. Files:" -ForegroundColor Green
    Get-ChildItem dist
    break
  }

  "release" {
    _ensure-venv
    $env:PIP_INDEX_URL = "https://pypi.org/simple"
    if (-not (Test-Path "dist")) {
      Write-Host ">> Geen dist/ gevonden. Eerst builden..." -ForegroundColor Yellow
      python -m pip install --upgrade pip build
      python -m build
    }
    Write-Host ">> Upload to PyPI via Twine..." -ForegroundColor Cyan
    python -m pip install --upgrade twine
    if ($env:PYPITOKEN) {
      python - << 'PY'
import os, sys, subprocess
cmd = [sys.executable, "-m", "twine", "upload", "dist/*", "-u", "__token__", "-p", os.environ["PYPITOKEN"]]
sys.exit(subprocess.call(" ".join(cmd), shell=True))
PY
    } else {
      Write-Host ">> PYPITOKEN niet gevonden in omgeving. Twine vraagt nu om token..." -ForegroundColor Yellow
      python -m twine upload dist/*
    }
    break
  }

  # --- GitHub Pages deploy ---
  "deploy-web" {
    $ErrorActionPreference = "Stop"
    Write-Host ">> Deploying ./web (+ ./exports) to gh-pages branch..." -ForegroundColor Cyan

    $root = (git rev-parse --show-toplevel) 2>$null
    if (-not $root) { throw "Dit lijkt geen git repo. Voer 'git init' uit of ga naar de projectroot." }

    git fetch origin 2>$null
    $hasRemote = (& git ls-remote --heads origin gh-pages) -ne $null
    if (-not $hasRemote) {
      Write-Host ">> 'gh-pages' bestaat nog niet op origin. Maak 'm aan..." -ForegroundColor Yellow
      git checkout --orphan gh-pages
      Remove-Item -Recurse -Force * -ErrorAction SilentlyContinue
      New-Item -ItemType Directory -Name ".placeholder" | Out-Null
      git add .
      git commit -m "init gh-pages"
      git push -u origin gh-pages
      git checkout -
    }

    if (Test-Path ".git\worktrees\gh-pages") {
      git worktree remove gh-pages -f
    }
    git worktree add gh-pages gh-pages

    robocopy web gh-pages /MIR | Out-Null
    if (Test-Path "exports") {
      New-Item -ItemType Directory -Path "gh-pages/exports" -ErrorAction SilentlyContinue | Out-Null
      robocopy exports gh-pages\exports /E | Out-Null
    }

    if (Test-Path "gh-pages\lemniscate.html" -and -not (Test-Path "gh-pages\index.html")) {
@"<!doctype html><meta http-equiv=""refresh"" content=""0; url=lemniscate.html"">"@ | Set-Content -NoNewline gh-pages\index.html -Encoding UTF8
    }

    Push-Location gh-pages
    git add .
    if ((git status --porcelain).Length -gt 0) {
      git commit -m "Publish website $(Get-Date -Format s)"
      git push origin gh-pages
      Write-Host ">> Published to gh-pages." -ForegroundColor Green
    } else {
      Write-Host ">> Nothing to publish (no changes)." -ForegroundColor Yellow
    }
    Pop-Location

    git worktree remove gh-pages -f
    break
  }

  "publish-pages" {
    Write-Host ">> Generating visuals (viz-all)..." -ForegroundColor Cyan
    & "$PSCommandPath" viz-all
    Write-Host ">> Deploying to gh-pages..." -ForegroundColor Cyan
    & "$PSCommandPath" deploy-web
    break
  }

  # --- Checks & bump ---
  "check" {
    Write-Host ">> Python & pip" -ForegroundColor Cyan
    python -V
    pip -V
    Write-Host "`n>> Installed package (a003558) version" -ForegroundColor Cyan
    python - << 'PY'
try:
    import a003558, sys
    print("a003558:", getattr(a003558, "__version__", "n/a"))
except Exception as e:
    print("a003558 not importable:", e)
PY
    Write-Host "`n>> Git status" -ForegroundColor Cyan
    git branch -vv
    git status -s
    Write-Host "`n>> Remote" -ForegroundColor Cyan
    git remote -v
    break
  }

  "bump" {
    if ($Arg -notin @("patch","minor","major")) {
      Write-Host "Gebruik: .\tasks.ps1 bump {patch|minor|major}" -ForegroundColor Yellow
      break
    }
    _require-file "pyproject.toml"
    $content = Get-Content pyproject.toml -Raw
    if ($content -notmatch 'version\s*=\s*"(.*?)"') { throw "Kon versie niet vinden in pyproject.toml" }
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
    Write-Host ">> Bumped to $new and tagged v$new" -ForegroundColor Green
    break
  }

  default {
    Write-Host "Available tasks:" -ForegroundColor Cyan
    Write-Host "  viz            - Genereer lemniscaat (PNG+SVG) naar ./exports"
    Write-Host "  viz-oct        - Genereer octaëder (PNG+SVG) naar ./exports"
    Write-Host "  viz-all        - Genereer beide visuals"
    Write-Host "  serve          - Start lokale webserver (./web) op http://localhost:8000"
    Write-Host "  serve-live     - Start server, open zelf /lemniscate-live.html"
    Write-Host "  clean          - Verwijder ./dist ./build ./exports"
    Write-Host "  build          - Bouw wheel + sdist naar ./dist"
    Write-Host "  release        - Upload naar PyPI (env PYPITOKEN of interactief twine-login)"
    Write-Host "  deploy-web     - Publiceer ./web + ./exports naar gh-pages"
    Write-Host "  publish-pages  - viz-all + deploy-web"
    Write-Host "  check          - Snelle omgeving- en repo-check"
    Write-Host "  bump {x}       - Bump semver: patch | minor | major"
  }
}
