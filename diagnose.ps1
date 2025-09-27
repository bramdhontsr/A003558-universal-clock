$ErrorActionPreference='Stop'
function OK($m){Write-Host "OK  " -NoNewline -ForegroundColor Green; Write-Host $m}
function NO($m){Write-Host "FOUT" -NoNewline -ForegroundColor Red; Write-Host " $m"}

Write-Host "`n== Basis ==" -ForegroundColor Cyan
$here=(Get-Location).Path
OK "Werkmap: $here"
if (Test-Path "$HOME\.git"){ NO "Er staat een .git in HOME ($HOME). Hernoem die: Rename-Item $HOME\.git .git_backup_HOME" } else { OK "Geen verdwaalde .git in HOME" }

Write-Host "`n== Git ==" -ForegroundColor Cyan
try {
  $top=(git rev-parse --show-toplevel).Trim().Replace('/','\')
  if($top -ne $here){ NO "Je staat niet in repo-root ($top). Ga naar repo-root." } else { OK "Repo-root gedetecteerd" }
} catch { NO "Geen git-repo?" }

$rem=(git remote -v) -join " "
if($rem -match "A003558-universal-clock\.git"){ OK "origin ok: $rem" } else { NO "origin afwijkt: $rem" }

$st=(git status --porcelain)
if([string]::IsNullOrWhiteSpace($st)){ OK "Werkboom schoon" } else { Write-Host $st; NO "Er zijn ongestage wijzigingen (zie boven)." }

Write-Host "`n== Build artefacten ==" -ForegroundColor Cyan
$wheels=Get-ChildItem dist\a003558-*.whl -ErrorAction SilentlyContinue
$sdist =Get-ChildItem dist\a003558-*.tar.gz -ErrorAction SilentlyContinue
if($wheels){ OK "Wheel: $($wheels[-1].Name)" } else { NO "Geen wheel in dist\. Run: .\tasks.ps1 build" }
if($sdist){  OK "sdist: $($sdist[-1].Name)" } else { NO "Geen sdist in dist\. Run: .\tasks.ps1 build" }

Write-Host "`n== Python/pakket lokaal ==" -ForegroundColor Cyan
python -c "import sys; print('python:', sys.version)"
python -c "import importlib; 
m=None
try:
 m=importlib.import_module('a003558'); print('a003558:', getattr(m,'__version__','n/a'))
except Exception as e:
 print('a003558 niet importeerbaar:', e)"
OK "Python & import test uitgevoerd"

Write-Host "`n== PyPI check (schone venv) ==" -ForegroundColor Cyan
try{
  $tmpvenv=".venv_check"
  if(!(Test-Path $tmpvenv)){ python -m venv $tmpvenv }
  & "$tmpvenv\Scripts\Activate.ps1"
  pip install -q -U pip >$null
  # installeer laatste op PyPI
  pip install -q a003558 >$null
  $v=(python - <<'PY'
import a003558; print(a003558.__version__)
PY
  ).Trim()
  OK "PyPI levert versie: $v"
  deactivate
} catch { NO "PyPI install test faalde: $_" }

Write-Host "`n== GitHub Pages ==" -ForegroundColor Cyan
try{
  $hasGh=(git ls-remote --heads origin gh-pages) -ne $null
  if($hasGh){ OK "Branch 'gh-pages' bestaat op origin" } else { NO "Geen 'gh-pages' op origin → publiceer: .\tasks.ps1 deploy-web" }
}catch{ NO "Kon gh-pages niet controleren: $_" }

$repoUrl="https://bramdhontsr.github.io/A003558-universal-clock/"
try{
  $resp=Invoke-WebRequest -Uri $repoUrl -UseBasicParsing -Method Head -TimeoutSec 10
  if($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 400){ OK "Site bereikbaar: $repoUrl (HTTP $($resp.StatusCode))" } else { NO "Site HTTP $($resp.StatusCode). Check Settings → Pages." }
}catch{ NO "Site niet bereikbaar. Check Settings → Pages: Branch 'gh-pages' / root" }

Write-Host "`n== Klaar ==" -ForegroundColor Cyan
