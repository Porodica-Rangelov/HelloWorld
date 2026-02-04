<#
.SYNOPSIS
  Update GitHub Issues based on README.md tasks.
.DESCRIPTION
  For each "### Task X:" section in README.md:
  - Finds the matching GitHub Issue by title
  - Updates its body with task content
  - Skips non-ASCII characters (safe for CLI)
#>

# ----------------------------
# Helper: remove non-ASCII chars
function Remove-NonAscii {
    param([string]$Text)

    -join ($Text.ToCharArray() | Where-Object { [int][char]$_ -lt 128 })
}

# ----------------------------
# Config
$ReadmePath = "README.md"

if (-not (Test-Path $ReadmePath)) {
    Write-Error "README.md not found: $ReadmePath"
    exit 1
}

# ----------------------------
# Load README
$Lines = Get-Content $ReadmePath

Write-Host "`nProcessing README tasks..." -ForegroundColor Cyan

for ($i = 0; $i -lt $Lines.Count; $i++) {

    # Match: ### Task X:
    if ($Lines[$i] -match '^###\s*Task\s+\d+:') {

        # Issue title
        $TitleRaw = $Lines[$i] -replace '^###\s*', ''
        $Title    = Remove-NonAscii $TitleRaw

        # Collect body lines
        $BodyLines = @()

        for ($j = $i + 1; $j -lt $Lines.Count; $j++) {
            if ($Lines[$j] -match '^###\s*Task\s+\d+:') { break }
            if ($Lines[$j].Trim()) {
                $BodyLines += $Lines[$j]
            }
        }

        if ($BodyLines.Count -eq 0) {
            Write-Warning "Skipping empty task: $Title"
            continue
        }

        $Body = Remove-NonAscii ($BodyLines -join "`n")

        Write-Host "`nSearching issue: $Title" -ForegroundColor Yellow

        # ----------------------------
        # Find issue by title
        $IssueNumber = gh issue list `
            --search "$Title" `
            --json number,title `
            --jq '.[0].number' 2>$null

        if (-not $IssueNumber) {
            Write-Warning "Issue not found: $Title"
            continue
        }

        Write-Host "Updating Issue #$IssueNumber" -ForegroundColor Green

        # ----------------------------
        # Update issue
        gh issue edit $IssueNumber `
            --body "$Body"
    }
}

Write-Host "`nAll tasks processed." -ForegroundColor Cyan