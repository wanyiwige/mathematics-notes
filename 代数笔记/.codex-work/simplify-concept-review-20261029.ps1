$ErrorActionPreference = 'Stop'
$root = 'C:\Users\WANYIWIGE\Desktop\我的笔记\代数笔记'
$path = Join-Path $root 'chapters\Part 2\concept-review.tex'
$old = [IO.File]::ReadAllText($path)
$rows = [regex]::Matches($old, '(?m)^\\hyperref\[([^\]]+)\]\{(.+?)\} & \\hyperref\[')
if ($rows.Count -ne 119) { throw '原概念条目数量不符，先检查当前文件。' }
$compare = [Globalization.CultureInfo]::GetCultureInfo('zh-CN').CompareInfo
$entries = foreach ($r in $rows) {
    $target = $r.Groups[1].Value
    $term = $r.Groups[2].Value
    if ($term -eq '导出子群与导出列') { $names = @('导出子群','导出列') }
    else { $names = $term -split '、' }
    foreach ($name in $names) {
        $keyName = $name -replace '\$', ''
        if ($keyName -eq 'n元对称群') { $keyName = '对称群' }
        $keyBytes = $compare.GetSortKey($keyName, [Globalization.CompareOptions]::IgnoreSymbols).KeyData
        $sortKey = [Convert]::ToHexString($keyBytes)
        [pscustomobject]@{ Name=$name; Target=$target; SortKey=$sortKey }
    }
}
$sorted = @($entries | Sort-Object SortKey,Name)
$out = [Collections.Generic.List[string]]::new()
$out.Add(@'
% !TEX root = ../../main.tex
\chapter*{前两章概念复查表}
\phantomsection
\addcontentsline{toc}{chapter}{前两章概念复查表}
\markboth{前两章概念复查表}{前两章概念复查表}

\begingroup
\setlength{\tabcolsep}{8pt}
\renewcommand{\arraystretch}{1.25}
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{0.47\linewidth}>{\raggedright\arraybackslash}p{0.47\linewidth}@{}}
\hline
\endfirsthead
\hline
\endhead
\hline
\endfoot
\hline
\endlastfoot
'@)
for ($i=0; $i -lt $sorted.Count; $i+=2) {
    $a = $sorted[$i]
    $left = '\hyperref[' + $a.Target + ']{' + $a.Name + '}'
    $right = ''
    if ($i+1 -lt $sorted.Count) {
        $b = $sorted[$i+1]
        $right = '\hyperref[' + $b.Target + ']{' + $b.Name + '}'
    }
    $out.Add($left + ' & ' + $right + '\\')
}
$out.Add("\end{longtable}`n\endgroup`n")
if ([IO.File]::ReadAllText($path) -cne $old) { throw '文件出现并发修改。' }
[IO.File]::WriteAllText($path, ($out -join "`n"), [Text.UTF8Encoding]::new($false))
$sorted | Select-Object Name,Target | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root '.codex-work\concept-review-sorted-20261029.json') -Encoding utf8
"已按中文音序排列为 $($sorted.Count) 个可点击概念，每行两项。"
$sorted | Select-Object -First 12 -ExpandProperty Name
