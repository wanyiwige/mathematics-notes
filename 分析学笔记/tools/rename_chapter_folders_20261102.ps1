$ErrorActionPreference = 'Stop'
$taskRoot = (Get-Location).Path
$chapterRoot = (Resolve-Path -LiteralPath (Join-Path $taskRoot 'chapters')).Path
$backupDir = Join-Path $taskRoot 'codex-build-chapter-rename-20261102'
if (Test-Path -LiteralPath $backupDir) { throw 'Backup directory already exists; stop to avoid overwriting.' }
$moves = @()
foreach ($part in (Get-ChildItem -LiteralPath $chapterRoot -Directory)) {
    foreach ($folder in (Get-ChildItem -LiteralPath $part.FullName -Directory | Where-Object { $_.Name -cmatch '^section[0-9]{2}$' })) {
        $source = (Resolve-Path -LiteralPath $folder.FullName).Path
        $destination = Join-Path $part.FullName ($folder.Name -creplace '^section','chapter')
        if (-not $source.StartsWith($chapterRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw "Outside chapters: $source" }
        if (Test-Path -LiteralPath $destination) { throw "Destination already exists: $destination" }
        $files = @(Get-ChildItem -LiteralPath $source -File -Recurse | ForEach-Object {
            [pscustomobject]@{ Relative = $_.FullName.Substring($source.Length); Hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
        })
        $moves += [pscustomobject]@{ Source = $source; Destination = $destination; Files = $files }
    }
}
if ($moves.Count -eq 0) { throw 'No section folders found.' }
New-Item -ItemType Directory -Path $backupDir | Out-Null
Compress-Archive -LiteralPath $chapterRoot -DestinationPath (Join-Path $backupDir 'chapters-before.zip')
Copy-Item -LiteralPath (Join-Path $taskRoot 'main.tex') -Destination (Join-Path $backupDir 'main-before.tex')
foreach ($item in $moves) { Rename-Item -LiteralPath $item.Source -NewName ([IO.Path]::GetFileName($item.Destination)) }
foreach ($item in $moves) {
    foreach ($file in $item.Files) {
        $newPath = $item.Destination + $file.Relative
        if (-not (Test-Path -LiteralPath $newPath) -or (Get-FileHash -LiteralPath $newPath -Algorithm SHA256).Hash -ne $file.Hash) { throw "Moved file failed hash check: $newPath" }
    }
}
$utf8 = [System.Text.UTF8Encoding]::new($false)
$candidates = @((Get-ChildItem -LiteralPath $chapterRoot -File -Recurse | Where-Object { $_.Extension -in '.tex','.md' }))
$candidates += Get-Item -LiteralPath (Join-Path $taskRoot 'main.tex')
$updated = 0
foreach ($file in $candidates) {
    $before = [IO.File]::ReadAllText($file.FullName, [Text.Encoding]::UTF8)
    $after = [regex]::Replace($before, '(part(?:[0-9]+|m)/)section([0-9]{2})/', '${1}chapter${2}/')
    if ($file.Name -eq 'README.md' -and $file.DirectoryName -eq $chapterRoot) {
        $after = $after.Replace('目录 sectionNN 对应', '目录 chapterNN 对应')
    }
    if ($file.FullName -eq (Join-Path $chapterRoot 'part2\section3-4.tex')) {
        $after = $after.Replace('section03/section04.tex', 'chapter03/section04.tex')
    }
    if ($before -cne $after) {
        $bytes = [IO.File]::ReadAllBytes($file.FullName)
        $hasBom = $bytes.Length -ge 3 -and $bytes[0] -eq 239 -and $bytes[1] -eq 187 -and $bytes[2] -eq 191
        [IO.File]::WriteAllText($file.FullName, $after, [Text.UTF8Encoding]::new($hasBom))
        $updated++
    }
}
Write-Output "Moved directories: $($moves.Count); updated source/index files: $updated; all moved file hashes matched before reference updates."
Write-Output "Backup: $backupDir\chapters-before.zip"
