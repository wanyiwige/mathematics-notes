from pathlib import Path
import re,json,math
import numpy as np
import sympy as sp
root=Path(__file__).resolve().parents[2]
report=json.loads((root/'教材对照/工作材料/TikZ配图记录.json').read_text(encoding='utf-8'))
checks={}
names=[f['name'] for f in report['figures']]
assert len(names)==len(set(names))==17
for f in report['figures']:
    text=(root/'figure/tikz'/f"{f['name']}.tex").read_text(encoding='utf-8')
    assert text.count(r'\begin{tikzpicture}')==text.count(r'\end{tikzpicture}')==1
    assert r'\includegraphics' not in text
    chapter=(root/'chapters'/f['chapter']).read_text(encoding='utf-8')
    assert text.strip() in chapter
    assert r'\input' not in chapter
    assert chapter.count(r'\label{fig:ode-tikz-'+f['name']+'}')==1
    assert chapter.count(r'\ref{fig:ode-tikz-'+f['name']+'}')==1
checks['17_vector_figures_linked_and_referenced']=True
lv=(root/'figure/tikz/lv-levels.tex').read_text(encoding='utf-8')
lines=re.findall(r'plot coordinates \{(.*?)\}',lv)
maxerr=0.
for line,E in zip(lines,(2.08,2.30,2.65)):
    xy=[tuple(map(float,p)) for p in re.findall(r'\(([-.0-9]+),([-.0-9]+)\)',line)]
    assert len(xy)==181
    for x,y in xy:
        assert x>0 and y>0
        maxerr=max(maxerr,abs(x-math.log(x)+y-math.log(y)-E))
checks['rounded_LV_level_error_below_1e-4']=maxerr<1e-4
checks['stable_coordinate_change_invertible']=1-.36**2*1.45**2>0
checks['return_multiplier_strictly_between_0_and_1']=0<math.exp(-.24*2*math.pi)<1
checks['trace_example_eigenvalue_product_1']=abs((1.2/.75)*(.46875/.75)-1)<1e-12
grid=np.linspace(-math.pi,math.pi,40001)
errors={}
for eps in (.2,.8):
    Z=report['checks'][f'gibbs_Z_{eps}']
    mass=float(np.trapezoid(np.exp(-(1-np.cos(grid))/eps)/Z,grid))
    errors[str(eps)]=abs(mass-1)
checks['gibbs_densities_normalized']=max(errors.values())<1e-8
bump_errors=[]
normalizer=1.20690032
for width in (1.,.5,.3):
    t=np.linspace(-width,width,40001);u=t/width
    bump=np.zeros_like(u);inside=np.abs(u)<1
    bump[inside]=np.exp(1-1/(1-u[inside]**2))/(width*normalizer)
    bump_errors.append(abs(float(np.trapezoid(bump,t))-1))
checks['bump_rescalings_preserve_mass']=max(bump_errors)<1e-7
t,p=sp.symbols('t p',real=True)
x=sp.sin(t);y=2*(sp.cos(t)-1)
checks['Hill_ellipse_satisfies_system']=sp.simplify(sp.diff(x,t,2)-2*sp.diff(y,t)-3*x)==0 and sp.simplify(sp.diff(y,t,2)+2*sp.diff(x,t))==0
checks['jet_cusp_has_slope_p']=sp.simplify(sp.diff(2*p**3/3,p)-p*sp.diff(p**2,p))==0
checks['Sturm_examples_Wronskian_minus_one']=sp.simplify(sp.sin(t)*sp.diff(sp.cos(t),t)-sp.diff(sp.sin(t),t)*sp.cos(t)+1)==0
result={'checks':checks,'max_rounded_LV_level_error':maxerr,'gibbs_mass_errors':errors,'bump_mass_errors':bump_errors,'passed':all(checks.values())}
(root/'教材对照/工作材料/TikZ图形核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2));assert result['passed']
