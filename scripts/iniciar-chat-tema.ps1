<#
Inicio de branch por tema para chats paralelos - Joyas MCGHR

Uso:
  powershell -ExecutionPolicy Bypass -File .\scripts\iniciar-chat-tema.ps1 -RepoPath "C:\ruta\al\repo" -Tema "modulo-inventario"

Si ExecutionPolicy del sistema bloquea scripts sin firmar, el flag
-ExecutionPolicy Bypass de arriba aplica solo a este proceso.

Que hace (ver ADR-008 en docs/ADR.md):
  - Verifica que RepoPath sea un repo git valido.
  - Actualiza main local desde origin.
  - Crea (o cambia a, si ya existe) una branch feature/<tema-slug> desde
    main actualizado.
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath,

    [Parameter(Mandatory = $true)]
    [string]$Tema
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

$temaSlug = $Tema.ToLowerInvariant() -replace '[^a-z0-9]+', '-'
$temaSlug = $temaSlug.Trim('-')
if ([string]::IsNullOrWhiteSpace($temaSlug)) {
    Write-Error "El tema no genero un slug valido: '$Tema'"
    exit 1
}
$branchName = "feature/$temaSlug"

try {
    git -C $repoPathResolved fetch origin 2>&1 | Out-Null
} catch {
    Write-Warning "No se pudo hacer fetch de origin. Sigo con el estado local de main."
}

try {
    git -C $repoPathResolved checkout main 2>&1 | Out-Null
    git -C $repoPathResolved pull origin main 2>&1 | Out-Null
} catch {
    Write-Warning "No se pudo actualizar main local desde origin. Reviso el error manualmente antes de seguir."
}

try {
    $existingBranches = @(git -C $repoPathResolved branch --list $branchName 2>$null)
} catch {
    $existingBranches = @()
}

if (@($existingBranches).Count -gt 0) {
    Write-Output "La branch $branchName ya existe. Cambiando a ella."
    try {
        git -C $repoPathResolved checkout $branchName 2>&1 | Out-Null
    } catch {
        Write-Error "No se pudo cambiar a la branch existente $branchName"
        exit 1
    }
} else {
    Write-Output "Creando branch $branchName desde main."
    try {
        git -C $repoPathResolved checkout -b $branchName 2>&1 | Out-Null
    } catch {
        Write-Error "No se pudo crear la branch $branchName"
        exit 1
    }
}

Write-Output "Listo. Branch activa: $branchName"
