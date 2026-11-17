from pathlib import Path
import math,json
import numpy as np
root=Path(__file__).resolve().parents[2]
folder=root/'figure/tikz';folder.mkdir(exist_ok=True)
figures=[];checks={}
def add(name,chapter,anchor,caption,intro,body):
    figures.append(dict(name=name,chapter=chapter,anchor=anchor,caption=caption,intro=intro,body=body.strip()))

add('flowbox','chapter7.tex',r'\section{对称群与齐次性}',
    r'流盒坐标将弯曲的积分曲线化为平行直线；横截面上的标号保持不变。',
    r'图~\ref{fig:ode-tikz-flowbox} 用 $F(s,z)=(s,z+s^2/5)$ 示意直化坐标：曲线的弯曲来自坐标，而运动时间仍由 $s$ 表示。',r'''
\begin{tikzpicture}[>=Stealth,font=\small]
\begin{scope}[x=1.05cm,y=.9cm]
 \draw[->,gray] (-2.1,-1.3)--(2.2,-1.3) node[right]{$x_1$};
 \draw[->,gray] (-2.1,-1.3)--(-2.1,2.1) node[above]{$x_2$};
 \draw[GoldMain,thick] (0,-1.2)--(0,1.8) node[above]{$\Sigma$};
 \foreach \z in {-.7,0,.7}{
  \draw[GreenMain,thick,domain=-1.8:1.8,samples=45] plot (\x,{\z+\x*\x/5});
  \draw[GreenMain,->,thick] (.55,{\z+.55*.55/5})--(.85,{\z+.85*.85/5});
  \fill[GoldMain] (0,\z) circle(1.6pt);
 }
 \node at (0,-1.9){原坐标};
\end{scope}
\draw[->,thick] (2.6,.45)--(4.1,.45) node[midway,above]{$F^{-1}$};
\begin{scope}[shift={(6.5,0)},x=1.05cm,y=.9cm]
 \draw[->,gray] (-1.8,-1.3)--(2,-1.3) node[right]{$s$};
 \draw[->,gray] (-1.8,-1.3)--(-1.8,2.1) node[above]{$z$};
 \draw[GoldMain,thick] (0,-1.2)--(0,1.8) node[above]{$s=0$};
 \foreach \z in {-.7,0,.7}{
  \draw[GreenMain,thick,->] (-1.5,\z)--(1.65,\z);
  \fill[GoldMain] (0,\z) circle(1.6pt);
 }
 \node at (.1,-1.9){$\dot s=1,\quad\dot z=0$};
\end{scope}
\end{tikzpicture}
''')

add('blowup-cusp','chapter7.tex',r'\section{相似性与时间尺度}',
    r'半三次抛物线的实吹起：严格变换在 $(x,v)$ 图中成为光滑曲线。',
    r'图~\ref{fig:ode-tikz-blowup-cusp} 对比压回前后的曲线；右图的虚线 $x=0$ 是这一坐标图中的例外纤维。',r'''
\begin{tikzpicture}[>=Stealth,font=\small]
\begin{scope}[x=1.5cm,y=1.1cm]
 \draw[->,gray] (-.35,0)--(2,0) node[right]{$x$};
 \draw[->,gray] (0,-1.9)--(0,1.9) node[above]{$y$};
 \draw[GreenMain,thick,domain=-1.18:1.18,samples=90] plot ({\x*\x},{\x*\x*\x});
 \fill (0,0) circle(1.5pt) node[below left]{$0$};
 \node at (1,-2.35){$y^2=x^3$};
\end{scope}
\draw[<-,thick] (3.6,0)--(5,0) node[midway,above]{$\pi$};
\begin{scope}[shift={(6,0)},x=1.5cm,y=1.1cm]
 \draw[->,gray] (-.35,0)--(2,0) node[right]{$x$};
 \draw[->,GoldMain,dashed] (0,-1.9)--(0,1.9) node[above]{$v$};
 \draw[GreenMain,thick,domain=-1.35:1.35,samples=70] plot ({\x*\x},\x);
 \draw[->,GreenMain,thick] (0,-.18)--(0,.22);
 \node[GoldMain,anchor=east] at (-.08,1.2){$x=0$};
 \fill (0,0) circle(1.5pt);
 \node at (1,-2.35){$x=v^2,\quad y=v^3$};
\end{scope}
\end{tikzpicture}
''')

add('energy-level','arnold-energy.tex',r'\begin{proposition}[数学摆的周期]',
    r'势阱与闭合能量层：以 $U(x)=x^2/2$、$E=1$ 为例。',
    r'图~\ref{fig:ode-tikz-energy-level} 将转向点与相平面中的上下两支对应起来；箭头表示真实的时间方向。',r'''
\begin{tikzpicture}[>=Stealth,font=\small]
\begin{scope}[x=1.2cm,y=1.45cm]
 \draw[->,gray] (-2,0)--(2.2,0) node[right]{$x$};
 \draw[->,gray] (0,-.18)--(0,2) node[above]{$U$};
 \draw[GreenMain,thick,domain=-1.8:1.8,samples=60] plot (\x,{\x*\x/2});
 \draw[GoldMain,thick] (-1.95,1)--(1.95,1) node[right]{$E$};
 \foreach \a/\lab in {-1.4142/a,1.4142/b}{
  \draw[dashed,gray] (\a,0)--(\a,1);
  \fill[GoldMain] (\a,1) circle(1.5pt);
  \node[below] at (\a,0){$\lab$};
 }
 \node at (0,-.55){允许位置：$a\leq x\leq b$};
\end{scope}
\begin{scope}[shift={(7,1.15)},scale=1.05]
 \draw[->,gray] (-1.85,0)--(1.95,0) node[right]{$x$};
 \draw[->,gray] (0,-1.8)--(0,1.9) node[above]{$y$};
 \draw[GreenMain,thick] (0,0) circle(1.4142);
 \draw[->,GreenMain,thick] (105:1.4142) arc[start angle=105,end angle=75,radius=1.4142];
 \draw[->,GreenMain,thick] (285:1.4142) arc[start angle=285,end angle=255,radius=1.4142];
 \fill[GoldMain] (-1.4142,0) circle(1.6pt) node[below left]{$(a,0)$};
 \fill[GoldMain] (1.4142,0) circle(1.6pt) node[below right]{$(b,0)$};
 \node at (0,-2.1){$y^2/2+U(x)=E$};
\end{scope}
\end{tikzpicture}
''')

# Exact level sets of H=x-log(x)+y-log(y), found along rays from (1,1).
lv=[];residual=0.
for energy in (2.08,2.30,2.65):
    pts=[]
    for theta in np.linspace(0,2*math.pi,181):
        u,v=math.cos(theta),math.sin(theta)
        limit=min([-1/u if u<0 else float('inf'),-1/v if v<0 else float('inf')])
        lo=0.;hi=min(4.,limit*(1-1e-10))
        def fun(r):
            x,y=1+r*u,1+r*v
            return x-math.log(x)+y-math.log(y)
        while fun(hi)<energy:hi*=2
        for _ in range(70):
            mid=(lo+hi)/2
            if fun(mid)<energy:lo=mid
            else:hi=mid
        r=(lo+hi)/2;x,y=1+r*u,1+r*v
        residual=max(residual,abs(fun(r)-energy));pts.append((x,y))
    lv.append((energy,pts))
checks['LV_level_residual']=residual
coords=lambda pts:' '.join(f'({x:.5f},{y:.5f})' for x,y in pts)
lvbody=r'''
\begin{tikzpicture}[>=Stealth,font=\small,x=1.8cm,y=1.55cm]
 \draw[->,gray] (0,0)--(3,0) node[right]{$x$};
 \draw[->,gray] (0,0)--(0,3) node[above]{$y$};
 \draw[dashed,GoldMain] (1,0)--(1,2.85);
 \draw[dashed,GoldMain] (0,1)--(2.85,1);
'''
for E,pts in lv:
    lvbody+=r'\draw[GreenMain,thick] plot coordinates {'+coords(pts)+r'};'+'\n'
    # Clockwise orientation is opposite the increasing polar parameter.
    for j in (25,85,145):
        x,y=pts[j];vx,vy=x*(y-1),y*(1-x);norm=math.hypot(vx,vy)
        lvbody+=f'\\draw[->,GreenMain,thick] ({x:.5f},{y:.5f})--({x+.13*vx/norm:.5f},{y+.13*vy/norm:.5f});\n'
lvbody+=r'''
 \fill[GoldMain] (1,1) circle(1.8pt) node[above right]{$(1,1)$};
 \node[below] at (1,0){$1$};\node[left] at (0,1){$1$};
 \node[anchor=west] at (3.2,2.25){$H=x-\log x+y-\log y$};
 \node[anchor=west] at (3.2,1.65){$H=2.08,\ 2.30,\ 2.65$};
 \node[anchor=west] at (3.2,1.05){箭头沿系统运动方向};
\end{tikzpicture}
'''
add('lv-levels','arnold-energy.tex',r'\section{保守振动的小扰动与自激振动}',
    r'参数 $a=b=c=d=1$ 时的 Lotka--Volterra 闭轨；各曲线为首次积分的等值线。',
    r'图~\ref{fig:ode-tikz-lv-levels} 中闭轨围绕唯一极小点，各坐标的周期平均值均为 1。',lvbody)

add('return-map','arnold-energy.tex',r'\section{轨道吸引与按时间参数的稳定}',
    r'返回映射的吸引不动点与吸引闭轨：模型 $\dot r=0.12r(1-r^2)$、$\dot\theta=-1$。',
    r'图~\ref{fig:ode-tikz-return-map} 示意横截面上的半径如何逐次趋近闭轨；这对应返回映射在不动点处的压缩。',r'''
\begin{tikzpicture}[>=Stealth,font=\small]
\begin{scope}[scale=1.25]
 \draw[gray,->] (-1.9,0)--(2.1,0) node[right]{$\Sigma$};
 \draw[GreenMain,thick] (0,0) circle(1);
 \draw[GoldMain,thick,domain=0:14,samples=200,variable=\t]
  plot ({cos(\t r)/sqrt(1+(1/2.89-1)*exp(-.24*\t))},{-sin(\t r)/sqrt(1+(1/2.89-1)*exp(-.24*\t))});
 \draw[->,GreenMain,thick] (135:1) arc[start angle=135,end angle=105,radius=1];
 \fill[GoldMain] (1.7,0) circle(1.7pt) node[above]{$A$};
 \fill[GoldMain] ({1/sqrt(1+(1/2.89-1)*exp(-.24*2*pi))},0) circle(1.7pt) node[below right]{$P(A)$};
 \node[GreenMain] at (-.9,-1.2){$\Gamma$};
\end{scope}
\begin{scope}[shift={(7,-1.6)},scale=1.5]
 \draw[->,gray] (0,0)--(2,0) node[right]{$A$};
 \draw[->,gray] (0,0)--(0,2) node[above]{$P(A)$};
 \draw[gray,dashed] (.25,.25)--(1.8,1.8) node[above right]{$P=A$};
 \draw[GreenMain,thick,domain=.3:1.8,samples=70] plot (\x,{1/sqrt(1+(1/(\x*\x)-1)*exp(-.24*2*pi))});
 \draw[GoldMain,dashed] (1,0)--(1,1)--(0,1);
 \fill[GoldMain] (1,1) circle(1.7pt);
 \node[below] at (1,0){$1$};\node[left] at (0,1){$1$};
\end{scope}
\end{tikzpicture}
''')

add('sturm-separation','chapter8.tex',r'\section{比较定理与零点间距}',
    r'同一方程的独立解零点交错；右图中每经过一个零点，相位穿过一个 $k\pi$。',
    r'图~\ref{fig:ode-tikz-sturm-separation} 取 $x_1=\sin t,x_2=\cos t$；右图使用本章的相位约定 $(x,y)=\rho(\sin\theta,\cos\theta)$。',r'''
\begin{tikzpicture}[>=Stealth,font=\small]
\begin{scope}[x=.8cm,y=1.15cm]
 \draw[->,gray] (-.25,0)--(6.95,0) node[right]{$t$};
 \draw[->,gray] (0,-1.4)--(0,1.5) node[above]{$x$};
 \draw[GreenMain,thick,domain=0:6.2832,samples=100] plot (\x,{sin(\x r)});
 \draw[GoldMain,thick,domain=0:6.2832,samples=100] plot (\x,{cos(\x r)});
 \foreach \t/\lab in {0/0,1.5708/\pi/2,3.1416/\pi,4.7124/3\pi/2,6.2832/2\pi}{
  \draw (\t,.05)--(\t,-.05);\node[below,font=\scriptsize] at (\t,-.1){$\lab$};
 }
 \foreach \t in {0,3.1416,6.2832}{\fill[GreenMain] (\t,0) circle(2pt);}
 \foreach \t in {1.5708,4.7124}{\fill[GoldMain] (\t,0) circle(2pt);}
 \node[GreenMain] at (2,1.45){$\sin t$};\node[GoldMain] at (4.4,1.45){$\cos t$};
\end{scope}
\begin{scope}[shift={(8,0)},scale=1.15]
 \draw[->,gray] (-1.4,0)--(1.5,0) node[right]{$x$};
 \draw[->,gray] (0,-1.4)--(0,1.5) node[above]{$y=x'$};
 \draw[GreenMain,thick] (0,0) circle(1);
 \draw[GreenMain,->,thick] (70:1) arc[start angle=70,end angle=25,radius=1];
 \draw[GoldMain,->] (90:.48) arc[start angle=90,end angle=40,radius=.48];
 \node[GoldMain] at (.28,.65){$\theta$};
 \fill (0,1) circle(1.6pt) node[above left]{$\theta=0$};
 \fill (0,-1) circle(1.6pt) node[below left]{$\theta=\pi$};
\end{scope}
\end{tikzpicture}
''')

add('monodromy-trace','chapter9.tex',r'\section{参数共振与振动稳定}',
    r'二维保面积单周期矩阵的迹判据：稳定区间为 $|\operatorname{tr}M|<2$。',
    r'图~\ref{fig:ode-tikz-monodromy-trace} 展示乘子随迹所处区间的三种位置；边界 $\pm2$ 仍须检查 Jordan 块。',r'''
\begin{tikzpicture}[>=Stealth,font=\small]
 \draw[->,gray] (-5,0)--(5.2,0) node[right]{$\operatorname{tr}M$};
 \draw[GreenMain,line width=2pt] (-1.8,0)--(1.8,0);
 \foreach \x/\lab in {-1.8/-2,1.8/2}{\draw (\x,.1)--(\x,-.1);\node[below]at(\x,-.1){$\lab$};}
 \node[GreenMain] at (0,.45){稳定};
 \node[GoldMain] at (-3.5,.45){不稳定};\node[GoldMain] at (3.5,.45){不稳定};
 \foreach \shift in {-3.5,0,3.5}{
  \begin{scope}[shift={(\shift,2)}]
   \draw[gray,dashed] (0,0) circle(.75);\draw[gray] (-1.35,0)--(1.35,0);
  \end{scope}
 }
 \fill[GoldMain] (-4.65,2) circle(2pt);\fill[GoldMain] (-3.99,2) circle(2pt);
 \fill[GreenMain] ({.75*cos(55)},{2+.75*sin(55)}) circle(2pt);
 \fill[GreenMain] ({.75*cos(55)},{2-.75*sin(55)}) circle(2pt);
 \fill[GoldMain] (4.65,2) circle(2pt);\fill[GoldMain] (3.99,2) circle(2pt);
 \node at (-3.5,3.1){负实互逆乘子};\node at (0,3.1){共轭单位乘子};\node at (3.5,3.1){正实互逆乘子};
\end{tikzpicture}
''')

def wrapped_path(alpha,T):
    events=sorted(set([0.,T]+[float(i) for i in range(1,math.ceil(T))]+[i/alpha for i in range(1,math.ceil(alpha*T)) if i/alpha<T]))
    out=[]
    for a,b in zip(events,events[1:]):
        mid=(a+b)/2;ix=math.floor(mid);iy=math.floor(alpha*mid)
        out.append(((a-ix,alpha*a-iy),(b-ix,alpha*b-iy)))
    return out
torus=r'\begin{tikzpicture}[>=Stealth,font=\small]'+'\n'
for shift,alpha,T,title in ((0,.5,2,r'$\omega_2/\omega_1=1/2$'),(6.5,math.sqrt(2),7.5,r'$\omega_2/\omega_1=\sqrt2$')):
    torus+=f'\\begin{{scope}}[shift={{({shift},0)}},scale=3.3]\n'
    torus+=r'''
 \fill[GreenPale,opacity=.25] (0,0) rectangle(1,1);
 \draw[gray] (0,0) rectangle(1,1);
 \draw[->,gray] (0,0)--(1.15,0) node[right]{$\theta_1$};
 \draw[->,gray] (0,0)--(0,1.15) node[above]{$\theta_2$};
 \node[below left] at (0,0){$0$};\node[below] at (1,0){$2\pi$};\node[left] at (0,1){$2\pi$};
 \draw[GoldMain,->,thick] (.4,0)--(.6,0);\draw[GoldMain,->,thick] (.4,1)--(.6,1);
 \draw[GoldMain,->,thick] (0,.4)--(0,.6);\draw[GoldMain,->,thick] (1,.4)--(1,.6);
'''
    for p,q in wrapped_path(alpha,T):
        torus+=f'\\draw[GreenMain,thick] ({p[0]:.6f},{p[1]:.6f})--({q[0]:.6f},{q[1]:.6f});\n'
    torus+=f'\\node at (.5,-.27){{{title}}};\n\\end{{scope}}\n'
torus+=r'\end{tikzpicture}'
add('torus-flow','chapter10.tex',r'\section{均匀分布与高维推广}',
    r'将环面沿经纬线展开为正方形；同向箭头标明需粘合的对边，右图只画有限轨道段。',
    r'图~\ref{fig:ode-tikz-torus-flow} 中，轨道从一条边离开后从对边继续。有理斜率给出闭轨，无理斜率的完整轨道稠密。',torus)

add('burgers-characteristics','chapter11.tex',r'\section{隐式常微分方程的 1-jet 几何}',
    r'初始速度 $g(\xi)=-\xi$ 的特征线在 $(t,x)=(1,0)$ 汇合；虚线表示交叉后的形式延长。',
    r'图~\ref{fig:ode-tikz-burgers-characteristics} 用线性初值展示投影退化：$x=\xi(1-t)$，在 $t=1$ 无法由 $x$ 唯一反解初始标号。',r'''
\begin{tikzpicture}[>=Stealth,font=\small,x=1.55cm,y=2.5cm]
 \draw[->,gray] (-2.25,0)--(2.3,0) node[right]{$x$};
 \draw[->,gray] (0,-.1)--(0,1.6) node[above]{$t$};
 \draw[GoldMain,dashed] (-2,1)--(2,1) node[right]{$t=1$};
 \foreach \xi in {-2,-1,-.5,.5,1,2}{
  \draw[GreenMain,thick] (\xi,0)--(0,1);
  \draw[GreenMain,dashed] (0,1)--({-.45*\xi},1.45);
  \draw[GreenMain,->,thick] ({.6*\xi},.4)--({.45*\xi},.55);
 }
 \fill[GoldMain] (0,1) circle(2pt);
 \node[fill=white,inner sep=2pt,anchor=east] at (-.25,1.45){投影退化};
 \node[below] at (-2,0){$\xi=-2$};\node[below] at (2,0){$\xi=2$};
\end{tikzpicture}
''')

add('jet-cusp','chapter11.tex',r'\section{一般非线性方程的特征系统}',
    r'隐式方程 $p^2=t$ 的两支与积分曲线投影：$t=p^2$、$x=2p^3/3$。',
    r'图~\ref{fig:ode-tikz-jet-cusp} 取积分常数 $C=0$，用同一参数 $p$ 将斜率分支与半三次尖点对应起来。',r'''
\begin{tikzpicture}[>=Stealth,font=\small]
\begin{scope}[x=1.55cm,y=1.15cm]
 \draw[->,gray] (-.2,0)--(2.1,0) node[right]{$t$};
 \draw[->,gray] (0,-1.55)--(0,1.6) node[above]{$p$};
 \draw[GreenMain,thick,domain=0:1.3,samples=55] plot ({\x*\x},\x);
 \draw[GoldMain,thick,domain=-1.3:0,samples=55] plot ({\x*\x},\x);
 \node[GreenMain] at (1,1.5){$p=\sqrt t$};\node[GoldMain] at (1,-1.5){$p=-\sqrt t$};
\end{scope}
\draw[->,thick] (3.8,0)--(5,0) node[midway,above]{$\pi$};
\begin{scope}[shift={(6,0)},x=1.55cm,y=1.15cm]
 \draw[->,gray] (-.2,0)--(2.1,0) node[right]{$t$};
 \draw[->,gray] (0,-1.7)--(0,1.8) node[above]{$x$};
 \draw[GreenMain,thick,domain=0:1.3,samples=55] plot ({\x*\x},{2*\x*\x*\x/3});
 \draw[GoldMain,thick,domain=-1.3:0,samples=55] plot ({\x*\x},{2*\x*\x*\x/3});
 \fill (0,0) circle(1.6pt);
 \node at (1,-2.05){$x^2=4t^3/9$};
\end{scope}
\end{tikzpicture}
''')

add('stereographic','chapter12.tex',r'\section{光滑映射、子流形与例子}',
    r'立体投影的二维截面：从北极 $N$ 出发的直线将球面点 $P$ 映到平面点 $q$。',
    r'图~\ref{fig:ode-tikz-stereographic} 画出球面的一张坐标图；北极自身不在这张图的定义域内。',r'''
\begin{tikzpicture}[>=Stealth,font=\small,scale=2.15]
 \fill[GreenPale,opacity=.3] (0,0) circle(1);
 \draw[GreenMain,thick] (0,0) circle(1);
 \draw[->,gray] (-1.45,0)--(2.55,0) node[right]{投影平面};
 \draw[gray,dashed] (0,-1.15)--(0,1.25);
 \draw[GoldMain,thick] (0,1)--(2,0);
 \draw[GoldMain,->,thick] (.95,.525)--(1.35,.325);
 \fill (0,1) circle(1pt) node[above left]{$N$};
 \fill[GreenMain] (.8,.6) circle(1pt) node[above right]{$P$};
 \fill[GoldMain] (2,0) circle(1pt) node[below]{$q$};
 \node[below left] at (0,0){$0$};
\end{tikzpicture}
''')

indexbody=r'\begin{tikzpicture}[>=Stealth,font=\small]'+'\n'
for shift,saddle in ((0,False),(6,True)):
    indexbody+=f'\\begin{{scope}}[shift={{({shift},0)}},scale=1.25]\n'
    indexbody+=r'\draw[gray,dashed] (0,0) circle(1);\fill (0,0) circle(1.5pt);'+'\n'
    for theta in range(0,360,30):
        x,y=math.cos(math.radians(theta)),math.sin(math.radians(theta));vx=x;vy=-y if saddle else y
        indexbody+=f'\\draw[->,GreenMain,thick] ({x:.5f},{y:.5f})--({x+.32*vx:.5f},{y+.32*vy:.5f});\n'
    title=r'$v=(x,-y),\quad\operatorname{ind}=-1$' if saddle else r'$v=(x,y),\quad\operatorname{ind}=+1$'
    indexbody+=f'\\node at (0,-1.85){{{title}}};\n\\end{{scope}}\n'
indexbody+=r'\end{tikzpicture}'
add('node-saddle-index','chapter13.tex',r'\section{指标的应用}',
    r'结点与鞍点的指标。虚圆是计算指标的边界，箭头表示边界各点的场向量。',
    r'图~\ref{fig:ode-tikz-node-saddle-index} 中，沿虚圆正向走一周，左图的向量方向正转一周，右图反转一周。',indexbody)

add('hill-ellipse','chapter14.tex',r'\section{分层介质中的光线与 Clairaut 守恒量}',
    r'初始径向速度为 $v>0$ 的线性相对轨道：椭圆中心在 $(0,-2v)$，并非空间站位置。',
    r'图~\ref{fig:ode-tikz-hill-ellipse} 取 $v=1$，标出空间站所在的相对原点及相对轨道的中心。',r'''
\begin{tikzpicture}[>=Stealth,font=\small,x=1.25cm,y=.85cm]
 \draw[->,gray] (-1.8,0)--(2.1,0) node[right]{$x$（径向）};
 \draw[->,gray] (0,-4.6)--(0,.8) node[above]{$y$（切向）};
 \draw[GreenMain,thick,domain=0:360,samples=100,variable=\t] plot ({sin(\t)},{2*(cos(\t)-1)});
 \draw[GreenMain,->,thick,domain=30:50,samples=12,variable=\t] plot ({sin(\t)},{2*(cos(\t)-1)});
 \draw[GreenMain,->,thick,domain=210:230,samples=12,variable=\t] plot ({sin(\t)},{2*(cos(\t)-1)});
 \draw[GoldMain,dashed] (-1,-2)--(1,-2);
 \fill[GoldMain] (0,-2) circle(1.7pt) node[above left]{$(0,-2)$};
 \fill (0,0) circle(1.7pt) node[above left]{空间站};
 \node at (3.1,-1.5){$x=\sin t$};\node at (3.1,-2.3){$y=2(\cos t-1)$};
\end{tikzpicture}
''')

add('optical-geodesics','chapter14.tex',r'\section{一维二重零点的光滑正规形}',
    r'折射率 $n(y)=1/y$ 时的射线：与边界正交的半圆及竖直直线。',
    r'图~\ref{fig:ode-tikz-optical-geodesics} 中只画上半平面 $y>0$ 内的曲线，边界 $y=0$ 不属于该介质模型。',r'''
\begin{tikzpicture}[>=Stealth,font=\small,x=1.1cm,y=1.1cm]
 \fill[GreenPale,opacity=.3] (-4,0) rectangle(4,2.9);
 \draw[gray,dashed] (-4,0)--(4,0) node[right]{$y=0$};
 \draw[->,gray] (-3.7,0)--(-3.7,3.1) node[above]{$y$};
 \draw[GreenMain,thick] (1,0) arc[start angle=0,end angle=180,radius=2];
 \draw[GoldMain,thick] (2.7,0) arc[start angle=0,end angle=180,radius=1.4];
 \draw[GreenMain,thick] (3.3,.08)--(3.3,2.75);
 \node at (0,2.6){$n(y)=1/y,\quad y>0$};
 \node[below] at (-1,0){$x_0$};\node[below] at (1.3,0){$x_1$};
\end{tikzpicture}
''')

stable=r'''
\begin{tikzpicture}[>=Stealth,font=\small]
\begin{scope}[scale=1.5]
 \draw[->,gray] (-1.7,0)--(1.8,0) node[right]{$u$};
 \draw[->,gray] (0,-1.6)--(0,1.8) node[above]{$v$};
'''
for k in (-.65,-.3,.3,.65):
    for sign in (-1,1):
        smin=abs(k)/1.25;smax=1.25
        pts=[]
        for s in np.linspace(smin,smax,55):
            s*=sign;r=k/s;pts.append((s+.18*r*r,r+.18*s*s))
        stable+=r'\draw[gray!65,thin] plot coordinates {'+coords(pts)+'};\n'
stable+=r'''
 \draw[GreenMain,very thick,domain=-1.45:1.45,samples=60] plot (\x,{.18*\x*\x});
 \draw[GoldMain,very thick,domain=-1.45:1.45,samples=60] plot ({.18*\x*\x},\x);
 \foreach \s/\t in {-.95/-.72,.95/.72}{\draw[GreenMain,->,very thick] (\s,{.18*\s*\s})--(\t,{.18*\t*\t});}
 \foreach \s/\t in {-.65/-.9,.65/.9}{\draw[GoldMain,->,very thick] ({.18*\s*\s},\s)--({.18*\t*\t},\t);}
 \node[GreenMain,below] at (-1.1,.2){$W^s$};\node[GoldMain,right] at (.28,1.3){$W^u$};
 \fill (0,0) circle(1.3pt);
\end{scope}
\draw[->,thick] (3,0)--(4.2,0) node[midway,above]{$h$};
\begin{scope}[shift={(6.5,0)},scale=1.4]
 \draw[->,GreenMain,thick] (-1.5,0)--(-.3,0);\draw[->,GreenMain,thick] (1.5,0)--(.3,0);
 \draw[->,GoldMain,thick] (0,.2)--(0,1.6);\draw[->,GoldMain,thick] (0,-.2)--(0,-1.6);
 \node[GreenMain,below] at (1.2,0){$E^s$};\node[GoldMain,right] at (0,1.3){$E^u$};
 \fill (0,0) circle(1.3pt);
 \node at (0,-2){$\dot s=-s,\quad\dot r=r$};
\end{scope}
\end{tikzpicture}
'''
add('stable-manifolds','chapter15.tex',r'\section{非线性双曲平衡点的局部共轭}',
    r'局部稳定、不稳定流形及其线性模型；粗线箭头分别趋向和离开平衡点。',
    r'图~\ref{fig:ode-tikz-stable-manifolds} 的曲线由局部换元 $(u,v)=(s+0.18r^2,r+0.18s^2)$ 得到，故两条不变曲线在原点的切线分别是稳定与不稳定子空间。',stable)
checks['stable_chart_min_jacobian']=1-.36**2*1.45**2

# A compact C-infinity bump, normalized once; dilations have area one.
u=np.linspace(-.999999,.999999,20001);bumps=np.exp(1-1/(1-u*u));C=float(np.trapz(bumps,u))
green=rf'''
\begin{{tikzpicture}}[>=Stealth,font=\small]
\begin{{scope}}[x=1.1cm,y=1cm]
 \draw[->,gray] (0,0)--(4,0) node[right]{{$t$}};
 \draw[->,gray] (.2,0)--(.2,3.2) node[above]{{$h_N(t-\xi)$}};
 \draw[gray,dashed] (2,0)--(2,3);
'''
for width,color in ((1.,'GreenMain'),(.5,'GoldMain'),(.3,'GreenDark')):
    a,b=2-width*.999,2+width*.999
    green+=f'\\draw[{color},thick,domain={a:.5f}:{b:.5f},samples=90] plot (\\x,{{exp(1-1/(1-((\\x-2)/{width})^2))/({width}*{C:.8f})}});\n'
green+=r'''
 \node[below] at (2,0){$\xi$};\node at (2,-.6){支集缩小，面积保持为 1};
\end{scope}
\begin{scope}[shift={(6.5,0)},x=1.1cm,y=1.8cm]
 \draw[->,gray] (0,0)--(4.4,0) node[right]{$t$};
 \draw[->,gray] (0,0)--(0,1.7) node[above]{$G(t,\xi)$};
 \draw[GreenMain,thick] (0,0)--(1,0);
 \draw[GreenMain,thick,domain=1:4,samples=65] plot (\x,{exp(-.7*(\x-1))});
 \draw[GoldMain,dashed] (1,0)--(1,1);
 \draw[fill=white,GreenMain] (1,0) circle(1.8pt);\draw[fill=white,GreenMain] (1,1) circle(1.8pt);
 \node[below] at (1,0){$\xi$};\node[left] at (0,1){$1$};
 \node at (2,-.34){$a(t)=-0.7$};
\end{scope}
\end{tikzpicture}
'''
add('pulse-green','arnold-green.tex',None,
    r'左：单位面积光滑集中脉冲。右：$a=-0.7$ 时推迟影响函数在扰动时刻产生单位跳跃。',
    r'图~\ref{fig:ode-tikz-pulse-green} 将光滑脉冲的集中过程与极限响应分开表示；空心点不指定 $t=\xi$ 处的单点取值。',green)

rho=r'\begin{tikzpicture}[>=Stealth,font=\small,x=1.3cm,y=1.6cm]'+'\n'
rho+=r'''
 \draw[->,gray] (-3.5,0)--(3.65,0) node[right]{$x$};
 \draw[->,gray] (0,0)--(0,1.35) node[above]{$\rho_\varepsilon$};
'''
for eps,color in ((.8,'GoldMain'),(.2,'GreenMain')):
    grid=np.linspace(-math.pi,math.pi,20001);Z=float(np.trapz(np.exp(-(1-np.cos(grid))/eps),grid))
    checks[f'gibbs_Z_{eps}']=Z
    rho+=f'\\draw[{color},thick,domain=-3.14159:3.14159,samples=120] plot (\\x,{{exp(-(1-cos(\\x r))/{eps})/{Z:.9f}}});\n'
rho+=r'''
 \node[below] at (-3.14159,0){$-\pi$};\node[below] at (3.14159,0){$\pi$};
 \node[GreenMain,anchor=west] at (1.3,1.05){$\varepsilon=0.2$};
 \node[GoldMain,anchor=west] at (1.3,.7){$\varepsilon=0.8$};
 \node at (0,-.65){$U(x)=1-\cos x$，两端按圆周粘合};
\end{tikzpicture}
'''
add('gibbs-concentration','chapter14.tex',None,
    r'同一周期势的归一化 Gibbs 稳态；扩散变小时，质量更集中于唯一势阱 $x=0$。',
    r'图~\ref{fig:ode-tikz-gibbs-concentration} 取周期势 $U=1-\cos x$，两条密度曲线均已归一化。',rho)

assert checks['LV_level_residual']<1e-10
assert checks['stable_chart_min_jacobian']>0
chapters={}
for f in figures:
    path=folder/(f['name']+'.tex');assert not path.exists(),path
    path.write_text('% TikZ mathematical illustration; compiled with the main document.\n'+f['body']+'\n',encoding='utf-8')
    chapter=root/'chapters'/f['chapter']
    text=chapters.get(chapter,chapter.read_text(encoding='utf-8'))
    insert='\n'+f['intro']+'\n'+r'''\begin{center}
\begin{minipage}{0.96\linewidth}
\centering
'''+r'\input{figure/tikz/'+f['name']+'}\n'+r'\captionof{figure}{'+f['caption']+'}\n'+r'\label{fig:ode-tikz-'+f['name']+'}\n'+r'''\end{minipage}
\end{center}

'''
    if f['anchor'] is None:text=text.rstrip()+'\n'+insert
    else:
        assert text.count(f['anchor'])==1,(f['name'],f['anchor'])
        text=text.replace(f['anchor'],insert+f['anchor'])
    chapters[chapter]=text
for p,text in chapters.items():p.write_text(text,encoding='utf-8')
report={'figures':[{k:v for k,v in f.items() if k!='body'} for f in figures],'checks':checks}
(root/'教材对照/工作材料/TikZ配图记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('FIGURES',len(figures),'CHAPTER_FILES',len(chapters),'CHECKS',checks)
