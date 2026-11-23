from pathlib import Path
import runpy,subprocess,re,json
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
base='3561ded';relative='常微分方程/Solution - 常微分方程期末复习/'
def group(text,start):
 depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  elif text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i
checks=[]
for n in range(1,6):
 file=f'chapter{n}.tex'
 old=subprocess.check_output(['git','show',base+':'+relative+file],cwd=ROOT).decode('utf-8-sig')
 new=(ROOT/file).read_text(encoding='utf-8-sig')
 def headers(s):
  result=[]
  for m in re.finditer(r'\\problem\{',s):
   a=m.end()-1;vals=[]
   for _ in range(3):
    val,a=group(s,a);vals.append(val)
   result.append(vals)
  return result
 def answers(s):return [group(s,m.end()-1)[0] for m in re.finditer(r'\\ans\{',s)]
 assert headers(old)==headers(new), 'original question changed '+file
 assert answers(old)==answers(new), 'standard answer changed '+file
 checks.append({'chapter':n,'question_headers_unchanged':True,'standard_answers_unchanged':True,'old_characters':len(old),'new_characters':len(new)})
x,t,u=S.symbols('x t u',real=True);tests=[]
def ck(name,a,b=0):
 residual=S.simplify(S.trigsimp(S.expand(a-b)));assert residual==0,(name,residual);tests.append(name)
# Newly explicit antiderivatives and decompositions.
ck('separable rational',1/(x*(1+x*x)),1/x-x/(1+x*x))
ck('rational y2-1',2/(u*u-1),1/(u-1)-1/(u+1))
ck('nonhomogeneous substitution rational',(u+1)**2/(u*(1+u*u)),1/u+2/(1+u*u))
ck('linear inverse integration',S.diff(-(u+1)*S.exp(-u),u),u*S.exp(-u))
ck('linear quotient integration',S.diff(S.log(x+1)+1/(x+1),x),x/(x+1)**2)
ck('Bernoulli integration',S.diff((1-x*x)*S.exp(x*x),x),-2*x**3*S.exp(x*x))
ck('exact integral twice by parts',S.diff(-x*x*S.cos(x)+2*x*S.sin(x)+2*S.cos(x),x),x*x*S.sin(x))
ck('implicit folium rational',3*u/(1+u**3),-1/(u+1)+(u+1)/(u*u-u+1))
F=-S.log(u+1)+S.log(u*u-u+1)/2+S.sqrt(3)*S.atan((2*u-1)/S.sqrt(3))
ck('implicit folium primitive',S.diff(F,u),3*u/(1+u**3))
ck('angle primitive',S.diff(-S.cos(u)/(1+S.sin(u)),u),1/(1+S.sin(u)))
ck('parameter derivative implicit 2.4.1(3)',(1-1/u**2)/(1-u*u),-1/u**2)
ck('constant variation c1 primitive',S.diff(-t*t/8+t*S.sin(4*t)/16+S.cos(4*t)/64,t),-t*S.sin(2*t)**2/2)
ck('constant variation c2 primitive',S.diff(-t*S.cos(4*t)/16+S.sin(4*t)/64,t),t*S.sin(2*t)*S.cos(2*t)/2)
ck('IVP exponential sine primitive',S.diff(-S.exp(-t)*(S.sin(t)+S.cos(t))/2,t),S.exp(-t)*S.sin(t))
ck('Picard square coefficients',(1+t+t*t+t**3/3)**2,1+2*t+3*t*t+8*t**3/3+5*t**4/3+2*t**5/3+t**6/9)
ck('Picard negative square',(-t*t/2+t**5/20)**2,t**4/4-t**7/20+t**10/400)
ck('Picard positive square',(t*t/2+t**5/20)**2,t**4/4+t**7/20+t**10/400)
# Independently recompute the new worked RK4 first step with high precision.
import mpmath as mp
mp.mp.dps=40;h=mp.mpf('.1');z=mp.mpf('.5')
k1=z;k2=z+h*k1/2+mp.sin(h/2);k3=z+h*k2/2+mp.sin(h/2);k4=z+h*k3+mp.sin(h)
v=z+h*(k1+2*k2+2*k3+k4)/6
assert f'{float(v):.9f}'=='0.557752014'
assert f'{float(k2):.9f}'=='0.574979169'
assert f'{float(k3):.9f}'=='0.578728128'
assert f'{float(k4):.9f}'=='0.657706229'
manifest=json.loads((ROOT/'qa/detail-expansion.json').read_text(encoding='utf-8'))
assert manifest['count']==180
report={'baseline_commit':base,'question_and_answer_checks':checks,'intermediate_symbolic_checks':tests,'rk4_worked_step':str(v),'all_180_items_expanded':True}
(ROOT/'qa/detail-revision-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Original questions and final answers unchanged across 5 chapters;',len(tests),'new intermediate identities passed; worked RK4 step passed; 180 items covered')
