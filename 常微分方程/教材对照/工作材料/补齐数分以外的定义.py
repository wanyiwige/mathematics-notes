from pathlib import Path
import re,json,zipfile,hashlib,datetime
root=Path(__file__).resolve().parents[2]
stamp='20261030-'+datetime.datetime.now().strftime('%H%M%S')
backup=root.parent/'常微分方程备份'/f'数分前置定义补全前-{stamp}.zip'
paths=[root/'main.tex',root/'main.pdf']+list((root/'chapters').glob('*.tex'))+list((root/'preamble').glob('*.tex'))
with zipfile.ZipFile(backup,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for p in paths:z.write(p,p.relative_to(root).as_posix())
assert zipfile.ZipFile(backup).testzip() is None
changes=[]
def add(n,anchor,body,before=True):
    p=root/f'chapters/chapter{n}.tex';s=p.read_text(encoding='utf-8')
    assert s.count(anchor)==1,(n,anchor,s.count(anchor))
    s=s.replace(anchor,(body+r'''

'''+anchor) if before else (anchor+r'''

'''+body))
    p.write_text(s,encoding='utf-8');changes.append({'chapter':n,'labels':re.findall(r'\\label\{([^}]+)\}',body),'characters':len(body)})
def replace(n,old,new):
    p=root/f'chapters/chapter{n}.tex';s=p.read_text(encoding='utf-8');assert s.count(old)==1,(n,old[:70]);p.write_text(s.replace(old,new),encoding='utf-8')

add(3,r'\begin{definition}[$\delta$ 型序列]',r'''
\begin{definition}[光滑函数、支撑与测试函数]\label{def:support-test}
在开集 $U\subset\R^n$ 上，$C^r(U)$ 表示所有总阶数不超过 $r$ 的偏导数都存在且连续的函数；
$C^\infty(U)$ 表示任意阶偏导数都存在且连续的函数，亦称光滑函数。
函数 $f$ 的支撑定义为相对于 $U$ 的闭包
\[
 \operatorname{supp}f=\overline{\{x\in U:f(x)\ne0\}}^{\,U}.
\]
若这个闭集是 $U$ 中的紧集，称 $f$ 有紧支撑。
光滑紧支撑函数称为测试函数，全体记为 $C_c^\infty(U)$。
在有限维空间内，本书的光滑向量函数指各分量均光滑。
\end{definition}
\begin{example}[光滑凸起与截断]\label{ex:smooth-cutoff}
令
\[
 b(s)=\begin{cases}e^{-1/s},&s>0,\\0,&s\leq0,\end{cases}
 \qquad \chi(x)=\frac{b(4-|x|^2)}{b(4-|x|^2)+b(|x|^2-1)}.
\]
每阶右导数都是 $e^{-1/s}$ 乘以 $s^{-1}$ 的多项式，在 $s\downarrow0$ 时趋于零，
所以 $b$ 光滑。分母处处为正，故 $\chi$ 光滑，且 $0\leq\chi\leq1$，
在 $|x|\leq1$ 时为 1，在 $|x|\geq2$ 时为零。$\chi(x/r)$ 称尺度为 $r$ 的截断函数。
此外，$b(1-|x|^2)$ 是非负、非零且紧支撑的光滑函数；除以其正积分即可使积分为 1。
\end{example}
\begin{definition}[单位集中质量的记号]
对连续函数 $f$，记 $\langle\delta_\xi,f\rangle=f(\xi)$。
这表示对函数取值的线性规则，不表示一个通常的函数 $\delta_\xi(s)$。
光滑函数序列 $h_N$ 趋向 $\delta_\xi$，在这里是指
\[
 \int h_N(s)\psi(s)\,ds\longrightarrow\psi(\xi)
 \quad\text{对每个 }\psi\in C_c^\infty(\R)\text{ 成立}.
\]
下文会直接证明更强的连续函数版本，因此不必预先建立广义函数的一般理论。
\end{definition}''')

add(4,r'\begin{theorem}\label{thm:arnold-translation}',r'''
\begin{definition}[线性泛函与对偶空间]
向量空间 $V$ 到其数域的线性映射称为线性泛函，全体组成对偶空间 $V^*$。
当 $V$ 是函数空间时，$f\mapsto f(t)$ 是求值泛函。
若 $V$ 的维数为 $n$，相对于一组基，每个泛函都唯一对应一个行向量，所以 $\dim V^*=n$。
\end{definition}
\begin{lemma}[Cayley--Hamilton 恒等式]\label{lem:cayley-hamilton-foundation}
若 $A$ 为 $n$ 阶矩阵，$p(z)=\det(zI-A)$，则 $p(A)=0$。
\end{lemma}
\begin{proof}
将伴随矩阵写为 $B(z)=\operatorname{adj}(zI-A)=\sum_{j=0}^{n-1}B_jz^j$。
恒等式 $(zI-A)B(z)=B(z)(zI-A)=p(z)I$ 首先说明 $AB_j=B_jA$。
因此可以在这一多项式矩阵恒等式中用 $A$ 代入标量变量 $z$：各系数与 $A$ 交换，
左边为 $(A-A)\sum_jB_jA^j=0$，右边为 $p(A)$，结论成立。
\end{proof}''')

add(4,r'\begin{definition}[线性单参数群]',r'''
\begin{definition}[群、子群与一般线性群]\label{def:group-notation}
集合 $G$ 连同乘法称为群，是指乘法封闭、满足结合律，有单位元 $e$，且每个元素 $g$ 有逆元 $g^{-1}$。
包含单位元并对乘法和取逆封闭的子集称子群。
$GL(n,\R)=\{A\in\R^{n\times n}:\det A\ne0\}$ 在矩阵乘法下构成一般线性群。
群间保持乘法的映射称同态；同态 $\Phi$ 的核为 $\{g:\Phi(g)=e\}$。
加法群的运算用加号书写，例如 $\R$ 和 $\Z$；其子群对加减封闭。
\end{definition}''')

add(4,r'\section{保守系统的主振动}\label{sec:normal-modes}',r'''
\begin{definition}[对称矩阵与正定性]
实矩阵 $A$ 对称，是指 $A^T=A$；正定，是指 $x^TAx>0$ 对每个非零实向量 $x$ 成立。
正交矩阵满足 $S^TS=I$，因而保持 Euclidean 内积和长度。
\end{definition}
\begin{lemma}[实对称矩阵的正交分解]\label{lem:symmetric-spectral-elementary}
每个实对称矩阵都有一组标准正交特征向量；它正定当且仅当所有特征值都为正。
\end{lemma}
\begin{proof}
连续函数 $x^TAx$ 在单位球面取到最大值，设最大点为 $e$。
对任意 $v\perp e$，沿 $(e+tv)/|e+tv|$ 求导，极值条件给出 $v^TAe=0$。
所以 $Ae=\lambda e$。对 $v\perp e$，对称性给出 $e^TAv=(Ae)^Tv=0$，
故正交补仍在 $A$ 下不变。在这个低一维空间归纳，得到所需正交基。
在该基中 $x^TAx=\sum_j\lambda_jx_j^2$，正定性的判别随即成立。
\end{proof}''')

add(5,r'\begin{theorem}[由压缩映射得到局部逆]',r'''
\begin{definition}[赋范空间、Banach 空间与有界算子]\label{def:banach-operator}
向量空间 $X$ 上的范数满足正定性、$\|ax\|=|a|\|x\|$ 及三角不等式；
由距离 $d(x,y)=\|x-y\|$ 得到的空间称赋范空间。若此距离下每个 Cauchy 列都收敛，称 Banach 空间。
线性映射 $T:X\to Y$ 有界，是指存在 $C$ 使 $\|Tx\|\leq C\|x\|$；其算子范数为
\[
 \|T\|=\sup_{\|x\|\leq1}\|Tx\|.
\]
它满足 $\|Tx\|\leq\|T\|\|x\|$ 与 $\|ST\|\leq\|S\|\|T\|$。
线性有界等价于连续：有界估计直接保证连续；反之在零点使用连续性，再缩放向量即得有界估计。
\end{definition}
\begin{lemma}[Neumann 级数]\label{lem:neumann-series}
若 $X$ 为 Banach 空间，$T:X\to X$ 线性有界且 $\|T\|<1$，则
\[
 (I-T)^{-1}=\sum_{j=0}^\infty T^j,
 \qquad\|(I-T)^{-1}\|\leq\frac1{1-\|T\|}.
\]
\end{lemma}
\begin{proof}
对每个 $x$，级数各项的范数由 $\|T\|^j\|x\|$ 控制，故由完备性收敛，记其和为 $Sx$。
这一估计同时证明 $S$ 线性有界。有限和满足
$(I-T)\sum_{j=0}^mT^j=\sum_{j=0}^mT^j(I-T)=I-T^{m+1}$。
令 $m\to\infty$，右边趋于 $I$，所以 $S$ 是双侧逆，范数估计由几何级数得到。
\end{proof}''')

add(6,r'''角度 $x$ 与 $x+2\pi$ 表示同一位置，因此摆的自然相空间是圆柱''',r'''
\begin{definition}[商空间、圆周与圆柱]\label{def:quotient-circle}
在集合 $X$ 上，满足自反、对称和传递性的关系称等价关系。
等价类记为 $[x]=\{y:y\sim x\}$，这些类组成商集 $X/{\sim}$，自然投影为 $\pi(x)=[x]$。
若 $X$ 有拓扑，规定 $U\subset X/{\sim}$ 开当且仅当 $\pi^{-1}(U)$ 开，称商拓扑。
关系 $x\sim y\Longleftrightarrow x-y\in2\pi\Z$ 给出圆周 $\R/2\pi\Z$，
映射 $[x]\mapsto(\cos x,\sin x)$ 将其与单位圆对应。
圆柱是圆周与实线的乘积：$(\R/2\pi\Z)\times\R$，其点由一个角度类及一个实数给出。
乘积拓扑以各因子开集的乘积为一组基。
\end{definition}''')

add(7,r'\begin{definition}[群作用与对称性]',r'''
\begin{definition}[光滑单参数变换群与生成场]\label{def:smooth-one-parameter}
开集上的一族变换 $g^s$，若 $(s,x)\mapsto g^s(x)$ 光滑，$g^0=\operatorname{id}$，且
$g^{s+t}=g^s\circ g^t$，称光滑单参数群；只在两边均有定义的小参数范围要求等式时，称局部单参数群。
其生成向量场为 $a(x)=\left.\partial_sg^s(x)\right|_{s=0}$。
对群等式求导可得 $\partial_sg^s(x)=a(g^s(x))$，所以它正是生成场的相流。
\end{definition}''')
replace(7,r'''射影直线 $\mathbb{RP}^1$ 是平面中过原点的直线所成的集合。''',
r'''射影直线 $\mathbb{RP}^1$ 是平面中过原点的直线所成的集合，也就是将 $\R^2\setminus\{0\}$ 中非零实数倍向量视为同一点所得的商空间，取定义~\ref{def:quotient-circle} 的商拓扑。''')
add(7,'对半三次抛物线 $y^2=x^3$，代入 $y=xv$ 并去掉原点外不为零的因子 $x^2$，',r'''
\begin{definition}[吹起中的纤维与严格变换]
映射 $\pi$ 在点 $a$ 上的纤维就是原像 $\pi^{-1}(a)$。
对含原点的曲线 $C$，它的严格变换是 $\pi^{-1}(C\setminus\{0\})$ 在 $E$ 中的闭包；
其中 $E$ 的局部开集和光滑性由上面两套坐标及其光滑过渡关系确定。
这也具体说明了此处“光滑曲面”的含义；抽象的统一定义见第~\ref{chap:manifolds}~章。
\end{definition}''')
add(7,r'\section{沿向量场求导与 Lie 括号}',r'''
\noindent
在坐标 $x_1,\ldots,x_n$ 中，$\partial_{x_i}$ 表示第 $i$ 个标准坐标方向的向量场，
所以 $v=\sum_i v_i\partial_{x_i}$；它作用于函数时就是方向导数。
两个线性算子 $A,B$ 的交换子记为 $[A,B]=AB-BA$。
\medskip''',before=False)
add(7,r'\begin{lemma}'+'\n'+r'$\R$ 的闭子群恰为',r'''
\begin{definition}[闭子群与陪集]
拓扑群是运算及取逆都连续的群；$\R$ 取通常拓扑和加法就是一例。
子群作为拓扑子集是闭集时，称闭子群。
子群 $H$ 的加法陪集为 $x+H=\{x+h:h\in H\}$；乘法记号下写为 $gH$。
\end{definition}''')

add(8,r'\begin{proposition}'+'\n'+'不同特征值的实特征函数在 $L^2(0,l)$ 中正交。',r'''
\begin{definition}[平方平均空间与正交]\label{def:l2-completion}
先在连续实函数上定义
\[
 \langle f,g\rangle=\int_0^l f(t)g(t)\,dt,
 \qquad\|f\|_2=\langle f,f\rangle^{1/2}.
\]
将这个内积空间按 $\|\cdot\|_2$ 完备化，得到 $L^2(0,l)$。
具体地，它的元素可由连续函数的 Cauchy 列表示；两列等价，是指它们之差的 $2$ 范数趋于零。
内积定义为代表列内积的极限，Cauchy--Schwarz 不等式保证该极限存在且与代表列无关。
内积为零称正交；范数为 1 且两两正交的族称标准正交系。
其有限线性组合在 $2$ 范数下稠密时，称完全正交系。
本节出现的特征函数都是经典光滑函数，因此其内积直接用上面的通常积分计算。
\end{definition}''')

add(10,'实线性系统在纯虚特征值均半单时分成若干独立旋转平面。',r'''
\begin{definition}[半单特征值]
特征值称半单，是指它在复 Jordan 形中的所有对应块均为一阶；等价地，其特征子空间维数等于它在特征多项式中的重数。
所有特征值的集合称矩阵的谱，“纯虚谱”指所有特征值实部为零。
环面 $\mathbb T^m$ 取圆周的乘积拓扑，其函数可用每个角变量均为 $2\pi$ 周期的函数表示。
\end{definition}''')

add(11,'定向图册要求过渡 Jacobian 为正。',r'''
\begin{definition}[定向、闭流形与带边界流形]\label{def:orientation-boundary}
在 $n$ 维实向量空间中，两组有序基若换基行列式为正，就规定它们有相同定向。
在每个坐标域选择定向，且所有重叠处换图行列式为正，称给流形选定了定向；
能够这样选择时称可定向。
紧且无边界的流形称闭流形，这里的“闭”不只是说它在某个环境空间中是闭集。
允许坐标域是半空间 $\{x_n\geq0\}$ 中的相对开集，就得到带边界流形；
局部对应 $x_n=0$ 的点组成边界 $\partial M$。
边界的定向约定为：先写向外法向量，再写边界的有序切向基，应得到内部的正向基。
\end{definition}''',before=False)
add(11,r'\begin{definition}'+'\n'+r'子集 $K\subset M$ 紧',r'''
\begin{definition}[覆盖映射]\label{def:covering-map}
连续满射 $\pi:\widetilde M\to M$ 称覆盖映射，若每个 $x\in M$ 有开邻域 $U$，
使 $\pi^{-1}(U)$ 是两两不交开集的并，且 $\pi$ 在每个这样的开集上都同胚到 $U$。
若每个点恰有 $k$ 个原像，称 $k$ 重覆盖。
例如 $\R\to\R/2\pi\Z$，$t\mapsto[t]$ 是覆盖；$S^n\to\mathbb{RP}^n$，$x\mapsto[x]$ 是双覆盖。
在半径足够小的球面片上，片与其对径片不交，各片都能唯一选取单位向量代表，故满足定义。
\end{definition}''')
add(11,r'\paragraph{拓扑预备结论。}',r'''
\begin{definition}[浸入、嵌入与把手]\label{def:immersion-embedding}
光滑映射 $f:M\to N$ 的每点微分单射时称浸入；若它还单射，且作为 $M\to f(M)$ 的映射是到子空间拓扑的同胚，称光滑嵌入。
因此嵌入不仅要求参数化没有零速度，还要求没有不同点重合或全局拓扑不相容。
从两个曲面各去掉一个开圆盘，再沿边界圆粘合，得到它们的连通和。
球面与 $g$ 个环面的连通和称为带 $g$ 个把手的可定向曲面；$g$ 称亏格。
\end{definition}''')
add(11,r'\begin{definition}'+'\n'+r'若存在逐纤维线性的丛同构',r'''
\begin{definition}[向量丛、截面与标架]\label{def:vector-bundle}
秩 $k$ 的光滑向量丛包括总空间 $E$、底空间 $M$ 和光滑投影 $p:E\to M$，
每个纤维 $E_x=p^{-1}(x)$ 是 $k$ 维向量空间；在每点附近有
$p^{-1}(U)\simeq U\times\R^k$ 的光滑对应，且在每条纤维上是线性同构。
这样的对应称局部平凡化。光滑映射 $s:M\to E$ 满足 $p\circ s=\operatorname{id}$ 时称截面。
两个同底空间向量丛之间逐纤维线性的微分同胚称丛同构。
一组在每条纤维组成基的光滑截面称标架；只在一个开集上选取时称局部标架。
切丛的局部平凡化就是前面构造的 $(x,v)$ 坐标，因而满足这些条件。
\end{definition}
\begin{definition}[度量与梯度]\label{def:riemannian-gradient}
Riemann 度量是在各切空间上光滑选取的正定内积 $g_x$。
在局部坐标中它由正定对称矩阵 $(g_{ij}(x))$ 表示，
$|v|_g^2=\sum_{i,j}g_{ij}v_iv_j$。
函数 $f$ 的梯度由
\[
 g_x(\operatorname{grad}f(x),v)=df_x(v)\quad(v\in T_xM)
\]
唯一确定，坐标分量是 $(g_{ij})^{-1}Df^T$。
对于 Euclidean 子流形，使用环境内积在切空间上的限制。
单位切向量丛为 $T^1M=\{(x,v)\in TM:|v|_g=1\}$。
\end{definition}''')
add(11,'Möbius 带不可平行化：',r'''
\begin{definition}[Möbius 带]
将 $[0,1]\times(-1,1)$ 中的 $(0,s)$ 与 $(1,-s)$ 识别，取商拓扑及由局部矩形诱导的光滑坐标，
所得曲面称开 Möbius 带。区间的中线拼成圆，横向坐标绕一周变号。
\end{definition}''')
replace(11,'正维球面中只有 $S^1,S^3,S^7$ 可平行化；这里将这一全维数分类作为拓扑预备结论。',
'正维球面的全维数平行化分类需要额外的拓扑理论；后面的论证只使用已经给出构造的例子和 $S^2$ 的指标证明。')
replace(11,r'''用有限个这样的邻域覆盖支撑紧集 $K$，取这些时间的一个正下界 $\delta$。''',
r'''这里 $K=\operatorname{supp}v$，支撑按定义~\ref{def:support-test} 在流形拓扑中取闭包。用有限个这样的邻域覆盖紧集 $K$，取这些时间的一个正下界 $\delta$。''')

add(12,r'\section{隐式常微分方程的 1-jet 几何}',r'''
\subsection*{微分形式的坐标定义}
\begin{definition}[余向量与微分形式]\label{def:forms-coordinate}
切空间 $T_xM$ 上的线性泛函称余向量，全体构成对偶空间 $T_x^*M$。
在坐标 $z_1,\ldots,z_N$ 中，$dz_i(v)=v_i$，所以 $df=\sum_i(\partial_i f)dz_i$。
$k$ 形式是每点一个交替的 $k$ 重线性函数，且系数光滑；
“交替”指交换两个向量位置会变号。其局部表达为
\[
 \omega=\sum_{i_1<\cdots<i_k}a_{i_1\cdots i_k}(z)
 dz_{i_1}\wedge\cdots\wedge dz_{i_k}.
\]
这里的楔积规定
\[
 (dz_{i_1}\wedge\cdots\wedge dz_{i_k})(v_1,\ldots,v_k)
 =\det\bigl((v_b)_{i_a}\bigr)_{a,b=1}^k.
\]
通过线性展开定义一般楔积；相邻两个 $dz_i$ 交换变号，重复指标的乘积为零。
$0$ 形式就是函数。$1$ 形式 $\alpha$ 的核为
$\ker\alpha_x=\{v:\alpha_x(v)=0\}$。
\end{definition}
\begin{definition}[拉回、外微分与收缩]\label{def:exterior-pullback}
光滑映射 $h:M\to N$ 对形式的拉回定义为
\[
 (h^*\omega)_x(v_1,\ldots,v_k)
 =\omega_{h(x)}(Dh_xv_1,\ldots,Dh_xv_k).
\]
对 $\omega=\sum_Ia_I dz_I$，定义外微分
$d\omega=\sum_{I,j}(\partial_j a_I)dz_j\wedge dz_I$。
收缩定义为 $(\iota_X\omega)(v_2,\ldots,v_k)=\omega(X,v_2,\ldots,v_k)$。
\end{definition}
\begin{proposition}
上述定义在换坐标后相容，并满足
\[
 d^2=0,\qquad d(h^*\omega)=h^*(d\omega),\qquad
 d(\alpha\wedge\beta)=d\alpha\wedge\beta+(-1)^k\alpha\wedge d\beta
\]
（$\alpha$ 为 $k$ 形式）。
\end{proposition}
\begin{proof}
坐标变换时 $dh_i=\sum_j\partial_jh_i\,dz_j$，将其代入楔积，得到子式行列式形式的换元规则，
也就是拉回的定义。再次求外微分时，混合二阶偏导对指标对称，而楔积对指标反对称，
因此二阶项成对抵消，给出 $d^2=0$ 和 $d(h^*\omega)=h^*d\omega$。
最后一式由系数的乘积求导得到；将新产生的微分移过 $k$ 个前置因子，就出现 $(-1)^k$。
这些恒等式还说明外微分的坐标定义彼此一致。
\end{proof}
\begin{definition}[闭形式与恰当形式]\label{def:closed-exact-form}
$d\omega=0$ 时称 $\omega$ 闭；存在 $\beta$ 使 $\omega=d\beta$ 时称恰当。
由 $d^2=0$，恰当形式总是闭的。
在凸开集上，闭 $1$ 形式 $\alpha=\sum a_i dx_i$ 有势函数：平移使 $0$ 在域内后取
\[
 H(x)=\int_0^1\sum_i a_i(tx)x_i\,dt.
\]
对 $x_j$ 求导，使用 $\partial_ja_i=\partial_i a_j$，被积函数变为 $\partial_t[ta_j(tx)]$，
所以 $\partial_jH=a_j(x)$。这一结论将用于平面首次积分的构造。
\end{definition}''')
replace(12,r'''1-形式是 $\alpha=\sum_j a_j(z)\,dz_j$；其外微分为''',
r'''依照定义~\ref{def:forms-coordinate}--\ref{def:exterior-pullback}，对 $1$ 形式 $\alpha=\sum_j a_j(z)\,dz_j$ 有''')
replace(12,r'''其中
$dz_i\wedge dz_j$ 是反对称乘积。
记 $\iota_X$ 为把一个向量位置代入 $X$ 的收缩，定义''',
'其中楔积和收缩均按前面的具体规则计算。定义')
add(12,r'''\begin{proposition}
在光滑嵌入子流形的充分小管状邻域内，距离函数 $r$ 在子流形外光滑，满足''',r'''
\begin{definition}[法空间与管状坐标]
对 Euclidean 空间中的子流形 $M$，法空间为切空间的正交补 $(T_qM)^\perp$。
一组光滑选取的正交单位法向量称局部单位法向标架；它可由局部切向基和 Gram--Schmidt 正交化取得。
将小法向量 $v\perp T_qM$ 送到 $q+v$，若在所考察区域为一一的光滑坐标变换，称这些坐标为管状坐标。
下面的距离结论取局部闭嵌入片，并将邻域缩小到最近点唯一的范围；不对任意非闭子流形声称统一正半径。
\end{definition}''')

add(13,r'\section{曲线指标及形变不变性}',r'''
\begin{definition}[同伦与曲线积分]\label{def:homotopy-line-integral}
两映射 $f_0,f_1:X\to Y$ 间的同伦是连续映射 $F:[0,1]\times X\to Y$，
满足 $F(0,x)=f_0(x)$、$F(1,x)=f_1(x)$；光滑对象间的光滑同伦另要求 $F$ 光滑。
对分段 $C^1$ 曲线 $\gamma:[a,b]\to\R^N$ 及 $1$ 形式 $\alpha=\sum_j a_jdx_j$，定义
\[
 \int_\gamma\alpha=\int_a^b\sum_j a_j(\gamma(t))\gamma_j'(t)\,dt.
\]
它在保方向的分段光滑换参数下不变，反向时变号；这是普通定积分换元公式的直接结果。
曲线闭合时也记为 $\oint_\gamma\alpha$。
\end{definition}''',before=False)
add(13,r'\begin{theorem}[平面指标和]',r'''
\begin{lemma}[平面 Green 公式]\label{lem:green-from-calculus}
设 $D$ 是边界分段光滑的有界平面区域，$P,Q$ 在其邻域连续可微，边界按内部在左侧的方向定向。则
\[
 \oint_{\partial D}P\,dx+Q\,dy
 =\iint_D(\partial_xQ-\partial_yP)\,dx\,dy.
\]
允许有限个孔，孔的边界因而取顺时针方向。
\end{lemma}
\begin{proof}
先对 $D=\{a\leq x\leq b,\ f(x)\leq y\leq g(x)\}$，
逐条计算上下边界的 $P\,dx$ 积分，再用一元微积分基本定理，得
\[
 \oint_{\partial D}P\,dx
 =\int_a^b[P(x,f(x))-P(x,g(x))]dx
 =-\iint_D\partial_yP\,dx\,dy.
\]
对水平简单区域同理得到 $\oint Q\,dy=\iint\partial_xQ$。
一般情形可在每个光滑边界片附近旋转坐标，把边界写成函数图像，并用有限光滑分片将形式分到这些片和内部小块。
每一片用刚才的基本定理计算；相邻片的内部边界成对反向而抵消，留下外边界及孔边界。
所需分片的明确构造和对任意维的同一计算见下面的命题~\ref{prop:forms-stokes-calculus}。
\end{proof}''')

add(13,r'\section{映射度的定义与计算}',r'''
\subsection*{定向积分与分片构造}
\begin{definition}[从属分片与形式的积分]\label{def:partition-integration}
有限开覆盖 $\{U_i\}$ 的光滑分片统一是非负光滑函数 $\rho_i$，满足
$\sum_i\rho_i=1$ 且 $\operatorname{supp}\rho_i\subset U_i$。
对紧流形，可在每点选较小坐标球，其闭包包含在一个 $U_i$ 内；有限个较小球覆盖全流形。
用例~\ref{ex:smooth-cutoff} 的凸起构造 $b_i$，使它在较小球为正、支撑在较大坐标球内。
于是 $\rho_i=b_i/\sum_jb_j$ 给出分片。
\end{definition}
在 $n$ 维定向坐标中，顶次形式为 $\omega=a(x)dx_1\wedge\cdots\wedge dx_n$。
若支撑在一张正向图中，定义 $\int_M\omega=\int a(x)dx$。
一般情形定义为 $\sum_i\int_M\rho_i\omega$。
重积分换元公式保证一张图的结果与正向坐标选择无关；对两组分片使用乘积 $\rho_i\sigma_j$，
便知总和也与分片选择无关。因此这确实是一个确定的积分。
\begin{proposition}[Stokes 公式]\label{prop:forms-stokes-calculus}
在紧定向带边界 $n$ 流形上，对光滑 $(n-1)$ 形式 $\beta$ 有
\[
 \int_M d\beta=\int_{\partial M}\beta.
\]
\end{proposition}
\begin{proof}
由刚构造的有限分片，$\beta=\sum_i\rho_i\beta$，而
$\sum_i d(\rho_i\beta)=d\beta$。因此只需证明支撑在一张图内的情形。
在内部图中，把各系数延零到 $\R^n$，写
\[
 \beta=\sum_{j=1}^n(-1)^{j-1}b_j(x)
 dx_1\wedge\cdots\wedge\widehat{dx_j}\wedge\cdots\wedge dx_n,
 \qquad d\beta=\sum_j\partial_jb_j\,dx_1\wedge\cdots\wedge dx_n.
\]
帽号表示省略该项。逐次积分和紧支撑使每个全轴导数积分为零，故内部图没有边界贡献。
在边界图中改在半空间积分，切向全轴导数仍积分为零；法向半轴导数的积分由微积分基本定理等于边界值。
按“向外法向在先”的边界定向，该边界值的符号正好是 $\int_{\partial M}\beta$ 的符号。
把有限各片相加即得结论。这一证明只使用重积分换元、累次积分及一元基本定理。
\end{proof}''')
add(13,r'\begin{lemma}[同维情形的正则值]',r'''
\begin{definition}[零测集的覆盖意义]
集合 $Z\subset\R^n$ 称零测集，是指任给 $\varepsilon>0$，均可用可数个开长方体覆盖它，
且这些长方体体积之和小于 $\varepsilon$。
可数个零测集的并仍零测：对第 $j$ 个集合使用总体积小于 $\varepsilon2^{-j}$ 的覆盖，再合并。
以下只用这一覆盖性质，不预设一般 Lebesgue 积分。
流形上的零测集按可数坐标图内的像判断；紧坐标块上光滑换图为 Lipschitz，
长方体覆盖的体积估计因而保证该性质与图无关。
临界点是微分不可逆的点，临界值是临界点的像。
\end{definition}''')
replace(13,r'''下面的映射度证明使用流形上的形式、积分与 Stokes 公式。
它们是本节的多元积分前提：形式局部是交替的微分乘积，$d$ 按偏导和反对称乘法定义，
积分由定向坐标图换元并分片相加，Stokes 公式由 Euclidean 分部积分和分片统一得到。''',
r'''下面使用前面已经定义的形式积分与命题~\ref{prop:forms-stokes-calculus}，将局部 Jacobian 符号与整体整数联系起来。''')
add(13,r'\paragraph{指标和的全局结论。}',r'''
\begin{definition}[有限三角剖分与 Euler 特征数]\label{def:euler-characteristic}
$k$ 单纯形是 $k+1$ 个仿射无关点的凸包，形如
$\{\sum_{j=0}^kt_jv_j:t_j\geq0,\ \sum_jt_j=1\}$；部分顶点的凸包称面。
有限个单纯形按公共面粘合，且每两单纯形相交为空或共同的面，得到有限单纯复形。
它到 $M$ 的一个同胚称 $M$ 的有限三角剖分。
若其中 $k$ 维单纯形有 $c_k$ 个，则
\[
 \chi(M)=\sum_k(-1)^kc_k
\]
称 Euler 特征数；对于曲面即顶点数减边数加面数。
同样可用有限胞腔分解计数：$k$ 维胞腔的内部是一份开 $k$ 球，边界粘到较低维部分。
这一整数对所选分解的不变性以及与向量场指标和的相等性，是下面全局指标和定理的内容。
\end{definition}''')
add(13,'取函数的梯度场。每个临界点的线性化为 Hessian，',r'''
\noindent
这里临界点指 $df=0$ 的点；非退化指该点坐标 Hessian 矩阵可逆。
在临界点换坐标时 Hessian 作可逆合同变换，故此条件不依赖坐标。
梯度按定义~\ref{def:riemannian-gradient} 选定任一光滑正定度量；
其线性化实际是 $g^{-1}\operatorname{Hess}f$，由于 $\det g>0$，行列式符号与 Hessian 相同。
\medskip''')
replace(13,'取函数的梯度场。每个临界点的线性化为 Hessian，故局部指标等于其行列式符号：',
'取上述梯度场，故局部指标等于 Hessian 的行列式符号：')

add(14,'下面只研究分段光滑射线与经典局部光学模型。',r'''
\begin{definition}[泛函、变分与驻曲线]\label{def:variation-functional}
把一条函数或曲线送到一个实数的规则称泛函。例如
\[
 \mathcal I[y]=\int_a^b L(x,y(x),y'(x))\,dx.
\]
固定端点，取光滑 $\eta$ 满足 $\eta(a)=\eta(b)=0$，将 $y$ 换成 $y+s\eta$，称作变分。
若对每个这样的 $\eta$，$\left.\frac d{ds}\mathcal I[y+s\eta]\right|_{s=0}=0$，称 $y$ 为驻曲线。
驻曲线不一定使泛函取最小值。
\end{definition}
\begin{lemma}[Euler--Lagrange 方程]\label{lem:euler-lagrange-elementary}
若 $L$ 足够光滑，$C^2$ 驻曲线满足
\[
 \frac d{dx}L_{y'}=L_y.
\]
\end{lemma}
\begin{proof}
在有限区间上微分积分，再分部积分，得到
\[
 0=\int_a^b(L_y\eta+L_{y'}\eta')dx
 =\int_a^b\left(L_y-\frac d{dx}L_{y'}\right)\eta\,dx.
\]
括号内若在一点严格为正，由连续性在一个小区间保持正；取支撑在其中的非负非零凸起函数作 $\eta$，积分便严格为正，矛盾。
负值同理排除，故括号处处为零。对向量曲线逐个分量作变分，得到相应方程组。
\end{proof}
\begin{definition}[长度、能量与测地线]\label{def:geodesic-variational}
在 Riemann 度量 $g$ 下，曲线 $q(t)$ 的长度与能量分别为
\[
 \ell[q]=\int |q'|_g\,dt,\qquad
 E[q]=\frac12\int\sum_{i,j}g_{ij}(q)q_i'q_j'\,dt.
\]
固定端点的能量驻曲线称有仿射参数的测地线；其方程由前一引理逐坐标给出。
沿该方程对 $|q'|_g^2$ 求导，代入 Euler--Lagrange 方程，得到导数为零，故速度长度恒定。
非零常速时，长度的一阶变分是能量一阶变分除以该速度，因而它也是长度驻曲线。
对于光学度量 $g=n(y)^2(dx^2+dy^2)$，长度就是光程，光线取为它的非零速度驻曲线。
\end{definition}''')
replace(14,'本章的力学与光学例子分别使用常系数线性化、首次积分与 Hamilton 方程；',
'本章的力学与光学例子分别使用常系数线性化、首次积分、Hamilton 方程以及下文给出定义的变分法；')
add(14,r'\begin{definition}'+'\n'+r'''概率流为 $J=bu-\varepsilon u_x$''',r'''
\begin{definition}[周期密度与经典解]
圆周上的概率密度指非负的 $L$ 周期连续函数 $u$，满足 $\int_0^Lu(x)dx=1$；
对一段圆弧赋予的质量为其上 $u$ 的积分。
含时间的经典解在这里指具有连续 $u_t,u_x,u_{xx}$ 并逐点满足密度方程的周期函数。
概率流 $J$ 以守恒式 $u_t=-J_x$ 定义其输运意义，不预设随机过程的一般理论。
\end{definition}''')
add(14,r'\begin{proposition}[小扩散极限]',r'''
\begin{definition}[密度的集中与弱收敛]\label{def:density-concentration}
概率密度 $\rho_\varepsilon$ 集中于闭集 $K$，是指对每个包含 $K$ 的开邻域 $V$，
$\int_{V^c}\rho_\varepsilon dx\to0$。
称它弱收敛到 $x_*$ 处的单位质量，是指对每个连续周期函数 $f$ 都有
\[
 \int_0^Lf(x)\rho_\varepsilon(x)dx\longrightarrow f(x_*).
\]
这不是逐点收敛。若密度集中于唯一点 $x_*$，在该点的小邻域内用 $f$ 的一致连续性控制差，
邻域外用 $2\|f\|_\infty$ 乘以趋零的质量控制差，即得到上述弱收敛。
$L^1$ 距离在本章指 $\|u-v\|_1=\int_0^L|u-v|dx$，所有函数光滑，均为通常积分。
\end{definition}''')

add(15,r'\begin{theorem}[局部稳定流形]',r'''
\begin{definition}[映射的稳定子空间与局部不变性]
对可逆矩阵 $A$，其模小于 1 的广义特征空间的实直和记为 $E^s$，模大于 1 者记为 $E^u$。
这与连续流按特征值实部正负划分不同；时间 $\tau$ 映射的特征值为 $e^{\tau\lambda}$，才将两种划分联系起来。
子集局部不变，是指点及其像都留在规定邻域时，映射将集合内的点仍送到该集合内。
子流形在零点与 $E^s$ 相切，是指 $T_0W=E^s$。
\end{definition}
\begin{definition}[等价范数与加权序列空间]\label{def:weighted-banach}
两个范数等价，是指存在 $c,C>0$ 使 $c\|x\|_1\leq\|x\|_2\leq C\|x\|_1$。
固定 $0<\sigma\leq1$，记
\[
 X_\sigma=\{z=(z_n)_{n\geq0}:\|z\|_\sigma:=\sup_{n\geq0}\sigma^{-n}|z_n|<\infty\}.
\]
这是 Banach 空间：加权 Cauchy 列在每个坐标有极限，统一的 Cauchy 界对坐标取极限后仍成立，
因而所得极限仍在 $X_\sigma$，且依此范数收敛。
特别地 $X_1=\ell^\infty$ 是有界序列空间。
\end{definition}
\begin{definition}[Banach 空间中的微分]\label{def:frechet-derivative}
对 Banach 空间间的映射 $F:U\subset X\to Y$，若存在有界线性映射 $A$ 使
\[
 \frac{\|F(x+h)-F(x)-Ah\|_Y}{\|h\|_X}\longrightarrow0,
\]
则称 $F$ 在 $x$ 处 Fréchet 可微，记 $DF(x)=A$。
若导数按算子范数连续，称 $F\in C^1$；将导数继续作为映射求导，定义 $C^r$。
高阶导数是连续多重线性映射，其范数是各输入范数不超过 1 时输出范数的上确界。
在有限维空间中，这就是全微分的线性主部定义。
后面的不动点导数公式会直接估计这一余项，不调用无穷维隐函数定理。
\end{definition}''')
add(15,r'''在有界连续函数的完备空间 $C_b(\R,\R^n)$ 中，定义''',r'''
\noindent
这里 $P_s,P_u$ 是按直和 $\R^n=E^s\oplus E^u$ 分取两个分量的线性投影，
$P_s+P_u=I$。$C_b(\R,\R^n)$ 指全轴上有界连续函数，取范数
$\|f\|_\infty=\sup_{t\in\R}|f(t)|$。
一致 Cauchy 列一致收敛到有界连续函数，故它是 Banach 空间。
对非线性映射 $R$，$\operatorname{Lip}(R)$ 是所有满足
$|R(x)-R(y)|\leq L|x-y|$ 的常数 $L$ 的下确界。
\medskip''')
add(15,'以下使用两个分析预备定理：',r'''
\begin{definition}[Dirichlet 算子、Rayleigh 商与算子性质]\label{def:dirichlet-rayleigh}
在有界区域 $\Omega\subset\R^d$ 上，记 $\Delta u=\sum_j\partial_{x_j}^2u$ 为 Laplace 算子。
给定连续实势 $V$，$Hu=-\Delta u+Vu$ 连同边界条件 $u|_{\partial\Omega}=0$，
称 Dirichlet Schrödinger 问题；方程 $Hu=\lambda u$ 的非零解称特征函数，$\lambda$ 称特征值。
对于零边界的分段光滑非零函数，其 Rayleigh 商定义为
\[
 \mathcal R[u]=\frac{\int_\Omega(|\nabla u|^2+V|u|^2)dx}
 {\int_\Omega|u|^2dx}.
\]
必要时先将光滑紧支撑函数按
$\|u\|_{H^1}^2=\int_\Omega(|u|^2+|\nabla u|^2)dx$ 完备化；所得空间记 $H_0^1(\Omega)$。
边界为零在这一完备化意义下解释。内积空间的完备化按定义~\ref{def:l2-completion} 的 Cauchy 列构造进行。
\end{definition}
\begin{definition}[紧算子、自伴与 Green 核]
Hilbert 空间上的有界线性算子 $T$ 自伴，是指 $\langle Tu,v\rangle=\langle u,Tv\rangle$。
$T$ 紧，是指任一有界序列的像都有范数收敛子列。
积分算子 $Tf(x)=\int K(x,y)f(y)dy$ 的函数 $K$ 称核；若 $T$ 是某个零边界微分问题的解算子，
则称 $K$ 为该问题的 Green 核。
最低特征值指全体特征值中的最小者，相应特征函数称最低特征函数；
“内部严格正”指 $u(x)>0$ 对每个 $x\in\Omega$ 成立。
以下的正性结论是额外列出的分析命题，不把术语定义本身当成该命题的证明。
\end{definition}''')
add(15,r'\paragraph{Cibrario 与 Davydov 正规形。}',r'''
\begin{definition}[投影曲线族的等价与一般位置]
两个隐式方程的解曲线族在底空间光滑等价，是指存在同一个底空间局部微分同胚，
把第一族的每条曲线弧送到第二族的一条曲线弧，逆映射也有此性质。
这比允许分别改变曲面上每条轨道的坐标更强。
“一般位置”指有关非退化条件成立；本节的非例外折叠具体是
$F_p=0,F_{pp}\ne0,F_t+pF_x\ne0$，不将这个用语作为省略条件的替代。
\end{definition}''')

alltext='\n'.join((root/f'chapters/chapter{i}.tex').read_text(encoding='utf-8') for i in range(1,16))
labels=re.findall(r'\\label\{([^}]+)\}',alltext);assert len(labels)==len(set(labels))
assert r'\input{' not in alltext
report={'date':'2026-10-30','backup':str(backup),'backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'changes':changes,'labels':len(labels)}
(root/'教材对照/工作材料/数分前置定义补全记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'backup':str(backup),'insertions':len(changes),'labels':len(labels)},ensure_ascii=False))
