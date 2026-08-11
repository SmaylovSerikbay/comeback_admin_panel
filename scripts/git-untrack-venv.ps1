# Убрать venv, node_modules и другие тяжёлые папки из индекса Git (файлы на диске не трогаем).
# Запуск: в PowerShell из корня репозитория:
#   cd "c:\Users\user\Desktop\Unity Projects\admincomebakweb\comeback_admin_panel"
#   .\scripts\git-untrack-venv.ps1

$ErrorActionPreference = 'Stop'
$root = if ($PSScriptRoot) { Split-Path -Parent $PSScriptRoot } else { Get-Location }
Set-Location $root

# Windows: убрать из индекса файлы с зарезервированными именами (nul, CON и т.д.)
foreach ($reserved in @('nul', 'NUL', 'CON', 'PRN', 'AUX')) {
    if (git ls-files "$reserved" 2>$null) {
        Write-Host "Untracking reserved name: $reserved"
        git rm --cached -- "$reserved" 2>$null
    }
}

$paths = @(
    'venv',
    '.venv',
    'env',
    'admin-next/node_modules',
    'admin-next/.next',
    'admin-next/out',
    'admin-next/.turbo'
)

foreach ($p in $paths) {
    $tracked = git ls-files "$p" 2>$null
    if ($LASTEXITCODE -eq 0 -and $tracked) {
        Write-Host "Untracking: $p"
        git rm -r --cached "$p" 2>$null
    }
}

# __pycache__ по всему репо (одна папка — один git rm)
$pycacheFiles = git ls-files '**/__pycache__/*' 2>$null
if ($pycacheFiles) {
    $pycacheDirs = $pycacheFiles | ForEach-Object { ($_ -split '/__pycache__/')[0] + '/__pycache__' } | Sort-Object -Unique
    Write-Host "Untracking: **/__pycache__/ ($($pycacheDirs.Count) dirs)"
    foreach ($d in $pycacheDirs) {
        git rm -r --cached "$d" 2>$null
    }
}

Write-Host "`nDone. Run: git status"
git status --short
