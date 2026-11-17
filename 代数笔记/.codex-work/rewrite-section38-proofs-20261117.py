from pathlib import Path
import re

root=Path(r'C:\Users\WANYIWIGE\Desktop\我的笔记\代数笔记')
p=root/'chapters/Part 2/chapter3.tex'
raw=p.read_bytes(); text=raw.decode('utf-8')
pos=text.index(r'\section{多项式函数}')
prefix,section=text[:pos],text[pos:]
proofs=list(re.finditer(r'\\begin\{proof\}(?:\[[^\]]*\])?[\s\S]*?\\end\{proof\}',section))
assert len(proofs)==3, '第八节证明数量改变，须先重新检查。'
new=[r'''\begin{proof}[验证]
先验证逐点加法构成交换群。对任意$f,g,h\in F^F$及$a\in F$，有
\begin{align*}
((f+g)+h)(a)
&=(f(a)+g(a))+h(a)\\
&=f(a)+(g(a)+h(a))\\
&=(f+(g+h))(a),\\
(f+g)(a)&=f(a)+g(a)=g(a)+f(a)=(g+f)(a).
\end{align*}
因为这些等式对每个$a$成立，所以函数的加法满足结合律和交换律。常函数$f_0$满足$(f+f_0)(a)=f(a)$，故为加法零元。对$f$定义$(-f)(a)=-f(a)$，则$f+(-f)=f_0$，故每个函数有加法逆元。

再验证乘法及分配律。对任意$a\in F$，
\begin{align*}
((fg)h)(a)
&=(f(a)g(a))h(a)\\
&=f(a)(g(a)h(a))=(f(gh))(a),\\
(fg)(a)&=f(a)g(a)=g(a)f(a)=(gf)(a),\\
(f(g+h))(a)
&=f(a)(g(a)+h(a))\\
&=f(a)g(a)+f(a)h(a)=(fg+fh)(a).
\end{align*}
因此乘法结合且交换，左分配律成立，右分配律由交换性得到。又$(ff_1)(a)=f(a)1=f(a)$，所以$f_1$是乘法单位元。由此$F^F$为交换幺环。

对$c,d\in F$，逐点计算得到
\[
f_c+f_d=f_{c+d},\qquad f_cf_d=f_{cd}.
\]
所以$c\mapsto f_c$保持两种运算及单位元。若$f_c=f_d$，在任意一点取值即得$c=d$，故该映射为单同态。其像为全部常函数；非零常函数$f_c$的逆为$f_{c^{-1}}$，所以像是子域。将$c$与$f_c$等同，便把$F$嵌入$F^F$。
\end{proof}''', r'''\begin{proof}
\begin{enumerate}
\item 设$f\in I$。由$I=\ker\sigma$，$f(s)$是零函数，即
\[
f(a)=0\qquad\text{对每个 }a\in F.
\]
若$f$不是零多项式，记$\deg f=m$。根据整环上的根数定理，$f$最多有$m$个不同的根；但无限域$F$的每个元素都是根，矛盾。因此$f=0$，所以$I=(0)$。

代入同态$\sigma:F[x]\to F[s]$本来就是满射，现在核为零，故为同构。又不存在非零多项式$f$使$f(s)=0$，所以$s$在$F$上超越。

\item 将$F$的全部元素列为$a_1,\ldots,a_q$，并令
\[
g(x)=\prod_{a\in F}(x-a)=\prod_{j=1}^q(x-a_j).
\]
这是首一$q$次多项式。先说明：若$h\in F[x]$在$F$的每一点取零值，则$g\mid h$。

由$h(a_1)=0$，因式定理给出$h=(x-a_1)h_1$。设已得到
\[
h(x)=\prod_{j=1}^k(x-a_j)h_k(x),\qquad k<q.
\]
代入$a_{k+1}$，得到
\[
0=\prod_{j=1}^k(a_{k+1}-a_j)h_k(a_{k+1}).
\]
各$a_j$互不相同，所以前面的每个因子均非零，其积在域中也非零。消去此积，得$h_k(a_{k+1})=0$。再由因式定理，$h_k=(x-a_{k+1})h_{k+1}$。如此继续到$k=q$，即得$h=gh_q$，所以$g\mid h$；$h=0$时此结论也成立。

由有限域乘法群的结论，任意$a\ne0$都满足$a^{q-1}=1$，从而$a^q-a=0$；$a=0$时也成立。把上面的结论用于$h=x^q-x$，得到$g\mid x^q-x$。两者都是首一$q$次多项式，所以商只能为$1$，即
\[
g(x)=x^q-x.
\]

现在求$I$。若$f\in I$，则$f$在$F$的每一点取零值，故$g\mid f$，即$f\in(g)$，因此$I\subseteq(g)$。反过来，$g$在每一点取零值，故$g\in I$；由于$I$为理想，$(g)\subseteq I$。于是
\[
I=(g)=(x^q-x).
\]
所以$F[s]\cong F[x]/(x^q-x)$，而$I$的首一生成元$x^q-x$正是$s$的极小多项式。

对任意$f\in F[x]$，作带余除法，
\[
f=h(x)(x^q-x)+r(x),\qquad\deg r<q.
\]
代入$s$后，$s^q-s$为零函数，所以$f(s)=r(s)$。因此每个多项式函数都有次数小于$q$的代表元。

若$r,t$均满足次数小于$q$，且$r(s)=t(s)$，则$r-t\in I=(x^q-x)$。若$r-t\ne0$，作为$x^q-x$的非零倍式，其次数至少为$q$；但$\deg(r-t)<q$，矛盾。所以$r=t$，代表元唯一。

这样的代表元恰为
\[
c_0+c_1x+\cdots+c_{q-1}x^{q-1},\qquad c_i\in F.
\]
它们的$q$个系数各有$q$种选择，共有$q^q$个，故$|F[s]|=q^q$。另一方面，一个函数$F\to F$由它在$q$个点的值唯一确定，每一点有$q$种取值，所以$|F^F|=q^q$。由$F[s]\subseteq F^F$且两者为同样大小的有限集合，得到$F[s]=F^F$。
\end{enumerate}
\end{proof}''',r'''\begin{proof}
\begin{enumerate}
\item 对变量个数$n$归纳。$n=1$为前一定理的第一条。设结论对$n-1$个变量成立，取$f\in I$，按最后一个变量展开：
\[
f(x_1,\ldots,x_n)=\sum_{j=0}^m f_j(x_1,\ldots,x_{n-1})x_n^j.
\]
因为$f\in I$，$f(s_1,\ldots,s_n)$是零函数。因此对任意$(a_1,\ldots,a_n)\in F^n$，
\[
\sum_{j=0}^m f_j(a_1,\ldots,a_{n-1})a_n^j=0.
\]
固定$a_1,\ldots,a_{n-1}$，将
\[
h(t)=\sum_{j=0}^m f_j(a_1,\ldots,a_{n-1})t^j
\]
看作$F[t]$中的一元多项式。让$a_n$取遍$F$，可知$h$在无限域$F$的每一点取零值。由一元结论，$h$是零多项式，所以各系数为零：
\[
f_j(a_1,\ldots,a_{n-1})=0\qquad(0\le j\le m).
\]
前$n-1$个坐标任意，因此每个$f_j$都在$F^{n-1}$上恒为零。由归纳假设，每个$f_j$是零多项式，于是$f=0$。

这证明$I=(0)$，代入同态成为同构，也说明不存在$s_1,\ldots,s_n$之间的非平凡代数关系，故它们代数无关。

\item 记
\[
I'=(x_1^q-x_1,\ldots,x_n^q-x_n).
\]
对每个$i$，函数$s_i^q-s_i$在任意$(a_1,\ldots,a_n)$处的值为$a_i^q-a_i=0$，故$x_i^q-x_i\in I$。由$I$为理想，$I'\subseteq I$。

先证明任意$f\in F[x_1,\ldots,x_n]$均可写成
\[
f=\sum_{i=1}^n q_i(x_1,\ldots,x_n)(x_i^q-x_i)+r,
\]
其中$r$对每个变量的次数均小于$q$。只须对每个单项式处理各变量的指数。若$e\ge q$，则
\[
x_i^e=x_i^{e-q+1}+x_i^{e-q}(x_i^q-x_i),
\]
所以模$I'$，可以把指数$e$降低$q-1$。因为$q\ge2$，指数严格下降；重复有限次后，得到$0\le r_i<q$，使$x_i^e\equiv x_i^{r_i}\pmod{I'}$。原指数小于$q$时直接保留，特别地，指数$0$仍为$0$。

因此任一单项式均满足
\[
x_1^{e_1}\cdots x_n^{e_n}
\equiv x_1^{r_1}\cdots x_n^{r_n}\pmod{I'},
\qquad0\le r_i<q.
\]
对$f$中的有限个单项式分别处理，再相加，得到一个各变量次数均小于$q$的$r$，使$f-r\in I'$。根据$I'$的生成方式，$f-r$就是上面所列的有限和，所需分解成立。

再证明：这样的$r$若给出零函数，就只能是零多项式。仍对$n$归纳。$n=1$时，一个次数小于$q$的非零多项式不可能有$q$个根，故结论成立。

设结论对$n-1$成立，将$r$写成
\[
r=\sum_{j=0}^{q-1}r_j(x_1,\ldots,x_{n-1})x_n^j.
\]
每个$r_j$对前$n-1$个变量的次数仍均小于$q$。固定$a_1,\ldots,a_{n-1}$，由$r$给出零函数，
\[
\sum_{j=0}^{q-1}r_j(a_1,\ldots,a_{n-1})a_n^j=0
\qquad(\forall a_n\in F).
\]
这是一个次数小于$q$的一元多项式在$q$个不同点取零值，所以所有系数均为零。于是每个$r_j$在$F^{n-1}$上给出零函数。应用归纳假设，得各$r_j=0$，从而$r=0$。

现在取$f\in I$并作上述分解。因为$f\in I$且$\sum_i q_i(x_i^q-x_i)\in I'\subseteq I$，所以$r\in I$，即$r$给出零函数。由刚证明的结论，$r=0$，故$f\in I'$。因此$I\subseteq I'$，结合先前的包含关系，得到
\[
I=I'=(x_1^q-x_1,\ldots,x_n^q-x_n).
\]

上述分解说明，每个剩余类都有各变量次数小于$q$的代表元。若$r,t$是同一剩余类的两个这样的代表元，则$r-t\in I$，给出零函数；其各变量次数仍小于$q$，所以$r-t=0$。故代表元唯一。

这些代表元恰为单项式
\[
x_1^{i_1}\cdots x_n^{i_n},\qquad0\le i_j<q,
\]
的$F$上线性组合。每个指数有$q$种选择，共有$q^n$个单项式；每个系数又有$q$种选择，所以商环及其同构像$F[s_1,\ldots,s_n]$均有$q^{q^n}$个元素。

而$F^n$有$q^n$个点，从它到$F$的函数由各点的取值决定，也恰有$q^{q^n}$个。由$F[s_1,\ldots,s_n]\subseteq F^{F^n}$，得到
\[
F[s_1,\ldots,s_n]=F^{F^n}.
\]
\end{enumerate}
\end{proof}''']

updated=section
for m,replacement in reversed(list(zip(proofs,new))):
    updated=updated[:m.start()]+replacement+updated[m.end():]
assert re.sub(r'\\begin\{proof\}(?:\[[^\]]*\])?[\s\S]*?\\end\{proof\}','',section)==re.sub(r'\\begin\{proof\}(?:\[[^\]]*\])?[\s\S]*?\\end\{proof\}','',updated)
backup=root/'.codex-work/chapter3-before-section38-proofs-20261117.tex'
if backup.exists(): raise RuntimeError('备份已存在，须核对是否已经执行。')
assert p.read_bytes()==raw, '文件出现并发修改。'
backup.write_bytes(raw)
p.write_bytes((prefix+updated).encode('utf-8'))
print('仅重写第3.8节三个证明环境，定义、定理陈述和其他各节保持原样。')
