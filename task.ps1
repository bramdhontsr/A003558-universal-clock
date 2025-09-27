param(
  [string]$Task = "help",
  [ValidateSet("patch","minor","major")]
  [string]$Part = "patch"
)

function Confirm-Action($Message) {
  $r = Read-Host "$Message (y/N)"
  if ($r -notin @("y","Y")) { Write-Host "Geannuleerd." -ForegroundColor Yellow; exit 0 }
}

function Ensure-WebIndex {
  if (-not (Test-Path "web")) { throw "Map 'web' ontbreekt." }
  if (-not (Test-Path "web\index.html") -and (Test-Path "web\lemniscate.html")) {
    '<!doctype html><meta http-equiv="refresh" content="0; url=lemniscate.html">' | Out-File web\index.html -Encoding utf8NoBOM -NoNewline
  }
}

switch ($Task.ToLower()) {

  "help" {
    @"
Taken:
  .\tasks.ps1 help           - toon dit overzicht
  .\tasks.ps1 check          - korte omgevingstest (python, pakket, git)
  .\tasks.ps1 serve          - lokale webserver (http://localhost:8000) voor ./web
  .\tasks.ps1 build          - bouw wheel + sdist in ./dist
  .\tasks.ps1 release        - upload ./dist/* naar PyPI (vraagt bevestiging)
  .\tasks.ps1 deploy-web     - publiceer ./web naar gh-pages (vraagt bevestiging)
  .\tasks.ps1 bump [patch|minor|major] - verhoog versie in pyproject.toml + commit + tag
"@ | Write-Host
    break
  }

  "check" {
    Write-Host ">> Python & pakket" -ForegroundColor Cyan
    python -c "import sys; print('python:', sys.version)"
    python -c "import importlib,sys; 
m=None
try: m=importlib.import_module('a003558'); print('a003558:', getattr(m,'__version__','n/a'))
except Exception as e: print('a003558 niet importeerbaar:', e)"
    Write-Host ">> Git" -ForegroundColor Cyan
    git remote -v
    git branch -vv
    git status -s
    break
  }

  "serve" {
    Ensure-WebIndex
    python -m http.server -d web 8000
    break
  }

  "build" {
    Write-Host ">> Build distributies" -ForegroundColor Cyan
    python -m pip install --upgrade pip build
    Remove-Item dist -Recurse -Force -ErrorAction SilentlyContinue
    python -m build
    Get-ChildItem dist
    break
  }

  "release" {
    Confirm-Action "Weet je zeker dat je naar PyPI wilt uploaden?"
    if (-not (Test-Path "dist")) { Write-Host "Geen dist/ gevonden; eerst build..." -ForegroundColor Yellow; & $PSCommandPath build }
    python -m pip install --upgrade twine
    if ($env:PYPITOKEN) {
      python -m twine upload --non-interactive -u __token__ -p $env:PYPITOKEN dist\*
    } else {
      Write-Host "Geen PYPITOKEN in omgeving; twine zal om inlog vragen." -ForegroundColor Yellow
      python -m twine upload dist\*
    }
    break
  }

  "deploy-web" {
    Confirm-Action "Publiceer ./web naar GitHub Pages (branch gh-pages)?"
    Ensure-WebIndex
    python -m pip install --upgrade ghp-import
    # (optioneel) neem exports mee:
    if (Test-Path "exports") {
      New-Item -ItemType Directory -Path "web\exports" -ErrorAction SilentlyContinue | Out-Null
      robocopy exports web\exports /E | Out-Null
    }
    ghp-import -n -p -m "Publish website" web
    Write-Host "Gepubliceerd. Check Settings → Pages: Branch 'gh-pages' / root." -ForegroundColor Green
    break
  }

  "bump" {
    if (-not (Test-Path "pyproject.toml")) { throw "pyproject.toml ontbreekt." }
    $text = Get-Content pyproject.toml -Raw
    if ($text -notmatch 'version\s*=\s*"(?<v>\d+\.\d+\.\d+)"') { throw "Kon 'version = ""x.y.z""' niet vinden." }
    $v = [Version]$Matches['v']
    switch ($Part) {
      "patch" { $new = "{0}.{1}.{2}" -f $v.Major, $v.Minor, ($v.Build + 1) }
      "minor" { $new = "{0}.{1}.{2}" -f $v.Major, ($v.Minor + 1), 0 }
      "major" { $new = "{0}.{1}.{2}" -f ($v.Major + 1), 0, 0 }
    }
    $newText = $text -replace "version\s*=\s*""$($v)""", "version = ""$new"""
    Set-Content pyproject.toml $newText -Encoding utf8NoBOM
    git add pyproject.toml
    git commit -m "Bump version to $new"
    git tag "v$new"
    Write-Host "Bumped naar $new. Vergeet niet: git push && git push --tags" -ForegroundColor Green
    break
  }

  default {
    Write-Host "Onbekende taak '$Task'. Gebruik: .\tasks.ps1 help" -ForegroundColor Yellow
  }
}
