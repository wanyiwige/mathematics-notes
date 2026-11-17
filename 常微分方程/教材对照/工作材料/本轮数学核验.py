from pathlib import Path
import sympy as s
import json,re
root=Path(__file__).resolve().parents[2]
checks={}
x,y,a,b,c,d,eps,lam=s.symbols('x y a b c d eps lam', real=True)
H=d*x-c*s.log(x)+b*y-a*s.log(y)
checks['Lotka_Volterra_energy']=s.simplify(s.diff(H,x)*x*(-a+b*y)+s.diff(H,y)*y*(c-d*x))==0
tr=s.symbols('tr',real=True)
M=s.Matrix([[1,1],[0,1]])
checks['Jordan_boundary_growth']=M**8==s.Matrix([[1,8],[0,1]])
t=s.symbols('t',real=True)
alpha=s.symbols('alpha',real=True)
z=s.Matrix([s.cos(t),s.sin(t)])
inversion= s.eye(2)-2*z*z.T
target=s.Matrix([-s.cos(2*t-alpha),-s.sin(2*t-alpha)])
checks['sphere_transition_direction']=all(s.trigsimp(q)==0 for q in inversion*s.Matrix([s.cos(alpha),s.sin(alpha)])-target)
A=s.symbols('A',real=True)
checks['Van_der_Pol_increment']=s.simplify(s.integrate(A**2*s.sin(t)**2*(1-A**2*s.cos(t)**2),(t,0,2*s.pi))-(s.pi*A**2-s.pi*A**4/4))==0
xx=s.Function('x')(t);ww=s.Function('w')(t);q=s.Function('q')(t)
expr=s.diff(s.diff(xx,t)*ww-xx*s.diff(ww,t),t)
expr=expr.subs({s.diff(xx,t,2):-(q+lam)*xx,s.diff(ww,t,2):-(q+lam)*ww-xx})
checks['Sturm_parameter_identity']=s.simplify(expr-xx**2)==0
k=s.symbols('k',real=True)
N=s.Matrix([[-2*k,2],[-2*k*k,2*k+1]])
checks['folded_field_trace_det']=s.simplify(s.trace(N)-1)==0 and s.simplify(N.det()+2*k)==0
sigma,aa=s.symbols('sigma aa',positive=True)
checks['stable_kernel_sum']=s.simplify(sigma**-1/(1-aa/sigma)-1/(sigma-aa))==0
checks['unstable_kernel_sum']=s.simplify(sum(aa**(j+1)*sigma**j for j in range(12))-aa*(1-(aa*sigma)**12)/(1-aa*sigma))==0
sources=list((root/'chapters').glob('*.tex'))
checks['no_source_editorial_notes']=not any(re.search(r'Arnold|原书|原教材|原笔记|补充证明|参考.*§',p.read_text(encoding='utf-8')) for p in sources)
for p in sources:
    text=p.read_text(encoding='utf-8')
    for env in ('proof','theorem','definition','proposition','lemma','corollary','align*'):
        if text.count('\\begin{'+env+'}')!=text.count('\\end{'+env+'}'):
            raise ValueError((p.name,env))
checks['math_environments_balanced']=True
result={'checks':checks,'passed':all(checks.values())}
(root/'教材对照/工作材料/本轮数学核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
assert result['passed']
