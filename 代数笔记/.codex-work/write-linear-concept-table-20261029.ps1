$ErrorActionPreference = 'Stop'
$root='C:\Users\WANYIWIGE\Desktop\我的笔记\代数笔记'
$work=Join-Path $root '.codex-work'
$entries=Get-Content -Raw -LiteralPath (Join-Path $work 'linear-concept-entries-20261029.json') | ConvertFrom-Json
$compare=[Globalization.CultureInfo]::GetCultureInfo('zh-CN').CompareInfo
$sorted=@($entries | ForEach-Object {
    $plain=$_.name -replace '\$', '' -replace '\\lambda','lambda'
    $key=[Convert]::ToHexString($compare.GetSortKey($plain,[Globalization.CompareOptions]::IgnoreSymbols).KeyData)
    [pscustomobject]@{name=$_.name;target=$_.target;sortKey=$key}
} | Sort-Object sortKey,name)
$reference=[IO.File]::ReadAllText((Join-Path $root 'chapters\Part 2\concept-review.tex'))
$cut=$reference.IndexOf('\endlastfoot')+'\endlastfoot'.Length
if($cut -lt 13) {throw '参考表结构不符。'}
$header=$reference.Substring(0,$cut).Replace('前两章概念复查表','线性代数概念复查表')
$lines=[Collections.Generic.List[string]]::new()
$lines.Add($header)
for($i=0;$i -lt $sorted.Count;$i+=2){
    $a=$sorted[$i]
    $left='\hyperref['+$a.target+']{'+$a.name+'}'
    $right=''
    if($i+1 -lt $sorted.Count){$b=$sorted[$i+1];$right='\hyperref['+$b.target+']{'+$b.name+'}'}
    $lines.Add($left+' & '+$right+'\\')
}
$lines.Add("\end{longtable}`n\endgroup`n")
[IO.File]::WriteAllText((Join-Path $root 'chapters\Part 1\concept-review.tex'),($lines -join "`n"),[Text.UTF8Encoding]::new($false))
$mainPath=Join-Path $root 'main.tex'
$main=[IO.File]::ReadAllText($mainPath)
[IO.File]::WriteAllText((Join-Path $work 'main-linear-concept-final-20261029.tex'),$main,[Text.UTF8Encoding]::new($false))
$validation=$main.Replace('%\input{chapters/Part 1/concept-review}','\input{chapters/Part 1/concept-review}')
$validation=[regex]::Replace($validation,'(?m)^%(\\(?:setpartimage\{figure/part1封面图\.jpg\}|setpartintro\{从整数与多项式[^\r\n]*|part\{线性代数\}|algebrachapter\{chapters/Part 1/chapter[1-7]\}))','$1')
if([regex]::Matches($validation,'(?m)^\\algebrachapter\{chapters/Part 1/chapter[1-7]\}').Count -ne 7){throw '线代七章未全部启用。'}
if([IO.File]::ReadAllText($mainPath) -cne $main){throw '主文档出现并发修改。'}
[IO.File]::WriteAllText((Join-Path $work 'main-linear-concept-validation-20261029.tex'),$validation,[Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText($mainPath,$validation,[Text.UTF8Encoding]::new($false))
"独立表已生成，共 $($sorted.Count) 项；临时启用七章与表入口检查。"
