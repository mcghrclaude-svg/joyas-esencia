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
  - Regenera la seccion "URLs para web_fetch" de CLAUDE.md, recalculando
    cual es el docs/HANDOFF_*.md mas reciente segun la fecha del archivo
    (LastWriteTime), no una fecha fija. Ver docs/citas/CITA-001.md para
    el motivo (api.github.com bloqueada para web_fetch).
  - No commitea ni pushea nada automaticamente: solo diagnostica y
    actualiza en disco la seccion autogenerada de CLAUDE.md.
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath
)

$ErrorActionPreference = 'Continue'

function Update-WebFetchUrlsSection {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoPathResolved
    )

    $rawBaseUrl = "https://raw.githubusercontent.com/mcghrclaude-svg/joyas-esencia/main"
    $claudeMdPath = Join-Path -Path $RepoPathResolved -ChildPath "CLAUDE.md"
    $docsPath = Join-Path -Path $RepoPathResolved -ChildPath "docs"

    if (-not (Test-Path -LiteralPath $claudeMdPath)) {
        Write-Warning "No se encontro CLAUDE.md en $RepoPathResolved. No se regenera la seccion de URLs."
        return
    }

    $handoffFiles = @(Get-ChildItem -LiteralPath $docsPath -Filter "HANDOFF_*.md" -File -ErrorAction SilentlyContinue)

    if (@($handoffFiles).Count -eq 0) {
        Write-Warning "No se encontro ningun docs/HANDOFF_*.md. No se regenera la seccion de URLs."
        return
    }

    $ultimoHandoff = $handoffFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1

    $urls = @(
        "$rawBaseUrl/docs/ADR.md",
        "$rawBaseUrl/docs/CITA.md",
        "$rawBaseUrl/docs/ESTADO_PROYECTO.md",
        "$rawBaseUrl/docs/$($ultimoHandoff.Name)"
    )

    $inicioMarcador = "<!-- INICIO-AUTOGENERADO: URLs para web_fetch, no editar a mano, ver scripts/cerrar-sesion.ps1 -->"
    $finMarcador = "<!-- FIN-AUTOGENERADO -->"

    $seccionLines = New-Object System.Collections.Generic.List[string]
    $seccionLines.Add($inicioMarcador)
    $seccionLines.Add("Estas URLs raw sirven para que Claude.ai (via web_fetch) lea el estado")
    $seccionLines.Add("real del repo sin depender de contenido de sesiones anteriores. Nunca")
    $seccionLines.Add("usar api.github.com para esto (ver docs/citas/CITA-001.md): esta")
    $seccionLines.Add("bloqueada por deteccion de bots para la herramienta web_fetch.")
    $seccionLines.Add("")
    foreach ($url in $urls) {
        $seccionLines.Add("- $url")
    }
    $seccionLines.Add("")
    $seccionLines.Add("Esta lista se regenera automaticamente en cada cierre de sesion (ver")
    $seccionLines.Add("scripts/cerrar-sesion.ps1); el HANDOFF listado es siempre el mas")
    $seccionLines.Add("reciente segun fecha de archivo.")
    $seccionLines.Add($finMarcador)

    $nuevaSeccion = [string]::Join("`r`n", $seccionLines)

    $contenidoActual = Get-Content -LiteralPath $claudeMdPath -Raw

    if ($contenidoActual -notmatch [regex]::Escape($inicioMarcador)) {
        Write-Warning "CLAUDE.md no tiene los marcadores autogenerados de 'URLs para web_fetch'. No se modifica el archivo; agregalos manualmente una vez."
        return
    }

    $patron = "(?s)$([regex]::Escape($inicioMarcador)).*?$([regex]::Escape($finMarcador))"
    $contenidoNuevo = [regex]::Replace($contenidoActual, $patron, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $nuevaSeccion })

    if ($contenidoNuevo -ne $contenidoActual) {
        Set-Content -LiteralPath $claudeMdPath -Value $contenidoNuevo -NoNewline
        Write-Output "CLAUDE.md actualizado: seccion 'URLs para web_fetch' regenerada (HANDOFF mas reciente: $($ultimoHandoff.Name))."
    } else {
        Write-Output "CLAUDE.md ya tenia la seccion 'URLs para web_fetch' al dia (HANDOFF mas reciente: $($ultimoHandoff.Name))."
    }
}

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

try {
    Update-WebFetchUrlsSection -RepoPathResolved $repoPathResolved
} catch {
    Write-Warning "No se pudo regenerar la seccion 'URLs para web_fetch' de CLAUDE.md: $($_.Exception.Message)"
}
