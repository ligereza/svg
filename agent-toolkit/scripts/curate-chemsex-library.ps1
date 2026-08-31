param(
  [switch]$Rebuild
)

$ErrorActionPreference = "Stop"
$toolkitRoot = Split-Path -Parent $PSScriptRoot
$repoRoot = Split-Path -Parent $toolkitRoot
$projectRoot = Join-Path $toolkitRoot "projects\chemsex"
$destination = Join-Path $projectRoot "context-shelf-library"
$manifestPath = Join-Path $destination "library-manifest.json"
$mediaExtensions = @(".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif")
$bioiconsCategories = @(
  "Blood_Immunology", "Cell_membrane", "Cell_types", "Chemistry", "General_items",
  "Human_physiology", "Lab_apparatus", "Microbiology", "Parasites", "People-Other",
  "Receptors_channels", "Safety_symbols", "Tissues", "Viruses"
)
$healthiconsCategories = @(
  "blood", "body", "conditions", "contraceptives", "devices", "diagnostics",
  "emotions", "medications", "nutrition", "objects", "people", "places", "ppe",
  "specialties", "symbols", "zoonoses"
)
$slideNames = @{
  "01" = "slide-01-cover"
  "02" = "slide-02-definition"
  "03" = "slide-03-care-context"
  "04" = "slide-04-substances"
  "05" = "slide-05-risks"
  "06" = "slide-06-care"
  "07" = "slide-07-interactions"
  "08" = "slide-08-close"
}

function Test-RejectedPath([string]$Path) {
  return $Path -match "[\\/]_rejected[^\\/]*(?:[\\/]|$)" -or $Path -match "[\\/]rejected[^\\/]*(?:[\\/]|$)"
}

function Get-SlideFolder([string]$Path) {
  $normalized = $Path.ToLowerInvariant()
  if ($normalized -match "iconos-transparentes-23[\\/](0[1-3])-") { return $slideNames["08"] }
  if ($normalized -match "iconos-transparentes-23[\\/](0[4-9]|1[0-1])-") { return $slideNames["05"] }
  if ($normalized -match "iconos-transparentes-23[\\/](1[2-9]|2[0-3])-") { return $slideNames["07"] }
  if ($normalized -match "slide[-_]?0?([1-8])") {
    $number = $Matches[1].PadLeft(2, "0")
    if ($slideNames.ContainsKey($number)) { return $slideNames[$number] }
  }
  if ($normalized -match "slide4[-_]?icon") { return $slideNames["04"] }
  return "other-generated"
}

function Add-MediaFile(
  [System.IO.FileInfo]$Source,
  [string]$TargetRelative,
  [string]$Category,
  [string]$Slide = $null,
  [string]$SourceType = "generated"
) {
  $target = Join-Path $destination ($TargetRelative -replace "/", "\")
  $targetDirectory = Split-Path -Parent $target
  New-Item -ItemType Directory -Force -Path $targetDirectory | Out-Null
  if (Test-Path -LiteralPath $target) {
    $existing = Get-Item -LiteralPath $target
    if ($existing.Length -ne $Source.Length) {
      throw "Destination collision with a different file: $target"
    }
  } else {
    New-Item -ItemType HardLink -Path $target -Target $Source.FullName | Out-Null
  }
  return [ordered]@{
    curatedPath = ($TargetRelative -replace "\\", "/")
    sourcePath = $Source.FullName
    category = $Category
    sourceType = $SourceType
    slide = $Slide
    format = $Source.Extension.TrimStart(".").ToLowerInvariant()
    bytes = $Source.Length
    linkType = "hardlink"
  }
}

if ($Rebuild -and (Test-Path -LiteralPath $destination)) {
  Remove-Item -LiteralPath $destination -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $destination | Out-Null
foreach ($slide in $slideNames.Values) {
  New-Item -ItemType Directory -Force -Path (Join-Path $destination "01-generated\02-slides\$slide") | Out-Null
}

$manifest = @()

$selectedRoot = Join-Path $projectRoot "assets"
foreach ($file in Get-ChildItem -LiteralPath $selectedRoot -File) {
  if ($mediaExtensions -contains $file.Extension.ToLowerInvariant()) {
    $manifest += Add-MediaFile $file "01-generated\01-selected-icons\$($file.Name)" "project-selected" $null "generated"
  }
}

$generatedRoot = Join-Path $projectRoot "generated"
foreach ($file in Get-ChildItem -LiteralPath $generatedRoot -File -Recurse) {
  if (($mediaExtensions -notcontains $file.Extension.ToLowerInvariant()) -or (Test-RejectedPath $file.FullName)) { continue }
  $relative = [System.IO.Path]::GetRelativePath($generatedRoot, $file.FullName)
  $slide = Get-SlideFolder $relative
  $manifest += Add-MediaFile $file "01-generated\02-slides\$slide\$($file.Name)" "project-generated" $slide "generated"
}

$editableRoot = Join-Path $projectRoot "editable"
foreach ($file in Get-ChildItem -LiteralPath $editableRoot -File -Recurse) {
  if ($mediaExtensions -contains $file.Extension.ToLowerInvariant()) {
    $relative = [System.IO.Path]::GetRelativePath($editableRoot, $file.FullName)
    $manifest += Add-MediaFile $file "01-generated\03-editable-previews\$relative" "project-editable" $null "generated"
  }
}

$historyRoot = Join-Path $repoRoot "rd_database_complete\assets"
foreach ($file in Get-ChildItem -LiteralPath $historyRoot -File -Recurse) {
  if (($mediaExtensions -notcontains $file.Extension.ToLowerInvariant()) -or (Test-RejectedPath $file.FullName)) { continue }
  $relative = [System.IO.Path]::GetRelativePath($historyRoot, $file.FullName)
  $slide = if ($relative -match "slide[-_]?0?([1-8])") { Get-SlideFolder $relative } else { $null }
  $manifest += Add-MediaFile $file "01-generated\04-history\rd-assets\$relative" "historical-chemsex" $slide "generated"
}

$bioiconsRoot = Join-Path $repoRoot "rd_database_complete\public_libraries\extracted\bioicons-main\static\icons"
foreach ($file in Get-ChildItem -LiteralPath $bioiconsRoot -File -Recurse) {
  if ($mediaExtensions -notcontains $file.Extension.ToLowerInvariant()) { continue }
  $relative = [System.IO.Path]::GetRelativePath($bioiconsRoot, $file.FullName)
  $parts = $relative -split '[\\/]'
  if (($parts.Count -lt 4) -or ($bioiconsCategories -notcontains $parts[1])) { continue }
  $tail = ($parts[2..($parts.Count - 1)] -join "\")
  $manifest += Add-MediaFile $file "02-downloaded-libraries\bioicons\$($parts[1])\$($parts[0])\$tail" "bioicons" $null "downloaded-library"
}

$healthiconsRoot = Join-Path $repoRoot "rd_database_complete\public_libraries\extracted\healthicons-icons\icons\svg"
foreach ($style in @("filled", "outline")) {
  $styleRoot = Join-Path $healthiconsRoot $style
  foreach ($file in Get-ChildItem -LiteralPath $styleRoot -File -Recurse) {
    if ($mediaExtensions -notcontains $file.Extension.ToLowerInvariant()) { continue }
    $relative = [System.IO.Path]::GetRelativePath($styleRoot, $file.FullName)
    $parts = $relative -split '[\\/]'
    if (($parts.Count -lt 2) -or ($healthiconsCategories -notcontains $parts[0])) { continue }
    $tail = ($parts[1..($parts.Count - 1)] -join "\")
    $manifest += Add-MediaFile $file "02-downloaded-libraries\healthicons\$style\$($parts[0])\$tail" "healthicons" $null "downloaded-library"
  }
}

$previewRoot = Join-Path $projectRoot "libraries\previews"
foreach ($file in Get-ChildItem -LiteralPath $previewRoot -File -Recurse) {
  if ($mediaExtensions -contains $file.Extension.ToLowerInvariant()) {
    $relative = [System.IO.Path]::GetRelativePath($previewRoot, $file.FullName)
    $manifest += Add-MediaFile $file "02-downloaded-libraries\previews\$relative" "reference-preview" $null "reference"
  }
}

$payload = [ordered]@{
  schemaVersion = 1
  generatedAt = (Get-Date).ToUniversalTime().ToString("o")
  project = "chemsex"
  root = $destination
  policy = [ordered]@{
    originalsPreserved = $true
    rejectedAssetsExcluded = $true
    storage = "hardlink"
  }
  counts = [ordered]@{
    total = $manifest.Count
    svg = @($manifest | Where-Object { $_.format -eq "svg" }).Count
    raster = @($manifest | Where-Object { $_.format -ne "svg" }).Count
  }
  files = $manifest
}
$payload | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding utf8
Write-Output ($payload | ConvertTo-Json -Depth 4)
