$ErrorActionPreference = 'Stop'
$projectRoot = 'C:\Users\WANYIWIGE\Desktop\我的笔记\代数笔记'
$chapterPath = Join-Path $projectRoot 'chapters\Part 2\chapter3.tex'
$workDir = Join-Path $projectRoot '.codex-work'
$backupPath = Join-Path $workDir 'chapter3-before-detailed-rewrite-20261028.tex'
if ((Get-FileHash -LiteralPath $chapterPath).Hash -ne (Get-FileHash -LiteralPath $backupPath).Hash) {
    throw '第三章在备份后有新的修改，请先合并用户改动。'
}
$old = [IO.File]::ReadAllText($chapterPath).Replace("`r`n", "`n")
$section1 = $old.Substring(0, $old.IndexOf('\section{环的直和}'))
$section1 = $section1.Replace('\section{环的同态定理}', @'
\section{环的同态定理}

环的同态同时保持加法与乘法。它的核是理想，因此可以先用加法群的同态定理构造商群之间的对应，再验证这些对应保持乘法。本节不要求环交换，也不要求有单位元；理想均指双边理想。

先说明交与和在子环、理想中分别具有哪些封闭性质。对非空子集，检验它是子环，可以验证任意两个元素之差及其乘积仍在其中；理想则还须验证左右乘以母环中任意元素后仍在其中。
'@)
$section1 = $section1.Replace("\begin{definition}`n`t定义", '\begin{definition}' + "`n" + '设$H,N$为环$R$的子环，定义它们的和为')
$section1 = $section1.Replace('集合$H+N$对加法和取负封闭。若$N$为理想，取$a_i\in H,b_i\in N$，则', @'
由于$0=0+0\in H+N$，此集合非空。若$a_i\in H,b_i\in N$，则
\[
(a_1+b_1)-(a_2+b_2)=(a_1-a_2)+(b_1-b_2)\in H+N.
\]
因此$H+N$是加法子群。若$N$为理想，则
'@)
$section1 = $section1.Replace('故$H+N$为子环。若$H$也为理想，则对$r\in R$有', '这里$a_1a_2\in H$，其余三项均在$N$中，所以乘积属于$H+N$，故它为子环。若$H$也为理想，则对$r\in R$有')
$section1 = $section1.Replace('$H,N$都是子环，但$H+N$不是子环：取其中两个非零矩阵相乘，可得到非零对角矩阵。', @'
$H,N$中的任意两个矩阵相乘均为零，且各自对减法封闭，所以都是子环。但取
\[
\begin{pmatrix}0&0\\1&0\end{pmatrix}\in H,\qquad
\begin{pmatrix}0&1\\0&0\end{pmatrix}\in N,
\]
它们相乘得到
\[
\begin{pmatrix}0&0\\1&0\end{pmatrix}
\begin{pmatrix}0&1\\0&0\end{pmatrix}
=\begin{pmatrix}0&0\\0&1\end{pmatrix}\notin H+N.
\]
因为$H+N$中每个矩阵的对角线元素均为零，故$H+N$不是子环。这说明不能从两个子环直接推出其和仍为子环。
'@)
$section1 = $section1.Replace('由命题\ref{p2:ring-image-preimage}', '由引理\ref{p2:ring-image-preimage}')
$section1 = $section1.Replace('若$H$为子环，则$\sigma(H)$对减法和乘法封闭。', @'
由于$0\in H$，$0\in\sigma(H)$。任取$\sigma(a),\sigma(b)\in\sigma(H)$，有
\[
\sigma(a)-\sigma(b)=\sigma(a-b)\in\sigma(H),\qquad
\sigma(a)\sigma(b)=\sigma(ab)\in\sigma(H).
\]
所以$\sigma(H)$为子环。
'@)
$section1 = $section1.Replace('反过来，子环$H\''\subseteq R\''$的完全反像$\sigma^{-1}(H\'')$是$R$的一个加法子群且对乘法封闭，从而为子环且包含$N$。'.Replace('\''', ''''), @'
若$x,y\in\sigma^{-1}(H')$，则$\sigma(x),\sigma(y)\in H'$，所以
\[
\sigma(x-y)=\sigma(x)-\sigma(y)\in H',\qquad
\sigma(xy)=\sigma(x)\sigma(y)\in H'.
\]
因此$x-y,xy\in\sigma^{-1}(H')$。又$0\in H'$，故$\ker\sigma\subseteq\sigma^{-1}(H')$，特别地该反像非空，是包含$N$的子环。
'@)
$needle = '再验证$\overline\sigma$保持乘法。'
$insert = @'
具体地，若$x+H=y+H$，则$x-y\in H$，故$\sigma(x)-\sigma(y)\in H'$，两者在$R'/H'$中的类相同，所以映射良好定义。它保持加法；由$\sigma$满射可知它满射。若$\overline\sigma(x+H)=H'$，则$\sigma(x)\in\sigma(H)$，于是
\[
x\in\sigma^{-1}(\sigma(H))=H+N=H.
\]
故核为零，确为加法群同构。这里用到了$N\subseteq H$，它正是单射性成立的条件。

再验证$\overline\sigma$保持乘法。
'@
$section1 = $section1.Replace($needle, $insert)
$section1 = $section1.Replace('其核为$H\cap N$，故', @'
此限制的核恰为$\{h\in H:h\in N\}=H\cap N$。其像是$\pi(H)$，应用环同态基本定理得
'@)
$section1 += @'

\begin{example}
设$m,n$为正整数，记$d=\gcd(m,n)$、$M=\operatorname{lcm}(m,n)$。在$\mathbb Z$中，
\[
(m)+(n)=(d),\qquad(m)\cap(n)=(M).
\]
第一式的理由是：和中的每个元素$am+bn$均被$d$整除；反过来，贝祖等式给出$d=um+vn$，所以每个$d$的倍数均在和中。第二式的理由是：同时属于两个理想，等价于同时被$m,n$整除，也就是被最小公倍数$M$整除。

在第二同构定理中取$H=(n)$、$N=(m)$，得到
\[
(n)/(M)\cong(d)/(m).
\]
左侧加法群有$M/n$个元素，右侧有$m/d$个元素：分别可取$0,n,\ldots,(M/n-1)n$及$0,d,\ldots,(m/d-1)d$为代表元。因此
\[
\frac Mn=\frac md,\qquad dM=mn.
\]
这也从理想与商环的关系说明最大公因数、最小公倍数之间的等式。
\end{example}

'@
[IO.File]::WriteAllText((Join-Path $workDir 'c3-section1-20261028.tex'), $section1, [Text.UTF8Encoding]::new($false))
$parts = @($section1)
for ($i=2; $i -le 8; $i++) {
    $fragment = [IO.File]::ReadAllText((Join-Path $workDir "c3-section$i-20261028.tex")).Replace("`r`n", "`n")
    $parts += $fragment
}
$full = ($parts -join "`n`n") + "`n`n%\section{章末习题中的知识与解法}`n%\input{chapters/Part 2/chapter3-exercises}`n"
[IO.File]::WriteAllText((Join-Path $workDir 'chapter3-full-rewrite-20261028.tex'), $full, [Text.UTF8Encoding]::new($false))
$cut = $full.IndexOf('\section{环的反同构}')
$active = $full.Substring(0,$cut)
$disabled = (($full.Substring($cut) -split "`n" | ForEach-Object { if ($_.StartsWith('%')) { $_ } else { '%' + $_ } }) -join "`n")
$final = $active + $disabled
[IO.File]::WriteAllText($chapterPath, $final, [Text.UTF8Encoding]::new($false))
Write-Output "第三章已保存；完整文本 $($full.Length) 字符；保留第三至八节的注释状态。"
