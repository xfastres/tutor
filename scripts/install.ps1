<#
.SYNOPSIS
  Link this tutor skill into the folders that common agents scan for skills.

.DESCRIPTION
  A skill is just this directory. Agents look in different places, so this
  script creates directory junctions (no admin needed) that all point back to
  the one source directory. Edit the repo once; every agent sees it.

  Default targets (user level):
    ~/.agents/skills/tutor   Cursor, Codex, and other agents reading .agents/skills
    ~/.claude/skills/tutor   Claude Code
    ~/.codex/skills/tutor    Codex CLI

  -Cursor        also ~/.cursor/skills/tutor
  -Project DIR   also DIR/.agents/skills/tutor and DIR/.claude/skills/tutor
  -Uninstall     remove junctions this script created; never deletes a real folder

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/install.ps1
  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -Project D:\work\repo
  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -Uninstall
#>
param(
    [switch]$Cursor,
    [string]$Project,
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'
$src = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path.TrimEnd('\')

if (-not (Test-Path (Join-Path $src 'SKILL.md'))) {
    throw "SKILL.md not found next to scripts/: $src"
}

$targets = @(
    (Join-Path $HOME '.agents\skills\tutor'),
    (Join-Path $HOME '.claude\skills\tutor'),
    (Join-Path $HOME '.codex\skills\tutor')
)
if ($Cursor) { $targets += (Join-Path $HOME '.cursor\skills\tutor') }
if ($Project) {
    $proj = (Resolve-Path $Project).Path
    $targets += (Join-Path $proj '.agents\skills\tutor'), (Join-Path $proj '.claude\skills\tutor')
}

function Get-LinkTarget($item) {
    $t = @($item.Target)[0]
    if (-not $t) { return $null }
    try { return (Resolve-Path $t).Path.TrimEnd('\') } catch { return $t }
}

foreach ($t in $targets) {
    $item = Get-Item -LiteralPath $t -ErrorAction SilentlyContinue

    if ($Uninstall) {
        if ($item -and $item.LinkType) {
            # Directory.Delete on a junction removes only the link, not the target contents
            [System.IO.Directory]::Delete($t, $false)
            Write-Host "removed  $t"
        } elseif ($item) {
            Write-Host "skip     $t (real folder, not touched)"
        } else {
            Write-Host "absent   $t"
        }
        continue
    }

    if ($item) {
        if ($item.LinkType) {
            $linkTarget = Get-LinkTarget $item
            if ($linkTarget -eq $src) { Write-Host "ok       $t" }
            else { Write-Host "conflict $t -> $linkTarget (different source; remove it first)" }
        } else {
            Write-Host "conflict $t is a real folder; move it away first"
        }
        continue
    }

    New-Item -ItemType Directory -Force -Path (Split-Path $t) | Out-Null
    New-Item -ItemType Junction -Path $t -Target $src | Out-Null
    Write-Host "linked   $t -> $src"
}

if (-not $Uninstall) {
    Write-Host ""
    Write-Host "Invoke with: /tutor 继续   (or: 用 tutor skill，继续)"
    Write-Host "If an agent does not list the skill, tell it: 读 $src\SKILL.md，按 RUNBOOK 开课"
}
