<#
.SYNOPSIS
  Create GitHub Issues from Sprint1.md tasks.
.DESCRIPTION
  Parses Sprint1.md, extracts each "### Task X:" section,
  and creates a new GitHub Issue with the appropriate title,
  body, and labels (sprint1, complexity level).
  Skips tasks that already have a matching open issue.
#>

# ----------------------------
# Helper: remove non-ASCII chars
function Remove-NonAscii {
    param([string]$Text)
    -join ($Text.ToCharArray() | Where-Object { [int][char]$_ -lt 128 })
}

# ----------------------------
# Config
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$MdPath    = Join-Path $ScriptDir "Sprint1.md"

if (-not (Test-Path $MdPath)) {
    Write-Error "Sprint1.md not found: $MdPath"
    exit 1
}

# ----------------------------
# Ensure labels exist
$RequiredLabels = @(
    @{ Name = "sprint1";       Color = "1D76DB"; Description = "Sprint 1 zadatak" }
    @{ Name = "complexity-1";  Color = "0E8A16"; Description = "Lak zadatak" }
    @{ Name = "complexity-2";  Color = "FBCA04"; Description = "Srednji zadatak" }
    @{ Name = "complexity-3";  Color = "D93F0B"; Description = "Tezi zadatak" }
)

Write-Host "`nChecking labels..." -ForegroundColor Cyan
$ExistingLabels = gh label list --json name --jq ".[].name" 2>$null

foreach ($lbl in $RequiredLabels) {
    if ($ExistingLabels -notcontains $lbl.Name) {
        Write-Host "  Creating label: $($lbl.Name)" -ForegroundColor Yellow
        gh label create $lbl.Name --color $lbl.Color --description $lbl.Description 2>$null
    } else {
        Write-Host "  Label exists: $($lbl.Name)" -ForegroundColor Green
    }
}

# ----------------------------
# Load existing open issues to avoid duplicates
Write-Host "`nLoading existing issues..." -ForegroundColor Cyan
$ExistingIssues = gh issue list --state open --limit 100 --json title --jq ".[].title" 2>$null

# ----------------------------
# Parse Sprint1.md
$Lines = Get-Content $MdPath

Write-Host "`nParsing Sprint1.md..." -ForegroundColor Cyan

$Tasks = @()

for ($i = 0; $i -lt $Lines.Count; $i++) {

    if ($Lines[$i] -match '^###\s*Task\s+(\d+):\s*(.+)\s*\[Kompleksnost:\s*(\d+)\]') {

        $TaskNum    = $Matches[1]
        $TaskTitle  = $Matches[2].Trim()
        $Complexity = $Matches[3]

        # Collect body lines until next task/separator/section
        $BodyLines = @()

        for ($j = $i + 1; $j -lt $Lines.Count; $j++) {
            if ($Lines[$j] -match '^###\s*Task\s+\d+:') { break }
            if ($Lines[$j] -match '^---\s*$')            { break }
            if ($Lines[$j] -match '^##\s+')              { break }
            $BodyLines += $Lines[$j]
        }

        # Trim leading/trailing empty lines from body
        while ($BodyLines.Count -gt 0 -and $BodyLines[0].Trim() -eq '') {
            $BodyLines = $BodyLines[1..($BodyLines.Count - 1)]
        }
        while ($BodyLines.Count -gt 0 -and $BodyLines[-1].Trim() -eq '') {
            $BodyLines = $BodyLines[0..($BodyLines.Count - 2)]
        }

        $Tasks += @{
            Number     = $TaskNum
            Title      = $TaskTitle
            Complexity = $Complexity
            Body       = $BodyLines -join "`n"
        }
    }
}

Write-Host "Found $($Tasks.Count) tasks." -ForegroundColor Cyan

# ----------------------------
# Create issues
$Created = 0
$Skipped = 0

foreach ($task in $Tasks) {

    $IssueTitle = "Sprint1 - Task $($task.Number): $($task.Title)"
    $IssueTitle = Remove-NonAscii $IssueTitle

    # Check for duplicate
    $Duplicate = $false
    foreach ($existing in $ExistingIssues) {
        if ($existing -eq $IssueTitle) {
            $Duplicate = $true
            break
        }
    }

    if ($Duplicate) {
        Write-Host "`n[SKIP] Issue already exists: $IssueTitle" -ForegroundColor DarkYellow
        $Skipped++
        continue
    }

    $Labels = "sprint1,complexity-$($task.Complexity)"

    $IssueBody = Remove-NonAscii $task.Body

    Write-Host "`n[CREATE] $IssueTitle" -ForegroundColor Green
    Write-Host "  Labels: $Labels" -ForegroundColor DarkGray

    # Write body to temp file to avoid CLI escaping issues
    $TempFile = [System.IO.Path]::GetTempFileName()
    $IssueBody | Out-File -FilePath $TempFile -Encoding utf8

    gh issue create `
        --title "$IssueTitle" `
        --body-file "$TempFile" `
        --label "$Labels"

    Remove-Item $TempFile -Force

    $Created++
}

# ----------------------------
# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Created: $Created issue(s)" -ForegroundColor Green
Write-Host "  Skipped: $Skipped (already exist)" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan