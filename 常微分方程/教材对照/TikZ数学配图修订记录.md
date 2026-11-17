# TikZ数学配图修订记录

2026-10-29新增17幅数学配图，全部以TikZ源码绘制，插入相应论述附近。每图使用 `center` 排版，图题采用 `captionof`，标签紧随图题；正文均有交叉引用。

覆盖集中脉冲与Green响应、能量层、Lotka--Volterra闭轨、返回映射、向量场直化、实吹起、Sturm零点、单周期乘子、环面运动、特征线交叉、jet投影尖点、立体投影、奇点指标、相对椭圆轨道、光学测地线、稳定流形及Gibbs密度。

原章节封面图片继续保留。新增数学图均为矢量路径，未以位图代替TikZ。

配图已单独编译检查，并核对曲线、向量方向、关键恒等式和归一化条件。最终整本PDF共245页；行宽溢出警告0处，无未定义引用、重复标签或缺字警告。

| 图号 | 内容 | 位置 | 源码 |
| --- | --- | --- | --- |
| 7.1 | 流盒坐标将弯曲的积分曲线化为平行直线；横截面上的标号保持不变。 | PDF第167页 | [flowbox.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/flowbox.tex>) |
| 7.2 | 半三次抛物线的实吹起：严格变换在 $(x,v)$ 图中成为光滑曲线。 | PDF第169页 | [blowup-cusp.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/blowup-cusp.tex>) |
| 6.19 | 势阱与闭合能量层：以 $U(x)=x^2/2$、$E=1$ 为例。 | PDF第159页 | [energy-level.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/energy-level.tex>) |
| 6.20 | 参数 $a=b=c=d=1$ 时的 Lotka--Volterra 闭轨；各曲线为首次积分的等值线。 | PDF第161页 | [lv-levels.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/lv-levels.tex>) |
| 6.16 | 返回映射的吸引不动点与吸引闭轨：模型 $\dot r=0.12r(1-r^2)$、$\dot\theta=-1$。 | PDF第153页 | [return-map.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/return-map.tex>) |
| 8.1 | 同一方程的独立解零点交错；右图中每经过一个零点，相位穿过一个 $k\pi$。 | PDF第177页 | [sturm-separation.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/sturm-separation.tex>) |
| 9.1 | 二维保面积单周期矩阵的迹判据：稳定区间为 $|\operatorname{tr}M|<2$。 | PDF第185页 | [monodromy-trace.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/monodromy-trace.tex>) |
| 10.1 | 将环面沿经纬线展开为正方形；同向箭头标明需粘合的对边，右图只画有限轨道段。 | PDF第194页 | [torus-flow.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/torus-flow.tex>) |
| 12.1 | 初始速度 $g(\xi)=-\xi$ 的特征线在 $(t,x)=(1,0)$ 汇合；虚线表示交叉后的形式延长。 | PDF第208页 | [burgers-characteristics.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/burgers-characteristics.tex>) |
| 12.2 | 隐式方程 $p^2=t$ 的两支与积分曲线投影：$t=p^2$、$x=2p^3/3$。 | PDF第210页 | [jet-cusp.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/jet-cusp.tex>) |
| 11.1 | 立体投影的二维截面：从北极 $N$ 出发的直线将球面点 $P$ 映到平面点 $q$。 | PDF第199页 | [stereographic.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/stereographic.tex>) |
| 13.1 | 结点与鞍点的指标。虚圆是计算指标的边界，箭头表示边界各点的场向量。 | PDF第219页 | [node-saddle-index.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/node-saddle-index.tex>) |
| 14.1 | 初始径向速度为 $v>0$ 的线性相对轨道：椭圆中心在 $(0,-2v)$，并非空间站位置。 | PDF第227页 | [hill-ellipse.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/hill-ellipse.tex>) |
| 14.2 | 折射率 $n(y)=1/y$ 时的射线：与边界正交的半圆及竖直直线。 | PDF第229页 | [optical-geodesics.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/optical-geodesics.tex>) |
| 15.1 | 局部稳定、不稳定流形及其线性模型；粗线箭头分别趋向和离开平衡点。 | PDF第239页 | [stable-manifolds.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/stable-manifolds.tex>) |
| 3.1 | 左：单位面积光滑集中脉冲。右：$a=-0.7$ 时推迟影响函数在扰动时刻产生单位跳跃。 | PDF第52页 | [pulse-green.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/pulse-green.tex>) |
| 14.3 | 同一周期势的归一化 Gibbs 稳态；扩散变小时，质量更集中于唯一势阱 $x=0$。 | PDF第233页 | [gibbs-concentration.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/gibbs-concentration.tex>) |

[更新后的笔记](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/main.pdf>) · [17幅图独立预览](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/教材对照/TikZ数学配图预览.pdf>) · [正文排版抽查](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/教材对照/TikZ正文排版抽查.jpg>)

本轮备份：[代数重复内容删减前-20261030-074256.zip](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程备份/代数重复内容删减前-20261030-074256.zip>)。
