from 扩写证明 import proof

proof('arnold-energy.tex', r'由前文的初值可微依赖', r'''
固定初值 $x$，令 $Z(t)=D\varphi^t(x)$。初值可微依赖定理给出
\[
 Z'(t)=Dv(\varphi^t(x))Z(t),\qquad Z(0)=I.
\]
这是系数连续的线性矩阵方程。应用线性 Liouville 公式，得到
\[
 J(t,x):=\det Z(t)
 =\exp\left(\int_0^t\operatorname{tr}Dv(\varphi^s(x))\,ds\right)>0.
\]
流的逆是反向时间流，故 $\varphi^t$ 在所考察区域上为微分同胚。
换元公式因而给出 $V(t)=\int_DJ(t,x)\,dx$，这里不必再对行列式取绝对值。
对上式求导，有
\[
 \partial_tJ(t,x)=\operatorname{div}v(\varphi^t(x))J(t,x).
\]
由于初值闭包和时间段紧，右端连续且一致有界，可在积分号下求导。因此
\begin{align*}
 V'(t)&=\int_D\operatorname{div}v(\varphi^t(x))J(t,x)\,dx\\
 &=\int_{D(t)}\operatorname{div}v(y)\,dy.
\end{align*}
若散度恒为零，则 $J=1$，从而每个这样的区域都保持体积。
对 Hamilton 场 $v=(H_p,-H_q)$，逐坐标计算得
\[
 \operatorname{div}v
 =\sum_i\left(\frac{\partial^2H}{\partial q_i\partial p_i}
 -\frac{\partial^2H}{\partial p_i\partial q_i}\right)=0.
\]
最后一步使用 $H\in C^2$ 时混合偏导相等，故 Hamilton 流保持体积。
''')

proof('arnold-energy.tex', r'令 $E=\frac12', r'''
把二阶方程写成状态变量 $(x,v)$ 的一阶方程
$\dot x_i=v_i,\ \dot v_i=-\partial_iU(x)/m_i$。其向量场为 $C^1$，
所以每个初值有唯一最大解。沿该解计算
\[
 \frac{d}{dt}\left(\frac12\sum_i m_iv_i^2+U(x)\right)
 =\sum_i v_i\bigl(m_i\dot v_i+\partial_iU(x)\bigr)=0.
\]
设常能量为 $E_0$，取 $C$ 使 $U(x)\geq-C$，再令 $m_*:=\min_i m_i>0$。
于是
\[
 \frac{m_*}{2}|v(t)|^2\leq\frac12\sum_i m_iv_i(t)^2
 =E_0-U(x(t))\leq E_0+C.
\]
因此存在与时间无关的 $M$，使 $|v(t)|\leq M$。
若最大正向存在端点 $\beta$ 有限，则对 $t_0\leq t<\beta$，
\[
 |x(t)|\leq |x(t_0)|+\int_{t_0}^t|v(s)|\,ds
 \leq |x(t_0)|+M(\beta-t_0).
\]
所以 $(x(t),v(t))$ 始终留在整个状态空间中的一个紧球内。
定理~\ref{thm:有限端点延拓判据} 说明解可越过 $\beta$ 延拓，与最大性矛盾。
负向时间同样有
$|x(t)|\leq|x(t_0)|+M|t-t_0|$，故负向端点也不可能有限。
两个方向的最大端点分别为 $+\infty$ 和 $-\infty$。
''')

proof('arnold-energy.tex', r'非临界性使有限端点', r'''
设 $(a,b)$ 是 $\{U<E\}$ 的一个有界连通分支。连续性给出
$U(a)=U(b)=E$；非临界假设又给出 $U'(a),U'(b)\ne0$。
由分支内部 $U<E$，必有 $U'(a)<0$、$U'(b)>0$。一阶展开于是给出
\[
 \lim_{x\downarrow a}\frac{E-U(x)}{x-a}=-U'(a)>0,
 \qquad
 \lim_{x\uparrow b}\frac{E-U(x)}{b-x}=U'(b)>0.
\]
故存在正常数 $c_1,c_2$，使靠近左端时
$c_1(x-a)\leq E-U(x)\leq c_2(x-a)$；右端有对应估计。
因为 $\int_0^\delta s^{-1/2}\,ds=2\sqrt\delta<\infty$，下式收敛：
\[
 \tau=\int_a^b\frac{dx}{\sqrt{2(E-U(x))}}.
\]
在上半支 $y=\sqrt{2(E-U(x))}$ 上，$\dot x=y>0$，分离变量说明
从 $a$ 到 $b$ 的时间正是 $\tau$。到达 $(b,0)$ 时，向量场为
$(0,-U'(b))$，竖直向下且非零；存在唯一性把解接到下半支。
下半支满足 $\dot x=-\sqrt{2(E-U(x))}$，在同样的时间 $\tau$ 内返回 $(a,0)$。
在 $(a,0)$ 处向量场竖直向上，解遂重复。第一次回到初始状态需要完整走过两支，
故其最小正周期为 $2\tau$。

再看曲线的光滑性。能量层上
$\nabla H=(U'(x),y)$ 不为零，隐函数定理表明它是一维光滑子流形。
在转向点附近可用 $y$ 为坐标，因此两条显式平方根分支虽然在 $x$ 坐标中
斜率无穷，接合后的曲线仍光滑。两支加两个端点构成一条简单闭曲线。

若分支只有一个有限端点，正负两支经此端点接合，构成一条非闭合的直线型曲线。
若分支是整个实轴，则 $y$ 始终不为零，两支分别构成两条直线型曲线。
每一支上的非零向量场使任意两个有限位置之间的行程时间有限，
所以这里所述每条连通曲线确是一条最大轨道的像。
这些分支穷尽全部非临界能量层，分类因而完整。
''')

proof('arnold-energy.tex', r'未扰动轨道与正', r'''
在半径 $A_0$ 附近取一个不含原点的小闭环带。未扰动解为
$(A\cos t,-A\sin t)$，在 $t=2\pi$ 横截正 $x$ 轴，因为此时
$\dot y=-A\ne0$。将横截条件写为 $y(t,A,\varepsilon)=0$，
在 $(2\pi,A_0,0)$ 对 $t$ 的导数非零。解的光滑依赖和隐函数定理给出光滑返回时间
$\tau(A,\varepsilon)$，且 $\tau(A,0)=2\pi$。
在该闭环带中角速度保持为负，故这一交点确是转过一周后的首次返回。
缩小参数邻域后，统一有
\[
 \tau(A,\varepsilon)=2\pi+O(\varepsilon),\qquad
 (x(t),y(t))=(A\cos t,-A\sin t)+O(\varepsilon)
\]
于所需的有界时间段内成立。

令 $B(x,y,\varepsilon)=xf(x,y,\varepsilon)+yg(x,y,\varepsilon)$。
沿解直接求导，线性项抵消，得到 $\dot E=\varepsilon B$。因此
\[
 \Delta E=\varepsilon\int_0^{\tau(A,\varepsilon)}B(x(t),y(t),\varepsilon)\,dt.
\]
被积函数在紧环带上有界且具有有界的一阶导数。改变轨道和参数使积分改变
$O(\varepsilon)$，将上限改为 $2\pi$ 又只改变 $O(\varepsilon)$；
乘外面的 $\varepsilon$ 后即得 $\Delta E=\varepsilon M(A)+O(\varepsilon^2)$。
同样估计可对 $A$ 求导，因而余项在 $C^1$ 意义下也成立。

为在 $\varepsilon=0$ 使用隐函数定理，定义
\[
 D(A,\varepsilon)=\int_0^1\partial_\varepsilon
 \Delta E(A,s\varepsilon)\,ds.
\]
微积分基本定理给出 $\Delta E=\varepsilon D$，且 $D(A,0)=M(A)$。
因 $\partial_AD(A_0,0)=M'(A_0)\ne0$，方程 $D=0$ 有唯一邻近解 $A(\varepsilon)$。
正 $x$ 轴上 $E=A^2/2$ 严格递增，故能量返回原值恰等价于返回同一点。
存在唯一性随即保证这条解为周期解；局部唯一性指横截面交点邻近 $A_0$ 的闭轨。

设半径返回映射为 $P_\varepsilon$。对
$[P_\varepsilon(A)^2-A^2]/2=\varepsilon D(A,\varepsilon)$ 求导，
再在 $P_\varepsilon(A)=A=A(\varepsilon)$ 处取值，得
\[
 P_\varepsilon'(A(\varepsilon))
 =1+\frac{\varepsilon}{A(\varepsilon)}\partial_AD(A(\varepsilon),\varepsilon)
 =1+\frac{\varepsilon M'(A_0)}{A_0}+O(\varepsilon^2).
\]
当 $\varepsilon M'(A_0)<0$ 且参数充分小时，该导数模小于 1，
横截面上的不动点渐近稳定，周期内部由流的连续依赖控制，故闭轨横向渐近稳定。
符号相反时导数大于 1，不动点及闭轨均横向不稳定。
''')

proof('chapter9.tex', r'解平移 $T$ 后', r'''
若 $x(t)=P_{t,s}\xi$，则 $z(t)=x(t+T)$ 满足
$z'=f(t+T,z)=f(t,z)$，且 $z(s)=x(s+T)$。
对在 $s+T$ 取初值 $\xi$ 的解作这一平移，由唯一性得到
$P_{t+T,s+T}\xi=P_{t,s}\xi$。再由演化复合关系，
\[
 P_{(n+1)T,0}=P_{(n+1)T,nT}P_{nT,0}=MP_{nT,0}.
\]
从 $P_{0,0}=I$ 归纳得 $P_{nT,0}=M^n$，继而
$P_{nT+s,0}=P_{nT+s,nT}M^n=P_{s,0}M^n$。
若 $M\xi=\xi$，解 $x(t+T)$ 与 $x(t)$ 在 $t=0$ 取同一初值，
唯一性使它们相同；反之，对周期解取 $t=0,T$ 即得不动点条件。

记不动点为 $\xi_*$，对应周期解 $x_*(s)=P_{s,0}\xi_*$。
连续稳定性蕴含离散稳定性，因为可取样 $t=nT$。
反向证明中，固定 $\epsilon>0$。映射 $(s,\xi)\mapsto P_{s,0}\xi$
在紧集 $[0,T]\times\{\xi_*\}$ 附近连续。用有限覆盖，存在 $\eta>0$，使
\[
 |\xi-\xi_*|<\eta\ \Longrightarrow\
 \sup_{0\leq s\leq T}|P_{s,0}\xi-P_{s,0}\xi_*|<\epsilon.
\]
离散稳定性给出 $\delta>0$，使 $|\xi-\xi_*|<\delta$ 时，对一切 $n\geq0$
均有 $|M^n\xi-\xi_*|<\eta$。将 $M^n\xi$ 代入上式，结合周期分解，
便控制了每一个 $t=nT+s$，从而得到连续稳定性。

若离散不动点还吸引附近初值，则 $M^n\xi\to\xi_*$。
对任意 $\epsilon>0$，充分大的所有 $n$ 均满足上述 $\eta$ 条件，
故整段 $[nT,(n+1)T]$ 上的解差均小于 $\epsilon$。
这证明连续吸引性。反向仍只需取样，因此两种渐近稳定性等价。
''')

proof('chapter9.tex', r'特征方程为', r'''
二维矩阵的特征多项式为
$p(\lambda)=\lambda^2-(\operatorname{tr}M)\lambda+1$。
先说明迭代稳定等价于 $\sup_{n\geq0}\|M^n\|<\infty$。
若该上界为 $C$，取 $|x_0|<\epsilon/(C+1)$ 即得稳定性。
反之，若零点稳定，对 $\epsilon=1$ 取稳定半径 $\delta$，
将任意单位向量乘以 $\delta/2$，便得 $\|M^n\|\leq2/\delta$。

当 $|\operatorname{tr}M|<2$，判别式为负，两根共轭，乘积为 1，故都在单位圆上。
写一根为 $e^{i\theta}$，$\sin\theta\ne0$。取复特征向量的实部与虚部为实基，
$M$ 的实矩阵为一个旋转矩阵，因而在此基下所有幂的范数均为 1。
换回原基仅引入固定常数，故稳定。

当 $|\operatorname{tr}M|>2$，两根实且互为倒数，并且至少一根 $\lambda$ 满足
$|\lambda|>1$。沿对应的实特征向量 $v$，有 $M^nv=\lambda^nv$，故不稳定。

最后设 $\operatorname{tr}M=2s$，其中 $s=1$ 或 $-1$。Cayley--Hamilton 公式给出
$(M-sI)^2=0$。若 $M=sI$，幂显然有界。否则写 $M=sI+N$，
$N\ne0,N^2=0$，则
\[
 M^n=s^nI+ns^{n-1}N.
\]
选 $v$ 使 $Nv\ne0$，反三角不等式给出
$|M^nv|\geq n|Nv|-|v|\to\infty$，故不稳定。这穷尽全部情形。
''')

proof('chapter9.tex', r'前文的参数连续依赖性', r'''
设 $A,\widetilde A$ 为两个同周期系数矩阵，$X(0)=\widetilde X(0)=I$。
固定 $B>\sup_{[0,T]}\|A(t)\|$，并限制扰动，使 $\|\widetilde A(t)\|\leq B$。
由积分方程和 Gronwall 不等式，$\|X(t)\|,\|\widetilde X(t)\|\leq e^{Bt}$。
设 $\eta=\sup_{[0,T]}\|A-\widetilde A\|$，作差得
\[
 \|X(t)-\widetilde X(t)\|
 \leq B\int_0^t\|X(s)-\widetilde X(s)\|\,ds
       +\eta\int_0^te^{Bs}\,ds.
\]
再次使用 Gronwall，或逐次代入积分不等式，得到
$\|X(t)-\widetilde X(t)\|\leq\eta t e^{Bt}$。特别地，
$\|M-\widetilde M\|\leq\eta T e^{BT}$，故单周期矩阵连续依赖系数。

令 $\gamma=2-|\operatorname{tr}M|>0$。迹是矩阵元的连续函数，
所以 $\eta$ 足够小时有
$|\operatorname{tr}\widetilde M-\operatorname{tr}M|<\gamma/2$，从而
$|\operatorname{tr}\widetilde M|<2$。
扰动仍在迹零的 Hamilton 系统类内，Liouville 公式保证
$\det\widetilde M=1$。迹判据说明每个这种邻近系统的离散迭代稳定，
再由连续与离散稳定性的等价性得到零解稳定，这正是强稳定的定义。
''')
