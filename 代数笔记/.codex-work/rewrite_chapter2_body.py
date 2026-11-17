from pathlib import Path
import re

path = Path(r'C:/Users/WANYIWIGE/Desktop/我的笔记/代数笔记/chapters/Part 2/chapter2.tex')
text = path.read_text(encoding='utf-8')
proofs = {}
proofs[0] = r'''
先按原书考虑自然同态$\pi:G\to G/K$。
若$\overline H\leq G/K$，则$\pi^{-1}(\overline H)$是包含$K$的子群；由满射性，
\[
\pi\bigl(\pi^{-1}(\overline H)\bigr)=\overline H.
\]

反过来，设$K\leq H\leq G$。显然$H\subseteq\pi^{-1}(\pi(H))$。
若$x\in\pi^{-1}(\pi(H))$，可取$h\in H$使$\pi(x)=\pi(h)$，于是
\[
h^{-1}x\in K,
\qquad x\in hK\subseteq H.
\]
因此
\[
\pi^{-1}(\pi(H))=H.
\]
这两个等式证明像与反像给出互逆对应，包含关系也由像与反像的定义保持。

再核对正规性。若$H\trianglelefteq G$，任取$g\in G$，有
\[
\pi(g)\pi(H)\pi(g)^{-1}
=\pi(gHg^{-1})=\pi(H).
\]
$\pi$满，所以$\pi(H)\trianglelefteq G/K$。
若$\overline H\trianglelefteq G/K$，对$x\in\pi^{-1}(\overline H)$及$g\in G$，
\[
\pi(gxg^{-1})=\pi(g)\pi(x)\pi(g)^{-1}\in\overline H,
\]
故其反像正规。

最后，对题设的一般满同态，第一同构定理给出
\[
G/K\xrightarrow{\ \cong\ }G',\qquad gK\longmapsto\varphi(g).
\]
通过此同构转移上述对应，就得到所述结论。
'''
proofs[1] = r'''
（补充证明。）逐项使用核的定义，得到
\begin{align*}
x\in\varphi^{-1}(\varphi(H))
&\iff \text{存在 }h\in H,\ \varphi(x)=\varphi(h)\\
&\iff \text{存在 }h\in H,\ h^{-1}x\in K\\
&\iff x\in HK.
\end{align*}
由于$K\trianglelefteq G$，$HK$确为子群。
'''
proofs[2] = r'''
按原书将两个自然同态复合：
\[
G\xrightarrow{\pi}G/N
\xrightarrow{q}(G/N)/(H/N).
\]
由子群对应定理，$H/N$在$G/N$中正规，所以$q$有定义。
两个映射都满，复合映射也满，且
\begin{align*}
g\in\ker(q\circ\pi)
&\iff gN\in H/N\\
&\iff g\in H.
\end{align*}
因此第一同构定理给出
\[
G/H\cong(G/N)/(H/N).
\]
在这个同构下，$gH$对应$(gN)(H/N)$，即得题述映射。
一般满同态的版本由$G/K\cong G'$以及子群对应定理得到。
'''
proofs[3] = r'''
令$\pi:G\to G/N$为自然同态，先把它限制在$H$上。
限制同态的核是$H\cap N$，所以
\[
H/(H\cap N)\cong\pi(H).
\]

下面按原书直接验证$HN$为子群。任取$h_1,h_2\in H$、$n_1,n_2\in N$，由$N$正规，
\begin{align*}
(h_1n_1)(h_2n_2)
&=h_1h_2(h_2^{-1}n_1h_2)n_2\in HN,\\
(h_1n_1)^{-1}
&=n_1^{-1}h_1^{-1}
=h_1^{-1}(h_1n_1^{-1}h_1^{-1})\in HN.
\end{align*}
$HN$非空，故为子群；且$N\leq HN$。

再把$\pi$限制在$HN$上，其核为$N$，并且
\[
\pi(HN)=\pi(H),
\]
因为$\pi(hn)=\pi(h)$。于是
\[
HN/N\cong\pi(H)\cong H/(H\cap N).
\]
两边的对应由同一个$h\in H$诱导，故所述映射为同构。
'''
proofs[4] = r'''
（补充原书“容易验证”的步骤。）令$W$为所述有限乘积的集合，空乘积保证$e\in W$。
连接两串乘积仍是这样的乘积；若$w=x_1\cdots x_r$，则
\[
w^{-1}=x_r^{-1}\cdots x_1^{-1}\in W,
\]
因为每个$x_i^{-1}$仍属于$S\cup S^{-1}$。故$W\leq G$，且$S\subseteq W$。

另一方面，任意包含$S$的子群都包含$S^{-1}$及这些有限乘积，因此$W$包含于这些子群的交。
而$W$本身就是交中参与的子群之一，所以
\[
W=\bigcap_{S\subseteq H\leq G}H=\langle S\rangle.
\]
'''
proofs[5] = r'''
先按原书考察到交换群$A$的同态$\psi:G\to A$。对任意$a,b\in G$，
\begin{align*}
\psi([a,b])
&=\psi(a)^{-1}\psi(b)^{-1}\psi(a)\psi(b)\\
&=e_A.
\end{align*}
因此所有换位子及其生成的子群都包含于$\ker\psi$。

补充正规性的验证。任取$g\in G$，有
\[
g[a,b]g^{-1}=[gag^{-1},gbg^{-1}].
\]
所以共轭把生成元映为生成元，给出$gG'g^{-1}\subseteq G'$；将$g$换成$g^{-1}$得到反向包含，故$G'\trianglelefteq G$。

若$N\trianglelefteq G$且$G/N$交换，取自然同态就得到$G'\leq N$。
反过来，若$G'\leq N$，则
\[
(aN)^{-1}(bN)^{-1}(aN)(bN)=[a,b]N=N,
\]
所以$aN,bN$交换。

特别地，取$N=G'$可知$G/G'$交换。
对到交换群的同态$\psi$，定义
\[
\overline\psi:G/G'\to A,\qquad gG'\longmapsto\psi(g).
\]
由于$G'\leq\ker\psi$，此映射良定义并保乘法，且$\psi=\overline\psi\circ\pi$。
每个陪集有代表，因而这一分解唯一。
'''
proofs[6] = r'''
设$H\leq\Z$。若$H=\{0\}$，取$m=0$即可。
否则$H$含非零整数，取负元后可知它含正整数。令$m$为其中最小的正整数。

任取$x\in H$，作带余除法：
\[
x=qm+r,\qquad q,r\in\Z,\quad0\leq r<m.
\]
由于$m,x\in H$，有
\[
r=x-qm\in H.
\]
若$r>0$就与$m$的最小性矛盾，所以$r=0$，即$x\in m\Z$。
反向，$m\in H$给出$m\Z\subseteq H$，故$H=m\Z$。

最后，若$n\Z\subseteq m\Z$，则$n\in m\Z$，所以$m\mid n$。
若$n=mk$，则任意$nt=m(kt)\in m\Z$，故$n\Z\subseteq m\Z$。
这里$m=0$时的整除仍按$n=mk$解释。
'''
proofs[7] = r'''
设$G=\langle a\rangle$，按原书定义满同态
\[
\varphi:\Z\to G,\qquad k\longmapsto a^k.
\]
其核为$\Z$的子群，所以等于某个$m\Z$，$m\geq0$。

若$m=0$，$\varphi$单射，从而$G\cong\Z$，其子群也由$\Z$的子群分类得到，均为循环群。
若$m>0$，第一同构定理给出
\[
G\cong\Z/m\Z.
\]
因此$|G|=m$，并且$a$的阶也是$m$。

由对应定理，$G$的子群对应于包含$m\Z$的$s\Z$，即$s\mid m$。
其像为
\[
\varphi(s\Z)=\langle a^s\rangle
=\{e,a^s,\ldots,a^{(m/s-1)s}\},
\]
这些元素两两不同，故阶为$m/s$。
给定$d\mid m$，必须取$s=m/d$，所以$d$阶子群存在且唯一。
'''
proofs[8] = r'''
按原书从循环子群的分类求阶。设$\varphi:\Z\to\langle a\rangle$、$t\mapsto a^t$，则
\[
\ker\varphi=m\Z,\qquad a^t=e\iff m\mid t.
\]
$\langle a^k\rangle$是$\langle a\rangle$的子群，故可写成$\langle a^d\rangle$，其中$d$为$m$的正因子。
由两个生成元互相属于对方生成的子群，可取$u,v,w,w'\in\Z$使
\[
k=ud+vm,\qquad d=wk+w'm.
\]
第一式及$d\mid m$给出$d\mid k$，所以$d\mid\gcd(m,k)$；第二式给出$\gcd(m,k)\mid d$。
因此
\[
d=\gcd(m,k).
\]
由前一定理，$\langle a^d\rangle$的阶为$m/d$，故
\[
\operatorname{ord}(a^k)=\frac{m}{\gcd(m,k)}.
\]
取此阶等于$m$，就得到生成元条件及其个数。
'''
proofs[9] = r'''
设$ab$的阶为$l$。因为$a,b$交换，
\[
(ab)^{mn}=a^{mn}b^{mn}=e,
\]
故$l\mid mn$。

另一方面，由$(ab)^l=e$，再取$m$次幂，得到
\[
e=(ab)^{lm}=a^{lm}b^{lm}=b^{lm}.
\]
于是$n\mid lm$；由$\gcd(m,n)=1$得到$n\mid l$。
同理取$n$次幂，可得$m\mid l$。
所以$mn\mid l$，结合$l\mid mn$，得$l=mn$。
'''
proofs[10] = r'''
取$G$中阶最大的元素$a$，记其阶为$n$。
若某个元素$b$的阶$t$不整除$n$，可选素数$p$使$t$中的$p$指数大于$n$中的$p$指数，写成
\[
t=p^ru,\qquad n=p^sv,\qquad r>s,\quad p\nmid u,\quad p\nmid v.
\]
由幂的阶公式，
\[
\operatorname{ord}(b^u)=p^r,
\qquad\operatorname{ord}(a^{p^s})=v.
\]
两者因$G$交换而交换，其阶互素。前一引理于是给出
\[
\operatorname{ord}(b^u a^{p^s})=p^rv>p^sv=n,
\]
与$n$最大矛盾。
故任意元素的阶均整除$n$。
'''
proofs[11] = r'''
先按原书证明充分性。由前一定理，存在$a\in G$，其阶$n$为所有元素阶的公倍数。
于是任意$x\in G$都满足$x^n=e$，题设给出
\[
|G|\leq n.
\]
但$\langle a\rangle\subseteq G$已有$n$个元素，所以$|G|=n$，从而$G=\langle a\rangle$。

下面补充原书留给读者的必要性。
设$G=\langle a\rangle$阶为$n$，令$d=\gcd(n,m)$，写$n=dn_0,m=dm_0$。
则
\begin{align*}
(a^k)^m=e
&\iff n\mid km\\
&\iff n_0\mid k.
\end{align*}
在$0\leq k<n$中恰有$d$个这样的指数，因此解数为$d\leq m$。
'''
proofs[12] = r'''
若交换群$G$单，任取$a\neq e$。交换群的子群全部正规，所以
\[
\{e\}\neq\langle a\rangle\trianglelefteq G
\quad\Longrightarrow\quad G=\langle a\rangle.
\]
因此$G$循环。
若它无限，则$\langle a^2\rangle$为非平凡真子群；若它的阶$m$为合数，取真因子$1<d<m$，唯一$d$阶子群也为非平凡真子群。
两种情况都与单性矛盾，所以$m$只能为素数。

反过来，素数阶循环群由拉格朗日定理没有非平凡真子群，当然也没有非平凡真正规子群，故为单群。
'''
proofs[13] = r'''
先把不相交轮换分解中的每个轮换写为
\[
(a_1a_2\cdots a_r)=(a_1a_r)\cdots(a_1a_2),
\]
即得置换的对换分解。

偶置换的对换分解包含偶数个对换，把它们相邻两两配对。
相同的两个对换之积为$e$；不同的两个对换，按原书分为两种情形：
\begin{align*}
(ij)(ik)&=(ikj),\\
(ij)(kl)&=(ij)(jk)(jk)(kl)\\
&=(jki)(klj),
\end{align*}
其中第二式的$i,j,k,l$两两不同。
这些等式均按右边先作用逐点验证。每一对都可化为3-轮换的积，故任意偶置换亦然。
'''
proofs[14] = r'''
令$\pi(a_i)=b_i$。对$1\leq i<r$，
\[
(\pi(a_1\cdots a_r)\pi^{-1})(b_i)
=\pi(a_{i+1})=b_{i+1};
\]
最后$b_r$被映为$b_1$，其余元素保持不变，故得到共轭公式。

（补充轮换类型的判别。）此公式使每个轮换长度保持不变。
反过来，若两个置换轮换类型相同，将等长轮换一一对应，再按循环次序匹配各元素，就构造出所需共轭置换。

再按原书核对3-轮换在$A_n$中的共轭性。
选$\pi\in S_n$使$\pi(a_i)=b_i$，$i=1,2,3$。
若$\pi$为偶置换已经满足要求；若$\pi$为奇置换，在$a_1,a_2,a_3$之外选不同的$l,m$，令
\[
\theta=\pi(lm).
\]
由于$n\geq5$，这样的$l,m$存在；$\theta$为偶置换，且仍满足$\theta(a_i)=b_i$。
因此$\theta(a_1a_2a_3)\theta^{-1}=(b_1b_2b_3)$。
'''
proofs[15] = r'''
设$\{e\}\neq H\trianglelefteq A_n$。
由全体3-轮换生成$A_n$，以及它们在$A_n$内互相共轭，只需证明$H$中有一个3-轮换。

按原书，在$H$的非单位元中取不动点最多的$\tau$。
非单位偶置换至多有$n-3$个不动点；若恰有$n-3$个，它就移动三个点，必为3-轮换，结论成立。
下面反设其移动点数$r>3$。

\textbf{情形一：分解中有长度至少3的轮换。}
重新给元素编号，使
\[
\tau=(123\cdots)\cdots.
\]
此时$r\geq5$：若只移动四点而有长度至少3的轮换，只能为4-轮换，它为奇置换。
所以可把另外两个被移动的点标为4、5，取
\[
\rho=(345),\qquad u=\tau^{-1}\rho\tau\rho^{-1}.
\]
正规性保证$\rho\tau\rho^{-1}\in H$，因而$u\in H$。
由$\rho$固定1、2，且$\tau(1)=2,\tau(2)=3$，有
\begin{align*}
u(1)&=\tau^{-1}(\rho(\tau(1)))=\tau^{-1}(2)=1,\\
(\rho\tau\rho^{-1})(2)&=4\neq3=\tau(2).
\end{align*}
第二式说明$u\neq e$。
$\tau$原来的每个不动点都不在1、2、3、4、5中，故也被$u$固定；而1原来被移动，现在被固定。
所以$u$的不动点更多，矛盾。

\textbf{情形二：分解中只有对换。}
若只移动四点，写$\tau=(12)(34)$。取第五个点5及$\rho=(345)$，有
\begin{align*}
\tau^{-1}\rho\tau&=(435)=\rho^{-1},\\
\tau^{-1}\rho\tau\rho^{-1}&=\rho^{-2}=\rho.
\end{align*}
故$H$已含3-轮换，与所选$\tau$不动点最多矛盾。
这是对原书选取4、5为移动点这一步在四点情形的补充处理。

若移动点多于四个，因为对换个数为偶数，至少有四个对换，可写
\[
\tau=(12)(34)(56)\cdots.
\]
仍令$\rho=(345)$、$u=\tau^{-1}\rho\tau\rho^{-1}$。
此时$u$固定1、2，而
\[
(\rho\tau\rho^{-1})(3)=6\neq4=\tau(3),
\]
所以$u\neq e$。原不动点仍然全部被固定，又得到更多不动点，矛盾。

因此$r>3$不可能，$H$含3-轮换，故$H=A_n$。
最后，$(123)$与$(124)$不交换，说明$A_n$非交换。
'''
proofs[16] = r'''
\textbf{必要性。}若$G^{(r)}=\{e\}$，取导出列的前$r+1$项。
每一项在前一项中正规，且由交换化的判别，
\[
G^{(i-1)}/G^{(i)}\text{ 为交换群}.
\]

\textbf{充分性。}由$G/G_1$交换，先得$G'\leq G_1$。
若已知$G^{(i-1)}\leq G_{i-1}$，则
\[
G^{(i)}=(G^{(i-1)})'\leq G_{i-1}'\leq G_i,
\]
最后一个包含关系来自$G_{i-1}/G_i$交换。
归纳得到$G^{(r)}\leq G_r=\{e\}$，所以$G$可解。

\textbf{有限情形。}按原书继续细分群列。
若某交换因子$G_{i-1}/G_i$不单，可在其中选非平凡真子群$L$；因商群交换，$L$正规。
对应定理给出可插入的$G_i<H<G_{i-1}$，并有
\[
H/G_i\cong L,\qquad
G_{i-1}/H\cong(G_{i-1}/G_i)/L.
\]
两因子仍交换。有限群的严格下降群列长度有限，因此有限次插入后，每个因子都交换且单，即为素数阶循环群。
反向，这样的群列是交换因子群列，已由充分性证明可解。
'''
proofs[17] = r'''
（补充证明，供后续习题使用。）若$H\leq G$，$H$中的换位子也是$G$中的换位子，所以
\[
H'\leq G',\qquad H^{(i)}\leq G^{(i)}.
\]
因此$G$的导出列终止时，$H$的导出列也终止。

设$\varphi:G\to Q$满。因
\[
\varphi([a,b])=[\varphi(a),\varphi(b)],
\]
且$Q$中所有换位子的两个元素都可以提升到$G$，有
\[
\varphi(G')=Q',\qquad\varphi(G^{(i)})=Q^{(i)}.
\]
故同态像也可解。

最后，若$N^{(s)}=\{e\}$且$(G/N)^{(r)}=\{N\}$，自然同态的上述性质给出$G^{(r)}\leq N$。
再取$s$次换位子群，得
\[
G^{(r+s)}=(G^{(r)})^{(s)}\leq N^{(s)}=\{e\},
\]
故$G$可解。
'''
proofs[18] = r'''
设循环群生成元为$a$。每个自同构由$a$的像唯一决定，满射性又要求像仍为生成元。

无限循环群的生成元只有$a,a^{-1}$。
映射$\alpha(a^t)=a^{-t}$为自同构，且
\[
\alpha^2(a^t)=a^t,\qquad\alpha\neq\operatorname{id}.
\]
所以它的自同构群同构于$C_2$。

有限循环群阶为$n$时，生成元恰为$a^k$、$\gcd(k,n)=1$。
指定$\alpha_k(a)=a^k$后，$\alpha_k(a^t)=a^{kt}$；它良定义，并由$k$模$n$可逆而为双射。
复合满足
\[
(\alpha_k\circ\alpha_l)(a)=\alpha_k(a^l)=a^{kl},
\]
故$\alpha_k\leftrightarrow\overline k$给出与$(\Z/n\Z)^\times$的群同构。
平凡群的自同构群也为平凡群。
'''
proofs[19] = r'''
先补齐内自同构的验证。对任意$x,y\in G$，
\begin{align*}
c_a(xy)&=axy a^{-1}\\
&=(axa^{-1})(aya^{-1})=c_a(x)c_a(y),\\
c_a\circ c_{a^{-1}}&=\operatorname{id}
=c_{a^{-1}}\circ c_a.
\end{align*}
所以$c_a$是自同构，且
\[
(c_a\circ c_b)(x)=abx(ab)^{-1}=c_{ab}(x).
\]
因此$a\mapsto c_a$为满到$\operatorname{Inn}(G)$的同态，其核满足
\begin{align*}
c_a=\operatorname{id}
&\iff axa^{-1}=x\quad(\forall x\in G)\\
&\iff a\in Z(G).
\end{align*}
第一同构定理给出$G/Z(G)\cong\operatorname{Inn}(G)$。

再按原书计算$\alpha\in\Aut(G)$对内自同构的共轭：
\begin{align*}
(\alpha c_a\alpha^{-1})(x)
&=\alpha\bigl(a\alpha^{-1}(x)a^{-1}\bigr)\\
&=\alpha(a)x\alpha(a)^{-1}\\
&=c_{\alpha(a)}(x).
\end{align*}
它仍为内自同构，所以$\operatorname{Inn}(G)\trianglelefteq\Aut(G)$。
'''
proofs[20] = r'''
设$\alpha$与所有内自同构交换。由上一计算，对任意$a\in G$，
\[
c_{\alpha(a)}=\alpha c_a\alpha^{-1}=c_a.
\]
所以$c_{a^{-1}\alpha(a)}=\operatorname{id}$，即
\[
a^{-1}\alpha(a)\in Z(G)=\{e\}.
\]
故$\alpha(a)=a$对所有$a$成立，$\alpha=\operatorname{id}$。
$\Aut(G)$的中心中元素当然与所有内自同构交换，因此其中心也平凡。
'''
proofs[21] = r'''
任取$g\in G$，由作用公理，
\begin{align*}
\rho(g^{-1})(\rho(g)(x))&=(g^{-1}g)\cdot x=x,\\
\rho(g)(\rho(g^{-1})(x))&=(gg^{-1})\cdot x=x.
\end{align*}
所以$\rho(g)$是双射，逆为$\rho(g^{-1})$。
另有
\[
\rho(gh)(x)=(gh)\cdot x=g\cdot(h\cdot x)
=(\rho(g)\rho(h))(x),
\]
故$\rho$为同态。

反过来，若$\rho:G\to S(X)$为同态，定义$g\cdot x=\rho(g)(x)$。
由$\rho(e)=\operatorname{id}$、$\rho(gh)=\rho(g)\rho(h)$，即得两条作用公理。
'''
proofs[22] = r'''
（补充验证。）若$aH=bH$，则$gaH=gbH$，故陪集作用与代表选择无关。
其核由以下等价关系得到：
\begin{align*}
g\in\ker\rho
&\iff gaH=aH\quad(\forall a\in G)\\
&\iff a^{-1}ga\in H\quad(\forall a\in G)\\
&\iff g\in\bigcap_{a\in G}aHa^{-1}.
\end{align*}

左、右正则作用的等价性由取逆双射$f(x)=x^{-1}$验证：
\[
f(gx)=(gx)^{-1}=x^{-1}g^{-1}=f(x)g^{-1}.
\]

对于$\GL_n(F)$作用于$F^n$，零向量被所有变换固定。
任取非零$u,v$，分别把它们扩充为基，再将第一组基依次映到第二组基，就得到可逆线性变换$T$使$T(u)=v$。
因此非零向量恰构成另一个轨道。
'''
proofs[23] = r'''
先补充原书略去的等价关系验证。定义$x\sim y$为存在$g\in G$使$y=g\cdot x$。
单位元给出自反性；若$y=g\cdot x$，则$x=g^{-1}\cdot y$，给出对称性；若再有$z=h\cdot y$，则$z=(hg)\cdot x$，给出传递性。
所以各等价类，即轨道，构成不交分解。

稳定子群含$e$，且对$g,h\in G_x$，
\[
(gh^{-1})\cdot x=g\cdot(h^{-1}\cdot x)=g\cdot x=x,
\]
故$G_x\leq G$。

按原书定义
\[
\theta:G/G_x\to G\cdot x,\qquad aG_x\longmapsto a\cdot x.
\]
因为
\begin{align*}
a\cdot x=b\cdot x
&\iff b^{-1}a\cdot x=x\\
&\iff b^{-1}a\in G_x\\
&\iff aG_x=bG_x,
\end{align*}
$\theta$良定义且单射；轨道中的每个元素都为$a\cdot x$，所以也满。
它还满足
\[
\theta(g\cdot(aG_x))=(ga)\cdot x
=g\cdot\theta(aG_x),
\]
因而两个作用等价。有限时计数即得$|G\cdot x|=[G:G_x]$。

最后，设$y=g\cdot x$。则
\begin{align*}
u\in G_y
&\iff u\cdot(g\cdot x)=g\cdot x\\
&\iff(g^{-1}ug)\cdot x=x\\
&\iff u\in gG_xg^{-1}.
\end{align*}
故$G_y=gG_xg^{-1}$。
'''
proofs[24] = r'''
把$X$按轨道分解，选每个轨道的代表$x_i$。
轨道--稳定子公式给出
\[
|G\cdot x_i|=[G:G_{x_i}],
\]
所以每个轨道大小均为$p$的幂。
大小为1的轨道恰对应不动点，大小大于1的轨道均被$p$整除。
因此
\[
|X|=|X^G|+\sum_{|G\cdot x_i|>1}|G\cdot x_i|
\equiv|X^G|\pmod p.
\]
若$p\nmid|X|$，就不可能有$|X^G|=0$，故必有不动点。
'''
proofs[25] = r'''
对共轭作用$g\cdot x=gxg^{-1}$，$x$的稳定子为
\[
C_G(x)=\{g\in G:gxg^{-1}=x\}
=\{g\in G:gx=xg\}.
\]
所以$x$的共轭类大小为$[G:C_G(x)]$。
共轭类大小为1当且仅当$x\in Z(G)$；将各类大小相加，就得到所列类方程。

若$G$是非平凡$p$群，把不动点同余结论用于此共轭作用：
\[
|Z(G)|\equiv|G|\equiv0\pmod p.
\]
又$e\in Z(G)$，所以$|Z(G)|\geq1$。正的$p$倍数至少为$p$，故中心非平凡。
'''
proofs[26] = r'''
若$k=0$，组合数为$n$，结论直接成立。下面设$k\geq1$。
按原书把组合数写成
\[
\binom n{p^k}
=\frac n{p^k}\,
\frac{(n-1)\cdots(n-p^k+1)}{(p^k-1)\cdots1}.
\]
对$0<i<p^k$，写$i=p^tu$，其中$p\nmid u$、$t<k\leq r$。
则
\begin{align*}
n-i&=p^t(p^{r-t}m-u),\\
p^k-i&=p^t(p^{k-t}-u).
\end{align*}
括号内两数都不被$p$整除，所以对应的分子、分母恰含相同个数的$p$因子。
逐项约去后，后一个分式的分子、分母均与$p$互素。
因此全部$p$因子来自
\[
\frac n{p^k}=p^{r-k}m,
\]
恰有$r-k$个。
'''
proofs[27] = r'''
设$|G|=p^rm$、$p\nmid m$，且$0\leq k\leq r$。
令$X$为$G$中所有含$p^k$个元素的子集组成的集合，按左乘定义作用
\[
g\cdot A=gA.
\]
有$|X|=\binom{|G|}{p^k}$。前一引理说明
\[
p^{r-k+1}\nmid|X|.
\]
若每个轨道大小都被$p^{r-k+1}$整除，其总和也被整除，矛盾。
故可选$A\in X$使其轨道大小不被$p^{r-k+1}$整除。

令$G_A$为稳定子，由
\[
|G\cdot A|=[G:G_A]=\frac{|G|}{|G_A|},
\]
可知$p^k\mid|G_A|$。
另一方面，取$a\in A$，对全部$h\in G_A$有$ha\in A$，而$h\mapsto ha$为单射，所以
\[
|G_A|=|G_Aa|\leq|A|=p^k.
\]
结合两式得$|G_A|=p^k$，故稳定子就是所求子群。
'''
proofs[28] = r'''
设$|G|=p^rm$、$p\nmid m$。让$H$左乘作用于全部左陪集构成的集合$G/P$。
由于
\[
|G/P|=m,\qquad p\nmid m,
\]
由$p$群作用的不动点结论，可选一个被$H$中全部元素固定的$gP$。
于是对每个$h\in H$，
\[
hgP=gP
\quad\Longrightarrow\quad g^{-1}hg\in P.
\]
因此$g^{-1}Hg\leq P$，即$H\leq gPg^{-1}$。
当$H$也为西罗子群时，两边阶均为$p^r$，所以必须相等。
'''
proofs[29] = r'''
令$\mathcal S$为全部西罗$p$子群组成的集合。
$G$在$\mathcal S$上的共轭作用由第二定理传递，$P$的稳定子为$N_G(P)$，所以
\[
n_p=|\mathcal S|=[G:N_G(P)].
\]
由于$P\leq N_G(P)$，
\[
[G:P]=[G:N_G(P)]\,[N_G(P):P]=m,
\]
故$n_p\mid m$。

再限制为$P$对$\mathcal S$的共轭作用。
若$Q$是不动点，就有$P\leq N_G(Q)$；$Q$在$N_G(Q)$中正规，而且是其中的西罗$p$子群，故它是其中唯一的西罗$p$子群。
$P$也包含在$N_G(Q)$内且阶相同，所以$P=Q$。
反过来，$P$当然固定自身，故不动点恰有一个。
由$p$群作用同余式，
\[
n_p\equiv1\pmod p.
\]
最后，全部西罗子群为$P$的共轭子群，故唯一性等价于$P$在$G$中正规。
'''
proofs[30] = r'''
$P\trianglelefteq N_G(P)$，所以$P$是$N_G(P)$中唯一的西罗$p$子群。
于是$N_G(P)$不可能含$G$的另一西罗$p$子群。

设$g\in N_G(N_G(P))$，则
\[
gN_G(P)g^{-1}=N_G(P).
\]
因此$gPg^{-1}$仍是$N_G(P)$的西罗$p$子群。由唯一性，
\[
gPg^{-1}=P,
\]
故$g\in N_G(P)$，得$N_G(N_G(P))\subseteq N_G(P)$。
反向包含由任一子群都正规化自身成立，故两者相等。
'''
proofs[31] = r'''
先按原书证明不同因子中的元素交换。
唯一性给出$N_i\cap N_j=\{e\}$，$i\neq j$：否则同一个非单位元可分别放在第$i$、第$j$个位置，产生两种表达。
任取$x_i\in N_i,x_j\in N_j$，考虑
\[
c=x_ix_jx_i^{-1}x_j^{-1}.
\]
由两个因子都正规，
\begin{align*}
c&=x_i(x_jx_i^{-1}x_j^{-1})\in N_i,\\
c&=(x_ix_jx_i^{-1})x_j^{-1}\in N_j.
\end{align*}
所以$c=e$，即$x_ix_j=x_jx_i$。

现在定义$\Phi:N_1\times\cdots\times N_s\to G$为乘法映射。
存在性、唯一性说明$\Phi$双射；不同因子交换又给出
\begin{align*}
\Phi(x_1,\ldots,x_s)\Phi(y_1,\ldots,y_s)
&=(x_1\cdots x_s)(y_1\cdots y_s)\\
&=(x_1y_1)\cdots(x_sy_s)\\
&=\Phi(x_1y_1,\ldots,x_sy_s).
\end{align*}
因此$\Phi$为同构。

下面补充原书列出的等价条件。
若单位元表达唯一，仍先得到两两交平凡及不同因子交换。
两个一般表达相等时，移项并按因子重排，得到
\[
(y_1^{-1}x_1)\cdots(y_s^{-1}x_s)=e,
\]
所以每个$x_i=y_i$，得到一般表达唯一。

若题述的交条件成立，从$x_1\cdots x_s=e$可隔离出$x_i$属于$N_i$与其余因子乘积的交，故$x_i=e$。
反过来，若某交含非单位元$x$，由$x=\prod_{j\neq i}x_j$可构造非平凡的单位元表达，矛盾。
这就证明了所有等价性。
'''
proofs[32] = r'''
设$|G|=\prod_{i=1}^s p_i^{r_i}$，其中各$p_i$不同，令$P_i$为西罗$p_i$子群。
交换性使每个子群正规，西罗共轭定理因而说明各$P_i$唯一。

令$Q_i=\prod_{j\neq i}P_j$。它是子群，且由乘法映射$\prod_{j\neq i}P_j\to Q_i$满，$|Q_i|$整除$\prod_{j\neq i}|P_j|$，所以不被$p_i$整除。
因此交子群的阶同时整除互素的$|P_i|$与$|Q_i|$，即
\[
P_i\cap Q_i=\{e\}.
\]
内直和判别表明$P_1\cdots P_s$同构于这些群的外直积，故
\[
|P_1\cdots P_s|=\prod_{i=1}^s|P_i|=|G|.
\]
所以$P_1\cdots P_s=G$，得所求分解。
'''
proofs[33] = r'''
（补充原书“显然”的结论。）对有限群阶作归纳。
若$G$不可分解，取它自身为唯一因子即可。
若可分解，写
\[
G\cong H\times K,\qquad |H|>1,\quad|K|>1.
\]
则$|H|,|K|<|G|$。由归纳假设，两因子均可分解为有限多个不可分解群的直积；将这两组因子连接即得$G$的分解。
'''
proofs[34] = r'''
在$G$的无重复项次正规群列中，选择长度最大的一个。
这样的选择存在，因为阶沿群列严格下降，长度有有限上界。

若其中某因子$G_i/G_{i+1}$不单，可取其非平凡真正规子群$L$。
由子群对应定理，可找到$H$满足
\[
G_{i+1}<H<G_i,\qquad H\trianglelefteq G_i,\qquad H/G_{i+1}=L.
\]
于是可以把$H$插入原群列，产生更长的无重复项次正规群列，矛盾。
因此各因子均单，原群列就是合成群列。

（补充反例。）$\Z$的每个非零子群均为$m\Z$，仍同构于无限循环群，因此不是单群。
若$\Z$有有限合成群列，其最后一个非平凡项必须为单子群，这不可能，所以无限群未必有合成群列。
'''
proofs[35] = r'''
按原书对一条合成群列的长度$r$归纳。
设两条群列为
\begin{align*}
G&=G_0\triangleright G_1\triangleright\cdots\triangleright G_r=\{e\},\\
G&=H_0\triangleright H_1\triangleright\cdots\triangleright H_s=\{e\}.
\end{align*}
平凡群情形直接成立。若$r=1$，$G$单，另一条无重复项合成群列也只能为$G\triangleright\{e\}$。

设$r>1$。若$G_1=H_1$，删去两列首项，得到$G_1$的两条合成群列。
对长度$r-1$应用归纳假设，再补回共同因子$G/G_1$，即可得到结论。

下面设$G_1\neq H_1$。它们都是$G$的极大真正规子群，所以
\[
G_1H_1=G.
\]
令$K=G_1\cap H_1$。第二同构定理给出
\[
G_1/K\cong G/H_1,\qquad H_1/K\cong G/G_1.
\]
这些商群都是单群。
任选$K$的一条合成群列，并接成
\begin{align*}
G&\triangleright G_1\triangleright K\triangleright K_1\triangleright\cdots\triangleright\{e\},\\
G&\triangleright H_1\triangleright K\triangleright K_1\triangleright\cdots\triangleright\{e\}.
\end{align*}
第一条新列与原第一条列有相同第二项$G_1$；由长度$r-1$的归纳假设，它们长度同为$r$，因子对应同构。
所以第一条新列从$K$起的长度为$r-2$，第二条新列也长为$r$。

再比较从$H_1$开始的第二条新列和原第二条列。
第二条新列从$H_1$起长为$r-1$，故可使用归纳假设，得到$s=r$且它们因子对应同构。
两条新列的下方因子相同，最上面两个因子则由前述同构互换，故两条原列的因子在允许重新排序后对应同构。
'''
proofs[36] = r'''
（补充验证。）若$a\sim a'$且$b\sim b'$，同余条件给出$ab\sim a'b'$，所以$[a][b]=[ab]$与代表选择无关。
对任意$a,b,c$，
\begin{align*}
([a][b])[c]&=[(ab)c]=[a(bc)]=[a]([b][c]),\\
[e][a]&=[ea]=[a],\qquad[a][e]=[ae]=[a].
\end{align*}
因此各等价类构成以$[e]$为单位元的幺半群。
\end{proof}

\begin{proposition}
任一幺半群$S$同构于集合$S$上的一个变换幺半群。
\end{proposition}
\begin{proof}
（补充原书定理20留给读者的证明。）令$L_a(x)=ax$，把$a\in S$映到自映射$L_a:S\to S$。
有
\[
L_aL_b(x)=a(bx)=(ab)x=L_{ab}(x),\qquad L_e=\operatorname{id}_S.
\]
若$L_a=L_b$，在$e$处取值即得$a=L_a(e)=L_b(e)=b$。
所以$a\mapsto L_a$是单射幺半群同态，满到其像，给出所述同构。
'''
proofs[37] = r'''
（补充原书定理21略去的验证，并展开定理22的证明。）
先定义$a\sim_\varphi b\iff\varphi(a)=\varphi(b)$。相等关系的三条性质说明它是等价关系；又若$a\sim_\varphi b$、$c\sim_\varphi d$，则
\[
\varphi(ac)=\varphi(a)\varphi(c)=\varphi(b)\varphi(d)=\varphi(bd),
\]
故它为同余。
定义$\theta([a])=\varphi(a)$，该定义与代表选择无关，且
\[
\theta([a][b])=\varphi(ab)=\theta([a])\theta([b]),
\qquad\theta([e])=e_T.
\]
它满到$\varphi(S)$；两类像相同当且仅当$a\sim_\varphi b$，因此它也单射。

对一般的$\sim$，由题设，$\varphi$在每个等价类上取值相同，所以可定义
\[
\overline\varphi:S/{\sim}\to T,\qquad[a]\longmapsto\varphi(a).
\]
同样的等式说明它是幺半群同态，且$\overline\varphi\circ\pi=\varphi$。
若$\psi$也满足此条件，则每个类$[a]=\pi(a)$都有
\[
\psi([a])=\psi(\pi(a))=\varphi(a)=\overline\varphi([a]),
\]
故该分解唯一。
'''
proofs[38] = r'''
按原书定义
\[
\widehat f(\Lambda)=e_S,\qquad
\widehat f(x_1\cdots x_r)=f(x_1)\cdots f(x_r).
\]
字中的字母排列本来就是确定的，$S$的结合律保证右侧乘积与括号无关。
若$u=x_1\cdots x_r,v=y_1\cdots y_t$，则
\begin{align*}
\widehat f(uv)
&=f(x_1)\cdots f(x_r)f(y_1)\cdots f(y_t)\\
&=\widehat f(u)\widehat f(v).
\end{align*}
空字被映为单位元，所以$\widehat f$为幺半群同态。
任何延拓都必须把每个字映为这些字母像的乘积，空字映为$e_S$，故延拓唯一。
'''
proofs[39] = r'''
（补充证明。原书给出存在性的归纳思路，未证明唯一性。）
\textbf{存在性。}对字长归纳。
若字已既约，就不必改动；否则删除一对相邻互逆字母，字长减少2，再对较短字使用归纳假设。
删除不改变等价类，所以每类都有既约代表。

\textbf{唯一性。}定义一个明确的约简过程：从左向右逐个读入字母，保留一个已既约的字。
若新字母与末尾字母互逆，就删去末尾字母；否则将新字母接在末尾。把最终结果记为$R(w)$。
每一步都保持已保留的字既约，并且$w\sim R(w)$。

关键是：在任意已既约前缀后连续读入$x,x^{-1}$，结果恢复该前缀。
若前缀不以$x^{-1}$结尾，先添$x$再删$x$；若前缀以$x^{-1}$结尾，先删去该字母，再添回$x^{-1}$。
第二种情形中，删去后剩余部分不能以$x$结尾，否则原前缀并非既约。
故无论哪种情形，均有
\[
R(uxx^{-1}v)=R(uv),
\]
对$x^{-1}x$也同样成立。
因此一次插入、删除逆对不改变$R$，有限次操作也不改变$R$。

若既约字$w_1,w_2$等价，就有
\[
w_1=R(w_1)=R(w_2)=w_2.
\]
所以每类的既约代表唯一，特别地，非空既约字不能代表单位元。
'''
proofs[40] = r'''
按原书，先在字母及形式逆字母上定义
\[
f(x^{-1})=f(x)^{-1}\qquad(x\in X).
\]
自由幺半群的性质将它唯一延拓为
\[
\widehat f:(X\cup X^{-1})^*\to G.
\]
插入或删除相邻逆对不改变该同态的值，因为
\[
f(x)f(x)^{-1}=e=f(x)^{-1}f(x).
\]
所以等价字有相同像，由幺半群的商映射性质，得到$\widetilde f:F(X)\to G$。
它保乘法且把单位元映为单位元，因此是群同态。
由于$X$生成$F(X)$，任一这样的延拓在每个字上的值都已确定，所以唯一。
'''
proofs[41] = r'''
取$G$的有限生成元$g_1,\ldots,g_r$，并取字母表$X=\{x_1,\ldots,x_r\}$。
指定
\[
f(x_i)=g_i\qquad(1\leq i\leq r).
\]
自由群的性质给出群同态$\widetilde f:F(X)\to G$。
它的像包含$G$的全部生成元，所以满射。
令$N=\ker\widetilde f$，由第一同构定理，
\[
G\cong F(X)/N.
\]
若$G$为平凡群，也可取一个字母映到$e$，同样成立。
'''

found = list(re.finditer(r'\\begin\{proof\}(.*?)\\end\{proof\}',text,re.S))
assert len(found) == 42, len(found)
for i in reversed(range(len(found))):
    m=found[i]
    text=text[:m.start()]+r'\begin{proof}'+'\n'+proofs[i].strip()+'\n'+r'\end{proof}'+text[m.end():]

text=text.replace('$G\'$为特征子群，因而正规。', '$G\'$为正规子群。')
text=text.replace('换位子采用教材约定', '正文有原书证明的结论沿用其方法；标明“补充证明”的部分用于补全原书省略处或说明补充结论。\n换位子采用教材约定')
text=text.replace('十一节正文依教材顺序排列，章末保留习题1--57的原题号。证明中补齐良定义性、有限性及正规性所需条件。', '十一节正文依教材顺序排列，章末保留习题1--57的原题号。证明按推理步骤分段，关键计算用行间公式展开；习题解答为补充解答，有原书提示的沿其提示展开。')
text=text.replace('本节只讨论有限个因子，两种称法指同一构造；无限族的直积与限制有限支撑的直和须另外区分。','本节只讨论有限个因子，两种称法指同一构造；不在这里引入无限族的直积、直和。')
text=text.replace('最大元素阶整除所有元素阶的结论','所有元素阶整除最大元素阶的结论')
text=text.replace('因此$G$循环。\n若它无限', '因此$G$循环。\n\n若它无限')
# Avoid unintroduced centralizer notation before the action section.
text=text.replace('若$Z(G)=\\{e\\}$，则$C_{\\Aut(G)}(\\operatorname{Inn}(G))=\\{\\operatorname{id}\\}$，特别地$Z(\\Aut(G))=\\{\\operatorname{id}\\}$。', '若$Z(G)=\\{e\\}$，则$\\Aut(G)$中与全部内自同构交换的元素只有$\\operatorname{id}$，特别地$Z(\\Aut(G))=\\{\\operatorname{id}\\}$。')
# Define the centralizer and normalizer at their first formula use.
text=text.replace('轨道$G\\cdot x=', '轨道$G\\cdot x=')
anchor='\\section{西罗定理}'
text=text.replace(anchor, r'''\begin{definition}
对$H\leq G$，定义其\textbf{正规化子}
\[
N_G(H)=\{g\in G:gHg^{-1}=H\}.
\]
它为子群，且$H\trianglelefteq N_G(H)$。
\end{definition}
\begin{proof}[补充证明]
单位元属于此集合。若$x,y\in N_G(H)$，则
\[
(xy)H(xy)^{-1}=x(yHy^{-1})x^{-1}=H.
\]
由$xHx^{-1}=H$两侧分别乘$x^{-1},x$，可得$x^{-1}Hx=H$，故逆元也在其中。
所以$N_G(H)$为子群，且其定义正好说明$H$在它里面正规。
\end{proof}

'''+anchor)
text=text.replace('中心为$Z(G)=', '中心为$Z(G)=')
text=text.replace('特征性具有传递性，所以导出列的每一项均为$G$的特征子群。', r'''特征性具有传递性。补充验证$G'$为特征子群：若$\alpha\in\Aut(G)$，则
\[
\alpha([a,b])=[\alpha(a),\alpha(b)].
\]
所以$\alpha(G')\subseteq G'$，再用$\alpha^{-1}$得到反向包含。因而导出列的每一项均为$G$的特征子群。''')
# Add proofs to examples whose claims had been left as compressed assertions.
text=text.replace('这些等式可由习题52及直接换位子计算核对。', r'''下面补充原书未展开的计算。
$S_n/A_n\cong C_2$，所以$S_n'\leq A_n$；而$(12),(23)$的换位子为一个3-轮换，$S_n'$正规使它包含全部3-轮换，故$n\geq3$时$S_n'=A_n$。
对$A_4$，商群$A_4/V_4\cong C_3$给出$A_4'\leq V_4$，又有
\[
[(123),(124)]=(12)(34).
\]
在$A_4$内共轭可得到全部三个双对换，故$A_4'=V_4$。$A_3,V_4$均交换，所以其换位子群平凡。''')
path.write_text(text,encoding='utf-8')
print('Rewrote all 42 existing body proofs and added omitted monoid/normalizer proofs.')
