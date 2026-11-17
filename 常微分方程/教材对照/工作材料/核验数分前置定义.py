from pathlib import Path
import re,json,hashlib,zipfile
import numpy as np
import sympy as sp
root=Path(__file__).resolve().parents[2]
record=root/'教材对照/工作材料/数分前置定义补全记录.json'
d=json.loads(record.read_text(encoding='utf-8'))
z=zipfile.ZipFile(d['backup']);assert z.testzip() is None
baseline=json.loads((root/'教材对照/工作材料/数分源文件哈希基线.json').read_text(encoding='utf-8'))
analysis=root.parent/'分析学笔记'
assert all(hashlib.sha256((analysis/k).read_bytes()).hexdigest()==v for k,v in baseline.items())
old='\n'.join(z.read(f'chapters/chapter{i}.tex').decode('utf-8-sig') for i in range(1,16))
new='\n'.join((root/f'chapters/chapter{i}.tex').read_text(encoding='utf-8') for i in range(1,16))
oldlabels=set(re.findall(r'\\label\{([^}]+)\}',old));labels=re.findall(r'\\label\{([^}]+)\}',new)
assert oldlabels<=set(labels) and len(labels)==len(set(labels))
assert r'\input{' not in new
for env in ('definition','lemma','proof','theorem','proposition','example','corollary'):
 assert new.count('\\begin{'+env+'}')==new.count('\\end{'+env+'}')
newenv={e:new.count('\\begin{'+e+'}')-old.count('\\begin{'+e+'}') for e in ('definition','lemma','proof','theorem','proposition','example','corollary')}
order=[['def:support-test','ex:smooth-cutoff','sec:quasipolynomials'],
 ['def:forms-coordinate','def:exterior-pullback','def:closed-exact-form','prop:forms-stokes-calculus'],
 ['def:partition-integration','prop:forms-stokes-calculus','def:euler-characteristic'],
 ['def:banach-operator','lem:neumann-series','def:weighted-banach','def:frechet-derivative'],
 ['def:l2-completion','def:dirichlet-rayleigh','lem:nonnegative-elliptic-positive']]
for chain in order:
 p=[new.index('\\label{'+s+'}') for s in chain];assert p==sorted(p),chain
checks={}
x,y,v,acc=sp.symbols('x y v acc',real=True)
phi=x**3+x*y**2+y**4;t=sp.symbols('t',real=True)
potential=sp.integrate(sp.diff(phi,x).subs({x:t*x,y:t*y})*x+sp.diff(phi,y).subs({x:t*x,y:t*y})*y,(t,0,1))
checks['convex_potential_formula']=sp.simplify(potential-phi)==0
n=sp.Function('n')(y);L=n*sp.sqrt(1+v*v)
D=lambda f:sp.diff(f,y)*v+sp.diff(f,v)*acc
checks['Beltrami_first_integral_identity']=sp.simplify(D(L-v*sp.diff(L,v))+v*(D(sp.diff(L,v))-sp.diff(L,y)))==0
s=sp.symbols('s',positive=True)
checks['cutoff_derivatives_match_zero']=all(sp.limit(sp.diff(sp.exp(-1/s),s,j),s,0,dir='+')==0 for j in range(5))
# Independent numerical checks of the matrix constructions and inverse series.
B=np.array([[3.,1.],[1.,2.]]);vals,S=np.linalg.eigh(B);P=S@np.diag(np.sqrt(vals))@S.T
A=np.array([[2.,1.],[-.5,1.5]]);vals,S=np.linalg.eigh(A.T@A);P=S@np.diag(np.sqrt(vals))@S.T;Q=A@np.linalg.inv(P)
checks['polar_construction']=np.linalg.norm(P@P-A.T@A)<1e-12 and np.linalg.norm(Q.T@Q-np.eye(2))<1e-12
T=np.array([[.2,.15],[0.,-.1]]);total=np.eye(2);power=np.eye(2)
for j in range(60):power=power@T;total+=power
checks['Neumann_inverse_two_sides']=np.linalg.norm((np.eye(2)-T)@total-np.eye(2))<1e-12 and np.linalg.norm(total@(np.eye(2)-T)-np.eye(2))<1e-12
checks['no_unescaped_control_characters']=not any(ord(c)<32 and c not in '\n\r\t' for c in new)
checks={k:bool(v) for k,v in checks.items()}
assert all(checks.values()),checks
original='\n'.join((root/f'教材对照/工作材料/整合前原稿/chapter{i}.tex').read_text(encoding='utf-8') for i in range(1,7))
d.update({'analysis_source_files_checked':len(baseline),'analysis_sources_unchanged':True,'new_environments_this_revision':newenv,
'total_new_environments_vs_original_notes':{e:new.count('\\begin{'+e+'}')-original.count('\\begin{'+e+'}') for e in newenv},
'retained_old_labels':len(oldlabels),'current_labels':len(labels),'definition_order_chains':order,'math_checks':checks,'backup_crc_valid':True})
record.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:d[k] for k in ['analysis_source_files_checked','analysis_sources_unchanged','new_environments_this_revision','retained_old_labels','current_labels','math_checks']},ensure_ascii=False,indent=2))
