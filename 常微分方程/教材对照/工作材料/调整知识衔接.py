from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[2]
files={p.name:p.read_text(encoding='utf-8') for p in (root/'chapters').glob('*.tex')}
before=dict(files);changes=[]
def replace(file,old,new):
    assert files[file].count(old)==1,(file,old,files[file].count(old))
    files[file]=files[file].replace(old,new)
def insert(file,anchor,body):replace(file,anchor,body.strip()+'\n\n'+anchor)
def put(name,text):
    assert name not in files,name
    files[name]=text.strip()+'\n'
def split_sections(text):
    return [x for x in re.split(r'(?=\\section\{)',text) if x.strip()]
def heading(text,old,new,label):
    return text.replace(r'\section{'+old+'}',r'\subsection*{'+new+'}\n'+r'\phantomsection\label{'+label+'}',1)
def inp(name):return r'\input{chapters/'+name.replace('.tex','')+'}'

# 1. Modeling belongs before the questions that close the introduction; stability is deferred.
models=files['arnold-models.tex']
pos=models.index(r'\begin{proposition}[捕捞阈值]')
end=models.index(r'\begin{example}[球摆的小振动]')
harvest=models[pos:end]
models=models[:pos]+models[end:]
models=models.replace(r'\section{种群模型与相空间的直积}',r'\section{联合状态与种群模型}\label{sec:joint-models}',1)
models=models.replace('本节进一步研究种群模型。','前面的模型已经区分了线性、非线性与自治性。下面进一步说明怎样把独立过程组成一个系统，再记录含捕捞的种群方程。',1)
models=models.replace(r'\begin{definition}[连续 Logistic 模型]',r'\begin{definition}[连续 Logistic 模型]\label{def:continuous-logistic}',1)
models=models.replace('这里讨论的连续方程不同于第六章中的离散 Logistic 映射。',r'这些方程描述连续时间中的数量变化。它们的平衡点及长期行为将在第~\ref{chap:qualitative}~章按稳定性的定义研究，不能与离散 Logistic 映射的迭代混为一谈。',1)
models=models.replace(r'解的水平投影是椭圆、直线段或圆，因为'+'\n'+r'$(x,y)=a\cos\omega t+b\sin\omega t$，这是单位圆在线性映射下的像。',r'两个水平方向构成两个独立的二阶振动，体现了前面的直积构造。其通解及水平投影将在第~\ref{sec:normal-modes}~节利用常系数线性方程求出。',1)
files['arnold-models.tex']=models
replace('chapter1.tex',inp('arnold-models.tex'),'')
insert('chapter1.tex',r'\section{求解时的基本问题}',inp('arnold-models.tex'))
harvest=harvest.replace(r'\begin{proposition}[捕捞阈值]',r'\begin{proposition}[捕捞阈值]\label{prop:harvest-threshold}',1)
put('continuity-harvest.tex',r'''\subsection*{连续种群模型的平衡点}
对定义~\ref{def:continuous-logistic} 中的方程，现在可以使用 Lyapunov 稳定性与渐近稳定性的定义。
一维自治方程 $x'=f(x)$ 在相邻平衡点之间的符号决定运动方向；其右端在这里光滑，故解的唯一性由 Picard 定理保证。
'''+harvest)
changes.append('绪论保留建模、直积与球摆状态；捕捞阈值移至第6章稳定性定义之后。')

# 2. Green response immediately extends the already proved variation-of-constants formula.
replace('chapter3.tex',inp('arnold-green.tex'),'')
files['arnold-green.tex']=heading(files['arnold-green.tex'],'集中脉冲与影响函数','集中脉冲与影响函数','sec:green-response')
files['arnold-green.tex']=files['arnold-green.tex'].replace('常数变易公式不仅是计算通解的公式，也说明每个时刻的外部作用',r'定理~\ref{thm:常数变易公式} 已把非齐次解写成初值演化与外部作用的积分。下面从标量情形 $y\prime=a(t)y+f(t)$ 出发，说明每个时刻的外部作用'.replace(r'\prime',"'"),1)
insert('chapter3.tex',r'\section{高阶线性方程}',inp('arnold-green.tex'))
changes.append('Green响应接在第3章常数变易公式之后；保留原有线性存在唯一性依据。')

# 3. The operator argument follows the nonhomogeneous operator method; other linear applications stay at the end.
linear=split_sections(files['arnold-linear-algebra.tex']);assert len(linear)==3
groups,quasi,modes=linear
quasi=heading(quasi,'准多项式与平移不变函数空间','准多项式、平移不变性与共振','sec:quasipolynomials')
quasi=quasi.replace('前面重根解中出现的',r'定理~\ref{thm:重特征根的基本解组} 中出现的',1)
quasi=quasi.replace('平移关系 $T_{s+t}=T_sT_t$ 说明它是线性单参数群。','平移关系 $T_{s+t}=T_sT_t$ 保证平移在 $V$ 上可逆。',1)
put('linear-quasipolynomials.tex',quasi)
insert('chapter4.tex',r'\section{常系数线性方程组}',inp('linear-quasipolynomials.tex'))
groups=groups.replace(r'\section{线性相流、生成元与离散步进}',r'\section{矩阵指数、线性演化与离散步进}\label{sec:linear-evolution}',1)
groups=groups.replace('前文从方程得到矩阵指数，现在反过来从运动的群性质恢复方程。',r'定理~\ref{thm:常系数线性方程组的矩阵指数解} 和 Jordan 块的计算已经给出连续演化 $e^{tA}$。本节反过来从群性质恢复生成矩阵，并用 Euler 极限和矩阵幂联系连续、离散两种演化。',1)
groups=groups.replace('线性相流','线性演化')
groups=groups.replace('这也与本书已有 Liouville 公式一致。',r'这正是定理~\ref{thm:Wronski判别与Liouville公式} 在常系数情形下的体积结论；这里的计算给出它与 Euler 极限的直接联系。',1)
modes=modes.replace(r'\section{保守系统的主振动}',r'\section{保守系统的主振动}\label{sec:normal-modes}',1)
modes=modes.replace('若 $A>0$，则零平衡稳定但不渐近稳定。','',1)
energy_start=modes.index('若 $A>0$，守恒能量')
energy_end=modes.index(r'\end{proof}',energy_start)
mode_stability=modes[energy_start:energy_end]
modes=modes[:energy_start]+modes[energy_end:]
modes=modes.replace(r'\end{proof}'+'\n'+'二维位置轨迹',r'''\end{proof}
\begin{example}[球摆的水平投影]
第一章球摆的小振动在这里对应 $A=\omega^2I_2$，因此
\[
 (x(t),y(t))=a\cos\omega t+b\sin\omega t,\qquad a,b\in\R^2.
\]
右端是单位圆在一个线性映射下的像，故水平投影为椭圆、圆或退化的线段。
这是位置空间中的投影，完整状态仍由四个量 $(x,\dot x,y,\dot y)$ 组成。
\end{example}
正定势下的稳定性将在 Lyapunov 直接法中由能量严格证明，见命题~\ref{prop:normal-mode-stability}。

二维位置轨迹''',1)
files['arnold-linear-algebra.tex']=groups+'\n'+modes
put('continuity-mode-stability.tex',r'''\subsection*{主振动的能量与稳定性}
\begin{proposition}\label{prop:normal-mode-stability}
对第~\ref{sec:normal-modes}~节的系统 $\ddot x=-Ax$，若实对称矩阵 $A$ 正定，则零平衡稳定但不渐近稳定。
\end{proposition}
\begin{proof}
'''+mode_stability+r'''
\end{proof}
''')
changes.append('准多项式与共振接在第4章算子解法之后；矩阵指数的演化应用与主振动仍放章末；稳定性论证移至Lyapunov直接法。')

# 4. Banach interprets the original Picard proof; Euler residual follows the original Euler construction.
contraction=files['arnold-contraction.tex']
boundary=contraction.index(r'\begin{theorem}[由压缩映射得到局部逆]')
banach=contraction[:boundary];inverse=contraction[boundary:]
start=banach.index('对近似曲线 $u$，上一不动点误差界直接给出')
euler=banach[start:];banach=banach[:start]
banach=heading(banach,'压缩映射与基本定理的统一证明','Picard迭代的压缩映射解释','sec:picard-contraction')
banach=banach.replace('本章前面已经用逐次逼近证明存在唯一性和光滑依赖性。\n这里把逐次逼近放入一般的完备度量空间框架，并记录以后构造直化坐标所需的方法。','上述 Picard 证明利用阶乘估计控制全部迭代。缩小时间区间后，同一积分算子还可看作完备度量空间上的压缩映射；这一观点将在局部逆和不变流形的构造中再次使用。',1)
put('continuity-banach.tex',banach)
insert('chapter5.tex',r'\section{Peano 存在性定理}',inp('continuity-banach.tex'))
put('continuity-euler.tex',r'''\subsection*{唯一性条件下的Euler折线}
Peano 定理利用紧性从 Euler 折线中抽取收敛子列。若另有 Lipschitz 条件，则第~\ref{sec:picard-contraction}~节的残差估计还能控制整个近似序列。
'''+euler)
insert('chapter5.tex',r'\section{解的延拓}',inp('continuity-euler.tex'))
inverse=r'''\section{局部逆与沿解移动的坐标}\label{sec:inverse-moving-coordinates}
解的 $C^1$、$C^r$ 依赖性已经由逐次逼近和变分方程证明。下面把这一分析工具与坐标变换联系起来：先构造局部逆，再沿已知解消去常数项和线性项。
局部逆的证明只使用第~\ref{sec:picard-contraction}~节的压缩映射定理，不依赖后面的直化定理。
'''+inverse
inverse=inverse.replace(r'\begin{theorem}[由压缩映射得到局部逆]',r'\begin{theorem}[由压缩映射得到局部逆]\label{thm:local-inverse}',1)
files['arnold-contraction.tex']=inverse
changes.append('第5章压缩映射观点紧接Picard证明，Euler残差接在Peano构造后；局部逆与移动坐标保留章末。')

# 5. Distribute the qualitative extensions according to the concepts used by their proofs.
div,energy,lv,perturb,orbital=split_sections(files['arnold-energy.tex'])
ham_start=div.index('对 Hamilton 场')
ham_end=div.index(r'\end{proof}',ham_start)
ham_proof=div[ham_start:ham_end]
div=div[:ham_start]+div[ham_end:]
div=heading(div,'散度与相流的体积变化','相流的体积变化','sec:nonlinear-volume')
div=div.replace('将线性 Liouville 公式应用于非线性流的变分方程，可以得到体积变化的表达式。',r'流的群性质给出点的运动；由推论~\ref{cor:解对初值和参数的偏导方程}，初值的微小变化满足线性变分方程。将定理~\ref{thm:Wronski判别与Liouville公式} 应用于该方程，就能计算相流的体积变化。',1)
div=div.replace(r'\begin{theorem}[非线性 Liouville 公式]',r'\begin{theorem}[非线性 Liouville 公式]\label{thm:nonlinear-liouville}',1)
div=div.replace('散度为零时相流保持体积；$C^2$ Hamilton 系统的相流保持体积。','散度为零时，相流保持体积。',1)
put('qualitative-volume.tex',div)
insert('chapter6.tex',r'\section{Lyapunov 稳定性}',inp('qualitative-volume.tex'))
insert('chapter6.tex',r'\section{Lyapunov 直接法}',inp('continuity-harvest.tex'))
insert('chapter6.tex',r'\section{平面平衡点分析}',inp('continuity-mode-stability.tex'))
start=energy.index(r'\begin{theorem}[能量与全局延拓]')
end=energy.index(r'\begin{definition}',start)
global_energy=energy[start:end]
energy=energy[:start]+energy[end:]
global_energy=global_energy.replace(r'\begin{theorem}[能量与全局延拓]',r'\begin{theorem}[能量与全局延拓]\label{thm:energy-global-extension}',1)
put('continuity-energy-extension.tex',r'''\subsection*{用能量控制有限时间内的状态}
第二章保守系统中的机械能也可用于延拓。这里不要求势能控制位置趋于无穷的行为：势能有下界即可先控制速度，再控制有限时间内的位置。
'''+global_energy)
insert('chapter5.tex',r'\section{微分不等式与比较定理}',inp('continuity-energy-extension.tex'))
energy=heading(energy,'能量层的轨道分解与振动周期','能量层的轨道分解与振动周期','sec:energy-levels')
energy=energy.replace('前面的能量相图给出轨道所在的集合，但一整条能量等值集不一定是同一条轨道。',r'定理~\ref{thm:Hamilton函数沿轨道守恒} 说明轨道包含在能量层中；平衡点分类给出了临界点附近的形状。下面进一步区分能量层的各条轨道，并由沿轨道的速度计算周期。全局延拓的能量估计已见定理~\ref{thm:energy-global-extension}。',1)
energy=energy.replace(r'\begin{theorem}[非临界能量层]',r'\begin{theorem}[非临界能量层]\label{thm:regular-energy-level}',1)
lv=heading(lv,'Lotka--Volterra 系统的闭轨与平均值','Lotka--Volterra系统的闭轨与平均值','sec:lv-energy')
lv=lv.replace('把绪论中的参数重新记为正数 $a,b,c,d$，考虑',r'回到绪论中的捕食者--食饵模型。虽然原坐标中的方程不直接具有标准 Hamilton 形式，仍可沿用“首次积分—紧等值线—周期运动”的论证。把参数记为正数 $a,b,c,d$，考虑',1)
files['arnold-energy.tex']=energy+'\n'+lv
put('qualitative-hamilton-volume.tex',r'''\begin{corollary}[Hamilton相流保持体积]\label{cor:hamilton-volume}
若 Hamilton 函数 $H$ 属于 $C^2$，则 Hamilton 相流保持相空间体积。
\end{corollary}
\begin{proof}
'''+ham_proof+r'''
再应用定理~\ref{thm:nonlinear-liouville} 即得结论。
\end{proof}
''')
insert('chapter6.tex','上述定理表明，在无阻尼的机械振动系统中',inp('qualitative-hamilton-volume.tex'))
orbital=heading(orbital,'轨道吸引与按时间参数的稳定','轨道吸引与按时间参数的稳定','sec:orbital-versus-time')
orbital=orbital.replace(r'\begin{definition}',r'前面的 Lyapunov 稳定性比较同一时刻的两个状态；极限环的稳定性则比较轨道与整个闭曲线的距离。为避免把两者混用，作如下区分。'+'\n'+r'\begin{definition}',1)
put('qualitative-orbital-stability.tex',orbital)
insert('chapter6.tex','平衡点和闭轨都可以成为轨道的极限状态。',inp('qualitative-orbital-stability.tex'))
perturb=heading(perturb,'保守振动的小扰动与自激振动','返回映射与保守振动的小扰动','sec:perturbed-oscillation')
perturb=perturb.replace('先考虑归一化的圆形振动及其扰动',r"Poincar\'e 映射已把闭轨化为不动点，下面的一周能量增量将直接给出该不动点方程。所用的稳定性判据是命题~\ref{prop:discrete-derivative-test}，返回时刻的构造使用第五章的可微依赖性与隐函数定理。考虑归一化的圆形振动及其扰动",1)
perturb=perturb.replace('结合前文一维不动点导数判据',r'结合命题~\ref{prop:discrete-derivative-test}',1)
put('qualitative-return-perturbation.tex',perturb)
insert('chapter6.tex',r'\paragraph{例 6.8}',inp('qualitative-return-perturbation.tex')+'\n\n'+r'\subsection*{一般区间映射的周期行为}'+'\n'+'下面回到一般区间映射。它们未必来自微分方程的返回映射，其周期结构可以比局部闭轨附近的情形复杂得多。')
changes.append('第6章按流、稳定性、返回映射、Hamilton能量的顺序安置体积公式、捕捞、主振动稳定性、小扰动闭轨与能量层；不是统一移出章末。')

# Stable labels for concepts reused across the reorganized text.
replace('chapter6.tex',r'\chapter{定性理论初步}',r'\chapter{定性理论初步}\label{chap:qualitative}')
criterion_start=files['chapter6.tex'].index('对于一维区间上的连续映射')
criterion_end=files['chapter6.tex'].index(inp('qualitative-return-perturbation.tex'),criterion_start)
criterion=files['chapter6.tex'][criterion_start:criterion_end].strip()
replace('chapter6.tex',criterion,r'''\begin{proposition}[一维周期点的导数判据]\label{prop:discrete-derivative-test}
'''+criterion+r'''
\end{proposition}
\begin{proof}
令 $g=f^p$，则 $g(x_0)=x_0$。若 $|g'(x_0)|<1$，取 $|g'(x_0)|<q<1$。
由导数的定义，充分靠近 $x_0$ 时，
\[
 |g(x)-x_0|\leq q|x-x_0|.
\]
这个小邻域被 $g$ 映入自身，归纳得到 $|g^n(x)-x_0|\leq q^n|x-x_0|$，故每隔 $p$ 步的迭代稳定且趋于 $x_0$。
再对有限多个连续映射 $f^j$（$0\leq j<p$）使用连续性，就同时控制了周期内其余各步，得到周期轨道的稳定性与吸引性。

若 $|g'(x_0)|>1$，取 $1<q<|g'(x_0)|$。同样由导数的定义，在某个固定小邻域内有
\[
 |g(x)-x_0|\geq q|x-x_0|.
\]
任一非零初始偏差若始终留在该邻域，就会在迭代后至少增大为原来的 $q^n$ 倍，产生矛盾。
因此无论初始偏差多小，均有一次迭代离开这个固定邻域，故周期点不稳定。
\end{proof}
''')

# 6. Tangent spaces precede their use in nonlinear characteristic surfaces.
old11,old12=files['chapter11.tex'],files['chapter12.tex']
files['chapter11.tex']=old12.replace('Chapter12封面图.jpg','Chapter11封面图.jpg',1)
files['chapter12.tex']=old11.replace('Chapter11封面图.jpg','Chapter12封面图.jpg',1)
replace('chapter11.tex',r'\chapter{流形上的微分方程}',r'\chapter{流形上的微分方程}\label{chap:manifolds}')
replace('chapter12.tex',r'\chapter{特征线、偏微分方程与接触结构}',r'\chapter{特征线、偏微分方程与接触结构}\label{chap:characteristics}')
replace('chapter8.tex',r'\chapter{Sturm 零点理论与边值问题}',r'\chapter{Sturm 零点理论与边值问题}\label{chap:sturm}')
replace('chapter9.tex',r'\chapter{周期系统、单周期映射与振动}',r'\chapter{周期系统、单周期映射与振动}\label{chap:periodic}')
replace('chapter10.tex',r'\chapter{线性系统的共轭分类与环面运动}',r'\chapter{线性系统的共轭分类与环面运动}\label{chap:linear-conjugacy}')
replace('chapter13.tex',r'\chapter{向量场的指标、映射度与 Euler 特征数}',r'\chapter{向量场的指标、映射度与 Euler 特征数}\label{chap:indices}')
replace('chapter14.tex',r'\chapter{几何方法的应用与若干进阶问题}',r'\chapter{几何方法的应用与若干进阶问题}\label{chap:applications}')
replace('chapter15.tex',r'\chapter{不变流形与进阶专题}',r'\chapter{不变流形与进阶专题}\label{chap:invariant-manifolds}')
insert('chapter7.tex',r'\section{微分同胚与向量场的变换}',r'第六章已由唯一性建立流的群性质。本章用第五章的可微依赖性和定理~\ref{thm:local-inverse} 研究换坐标后的向量场；先限于 Euclidean 开集上的局部问题，随后再推广到流形。')
insert('chapter7.tex',r'\begin{definition}'+'\n'+'通过 $x_0$ 的超曲面',r'在本章的 Euclidean 情形，光滑超曲面可局部写成秩为 $n-1$ 的参数化 $\sigma(z)$；其切空间就是 $D\sigma(z)$ 的像。这里不需要先使用抽象流形理论。')
insert('chapter8.tex',r'\section{零点与相位角}',r'第三章已由 Wronski 行列式说明两个解是否独立，第五章又给出解对参数的可微依赖性。现在将这两个结果用于二阶方程：先数零点，再通过参数改变研究边值问题。相位角沿用第六章相平面分析的几何思想。')
insert('chapter9.tex',r'\section{单周期映射}',r"第六章的 Poincar\'e 映射在每次经过横截面时取样。本章对周期含时方程每隔一个固定周期取样，并利用第三章的标准解矩阵与第六章的稳定性定义，把连续时间问题化为矩阵或映射的迭代。")
insert('chapter10.tex',r'\section{三种等价关系}',r'第四章和第六章已经按 Jordan 结构计算并分类线性解，第~\ref{chap:arnold-geometry}~章又说明坐标变换如何改变向量场。本章进一步区分允许的变换类别：线性或可微变换保留较多代数信息，同胚变换则允许更粗的相图分类。')
insert('chapter11.tex',r'\section{坐标图与微分结构}',r'第~\ref{chap:arnold-geometry}~章中的坐标变换发生在 Euclidean 开集之间；环面运动又表明，一个相空间未必能由单张 Euclidean 坐标图覆盖。本章先建立换图、切空间和切丛，再把已有局部方程拼接为流形上的相流。')
insert('chapter12.tex',r'\section{线性方程的特征线与 Cauchy 问题}',r'第二章用全微分与首次积分求解平面方程，第~\ref{chap:arnold-geometry}~章给出非奇点附近的独立首次积分，而第~\ref{chap:manifolds}~章已定义切空间与子流形。本章据此研究向量场与初始曲面的横截性，并把隐式方程中的关系 $dy=p\,dx$ 表示为接触条件。')
insert('chapter13.tex',r'\section{曲线指标及形变不变性}',r'第六章已经用结点、鞍点和闭轨描述局部相图。本章先用平面绕数给这些图形赋予指标，再利用第~\ref{chap:manifolds}~章的流形与定向概念讨论全局限制；涉及积分形式时采用第~\ref{chap:characteristics}~章的微分形式记号。')
insert('chapter14.tex',r'\section{中心力与相邻轨道的相对运动}',r'本章的力学与光学例子分别使用常系数线性化、首次积分与 Hamilton 方程；广义种群系统还会同时用到第六章的 Dulac 判据和第~\ref{chap:indices}~章的指标。最后的扩散模型以已存在的光滑解为分析前提，不把其存在理论归入常微分方程基本定理。')
insert('chapter15.tex',r'\section{双曲映射的稳定与不稳定流形}',r'第六章的线性近似给出稳定性判据，第~\ref{chap:linear-conjugacy}~章则分类双曲线性系统。下面用压缩映射构造非线性不变流形及局部共轭；后两节分别回到第~\ref{chap:sturm}~章的零点问题和第~\ref{chap:characteristics}~章的隐式方程几何。')
changes.append('新增章节仅交换流形章与特征线章，使切空间、子流形先于其在特征初值问题中的使用；其余章序保留并补出实质性衔接。')

# All mutations are committed only after every exact anchor has matched.
old_labels=set(re.findall(r'\\label\{([^}]+)\}','\n'.join(before.values())))
new_labels=re.findall(r'\\label\{([^}]+)\}','\n'.join(files.values()))
assert old_labels<=set(new_labels),old_labels-set(new_labels)
assert len(new_labels)==len(set(new_labels)),[x for x in new_labels if new_labels.count(x)>1]
for name,text in files.items():
    for env in ('proof','theorem','definition','proposition','corollary','lemma','align*','aligned','center','minipage'):
        assert text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),(name,env)
for name,text in files.items():
    if before.get(name)!=text:(root/'chapters'/name).write_text(text.strip()+'\n',encoding='utf-8')
report={'changes':changes,'new_modules':[name for name in files if name not in before],'changed_sources':[name for name in before if files[name]!=before[name]],'retained_old_labels':len(old_labels),'new_labels':len(new_labels)-len(old_labels)}
(root/'教材对照/工作材料/知识衔接调整记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
