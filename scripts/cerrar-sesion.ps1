<#
Cierre de sesion de trabajo - Joyas MCGHR

Uso:
  powershell -ExecutionPolicy Bypass -File .\scripts\cerrar-sesion.ps1 -RepoPath "C:\ruta\al\repo"

Si ExecutionPolicy del sistema bloquea scripts sin firmar, el flag
-ExecutionPolicy Bypass de arriba aplica solo a este proceso, no cambia
la politica global de la maquina.

Que hace:
  - Verifica que RepoPath sea un repo git valido.
  - Muestra la branch actual y el estado (archivos modificados,
    agregados, sin trackear).
  - Advierte si hay cambios pendientes fuera de docs/ESTADO_PROYECTO.md,
    recordando que ese archivo se debe actualizar en el mismo commit de
    cierre (ver CLAUDE.md).
  - No commitea ni pushea nada automaticamente: solo diagnostica.
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath
)

$ErrorActionPreference = 'Continue'

if (-not (Test-Path -LiteralPath $RepoPath)) {
    Write-Error "RepoPath no existe: $RepoPath"
    exit 1
}

$repoPathResolved = (Resolve-Path -LiteralPath $RepoPath).Path

try {
    $insideRepo = git -C $repoPathResolved rev-parse --is-inside-work-tree 2>$null
} catch {
    $insideRepo = $null
}

if ($insideRepo -ne 'true') {
    Write-Error "No es un repo git valido: $repoPathResolved"
    exit 1
}

try {
    $branch = git -C $repoPathResolved rev-parse --abbrev-ref HEAD 2>$null
} catch {
    $branch = '(desconocida)'
}
Write-Output "Branch actual: $branch"

try {
    $statusLines = @(git -C $repoPathResolved status --porcelain 2>$null)
} catch {
    $statusLines = @()
}

if (@($statusLines).Count -eq 0) {
    Write-Output "Sin cambios pendientes. Repo limpio."
} else {
    Write-Output "Cambios pendientes ($(@($statusLines).Count) archivo(s)):"
    foreach ($line in $statusLines) {
        Write-Output "  $line"
    }

    $estadoTocado = @($statusLines) | Where-Object { $_ -match 'ESTADO_PROYECTO\.md' }
    if (@($estadoTocado).Count -eq 0) {
        Write-Warning "docs/ESTADO_PROYECTO.md no aparece entre los cambios. Recorda actualizarlo antes de commitear el cierre de esta sesion (ver CLAUDE.md)."
    }
}

try {
    $lastCommit = git -C $repoPathResolved log -1 --format="%h %ad %s" --date=short 2>$null
    Write-Output "Ultimo commit: $lastCommit"
} catch {
    Write-Warning "No se pudo leer el ultimo commit (repo sin commits todavia?)."
}
