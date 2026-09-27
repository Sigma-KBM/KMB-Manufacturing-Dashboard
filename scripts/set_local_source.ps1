[CmdletBinding()]
param(
    [switch]$Reset
)

$projectRoot = Split-Path -Parent $PSScriptRoot
$sourceFile = Join-Path $projectRoot 'data\kmb_synthetic_operations.xlsx'
$expressionFile = Join-Path $projectRoot 'powerbi\KMB_SemanticModel.SemanticModel\definition\expressions.tmdl'

if (-not $Reset -and -not (Test-Path -LiteralPath $sourceFile)) {
    throw "The synthetic source workbook was not found at: $sourceFile"
}

if (-not (Test-Path -LiteralPath $expressionFile)) {
    throw "The semantic model expression file was not found at: $expressionFile"
}

$content = [System.IO.File]::ReadAllText($expressionFile)
if ($Reset) {
    $replacement = 'expression pSourceFile = "__RUN_scripts_set_local_source.ps1__" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'
}
else {
    $portablePath = [System.IO.Path]::GetFullPath($sourceFile)
    $replacement = 'expression pSourceFile = "' + $portablePath + '" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'
}
$updated = [System.Text.RegularExpressions.Regex]::Replace(
    $content,
    '(?m)^expression pSourceFile = .*$',
    $replacement,
    1
)

if ($updated -eq $content) {
    Write-Host 'Power BI source configuration is already in the requested state.'
    return
}

[System.IO.File]::WriteAllText($expressionFile, $updated, [System.Text.UTF8Encoding]::new($false))
if ($Reset) {
    Write-Host 'Power BI source reset to the portable repository placeholder.'
}
else {
    Write-Host "Power BI source configured for: $portablePath"
}
