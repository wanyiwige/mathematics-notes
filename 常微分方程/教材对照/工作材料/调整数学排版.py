from pathlib import Path
import re,json,hashlib
root=Path(__file__).resolve().parents[2]
texts={p.name:p.read_text(encoding='utf-8') for p in (root/'chapters').glob('*.tex')}
before=dict(texts); edits=[]
def change(file,old,new):
    if texts[file].count(old)!=1: raise ValueError((file,old,texts[file].count(old)))
    texts[file]=texts[file].replace(old,new)
    edits.append({'file':file,'before':old,'after':new})
def display(file,formula,body=None):
    old='$'+formula+'$'
    if texts[file].count(old)!=1:raise ValueError((file,formula,texts[file].count(old)))
    j=texts[file].index(old)+len(old)
    punct=texts[file][j:j+1]
    tail={'。':'.','，':',','；':';'}.get(punct,'')
    if tail:old+=punct
    change(file,old,'\n\\[\n '+(body or formula)+tail+'\n\\]\n')

items={
'arnold-contraction.tex':[
r'd(Ax,Ay)\leq\lambda d(x,y)',
r'Ax_*=\lim Ax_n=\lim x_{n+1}=x_*',
r'd(x_*,y_*)\leq\lambda d(x_*,y_*)',
r'\|Au-Aw\|_\infty\leq Lh\|u-w\|_\infty',
r'\|u-x\|_\infty\leq\|u-Au\|_\infty/(1-Lh)',
r'|R(x)-R(z)|\leq\theta|x-z|',
r'v=F(x+u)-F(x)=DF(x)u+o(|u|)',
r'DG(y)=DF(G(y))^{-1}',
r'\dot\xi=A(t)\xi+R(t,\xi)',
r'\eta(t)=\eta_0+o(|\eta_0|)'],
'arnold-linear-algebra.tex':[
r'u_{j+1}=Bu_j=B^{j+1}u_0',
r'\binom jr=j(j-1)\cdots(j-r+1)/r!',
r'a_j=(\lambda_+^j-\lambda_-^j)/\sqrt5',
r'Ef=(f(t_1),\ldots,f(t_n))',
r'V=\bigoplus_\lambda E_\lambda^{m_\lambda}',
r'y=e^{\lambda t}t^\nu q(t)',
r'y=e^{\lambda t}\sum_{j=0}^{k+\nu-1}c_jt^j',
r'P(D)y_0=Q(N)N^\nu y_0=0',
r'S^TAS=\operatorname{diag}(a_1,\ldots,a_n)',
r'E=\frac12\sum_j(\dot q_j^2+a_jq_j^2)'],
'arnold-energy.tex':[
r'V(t)=\displaystyle\int_DJ(t,x)\,dx',
r'c_1(x-a)\leq E-U(x)\leq c_2(x-a)',
r'\dot x^2=2(\cos x-\cos A)',
r'0=-aT+b\displaystyle\int_0^Ty(t)\,\dd t',
r'0=cT-d\displaystyle\int_0^Tx(t)\,\dd t',
r'\displaystyle\int_0^tu(s)\,\dd s=(\sqrt{1+2u_0^2t}-1)/u_0'],
'chapter7.tex':[
r'''\ddot x_\lambda(t)=\lambda c^{-2}F(x(t/c))
=\lambda^mF(x(t/c))=F(x_\lambda(t))''',
r'L_v(c_1f+c_2g)=c_1L_vf+c_2L_vg',
r'L_v(fg)=fL_vg+gL_vf'],
'chapter8.tex':[
r'c(t)=\displaystyle\int_0^1\partial_s f_Q(t,\alpha(t)+\tau w(t))\,d\tau',
r'x=e^{-\frac12\displaystyle\int p}u',
r'x\primew-xw\prime=\displaystyle\int_0^t x(s,\lambda)^2ds'],
'chapter9.tex':[
r'P_{nT+s,0}=P_{nT+s,nT}M^n=P_{s,0}M^n',
r'\mu=\exp\displaystyle\int_0^Ta(t)\,\dd t>0',
r'p(\lambda)=\lambda^2-(\operatorname{tr}M)\lambda+1',
r'|M^nv|\geq n|Nv|-|v|\to\infty',
r'\|X(t)-\widetilde X(t)\|\leq\eta t e^{Bt}',
r'\|M-\widetilde M\|\leq\eta T e^{BT}',
r'|\operatorname{tr}\widetilde M-\operatorname{tr}M|<\gamma/2',
r'M=R_{\omega_2}(\tau_2)R_{\omega_1}(\tau_1)',
r'\eta=\pm\varepsilon/[\pi(k+1/2)]+o(\varepsilon)',
r'''\omega_1/\omega_2+\omega_2/\omega_1
=2+4\varepsilon^2/\omega^2+O(\varepsilon^4)''',
r'2\cos a\cos b-2\sin a\sin b=2\cos(a+b)',
r'2\cosh\sqrt s\cos\sqrt s=2-s^2/3+O(s^4)',
r'\cos((1-A^2/16)t)=\cos t+(A^2/16)t\sin t+O(A^4)'],
'chapter10.tex':[
r'B=HAH^{-1}',
r'He^{tA}=e^{tB}H',
r'e^{Ct}Q(x)\leq Q(e^{tA}x)\leq e^{ct}Q(x)',
r'Q(e^{-tA}x)=1',
r't\leq C^{-1}\log Q(x)\to-\infty'],
'chapter11.tex':[
r'L_a u=\sum_i a_i(x)\partial_i u=0',
r'F(s,z)=\varphi^s(\sigma(z))',
r'u(F(s,z))=g(\sigma(z))',
r'\frac{\dd}{\dd s}u(F(s,z))=b(F(s,z))',
r'u_x=g\prime(\xi)/(1+tg\prime(\xi))',
r'u_t+uu_x=-x\sec^2t+x\tan^2t=-x',
r'dF(X_F)=F_tF_p+F_xpF_p-F_p(F_t+pF_x)=0',
r'd\alpha=\sum_{i,j}(\partial_i a_j)\,dz_i\wedge dz_j',
r'\mathcal L_X\alpha=d(\alpha(X))+\iota_Xd\alpha',
r'\nabla(r^2)=2(x-q(z(x)))'],
'chapter12.tex':[
r'T_xf:T_xM\to T_{f(x)}N',
r'TM=\coprod_{x\in M}T_xM',
r'T_xf[\gamma]=[f\gamma]'],
'chapter13.tex':[
r'\operatorname{ind}_v\gamma=(\theta(1)-\theta(0))/(2\pi)',
r'\omega=(P\,dQ-Q\,dP)/(P^2+Q^2)',
r'\operatorname{ind}_v(x_0)=\operatorname{sgn}\det A',
r'\displaystyle\int_MF_1^*\eta-\displaystyle\int_MF_0^*\eta=\displaystyle\int_{[0,1]\times M}dF^*\eta=0',
r'm_0-m_1+m_2=\chi(M)'],
'chapter14.tex':[
r'''\frac{\dd}{\dd t}(r\times\dot r)=\dot r\times\dot r+r\times\ddot r
=r\times a(|r|)r=0''',
r'L-y\primeL_{y\prime}=n(y)/\sqrt{1+y\prime^2}',
r'L=(\dot s^2+r(s)^2\dot\phi^2)/2',
r'g\prime(x)/[g(x)^2+Cg(x)^3]=1/v(x)',
r'\rho=C_\varepsilon e^{-U/\varepsilon}',
r'\varepsilon\rho\prime+U\prime\rho=\varepsilon C_\varepsilon(e^{c/\varepsilon}-1)',
r'\mathcal E(t)=\displaystyle\int_0^L\rho(w-1)^2\,dx',
r'\mathcal E\leq(L/m)\displaystyle\int\rho w_x^2',
r'\displaystyle\int_0^L|u-\rho|\,dx\leq(\displaystyle\int\rho)^{1/2}\mathcal E^{1/2}=\mathcal E^{1/2}'],
'chapter15.tex':[
r'v_n=U^{-1}v_{n+1}-U^{-1}g(z_n)',
r'(Gf)\prime=A(Gf)+f',
r'|Ax+R(x)|\leq\|A\||x|+M',
r'y\prime=Ax+R(x)-[AG(R(x))+R(x)]=Ay',
r'h(\varphi^tx_0)=e^{tA}h(x_0)',
r'z_{j+1}=G(R(e^{\cdot A}y_0+z_j))',
r'\Psi(x_1,\ldots,x_n)=\det(\phi_i(x_j))_{i,j=1}^n',
r'\Delta=\{0<x_1<\cdots<x_n<l\}'],
}
# Prime notation is kept exactly as in the existing source.
missing=[]
for file,formulas in items.items():
    for formula in formulas:
        formula=formula.replace(r'\prime',"'")
        if texts[file].count('$'+formula+'$')!=1:missing.append((file,formula,texts[file].count('$'+formula+'$')))
if missing:raise ValueError(missing)
for file,formulas in items.items():
    for formula in formulas:
        formula=formula.replace(r'\prime',"'")
        display(file,formula)

for file,text in texts.items():
    if text!=before[file]:
        text=re.sub(r'\n[ \t]*\n(?=\\\[)', '\n',text)
        text=re.sub(r'(?<=\\\])\n[ \t]*\n','\n',text)
        texts[file]=text

# Remaining edits below arrange already displayed calculations by their logical steps.
def block(file,old,new):change(file,old.strip(),new.strip())

block('chapter15.tex',r'''
F(u,v)=(Su+f(u,v),Uv+g(u,v)),\qquad
 f(0)=g(0)=0,\quad Df(0)=Dg(0)=0.
''',r'''
\begin{aligned}
 F(u,v)&=(Su+f(u,v),Uv+g(u,v)),\\
 f(0)&=g(0)=0,\qquad Df(0)=Dg(0)=0.
\end{aligned}
''')
block('chapter15.tex',r'''
\|z(\xi)\|_\sigma\leq\frac{|\xi|}{1-q},\qquad
 \|z(\xi)-z(\eta)\|_\sigma\leq\frac{|\xi-\eta|}{1-q}.
''',r'''
\begin{aligned}
 \|z(\xi)\|_\sigma&\leq\frac{|\xi|}{1-q},\\
 \|z(\xi)-z(\eta)\|_\sigma&\leq\frac{|\xi-\eta|}{1-q}.
\end{aligned}
''')
block('chapter15.tex',r'''
(Gf)(t)=\int_{-\infty}^te^{A(t-s)}P_sf(s)\,ds
 -\int_t^\infty e^{A(t-s)}P_uf(s)\,ds.
''',r'''
\begin{aligned}
 (Gf)(t)={}&\int_{-\infty}^te^{A(t-s)}P_sf(s)\,ds\\
 &-\int_t^\infty e^{A(t-s)}P_uf(s)\,ds.
\end{aligned}
''')
block('chapter11.tex',r'''
\dot x_i=F_{p_i},\qquad
 \dot p_i=-F_{x_i}-p_iF_u,\qquad
 \dot u=\sum_i p_iF_{p_i}.
''',r'''
\begin{aligned}
 \dot x_i&=F_{p_i},\\
 \dot p_i&=-F_{x_i}-p_iF_u,\\
 \dot u&=\sum_i p_iF_{p_i}.
\end{aligned}
''')

report=[]
for file,text in texts.items():
    if text!=before[file]:
        # No substantive math tokens are removed by moving a formula out of a paragraph.
        for env in ('proof','theorem','proposition','definition','aligned','align*'):
            assert text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),(file,env)
        (root/'chapters'/file).write_text(text,encoding='utf-8')
        report.append({'file':file,'edits':sum(e['file']==file for e in edits),'sha256_before':hashlib.sha256(before[file].encode()).hexdigest(),'sha256_after':hashlib.sha256(text.encode()).hexdigest()})
(root/'教材对照/工作材料/本轮分行排版记录.json').write_text(json.dumps({'files':report,'edits':edits},ensure_ascii=False,indent=2),encoding='utf-8')
print('FILES',len(report),'EDITS',len(edits))
