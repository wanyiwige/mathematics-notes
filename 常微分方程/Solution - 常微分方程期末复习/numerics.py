from pathlib import Path
import math,json
import mpmath as mp
ROOT=Path(__file__).resolve().parent

def euler(f,t,x,h): return x+h*f(t,x)
def heun(f,t,x,h):
    p=x+h*f(t,x)
    return x+h*(f(t,x)+f(t+h,p))/2

def rk4(f,t,x,h):
    k1=f(t,x);k2=f(t+h/2,x+h*k1/2)
    k3=f(t+h/2,x+h*k2/2);k4=f(t+h,x+h*k3)
    return x+h*(k1+2*k2+2*k3+k4)/6

def solve(f,x0,h,n,step):
    rows=[(0.,x0)];x=x0
    for k in range(n):
        t=k*h;x=step(f,t,x,h);rows.append(((k+1)*h,x))
    return rows

def scientific(v):
    if v==0:return '$0$'
    a,b=f'{v:.3e}'.split('e')
    return '$'+a+r'\times10^{'+str(int(b))+'}$'

if __name__=='__main__':
    f=lambda t,x:x+math.sin(t)
    exact=lambda t:math.exp(t)-(math.sin(t)+math.cos(t))/2
    data={name:solve(f,.5,.1,10,step) for name,step in [('Euler',euler),('Heun',heun),('RK4',rk4)]}
    lines=[r'\begin{center}\small\setlength{\tabcolsep}{3pt}',r'\begin{tabular}{rrrrrrr}\toprule',
      r'$t$&精确值&Euler&绝对误差&改进Euler&绝对误差&RK4\\\midrule']
    for k in range(11):
        t=k/10;e=exact(t);a=data['Euler'][k][1];b=data['Heun'][k][1];c=data['RK4'][k][1]
        lines.append(f'{t:.1f}&{e:.9f}&{a:.9f}&{scientific(abs(a-e))}&{b:.9f}&{scientific(abs(b-e))}&{c:.9f}'+r'\\')
    lines.extend([r'\bottomrule\end{tabular}\end{center}',r'\begin{center}\small\begin{tabular}{rr}\toprule $t$&RK4绝对误差\\\midrule'])
    for k in range(1,11):
        t=k/10;c=data['RK4'][k][1];lines.append(f'{t:.1f}&{scientific(abs(c-exact(t)))}'+r'\\')
    lines.append(r'\bottomrule\end{tabular}\end{center}')
    a,b,c=[data[n][-1][1] for n in ['Euler','Heun','RK4']]
    lines.append(r'\ans{X_{10}^{\mathrm E}='+f'{a:.9f}'+r',\quad X_{10}^{\mathrm H}='+f'{b:.9f}'+r',\quad X_{10}^{\mathrm {RK4}}='+f'{c:.9f}'+r'.}')
    (ROOT/'numerical-table.tex').write_text('\n'.join(lines),encoding='utf-8')
    lines=[r'\begin{center}\begin{tabular}{rrrr}\toprule $t$&$\e^t$&Euler近似&绝对误差\\\midrule']
    eu=[]
    for k in range(-4,5):
        t=k/4;v=(1.25**k if k>=0 else .75**(-k));err=abs(math.exp(t)-v)
        eu.append((t,v,err));lines.append(f'{t:.2f}&{math.exp(t):.5f}&{v:.5f}&{err:.5f}'+r'\\')
    lines.append(r'\bottomrule\end{tabular}\end{center}')
    (ROOT/'euler-table.tex').write_text('\n'.join(lines),encoding='utf-8')
    mp.mp.dps=60
    I=mp.mpf('0');h=mp.mpf('.1');increments=[]
    for k in range(10):
        t=k*h;d=h/6*(mp.exp(-t*t)+4*mp.exp(-(t+h/2)**2)+mp.exp(-(t+h)**2));I+=d;increments.append(d)
    ref=mp.quad(lambda t:mp.exp(-t*t),[0,1]);err=abs(I-ref)
    result=r'\ans{I_{\mathrm{RK4}}='+mp.nstr(I,16)+r',\qquad I_{\mathrm{ref}}='+mp.nstr(ref,16)+r',\\ |I_{\mathrm{RK4}}-I_{\mathrm{ref}}|\approx '+scientific(float(err)).strip('$')+r'.}'
    lines=[r'\begin{center}\small\begin{tabular}{rr}\toprule 区间& RK4积分增量\\\midrule']
    for k,d in enumerate(increments):lines.append(f'$[{k/10:.1f},{(k+1)/10:.1f}]$&{float(d):.12f}'+r'\\')
    lines.extend([r'\bottomrule\end{tabular}\end{center}',result])
    (ROOT/'integral-result.tex').write_text('\n'.join(lines),encoding='utf-8')
    # Independent high-precision ODE reference, and composite Simpson verification.
    high=mp.odefun(lambda t,x:x+mp.sin(t),0,mp.mpf('.5'))
    assert abs(high(1)-(mp.e-(mp.sin(1)+mp.cos(1))/2))<mp.mpf('1e-45')
    sim=h/6*(mp.mpf(1)+mp.exp(-1)+4*sum(mp.exp(-(j*h/2)**2) for j in range(1,20,2))+2*sum(mp.exp(-(j*h/2)**2) for j in range(2,20,2)))
    assert abs(sim-I)<mp.mpf('1e-55')
    # Step halving confirms global convergence orders without using the exact result to advance.
    convergence={}
    for name,step in [('Euler',euler),('Heun',heun),('RK4',rk4)]:
        fine=solve(f,.5,.05,20,step)[-1][1]
        convergence[name]=abs(data[name][-1][1]-exact(1))/abs(fine-exact(1))
    report={'problem_5.6.2':data,'error_ratio_h_to_half_h':convergence,
            'problem_5.6.3':{'rk4':str(I),'independent_quadrature':str(ref),'error':str(err)},'problem_5.2.1':eu}
    (ROOT/'qa'/'numerical-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'RK4_integral':str(I),'error':str(err),'order_ratios':convergence},indent=2))
