<#
Chequeo de conflictos entre branches de tema y main - Joyas MCGHR

Uso:
  powershell -ExecutionPolicy Bypass -File .\scripts\chequear-conflictos.ps1 -RepoPath "C:\ruta\al\repo"

Si ExecutionPolicy del sistema bloquea scripts sin firmar, el flag
-ExecutionPolicy Bypass de arriba aplica solo a este proceso.

Que hace (ver ADR-008 en docs/ADR.md):
  - Verifica que RepoPath sea un repo git valido.
  - Actualiza informacion remota (fetch).
  - Para cada branch local feature/*, intenta un merge de prueba contra
    main en un branch temporal descartable, sin tocar el working tree
    real, y reporta si hay conflicto.
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
    git -C $repoPathResolved fetch origin 2>&1 | Out-Null
} catch {
    Write-Warning "No se pudo hacer fetch de origin. Sigo con las branches locales conocidas."
}

try {
    $temaBranches = @(git -C $repoPathResolved branch --list 'feature/*' --format='%(refname:short)' 2>$null)
} catch {
    $temaBranches = @()
}

if (@($temaBranches).Count -eq 0) {
    Write-Output "No hay branches feature/* locales para chequear."
    exit 0
}

$originalBranch = git -C $repoPathResolved rev-parse --abbrev-ref HEAD 2>$null
$tempBranch = "tmp/chequeo-conflictos-$(Get-Date -Format 'yyyyMMddHHmmss')"

$conflictivas = @()
$limpias = @()

foreach ($branch in $temaBranches) {
    try {
        git -C $repoPathResolved checkout main 2>&1 | Out-Null
        git -C $repoPathResolved checkout -b $tempBranch 2>&1 | Out-Null

        $mergeOutput = git -C $repoPathResolved merge --no-commit --no-ff $branch 2>&1
        $mergeExit = $LASTEXITCODE

        if ($mergeExit -ne 0) {
            $conflictivas += $branch
        } else {
            $limpias += $branch
        }

        git -C $repoPathResolved merge --abort 2>&1 | Out-Null
    } catch {
        Write-Warning "Error chequeando la branch $branch. La marco como a revisar manualmente."
        $conflictivas += $branch
    } finally {
        try {
            git -C $repoPathResolved checkout main 2>&1 | Out-Null
            git -C $repoPathResolved branch -D $tempBranch 2>&1 | Out-Null
        } catch {
            Write-Warning "No se pudo limpiar la branch temporal $tempBranch. Revisar manualmente."
        }
    }
}

if ($originalBranch) {
    try {
        git -C $repoPathResolved checkout $originalBranch 2>&1 | Out-Null
    } catch {
        Write-Warning "No se pudo volver a la branch original $originalBranch."
    }
}

Write-Output ""
Write-Output "Branches sin conflicto contra main ($(@($limpias).Count)):"
foreach ($b in $limpias) { Write-Output "  OK  $b" }

Write-Output ""
Write-Output "Branches con conflicto contra main ($(@($conflictivas).Count)):"
foreach ($b in $conflictivas) { Write-Output "  CONFLICTO  $b" }
