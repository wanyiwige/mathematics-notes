from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[2]
edits=[]
def proof(file,key,body): edits.append((file,key,body.strip()))

proof('arnold-models.tex',r'对分量求导',r'''
先设 $\varphi=(\varphi_1,\varphi_2)$ 是直积方程在 $I$ 上的解。
向量函数的可微性等价于各分量可微，且微分逐分量进行，因此
\[
 (\varphi_1'(t),\varphi_2'(t))
 =(v_1(\varphi_1(t)),v_2(\varphi_2(t))).
\]
比较两个分量，便得到各自的微分方程。

反过来，若 $\varphi_i$ 分别满足相应方程，则把两个分量等式合并，
就得到 $\varphi'=v(\varphi)$；同时 $\varphi(t)\in U_1\times U_2$。
所以它确实是直积方程的解。
如果分量解起初定义在不同区间 $I_1,I_2$ 上，则这一步只能在公共区间
$I_1\cap I_2$ 上进行，不能把其中一个分量未定义的时刻也纳入联合运动。
''')
proof('arnold-green.tex',r'积分与 $f(\xi)$',r'''
因为脉冲非负且积分为 1，先把常数 $f(\xi)$ 写成
$f(\xi)\int h_N(s-\xi)\,ds$。于是
\begin{align*}
 \left|\int h_N(s-\xi)f(s)\,ds-f(\xi)\right|
 &=\left|\int h_N(s-\xi)(f(s)-f(\xi))\,ds\right|\\
 &\leq\sup_{|s-\xi|\leq\varepsilon_N}|f(s)-f(\xi)|
       \int h_N(s-\xi)\,ds\\
 &=\sup_{|s-\xi|\leq\varepsilon_N}|f(s)-f(\xi)|.
\end{align*}
这里用支集条件把所有非零贡献限制在 $\xi$ 的小邻域内。
给定任意 $\eta>0$，连续性给出 $\delta>0$，使 $|s-\xi|<\delta$ 时
$|f(s)-f(\xi)|<\eta$。充分大的 $N$ 满足 $\varepsilon_N<\delta$，
所以上述差小于 $\eta$，极限成立。
''')
proof('arnold-linear-algebra.tex',r'由群性质，对 $s$',r'''
首先由 $g^{t+h}=g^hg^t$，在固定 $t$ 时作差商：
\[
 \frac{g^{t+h}-g^t}{h}=\frac{g^h-I}{h}\,g^t.
\]
令 $h\to0$，生成元的定义给出 $(g^t)'=Ag^t$。
又因为 $g^0=I$，对任意初始向量 $x_0$，曲线 $x(t)=g^tx_0$ 满足
\[
 x'=Ax,\qquad x(0)=x_0.
\]
由定理~\ref{thm:常系数线性方程组的矩阵指数解}，这一初值问题的解是
$e^{tA}x_0$；唯一性说明 $g^tx_0=e^{tA}x_0$ 对所有 $x_0$ 成立。
因此两个线性算子相同。

若另有矩阵 $B$ 也满足 $g^t=e^{tB}$，对 $t=0$ 求导得到 $A=B$。
这证明的不仅是表示的存在性，也包括生成元的唯一性。
''')
proof('arnold-linear-algebra.tex',r'取满足 $\|AB\|',r'''
取次乘性矩阵范数，令 $a=\|A\|$。二项式展开为
\[
 \left(I+\frac Am\right)^m
 =\sum_{k=0}^m c_{m,k}A^k,\qquad
 c_{m,k}=\frac1{k!}\prod_{j=0}^{k-1}\left(1-\frac jm\right).
\]
对固定 $k$，当 $m\to\infty$ 时 $c_{m,k}\to1/k!$；并且
$0\leq c_{m,k}\leq1/k!$。把 $k>m$ 时的 $c_{m,k}$ 定义为零，则可统一比较无穷级数。

给定 $\eta>0$，先由数项指数级数的收敛性选 $K$，使
$2\sum_{k>K}a^k/k!<\eta/2$。随后对 $m>K$ 分成有限头部与尾部：
\begin{align*}
 \left\|e^A-\left(I+\frac Am\right)^m\right\|
 &\leq\sum_{k=0}^K\left|\frac1{k!}-c_{m,k}\right|a^k
       +2\sum_{k>K}\frac{a^k}{k!}.
\end{align*}
头部只有有限项，可令 $m$ 足够大使其小于 $\eta/2$；尾部已被统一控制。
总差小于 $\eta$，因此范数极限成立。
''')
proof('arnold-linear-algebra.tex',r'归纳得 $u_j=B^ju_0$',r'''
递推关系给出 $u_1=Bu_0$。若已有 $u_j=B^ju_0$，则
$u_{j+1}=Bu_j=B^{j+1}u_0$，故归纳得到所有非负整数时刻的公式。

令 $B=PJP^{-1}$，则 $B^j=PJ^jP^{-1}$。
在大小为 $s$ 的 Jordan 块 $J_\lambda=\lambda I+N$ 中，$N^s=0$，
且 $N$ 与 $\lambda I$ 交换，所以二项式给出
\[
 J_\lambda^j=\sum_{r=0}^{\min(j,s-1)}\binom jr\lambda^{j-r}N^r.
\]
当 $\lambda\ne0$，可提出 $\lambda^j$；
$\binom jr=j(j-1)\cdots(j-r+1)/r!$ 是 $j$ 的 $r$ 次多项式。
所以该块的每个矩阵元都是 $\lambda^j$ 乘以次数至多 $s-1$ 的多项式。
当 $\lambda=0$，该块就是 $N$，其 $j$ 次幂对 $j\geq s$ 为零。
最后乘上固定矩阵 $P,P^{-1}$，只对这些矩阵元作有限线性组合，因此结论保持。
''')
proof('arnold-linear-algebra.tex',r'设 $\dim V=n$',r'''
设 $\dim V=n>0$，取基 $f_1,\ldots,f_n$。先证明存在 $n$ 个点
$t_1,\ldots,t_n$，使求值映射
$E:V\to\C^n$，$Ef=(f(t_1),\ldots,f(t_n))$ 可逆。
所有求值泛函若不能张成 $V^*$，其公共零空间中就有一个非零 $f\in V$。
但这意味着 $f(t)=0$ 对每个 $t$ 成立，与 $f$ 为非零函数矛盾。
因此可从这些泛函选出一组基，得到所需的 $t_j$。

在这组坐标中，$T_s|_V$ 的矩阵为 $ET_sE^{-1}$。
其元素是 $f_i(t_j+s)$ 的固定线性组合，因而关于 $s$ 光滑。
平移关系 $T_{s+t}=T_sT_t$ 说明它是线性单参数群。
在 $s=0$ 求导，其生成元作用于 $f$ 的结果在每个求值点为 $f'(t_j)$。
事实上该导数也逐点为 $f'$：任意求值泛函都是 $V$ 上的连续线性泛函，
可与有限维导数交换。因此 $D(V)\subset V$。

令 $p$ 为 $D|_V$ 的特征多项式。Cayley--Hamilton 定理说明
$p(D)f=0$ 对每个 $f\in V$ 成立。
$p$ 是 $n$ 次首一多项式，而常系数 $n$ 阶方程的全部解空间恰为 $n$ 维。
这个解空间包含同为 $n$ 维的 $V$，所以二者相等。
重根基本解定理进一步给出
$V=\bigoplus_\lambda E_\lambda^{m_\lambda}$。

反过来，平移后的 $e^{\lambda(t+s)}p(t+s)$ 仍属于同一个
$E_\lambda^m$，所以这些直和确实平移不变。
若 $V=\{0\}$，取零阶方程 $f=0$ 即可，结论也成立。
''')
proof('arnold-linear-algebra.tex',r'在 $E_\lambda^m$ 的基',r'''
在 $E_\lambda^m$ 中取基 $e_j(t)=e^{\lambda t}t^j/j!$，$0\leq j<m$。
直接求导得到 $(D-\lambda I)e_0=0$、$(D-\lambda I)e_j=e_{j-1}$。
因此 $N=D-\lambda I$ 在这个空间中是幂零移位。

由 $P(\lambda+z)=z^\nu Q(z)$，有 $P(D)=N^\nu Q(N)$。
$Q(N)$ 的矩阵是对角元全为 $Q(0)\ne0$ 的三角矩阵，故可逆；
$N^\nu$ 则把 $E_\lambda^{k+\nu}$ 满射到 $E_\lambda^k$。
所以任意 $f\in E_\lambda^k$ 都有一个原像
$y=e^{\lambda t}\sum_{j=0}^{k+\nu-1}c_jt^j$。

把其中次数小于 $\nu$ 的项记为 $y_0$。
它被 $N^\nu$ 消去，故 $P(D)y_0=Q(N)N^\nu y_0=0$。
于是 $y-y_0$ 仍为特解，而它的多项式部分可提出 $t^\nu$，
余下次数小于 $k$，得到所述形式。
$\nu=0$ 时无需去掉低次项，同一论证给出非共振情形。
''')
proof('arnold-contraction.tex',r'反复应用压缩估计',r'''
\textbf{第一步：构造 Cauchy 序列。}
固定 $x_0\in M$，令 $x_{n+1}=Ax_n$，记 $d_0=d(x_1,x_0)$。
反复应用压缩条件，得到
$d(x_{j+1},x_j)\leq\lambda^jd_0$。
对 $m>n$，三角不等式和几何级数给出
\[
 d(x_m,x_n)\leq\sum_{j=n}^{m-1}d(x_{j+1},x_j)
 \leq d_0\sum_{j=n}^{m-1}\lambda^j
 \leq\frac{\lambda^n}{1-\lambda}d_0.
\]
右端不依赖 $m$，且随 $n\to\infty$ 趋于零，所以这是 Cauchy 序列。
由完备性，存在 $x_*\in M$ 使 $x_n\to x_*$。

\textbf{第二步：验证不动点并证明唯一性。}
由压缩估计，$A$ 连续，故
$Ax_*=\lim Ax_n=\lim x_{n+1}=x_*$。
若 $Ay_*=y_*$，则
$d(x_*,y_*)\leq\lambda d(x_*,y_*)$。
由于 $1-\lambda>0$，只能有 $d(x_*,y_*)=0$，即 $x_*=y_*$。

\textbf{第三步：误差估计。}
让第一步的不等式中 $m\to\infty$，便得到迭代误差界。
对任意近似点 $x$，另由
\[
 d(x,x_*)\leq d(x,Ax)+d(Ax,Ax_*)
 \leq d(x,Ax)+\lambda d(x,x_*)
\]
移项得到残差界 $d(x,x_*)\leq d(x,Ax)/(1-\lambda)$。
''')
proof('arnold-contraction.tex',r'该闭集属于完备',r'''
令 $J=[t_0-h,t_0+h]$，在 $C(J,\R^n)$ 上取一致范数。
连续函数列若依一致范数 Cauchy，便一致收敛到连续函数，故该空间完备。
集合 $\mathcal M=\{u:\|u-x_0\|_\infty\leq b\}$ 是闭集，且包含常函数 $u=x_0$，
因此是非空完备度量空间。

若 $u\in\mathcal M$，则所有 $(t,u(t))$ 都在给定矩形内，所以积分有定义，且
\[
 |(Au)(t)-x_0|\leq\left|\int_{t_0}^t M\,ds\right|
 \leq Mh\leq b.
\]
这证明 $A\mathcal M\subset\mathcal M$。
对任意 $u,w\in\mathcal M$，Lipschitz 条件给出
\[
 |(Au)(t)-(Aw)(t)|\leq L|t-t_0|\|u-w\|_\infty.
\]
取上确界得 $\|Au-Aw\|_\infty\leq Lh\|u-w\|_\infty$。
由于 $Lh<1$，压缩映射定理适用。
其不动点满足积分方程，右端连续，所以对时间可微，微分后满足原初值问题。
反过来，每个处于此矩形内的解积分后也是不动点，唯一性随之成立。
''')
proof('arnold-contraction.tex',r'平移并作可逆线性换元',r'''
平移定义点、值域原点，再左乘 $DF(x_0)^{-1}$，只需研究
$F(0)=0,DF(0)=I$ 的情形。写 $F(x)=x+R(x)$，则 $R(0)=0,DR(0)=0$。
由 $DR$ 连续，可取闭球 $B_r$，使其中 $\|DR\|\leq\theta<1$。
球的凸性与微积分中值估计给出
$|R(x)-R(z)|\leq\theta|x-z|$，特别地 $|R(x)|\leq\theta r$。

给定 $|y|<(1-\theta)r$，定义 $A_y(x)=y-R(x)$。
于是 $|A_y(x)|\leq|y|+\theta r\leq r$，且其压缩常数为 $\theta$。
因此存在唯一 $G(y)\in B_r$ 满足 $G(y)+R(G(y))=y$。
对 $y,z$ 的不动点方程相减，得到
\[
 |G(y)-G(z)|\leq|y-z|+\theta|G(y)-G(z)|,
\]
所以 $G$ 为 Lipschitz 连续，常数不超过 $(1-\theta)^{-1}$。

还要证明逆可微。固定 $y$，令 $x=G(y)$、$u=G(y+v)-G(y)$。
由刚得的界，$|u|\leq(1-\theta)^{-1}|v|$。
Taylor 公式给出 $v=F(x+u)-F(x)=DF(x)u+o(|u|)$。
$DF(x)=I+DR(x)$ 可逆，其逆由收敛 Neumann 级数给出，故
\[
 u=DF(x)^{-1}v+o(|v|).
\]
于是 $DG(y)=DF(G(y))^{-1}$。
右端连续，所以 $G\in C^1$；而 $F$ 在小球内的单射性还可由
$|F(x)-F(z)|\geq(1-\theta)|x-z|$ 直接验证。
这给出了局部互逆的两个映射。
''')

def apply():
    report=[]
    for file,key,body in edits:
        p=root/'chapters'/file; text=p.read_text(encoding='utf-8')
        matches=list(re.finditer(r'\\begin\{proof\}(.*?)\\end\{proof\}',text,re.S))
        candidates=[m for m in matches if key in m.group(1)]
        if len(candidates)!=1: raise RuntimeError((file,key,len(candidates)))
        m=candidates[0]; old=m.group(1)
        text=text[:m.start(1)]+'\n'+body+'\n'+text[m.end(1):]
        p.write_text(text,encoding='utf-8')
        report.append({'file':file,'key':key,'before':len(old),'after':len(body)})
    (root/'教材对照/工作材料/本轮证明扩写记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('EXPANDED',len(report),'BEFORE',sum(x['before'] for x in report),'AFTER',sum(x['after'] for x in report))
if __name__=='__main__': apply()
