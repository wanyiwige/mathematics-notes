from pathlib import Path
import math
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
def coords(points):return ' '.join(f'({a:.5f},{b:.5f})' for a,b in points)
def stroke(points,color='blue',options='thick'):
 return r'\draw['+color+','+options+r'] plot coordinates {'+coords(points)+'};'
plots=[]
for j,(f,initials) in enumerate([(lambda t,x:abs(x),[(0,0),(0,-1)]),(lambda t,x:t*t+x*x,[(0,0),(0,-.5),(math.sqrt(2),0)]),(lambda t,x:t*t-x*x,[(0,0),(0,1)])]):
 lines=[r'\begin{minipage}[t]{.32\textwidth}\centering',r'\begin{tikzpicture}[x=1.05cm,y=.77cm,>=stealth]',r'\clip (-2.2,-2.7) rectangle (2.2,2.7);',r'\draw[->] (-2.05,0)--(2.05,0) node[below left]{$t$};',r'\draw[->] (0,-2.5)--(0,2.5) node[below left]{$x$};']
 for t in np.arange(-1.8,2,.3):
  for x in np.arange(-2.1,2.2,.3):
   slope=f(float(t),float(x));norm=math.sqrt(1+slope*slope);dt=.085/norm;dx=slope*dt
   lines.append(r'\draw[gray!55,->,line width=.23pt] '+f'({t-dt:.4f},{x-dx:.4f})--({t+dt:.4f},{x+dx:.4f});')
 for m,(t0,x0) in enumerate(initials):
  color=['blue!80!black','red!80!black','green!50!black'][m]
  for end in [-2.,2.]:
   def event(t,z):return 3.0-abs(z[0])
   event.terminal=True
   sol=solve_ivp(lambda t,z:[f(t,z[0])],(t0,end),[x0],max_step=.025,rtol=1e-10,atol=1e-12,events=event)
   lines.append(stroke(zip(sol.t,sol.y[0]),color))
  lines.append(r'\fill['+color+f'] ({t0:.5f},{x0:.5f}) circle (1.7pt);')
 lines.extend([r'\end{tikzpicture}',r'\par\small ('+str(j+1)+r')\end{minipage}'])
 plots.append('\n'.join(lines))
(ROOT/'direction-fields.tex').write_text(r'\begin{center}'+'\n'+r'\hfill'.join(plots)+'\n'+r'\end{center}'+'\n'+r'\noindent{\small 蓝线分别从$(0,0)$出发；红线依次对应$(0,-1),(0,-1/2),(0,1)$；中图绿线从$(\sqrt2,0)$出发。图示仅显示有限窗口内的曲线段，不表示端点就是最大存在区间端点。}',encoding='utf-8')
# Dipole field, normalized to arclength; each streamline ends before the negative pole.
def B(x,y):
 r1=((x+1)**2+y*y)**1.5;r2=((x-1)**2+y*y)**1.5
 return ((x+1)/r1-(x-1)/r2,y*(1/r1-1/r2))
lines=[r'\begin{center}\begin{tikzpicture}[x=1.75cm,y=1.3cm,>=stealth]',r'\clip (-3,-2.4) rectangle (3,2.4);',r'\draw[gray,->] (-2.9,0)--(2.9,0) node[below left]{$x$};',r'\draw[gray,->] (0,-2.3)--(0,2.3) node[below left]{$y$};']
for x in np.arange(-2.6,2.7,.4):
 for y in np.arange(-2,2.1,.4):
  if min(math.hypot(x+1,y),math.hypot(x-1,y))<.2:continue
  bx,by=B(x,y);q=math.hypot(bx,by);dx=.075*bx/q;dy=.075*by/q
  lines.append(r'\draw[gray!55,->,line width=.25pt]'+f'({x-dx:.4f},{y-dy:.4f})--({x+dx:.4f},{y+dy:.4f});')
for theta in [15,35,55,75,95,115,135,155]:
 for sign in [-1,1]:
  th=math.radians(theta);p=[-1+.025*math.cos(th),sign*.025*math.sin(th)]
  def fun(s,z):
   bx,by=B(*z);q=math.hypot(bx,by);return [bx/q,by/q]
  def pole(s,z):return math.hypot(z[0]-1,z[1])-.025
  pole.terminal=True;pole.direction=-1
  sol=solve_ivp(fun,(0,20),p,max_step=.025,rtol=1e-9,atol=1e-11,events=pole)
  lines.append(stroke(zip(sol.y[0],sol.y[1]),'blue!70!black','line width=.65pt'))
lines.extend([r'\fill[red] (-1,0) circle (2pt) node[above left,black]{$+1$};',r'\fill[blue] (1,0) circle (2pt) node[above right,black]{$-1$};',r'\end{tikzpicture}\end{center}'])
(ROOT/'magnetic-field.tex').write_text('\n'.join(lines),encoding='utf-8')
lines=[r'\begin{center}\begin{tikzpicture}[x=3.5cm,y=1.25cm]',r'\draw[->] (-1.1,0)--(1.15,0) node[right]{$t$};',r'\draw[->] (0,0)--(0,3) node[above]{$x$};']
lines.append(stroke([(t,math.exp(t)) for t in np.linspace(-1,1,150)],'blue'))
pts=[(k/4,1.25**k if k>=0 else .75**(-k)) for k in range(-4,5)]
lines.append(stroke(pts,'red'))
for x,y in pts:lines.append(f'\\fill[red] ({x:.5f},{y:.5f}) circle (1.1pt);')
lines.extend([r'\node[blue] at (.65,2.8){$\e^t$};',r'\node[red] at (-.65,1.1){Euler折线};',r'\end{tikzpicture}\end{center}'])
(ROOT/'euler-plot.tex').write_text('\n'.join(lines),encoding='utf-8')
print('3 direction plots, dipole plot and Euler plot generated as TikZ')
