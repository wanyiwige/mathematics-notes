from 扩写证明 import proof

proof('chapter10.tex', r'在几乎特征基中令', r'''
令 $\gamma=\min_j\operatorname{Re}\lambda_j>0$。
在几乎特征基中，严格上三角元都可取为绝对值不超过 $\eta$。
设 $Q(z)=\sum_j|z_j|^2$，沿 $z'=Az$ 有
\[
 \dot Q=2\sum_j\operatorname{Re}\lambda_j|z_j|^2
 +2\operatorname{Re}\sum_{i<j}a_{ij}z_j\overline z_i.
\]
利用 $2|z_i||z_j|\leq|z_i|^2+|z_j|^2$，交叉项绝对值满足
\[
 \left|2\operatorname{Re}\sum_{i<j}a_{ij}z_j\overline z_i\right|
 \leq\eta\sum_{i<j}(|z_i|^2+|z_j|^2)
 =\eta(n-1)Q(z).
\]
故取 $\eta(n-1)<\gamma$ 即有 $\dot Q\geq\gamma Q$（$n=1$ 时无交叉项）。
上界同理由有限个矩阵元得到，例如
$\dot Q\leq[2\max_j\operatorname{Re}\lambda_j+\eta(n-1)]Q$。

虽然构造使用了复基，原实空间在复化后仍是一个实线性子空间，且在实矩阵 $A$ 下不变。
将 $Q$ 限制在该子空间，再用原来的实坐标表示，就得到实正定二次型。
上述沿流导数不等式在限制后仍成立。
若上界常数与下界相同，可将下界减半、上界增大，取得所需 $0<c<C$。
''')

proof('chapter10.tex', r'先考虑全部实部为正', r'''
先设全部特征值实部为正，取 Lyapunov 二次型 $Q$，令 $S=\{Q=1\}$。
对非零 $x$ 记 $q(t)=Q(e^{tA}x)>0$。导数估计给出
$c\leq (\log q)'\leq C$。因此对 $t\geq0$，
\[
 e^{ct}Q(x)\leq Q(e^{tA}x)\leq e^{Ct}Q(x),
\]
对 $t\leq0$ 则有 $e^{Ct}Q(x)\leq Q(e^{tA}x)\leq e^{ct}Q(x)$。
所以 $q$ 严格递增，负向趋零、正向趋无穷。介值定理和严格单调性说明
每条非零轨道恰经过 $S$ 一次，且每个非零点唯一写成 $x=e^{tA}\xi$，$\xi\in S$。

以此表示定义 $h(e^{tA}\xi)=e^t\xi$，并置 $h(0)=0$。
因为每条从零点出发的射线也恰交 $S$ 一次，$e^t\xi$ 同样唯一表示任意非零点，
故 $h$ 是双射。确定时间的方程为 $Q(e^{-tA}x)=1$，其对 $t$ 的导数
为 $-L_{Ax}Q(e^{-tA}x)<0$。隐函数定理保证 $t=t(x)$ 在非零点光滑，
$\xi=e^{-t(x)A}x$ 亦然；逆映射由射线坐标给出，也在非零点连续。

还须检查零点。若 $x=e^{tA}\xi\to0$，则 $Q(x)\to0$，最终 $t<0$。
上面的估计给出 $e^{Ct}\leq Q(x)$，故
$t\leq C^{-1}\log Q(x)\to-\infty$。
椭球 $S$ 紧，因而 $h(x)=e^t\xi\to0$。
反之，若 $y=e^t\xi\to0$，$S$ 上的 Euclidean 长度有正常数下界，故 $t\to-\infty$；
再由 $Q(e^{tA}\xi)\leq e^{ct}$ 得 $h^{-1}(y)\to0$。
因此 $h$ 在全空间为同胚。最后直接计算
\[
 h(e^{sA}e^{tA}\xi)=e^{t+s}\xi=e^sh(e^{tA}\xi),
\]
故它把原系统保时间地共轭到 $y'=y$。

对负实部部分反向时间，得到与 $u'=-u$ 的共轭。
一般双曲系统分解为稳定与不稳定两个不变子空间，在各部分应用上述构造，
再取两个同胚的直积，得到标准系统 $u'=-u,v'=v$。
两个系统的稳定维数相同且总维数相同，便有同一个标准系统，充分性得证。

反过来，设存在共轭。双曲矩阵可逆，所以两系统的唯一平衡点均为零，共轭必固定零。
由连续性，$e^{tA}x\to0$ 蕴含 $e^{tB}h(x)\to0$；应用逆共轭得反向蕴含。
对于双曲线性系统，趋零点集恰为稳定子空间：不稳定分量只要非零，正向就不能趋零。
于是共轭将 $E_A^s$ 同胚到 $E_B^s$。由拓扑维数不变性
（Euclidean 空间 $\R^p,\R^q$ 同胚必有 $p=q$），两稳定维数相同。
''')

proof('chapter11.tex', r'局部取 $\Sigma=\{x_n=0\}$', r'''
先用光滑底空间坐标把初始超曲面写成 $\Sigma=\{x_n=0\}$。
记其参数为 $z=(x_1,\ldots,x_{n-1})$，初值为 $g(z)$。
条件 $p|_{T\Sigma}=dg$ 确定 $p_i=g_{z_i}$（$i<n$）。
横截条件为 $F_{p_n}\ne0$，因此在已经选择的初始 $p_n$ 分支附近，
方程 $F(z,0,D_zg,p_n,g)=0$ 由隐函数定理唯一解出光滑 $p_n(z)$。
这里的唯一性均针对这一初始 jet 分支。

从初始 jet 参数化 $j(z)$ 出发，记特征流为 $\Phi^s$，并写
\[
 J(s,z)=\Phi^s(j(z))=(x(s,z),p(s,z),U(s,z)).
\]
在 $s=0$，$x_{z_i}$ 是初始超曲面的切向基，而 $x_s=F_p$ 横截该超曲面，
故 $(s,z)\mapsto x(s,z)$ 的 Jacobian 可逆。缩小邻域后，可将扫出的曲面
写成 $x\mapsto(x,p(x),U(x))$。还须证明 $p=DU$，这一步不由投影可逆自动得到。

首先 $\alpha(X)=0$，初始曲面上也有 $j^*\alpha=0$。
对 $\alpha=dU-\sum_ip_i\,dx_i$，坐标计算给出
\[
 \mathcal L_X\alpha=dF-F_u\alpha.
\]
由前一定理 $F(J(s,z))=0$，故 $J^*dF=0$。
设 $a_i(s,z)=\alpha(J_{z_i}(s,z))$，对 $s$ 求导便得
\[
 \partial_sa_i=-F_u(J(s,z))a_i,\qquad a_i(0,z)=0.
\]
这一齐次标量方程只有零解，所以 $\alpha$ 在所有 $J_{z_i}$ 上为零；
在 $J_s=X$ 上也为零。这些向量张成扫出曲面的切空间，因此 $J^*\alpha=0$。
改用 $x$ 参数后即为 $dU=\sum_ip_i\,dx_i$，也就是 $p=DU$。
再代入沿流保持的 $F=0$，得到所求 PDE 解及初始条件。

若另一局部解具有相同初值和所选初始 jet 分支，则其 1-图包含 $j(z)$。
前一定理说明该图由特征线组成，ODE 唯一性使其包含同样的 $J(s,z)$。
投影局部可逆，所以两个解在共同邻域相同，局部唯一性得证。
''')

proof('chapter13.tex', r'选一个非零点 $N$', r'''
若场不恒为零，可选一个非零点 $N$ 作北极；恒零场不符合只有孤立零点的假设。
零点集是紧球面上的闭集。由于每个零点孤立，紧性保证零点总数有限。
以南图坐标 $z$ 表示 $S^2\setminus\{N\}$，将所有零点包含在充分大的圆盘中。
平面指标和定理把所求总和化为大圆 $z=Re^{i\theta}$ 上向量分量的绕数。

在北极附近取另一坐标 $w=g(z)=z/|z|^2$，两图过渡反转平面定向。
记场在南、北图中的复数分量分别为 $u(z),v(w)$，则 $v(g(z))=Dg(z)u(z)$。
若 $z=Re^{i\theta}$，直接对反演求导，得到
\[
 Dg(z)\zeta=-R^{-2}e^{2i\theta}\overline\zeta,
 \qquad
 v(g(z))=-R^{-2}e^{2i\theta}\overline{u(z)}.
\]
这里复数共轭正是反射，正因子 $R^{-2}$ 不影响方向。
北图中 $N$ 附近场无零点，故其在小圆盘上的归一化方向连续延伸到盘内，
边界绕数为零。无论选择小圆的哪一方向，这个绕数都仍为零。
沿 $\theta:0\to2\pi$ 对上式取方向角增量，得到
\[
 0=2-\operatorname{wind}_{|z|=R}u.
\]
其中 $e^{2i\theta}$ 贡献两圈，复共轭使 $u$ 的绕数变号，负号只增加常角 $\pi$。
因此南图大圆上场的绕数为 2，也就是全部零点指标之和。
这一计算同时处理了过渡图的定向反转，避免仅由基向量转两圈直接判断符号。
''')

proof('chapter14.tex', r'稳态要求 $J$ 常数', r'''
稳态方程为 $(b\rho-\varepsilon\rho')'=0$，故概率流为常数 $J$，即
$\varepsilon\rho'+U'\rho=-J$。积分因子给出
\[
 (e^{U/\varepsilon}\rho)'=-\frac{J}{\varepsilon}e^{U/\varepsilon}.
\]
令 $I(x)=\int_x^{x+L}e^{U(s)/\varepsilon}\,ds>0$。因 $U(x+L)=U(x)+c$，有
\[
 I'(x)=e^{U(x+L)/\varepsilon}-e^{U(x)/\varepsilon}
 =(e^{c/\varepsilon}-1)e^{U(x)/\varepsilon}.
\]
所以 $\rho=C_\varepsilon e^{-U/\varepsilon}I$ 满足
$\varepsilon\rho'+U'\rho=\varepsilon C_\varepsilon(e^{c/\varepsilon}-1)$，确为常流稳态。
又 $I(x+L)=e^{c/\varepsilon}I(x)$，与前面的指数因子抵消，故 $\rho$ 周期。
其严格正性保证可选唯一正数 $C_\varepsilon$ 使总积分为 1。

证明唯一性时，先设 $c\ne0$。将积分因子等式在 $[x,x+L]$ 上积分，
对任意周期稳态均得
\[
 (e^{c/\varepsilon}-1)e^{U(x)/\varepsilon}\rho(x)
 =-\frac{J}{\varepsilon}I(x).
\]
故所有周期稳态都为上述正函数的常数倍，再由归一化唯一确定。
若 $c=0$，同一等式给出 $JI(x)=0$，所以 $J=0$。
积分因子方程随即给出 $\rho=C e^{-U/\varepsilon}$，归一化后也唯一。
此时 $e^{U/\varepsilon}$ 周期，窗口积分 $I(x)$ 与 $x$ 无关，
故一般公式正好化为 Gibbs 型表达式。
''')

proof('chapter14.tex', r'令 $w=u/\rho$', r'''
固定 $\varepsilon>0$，令 $w=u/\rho$。将 $u=\rho w$ 代入密度方程，
利用 $(\varepsilon\rho'-b\rho)'=0$ 和 $J=b\rho-\varepsilon\rho'$，整理得
\[
 \rho w_t=\varepsilon(\rho w_x)_x-Jw_x.
\]
记 $\mathcal E(t)=\int_0^L\rho(w-1)^2\,dx$。由于 $\rho$ 不依赖时间，
乘 $w-1$ 并积分，周期边界项消失，有
\begin{align*}
 \tfrac12\mathcal E'(t)
 &=-\varepsilon\int_0^L\rho w_x^2\,dx
   -J\int_0^L(w-1)w_x\,dx\\
 &=-\varepsilon\int_0^L\rho w_x^2\,dx.
\end{align*}
最后一个积分为 $\tfrac12[(w-1)^2]_0^L=0$；因此即使稳态流不为零，耗散恒等式仍成立。

归一化给出 $\int_0^L\rho(w-1)\,dx=0$。因 $\rho>0$ 且 $w$ 连续，
若 $w$ 不恒等于 1，必在某点 $x_0$ 取值 1。
沿圆周长度不超过 $L$ 的一条弧，从该点积分并用 Cauchy--Schwarz，得到
\[
 |w(x)-1|^2\leq L\int_0^L|w_x|^2\,dx
 \leq\frac{L}{m}\int_0^L\rho w_x^2\,dx,
 \qquad m=\min_{[0,L]}\rho>0.
\]
再乘 $\rho$ 积分，并用 $\int\rho=1$，得
$\mathcal E\leq(L/m)\int\rho w_x^2$。当 $w\equiv1$ 时此式也成立。
因此 $\mathcal E'\leq-(2\varepsilon m/L)\mathcal E$，积分得到
\[
 \mathcal E(t)\leq\mathcal E(0)e^{-2\varepsilon mt/L}.
\]
这就是所述加权平方平均意义下的指数吸引性。
它还蕴含 $L^1$ 收敛，因为
$\int_0^L|u-\rho|\,dx\leq(\int\rho)^{1/2}\mathcal E^{1/2}=\mathcal E^{1/2}$。
本证明针对已经存在的光滑周期解；抛物方程的存在理论是另一个分析前提。
''')
