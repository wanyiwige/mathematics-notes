from pathlib import Path
root=Path(__file__).resolve().parents[2]
def edit(file,old,new):
    p=root/'chapters'/file;s=p.read_text(encoding='utf-8');assert s.count(old)==1,(file,old,s.count(old));p.write_text(s.replace(old,new),encoding='utf-8')

edit('arnold-models.tex','独立过程的联合状态由各自的状态组成，但联合运动只使用同一个时间参数。',r'''独立过程的联合状态由各自的状态组成，但联合运动只使用同一个时间参数。
所有允许状态组成的集合称为状态空间；在自治系统中亦称相空间。解在状态空间中的像称为轨道。
这里先用这些词描述模型，第六章再系统研究其几何性质。''')

p=root/'chapters/chapter5.tex';s=p.read_text(encoding='utf-8')
start=s.index(r'\textbf{法二：}',s.index(r'\label{thm:C1依赖性定理}'))
end=s.index(r'\end{proof}',start)
s=s[:start]+r'''\textbf{法二：利用增量方程与Gronwall估计。}
这一方法仍沿原来的思路：先构造候选导数，再证明解的增量与其线性部分之差为高阶小量。
记
\[
 A(t,\lambda)=D_xf(t,\varphi(t,\lambda),\lambda),\qquad
 B(t,\lambda)=D_\lambda f(t,\varphi(t,\lambda),\lambda).
\]
这里用 $f,\varphi,\lambda$ 简记原来的向量函数与参数。由线性方程的存在唯一性，矩阵初值问题
\[
 Z'=AZ+B,\qquad Z(0,\lambda)=0
\]
有唯一解。其列分别满足线性非齐次方程；由已经证明的连续依赖性，$Z$ 关于 $(t,\lambda)$ 连续。

对参数增量 $\Delta\lambda$，定义真正的解增量
\[
 \Delta x(t)=\varphi(t,\lambda+\Delta\lambda)-\varphi(t,\lambda).
\]
连续依赖性使它在固定紧时间段上一致趋于零。对 $f$ 使用带积分余项的一阶展开，得到
\begin{align*}
 (\Delta x)'&=(A+E_1)\Delta x+(B+E_2)\Delta\lambda,\\
 \Delta x(0)&=0,
\end{align*}
其中 $E_1,E_2$ 分别为 $n\times n,n\times m$ 矩阵，并且
\[
 \sup_{|t|\leq h}\bigl(\|E_1\|+\|E_2\|\bigr)\longrightarrow0
 \qquad(\Delta\lambda\to0).
\]
这一一致性来自 $D_xf,D_\lambda f$ 在所考察紧邻域上的一致连续性。

令 $u=\Delta x-Z\Delta\lambda$。将上式与 $Z'=AZ+B$ 相减，得
\[
 u'=(A+E_1)u+(E_1Z+E_2)\Delta\lambda,\qquad u(0)=0.
\]
取常数 $N$ 控制 $\|A\|$，并以 $\eta(\Delta\lambda)\to0$ 同时控制
$\|E_1\|$ 和 $\|E_1Z+E_2\|$。积分后使用 Gronwall 不等式，正负时间分别估计，均得到
\[
 \|u(t)\|\leq h\eta(\Delta\lambda)
 e^{(N+\eta(\Delta\lambda))h}\|\Delta\lambda\|,
 \qquad |t|\leq h.
\]
因此
\[
 \sup_{|t|\leq h}
 \frac{\|\varphi(t,\lambda+\Delta\lambda)-\varphi(t,\lambda)-Z(t,\lambda)\Delta\lambda\|}
 {\|\Delta\lambda\|}\longrightarrow0.
\]
所以 $D_\lambda\varphi=Z$。由 $Z$ 的连续性，参数导数连续；又
$\partial_t\varphi=f(t,\varphi,\lambda)$ 连续，从而得到所需的联合 $C^1$ 依赖性。
''' +s[end:]
anchor=r'\begin{corollary}($C^r$ 依赖性推论)'
assert s.count(anchor)==1
matrix=r'''\begin{proposition}[初值导数的矩阵变分方程]\label{prop:matrix-variation}
设有限维方程 $x'=f(t,x)$ 的右端关于 $x$ 连续可微，记解为 $\varphi(t;t_0,\xi)$。
在解共同存在的区间内，矩阵
\[
 Z(t)=D_\xi\varphi(t;t_0,\xi)
\]
满足
\[
 Z'=D_xf(t,\varphi(t;t_0,\xi))Z,\qquad Z(t_0)=I.
\]
\end{proposition}
\begin{proof}
第五章开头的平移把初值 $\xi$ 变成参数，因此 $C^1$ 依赖性定理保证这个导数存在且连续。
对积分方程
\[
 \varphi(t;t_0,\xi)=\xi+\int_{t_0}^t f(s,\varphi(s;t_0,\xi))\,ds
\]
关于 $\xi$ 求导。在固定紧时间段内，相关导数连续，可交换参数微分与积分，得到
\[
 Z(t)=I+\int_{t_0}^tD_xf(s,\varphi(s;t_0,\xi))Z(s)\,ds.
\]
再对 $t$ 求导即得方程，取 $t=t_0$ 得到初始矩阵 $I$。
该矩阵方程逐列是一阶线性初值问题，故解唯一。
\end{proof}

'''
s=s.replace(anchor,matrix+anchor);p.write_text(s,encoding='utf-8')
edit('qualitative-volume.tex',r'由推论~\ref{cor:解对初值和参数的偏导方程}',r'由命题~\ref{prop:matrix-variation}')
edit('qualitative-volume.tex',r'固定初值 $x$，令 $Z(t)=D\varphi^t(x)$。初值可微依赖定理给出',r'固定初值 $x$，令 $Z(t)=D\varphi^t(x)$。命题~\ref{prop:matrix-variation} 给出')
edit('arnold-contraction.tex',r'推论~\ref{cor:解对初值和参数的偏导方程}',r'命题~\ref{prop:matrix-variation}')
edit('qualitative-hamilton-volume.tex','最后一步使用 $H\in C^2$ 时混合偏导相等，故 Hamilton 流保持体积。','最后一步使用 $H\in C^2$ 时混合偏导相等，因而散度恒为零。')

p=root/'chapters/continuity-mode-stability.tex';s=p.read_text(encoding='utf-8');a=s.index(r'\begin{proof}');b=s.index(r'\end{proof}',a)
s=s[:a]+r'''\begin{proof}
第~\ref{sec:normal-modes}~节的正交换元把方程写成 $\ddot q_j=-a_jq_j$，其中 $a_j>0$。
令 $p_j=\dot q_j$，取能量
\[
 E(q,p)=\frac12\sum_j(p_j^2+a_jq_j^2).
\]
记 $a_{\min}=\min_ja_j>0,a_{\max}=\max_ja_j$，则
\[
 \tfrac12\min\{1,a_{\min}\}(|q|^2+|p|^2)
 \leq E(q,p)
 \leq\tfrac12\max\{1,a_{\max}\}(|q|^2+|p|^2).
\]
所以 $E$ 是状态 $(q,p)$ 的正定二次型。沿解求导，
\[
 \dot E=\sum_jp_j(\dot p_j+a_jq_j)=0.
\]
由定理~\ref{thm:Lyapunov稳定性判据} 的第一种情形，零解稳定。
另一方面，任何非零初值的能量都严格为正并保持不变；若相应解趋于零，则连续性使其能量趋于零，矛盾。
因此它不渐近稳定。正交换元及其逆均连续，结论也适用于原坐标。
''' +s[b:];p.write_text(s,encoding='utf-8')

# The original Hamilton argument follows conserved levels; fill the precise closed-orbit step in that route.
p=root/'chapters/chapter6.tex';s=p.read_text(encoding='utf-8')
old='上述系统的平衡点都在 $x$ 轴上，$(x_0,0)$ 为平衡点当且仅当 $x_0$ 为势能函数 $G(x)$ 的临界点。当 $x_0$ 为 $G(x)$ 的严格极大值点，即 $G\'\'(x_0)<0$ 时，$(x_0,0)$ 为系统的鞍点；当 $x_0$ 为 $G(x)$ 的严格极小值点，即 $G\'\'(x_0)>0$ 时，$(x_0,0)$ 为系统的中心。'
new=r'''上述系统的平衡点都在 $x$ 轴上，$(x_0,0)$ 为平衡点当且仅当 $G'(x_0)=0$。
若这一临界点非退化，则 $G''(x_0)<0$ 时 $(x_0,0)$ 为鞍点，$G''(x_0)>0$ 时为中心。
仅有“严格极值”而不附加非退化条件时，不能将它与二阶导数严格有符号写成等价条件。'''
assert s.count(old)==1;s=s.replace(old,new)
a=s.index('只要 $0<C<l$，曲线 $V(x,y)=C$')
b=s.index(r'\end{proof}',a)
s=s[:a]+r'''由 $G''(x_0)>0$ 及连续性，可将 $\delta$ 取得足够小，使
\[
 D^2V(x,y)=\operatorname{diag}(G''(x),1)
\]
在 $N_\delta$ 上处处正定。固定单位方向 $e$，令
$v_e(r)=V((x_0,0)+re)$。因为 $v_e(0)=v_e'(0)=0$ 且 $v_e''(r)>0$，
所以 $v_e$ 对 $0<r\leq\delta$ 严格增加。
对每个 $0<C<l$，介值定理及严格单调性给出唯一的 $r=r_C(e)\in(0,\delta)$，使 $v_e(r)=C$。
又有 $v_e'(r_C(e))>0$，故隐函数定理说明 $r_C$ 随方向光滑变化。
因此 $V=C$ 在此邻域中是一条围绕 $(x_0,0)$ 的光滑简单闭曲线，而不只是与每条径向线相交的集合。

在该曲线上 $\nabla V\ne0$，Hamilton 向量场为 $(V_y,-V_x)$，因而处处非零并与曲线相切。
紧性给出速度的正下界，而曲线弧长有限，所以解在有限时间内走完一周，确实形成周期轨道。
当 $C\downarrow0$ 时，这些互不相交的闭轨收缩到平衡点；它们覆盖一个去心邻域，故 $(x_0,0)$ 为中心。
''' +s[b:]
s=s.replace('如果势能函数 $G(x)$ 仅有孤立临界点，并且每个临界点都是严格极值点','如果势能函数 $G(x)$ 的临界点均非退化',1)
p.write_text(s,encoding='utf-8')

# Explicit preliminaries must be stated before, rather than after, their use.
p=root/'chapters/chapter13.tex';s=p.read_text(encoding='utf-8')
start=s.index('以上证明明确使用流形上的形式、积分与 Stokes 公式。')
end=s.index(r'\begin{proposition}',start)
pre=s[start:end]
s=s[:start]+s[end:]
pre=pre.replace('以上证明明确使用','下面的映射度证明使用',1)
anchor=r'\begin{theorem}[度数不依赖正则值]'
definition=r'''\begin{definition}[同伦与顶次形式]
两个映射 $f_0,f_1:M\to N$ 间的光滑同伦是光滑映射 $F:[0,1]\times M\to N$，满足 $F(0,x)=f_0(x)$、$F(1,x)=f_1(x)$。
在 $n$ 维定向坐标中，形如 $a(x)\,dx_1\wedge\cdots\wedge dx_n$ 的微分形式称为顶次形式；可写成 $d\beta$ 的形式称为恰当形式。
\end{definition}

'''
assert s.count(anchor)==1;s=s.replace(anchor,definition+pre+anchor);p.write_text(s,encoding='utf-8')
print('Filled: vector variation, original C1 increment proof, normal-mode energy proof, Hamilton level-set step, degree preliminaries.')
