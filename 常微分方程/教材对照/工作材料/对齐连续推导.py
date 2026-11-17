from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
texts={p.name:p.read_text(encoding='utf-8') for p in (root/'chapters').glob('*.tex')}
edits=[]
def block(file,old,new):
    old=old.strip();new=new.strip()
    if texts[file].count(old)!=1:raise ValueError((file,old,texts[file].count(old)))
    texts[file]=texts[file].replace(old,new);edits.append({'file':file,'before':old,'after':new})

block('arnold-contraction.tex',r'''
d(x_n,x_*)\leq\frac{\lambda^n}{1-\lambda}d(x_0,Ax_0),
 \qquad d(x,x_*)\leq\frac{d(x,Ax)}{1-\lambda}.
''',r'''
\begin{aligned}
 d(x_n,x_*)&\leq\frac{\lambda^n}{1-\lambda}d(x_0,Ax_0),\\
 d(x,x_*)&\leq\frac{d(x,Ax)}{1-\lambda}.
\end{aligned}
''')
block('arnold-contraction.tex',r'''
d(x_m,x_n)\leq\sum_{j=n}^{m-1}d(x_{j+1},x_j)
 \leq d_0\sum_{j=n}^{m-1}\lambda^j
 \leq\frac{\lambda^n}{1-\lambda}d_0.
''',r'''
\begin{aligned}
 d(x_m,x_n)&\leq\sum_{j=n}^{m-1}d(x_{j+1},x_j)\\
 &\leq d_0\sum_{j=n}^{m-1}\lambda^j\\
 &\leq\frac{\lambda^n}{1-\lambda}d_0.
\end{aligned}
''')
block('arnold-contraction.tex',r'''
d(x,x_*)\leq d(x,Ax)+d(Ax,Ax_*)
 \leq d(x,Ax)+\lambda d(x,x_*)
''',r'''
\begin{aligned}
 d(x,x_*)&\leq d(x,Ax)+d(Ax,Ax_*)\\
 &\leq d(x,Ax)+\lambda d(x,x_*)
\end{aligned}
''')
block('arnold-linear-algebra.tex',r'''
\left(I+\frac Am\right)^m
 =\sum_{k=0}^m c_{m,k}A^k,\qquad
 c_{m,k}=\frac1{k!}\prod_{j=0}^{k-1}\left(1-\frac jm\right).
''',r'''
\begin{aligned}
 \left(I+\frac Am\right)^m&=\sum_{k=0}^m c_{m,k}A^k,\\
 c_{m,k}&=\frac1{k!}\prod_{j=0}^{k-1}\left(1-\frac jm\right).
\end{aligned}
''')
block('arnold-energy.tex',r'''
\frac{m_*}{2}|v(t)|^2\leq\frac12\sum_i m_iv_i(t)^2
 =E_0-U(x(t))\leq E_0+C.
''',r'''
\begin{aligned}
 \frac{m_*}{2}|v(t)|^2&\leq\frac12\sum_i m_iv_i(t)^2\\
 &=E_0-U(x(t))\\
 &\leq E_0+C.
\end{aligned}
''')
block('arnold-energy.tex',r'''
\lim_{x\downarrow a}\frac{E-U(x)}{x-a}=-U'(a)>0,
 \qquad
 \lim_{x\uparrow b}\frac{E-U(x)}{b-x}=U'(b)>0.
''',r'''
\begin{aligned}
 \lim_{x\downarrow a}\frac{E-U(x)}{x-a}&=-U'(a)>0,\\
 \lim_{x\uparrow b}\frac{E-U(x)}{b-x}&=U'(b)>0.
\end{aligned}
''')
block('chapter7.tex',r'''
\ddot x_\lambda(t)=\lambda c^{-2}F(x(t/c))
=\lambda^mF(x(t/c))=F(x_\lambda(t)).
''',r'''
\begin{aligned}
 \ddot x_\lambda(t)&=\lambda c^{-2}F(x(t/c))\\
 &=\lambda^mF(x(t/c))\\
 &=F(x_\lambda(t)).
\end{aligned}
''')
block('chapter8.tex',r'''
w'=c(t)w+d(t),\qquad
 d(t)=(Q(t)-q(t))\sin^2\alpha(t)\geq0,
''',r'''
\begin{aligned}
 w'&=c(t)w+d(t),\\
 d(t)&=(Q(t)-q(t))\sin^2\alpha(t)\geq0,
\end{aligned}
''')
block('chapter9.tex',r'''
P_{t+T,s+T}=P_{t,s},\qquad P_{nT,0}=M^n,
 \qquad P_{nT+s,0}=P_{s,0}M^n\quad(0\leq s\leq T).
''',r'''
\begin{aligned}
 P_{t+T,s+T}&=P_{t,s},\\
 P_{nT,0}&=M^n,\\
 P_{nT+s,0}&=P_{s,0}M^n\qquad(0\leq s\leq T).
\end{aligned}
''')
block('chapter9.tex',r'''
第一段的双曲矩阵为
$\left(\begin{smallmatrix}\cosh k\tau&\sinh k\tau/k\\k\sinh k\tau&\cosh k\tau\end{smallmatrix}\right)$，
第二段为 $R_\Omega(\tau)$。
''',r'''
第一段的双曲矩阵为
\[
 \begin{pmatrix}
  \cosh(k\tau)&\sinh(k\tau)/k\\
  k\sinh(k\tau)&\cosh(k\tau)
 \end{pmatrix},
\]
第二段为 $R_\Omega(\tau)$。
''')
block('chapter9.tex',r'''
C(\nu)=\frac1{\omega^2-\nu^2+ik\nu},\qquad
 r(\nu)=\frac1{\sqrt{(\omega^2-\nu^2)^2+k^2\nu^2}}.
''',r'''
\begin{aligned}
 C(\nu)&=\frac1{\omega^2-\nu^2+ik\nu},\\
 r(\nu)&=\frac1{\sqrt{(\omega^2-\nu^2)^2+k^2\nu^2}}.
\end{aligned}
''')
block('chapter11.tex',r'''
于是沿 $x'=F_p$ 的曲线，$p_i'=\sum_j u_{x_ix_j}F_{p_j}
=-F_{x_i}-p_iF_u$，而 $u'=Du\,x'=p\cdot F_p$。
''',r'''
于是沿 $x'=F_p$ 的曲线，
\begin{align*}
 p_i'&=\sum_j u_{x_ix_j}F_{p_j}\\
 &=-F_{x_i}-p_iF_u,\\
 u'&=Du\,x'=p\cdot F_p.
\end{align*}
''')
block('chapter11.tex',r'''
代入得 $\alpha(X_F)=pF_p-pF_p=0$，且
\[
 dF(X_F)=F_tF_p+F_xpF_p-F_p(F_t+pF_x)=0.
\]
''',r'''
代入计算得
\begin{align*}
 \alpha(X_F)&=pF_p-pF_p=0,\\
 dF(X_F)&=F_tF_p+F_xpF_p-F_p(F_t+pF_x)\\
 &=0.
\end{align*}
''')
block('chapter11.tex',r'''
代入 $X$ 后得到 $\sum_iF_{p_i}dp_i+\sum_i(F_{x_i}+p_iF_u)dx_i
=dF-F_u\alpha$。
''',r'''
代入 $X$ 后得到
\begin{align*}
 \iota_Xd\alpha
 &=\sum_iF_{p_i}dp_i+\sum_i(F_{x_i}+p_iF_u)dx_i\\
 &=dF-F_u\alpha.
\end{align*}
''')
block('chapter13.tex',r'''
\displaystyle\int_MF_1^*\eta-\displaystyle\int_MF_0^*\eta=\displaystyle\int_{[0,1]\times M}dF^*\eta=0.
''',r'''
\begin{aligned}
 \int_MF_1^*\eta-\int_MF_0^*\eta
 &=\int_{[0,1]\times M}dF^*\eta\\
 &=0.
\end{aligned}
''')
block('chapter14.tex',r'''
\frac{\dd}{\dd t}(r\times\dot r)=\dot r\times\dot r+r\times\ddot r
=r\times a(|r|)r=0.
''',r'''
\begin{aligned}
 \frac{\dd}{\dd t}(r\times\dot r)
 &=\dot r\times\dot r+r\times\ddot r\\
 &=r\times a(|r|)r\\
 &=0.
\end{aligned}
''')
block('chapter14.tex',r'''
\displaystyle\int_0^L|u-\rho|\,dx\leq(\displaystyle\int\rho)^{1/2}\mathcal E^{1/2}=\mathcal E^{1/2}.
''',r'''
\begin{aligned}
 \int_0^L|u-\rho|\,dx
 &\leq\left(\int\rho\right)^{1/2}\mathcal E^{1/2}\\
 &=\mathcal E^{1/2}.
\end{aligned}
''')
block('chapter15.tex',r'''
y'=Ax+R(x)-[AG(R(x))+R(x)]=Ay.
''',r'''
\begin{aligned}
 y'&=Ax+R(x)-[AG(R(x))+R(x)]\\
 &=A[x-G(R(x))]\\
 &=Ay.
\end{aligned}
''')
block('chapter15.tex',r'''
\|z-z_j\|_\infty\leq\frac{q^j}{1-q}\|z_1-z_0\|_\infty
 \leq\frac{q^j C_GM}{1-q},
''',r'''
\begin{aligned}
 \|z-z_j\|_\infty&\leq\frac{q^j}{1-q}\|z_1-z_0\|_\infty\\
 &\leq\frac{q^j C_GM}{1-q},
\end{aligned}
''')

for file in {e['file'] for e in edits}:
    (root/'chapters'/file).write_text(texts[file],encoding='utf-8')
(root/'教材对照/工作材料/连续推导对齐记录.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2),encoding='utf-8')
print('ALIGNED',len(edits))
