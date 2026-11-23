from pathlib import Path
import sympy as S
import json
R=Path(__file__).resolve().parents[1]
x,y,t,p,u=S.symbols('x y t p u',real=True)
C,A,B,k=S.symbols('C A B k',real=True)
checks=[]
def zero(name,expr):
 r=S.simplify(S.trigsimp(S.expand(expr)))
 ok=r==0
 checks.append({'name':name,'passed':ok,'residual':str(r)})
 if not ok:print('FAIL',name,r)
def expcheck(name,Y,f):zero(name,S.diff(Y,x)-f.subs(y,Y))
def imp(name,F,M,N):zero(name,S.diff(F,x)*N-S.diff(F,y)*M)
def par(name,X,Y,eq):
 pr=S.cancel(S.diff(Y,p)/S.diff(X,p))
 zero(name,eq.subs({x:X,y:Y,u:pr},simultaneous=True))
# All first-order separable exercises, checked against original differential forms.
imp('2.1.2(1)',x*x+y*y,x,y)
expcheck('2.1.2(2)',-1/(S.sin(x)+C),y*y*S.cos(x))
expcheck('2.1.2(3)',C*S.exp(x*x),2*x*y)
imp('2.1.2(4)',(1+x*x)*(1+y*y)/x**2,-(1+y*y),x*y*(1+x*x))
expcheck('2.1.2(5)',-S.log(S.exp(-4*x)/2+C)/2,S.exp(2*y-4*x))
expcheck('2.1.2(6)',S.log((x-1)/(x+1)),2/(x*x-1))
expcheck('2.1.2(7)',(1+C*S.exp(x))/(1-C*S.exp(x)),(y*y-1)/2)
imp('2.1.2(8)',S.tan(y)-S.exp(x),-S.exp(x)*S.cos(y)**2,1)
imp('2.1.2(9)',S.asin(y)-S.asin(x),-S.sqrt(1-y*y),S.sqrt(1-x*x))
expcheck('2.1.2(10)',-1/(x*x+C),2*x*y*y)
zero('2.1.2(11)',(x+1)*S.diff(C*(x+1)**2,x)-2*C*(x+1)**2)
imp('2.1.2(12)',y**3+S.exp(y)-S.sin(x),-S.cos(x),3*y*y+S.exp(y))
imp('2.1.2(13)',(x*x-1)*(y*y-1),x*(y*y-1),y*(x*x-1))
imp('2.1.3(1)',S.sin(y/x)/x,-(y/x+S.tan(y/x)),1)
X=x-1;Y=y-2
imp('2.1.3(2)',X*X-2*X*Y-Y*Y,-(x-y+1),x+y-3)
imp('2.1.3(3)',y/x-S.log(y),y*y,x*x-x*y)
imp('2.1.3(4)',(x+y+1)*S.exp(-y),-1,x+y)
imp('2.1.3(5)',(x-3)**2+(x+y-1)**2,2*x+y-4,x+y-1)
imp('2.1.3(6)',(x**3-2*y**3)/x,x**3+y**3,-3*x*y*y)
imp('2.1.3(7)',(x-y)**2+2*x,-(x-y+1),x-y)
imp('2.1.3(8)',y*y/x**2-2*S.log(x),-(x*x+y*y),x*y)
imp('2.1.3(9)',(x-y-2)**2+14*x,-(x-y+5),x-y-2)
imp('2.1.3(10)',S.log(y+2)+2*S.atan((y+2)/(x-3)),-2*(y+2)**2,(x+y-1)**2)
# Square-root equations checked in coordinates satisfying the required sign constraints.
z=S.symbols('z',positive=True)
zero('2.1.3(11) positive phase',S.diff(x*(S.log(x)+C)**2,x)-(2*(S.log(x)+C)+(S.log(x)+C)**2))
imp('2.1.3(12)',S.log((x+3)**2+(y+1)**2)/2+S.atan((y+1)/(x+3)),-(y-x-2),x+y+4)
Y=x+2*x/(C-S.log(x));zero('2.1.3(13)',2*x*x*S.diff(Y,x)-x*x-Y*Y)
imp('2.1.3(14)',-S.cos(x+y+1)/(1+S.sin(x+y+1))-x,-S.sin(x+y+1),1)
zero('2.1.3(15) positive x phase',S.diff(x*S.sin(S.log(x)+C),x)-(S.cos(S.log(x)+C)+S.sin(S.log(x)+C)))
for n,Y,aa,bb,rr in [
 (1,S.Rational(2,3)*(x+1)**S.Rational(7,2)+C*(x+1)**2,1,-2/(x+1),(x+1)**S.Rational(5,2)),
 (2,(C-S.cos(x))/x,1,1/x,S.sin(x)/x),
 (3,(S.exp(x)+C)/x,x,1,S.exp(x)),
 (4,-S.Rational(1,3)+2/x+C/x**3,x*x,3*x,4-x),
 (5,(x+1)*(S.log(x+1)+C)+1,x+1,-1,x),
 (6,C*S.exp(x*x)-S.Rational(1,2),1,-2*x,x)]:
 zero(f'2.1.4({n})',aa*S.diff(Y,x)+bb*Y-rr)
imp('2.1.5(1)',x/y**2+S.log(y),-y,2*x-y*y)
imp('2.1.5(2)',x*y-y**4/4,y,x-y**3)
# Parametrized x(y) for 2.1.5(3), A positive: sqrt is explicitly (Ay^2+1/A)/2.
X=(A*y*y-1/A)/2
zero('2.1.5(3)',y*S.diff(X,y)-X-(A*y*y+1/A)/2)
imp('2.1.6(1)',y+S.exp(y)-S.sin(x),-S.cos(x),1+S.exp(y))
imp('2.1.6(2)',(1+y*y)/(1+x*x),-x*(1+y*y),y*(1+x*x))
imp('2.1.6(3)',y*y/2-S.log(1+S.exp(x)),-S.exp(x),(1+S.exp(x))*y)
expcheck('2.1.6(4)',S.Rational(3,2)*S.exp(S.cos(x)-1),-y*S.sin(x))
expcheck('2.1.6(5)',S.log(x*x/2+x**4/4+S.E-S.Rational(3,4)),(x+x**3)*S.exp(-y))
expcheck('2.1.6(6)',S.Rational(1,2)+S.Rational(3,2)*S.exp(1-x*x),x-2*x*y)
for i,Y,f in [(1,8*x**6/(x**8+C),6*y/x-x*y*y),(2,1/(x*(C-S.log(x)**2/2)),y*y*S.log(x)-y/x),(4,1/(1-x*x+C*S.exp(-x*x)),2*x*y+2*x**3*y*y)]:expcheck(f'2.1.7({i})',Y,f)
U=x*x*(S.log(x)+C);zero('2.1.7(3) positive root',x*S.diff(U*U,x)-4*U*U-2*x*x*U)
expcheck('2.1.8',x/S.sqrt(1+x*x),S.sqrt(1-y*y)/(1+x*x))
expcheck('2.1.9',24/x,-y/x)
exact=[
 (x**3+3*x*x*y*y+y**4,3*x*x+6*x*y*y,6*x*x*y+4*y**3),
 (S.sin(x)+x/y+S.log(y),S.cos(x)+1/y,1/y-x/y**2),
 (x**5+S.Rational(3,2)*x*x*y*y-x*y**3+y**3/3,5*x**4+3*x*y*y-y**3,3*x*x*y-3*x*y*y+y*y),
 (x**3/3+x*y+y*y/2,x*x+y,x+y),
 (3*x*x+x*y+2*x+4*y*y-3*y,6*x+y+2,x+8*y-3),
 (x*x*y/2+S.log(y),x*y,x*x/2+1/y),
 (x**3-2*x*y*y+y,3*x*x-2*y*y,1-4*x*y),
 ((x*x+y*y)**2/4,x**3+x*y*y,x*x*y+y**3),
 (3*x*y+S.exp(x)+S.sin(y),3*y+S.exp(x),3*x+S.cos(y))]
for i,(F,M,N) in enumerate(exact,1):
 zero(f'2.2.1({i}) potential x',S.diff(F,x)-M);zero(f'2.2.1({i}) potential y',S.diff(F,y)-N)
for name,F,M,N in [
 ('2.2.2(1)',x**3*y+4*x*x*y*y+4*y**3,3*x*x*y+8*x*y*y,x**3+8*x*x*y+12*y*y),
 ('2.2.2(2)',x**4*S.exp(x+y)+x*x+y*y,4*x**3*S.exp(x+y)+x**4*S.exp(x+y)+2*x,x**4*S.exp(x+y)+2*y),
 ('2.2.4(1)',x/y+S.log(y),y,y-x),
 ('2.2.4(2)',S.sqrt(x*x+y*y)-x,x-S.sqrt(x*x+y*y),y),
 ('2.2.4(3)',x-S.atan(y/x),x*x+y*y+y,-x),
 ('2.2.4(4)',S.exp(x)*(x*x*y+y**3/3),2*x*y+x*x*y+y**3/3,x*x+y*y),
 ('2.2.4(5)',x*x*S.log(y)+(1+y*y)**S.Rational(3,2)/3,2*x*y*S.log(y),x*x+y*y*S.sqrt(1+y*y)),
 ('2.2.7',-x*x*S.cos(x)+2*x*S.sin(x)+2*S.cos(x)+C*y*y/2,x*x*S.sin(x),C*y),
 ('2.2.8',x**4/4+x*x*y/2+C*y,x*x+y,x/2+C/x),
 ('2.2.9',S.exp(-x)*S.sin(y)+x,S.exp(x)/S.cos(y)-S.tan(y),1)]:imp(name,F,M,N)
# Implicit first-order equations: parametrized or explicit solution verification.
par('2.4.1(1)',p*p+2*p,S.Rational(2,3)*p**3+p*p+C,u*u+2*u-x)
for name,Y,eq in [
 ('2.4.1(2) family',x*x/2+C*x+C*C,y-u*u+x*u-x*x/2),
 ('2.4.1(2) singular',x*x/4,y-u*u+x*u-x*x/2),
 ('2.4.1(3)',x-C+1/(x-C),y*y*(1-u)-(2-u)**2),
 ('2.4.1(4) family',C*(x-C)**2,u**3-4*x*y*u+8*y*y),
 ('2.4.1(4) singular',4*x**3/27,u**3-4*x*y*u+8*y*y),
 ('2.4.2(1)',S.sin(x+C),u*u+y*y-1),
 ('2.4.2(2) family',C*x+1/C,x*u*u-y*u+1),
 ('2.4.2(3)',(x-C)**2/4,y-u*u),
 ('2.4.4',1-x,x*u+u*u-y)]:zero(name,eq.subs({y:Y,u:S.diff(Y,x)},simultaneous=True))
# Folium parametric expression is checked using derivative from the integrated expression.
Y=3*p/(1+p**3);dx=(1-2*p**3)/(p*p*(1+p**3));pr=S.cancel(S.diff(Y,p)/dx)
zero('2.4.1(5)',Y**3+pr**3-3*Y*pr)
par('2.4.2(4)',C+4*p*p/9,C+8*p**3/27,x-y-4*u*u/9+8*u**3/27)
# Higher-order differential residuals.
def high(name,Y,expr):
 derivatives={S.Symbol('d'+str(n)):S.diff(Y,x,n) for n in range(1,6)}
 derivatives[y]=Y;zero(name,expr.subs(derivatives,simultaneous=True))
d1,d2,d3,d4,d5=S.symbols('d1 d2 d3 d4 d5')
for name,Y,eq in [
 ('2.4.3(1)',A*x**5+B*x**3+C*x*x+k*x+1,d5-d4/x),
 ('2.4.3(2)',S.sqrt(A*x+B),y*d2+d1*d1),
 ('2.4.3(3)',A*(x+x**3/3)+B,(1+x*x)*d2-2*x*d1),
 ('2.4.3(4)',A*S.exp(k*x),y*d2-d1*d1),
 ('2.4.3(5)',(x-A)**3/12+B,d2*d2-d1),
 ('2.4.3(6)',1+A*S.exp(B*x),d2+d1*d1/(1-y)),
 ('2.4.3(7)',A*S.exp(x/2)+B*S.exp(-x/2)+C*x+k,4*d4-d2),
 ('2.4.3(8)a',-x/A+(1+A*A)/A**2*S.log(1+A*x)+B,(1+x*x)*d2+d1*d1+1),
 ('2.4.3(8)b',-x*x/2+B,(1+x*x)*d2+d1*d1+1),
 ('2.4.3(8)c',S.log(x)+B,(1+x*x)*d2+d1*d1+1),
 ('2.4.3(9)',A*S.exp(k*x)+B,d1*d3-d2*d2)]:high(name,Y,eq)
# Chapter 3
At=S.Matrix([[2*t**3+1,t*t],[t,4*t*t]])
zero('3.1.2 det derivative',S.diff(At.det(),t)-(40*t**4-3*t*t+8*t))
zero('3.1.2 derivative det',At.diff(t).det()-(48*t**3-2*t))
Y=S.sin(t)/t;zero('3.4.3',S.diff(Y,t,2)+2/t*S.diff(Y,t)+Y)
for label,sign in [('5.1.4',-1),('5.1.5',1)]:
 ph1=sign*t*t/2;ph2=ph1+t**5/20;ph3=ph2+sign*t**8/160+t**11/4400
 zero(label+' Picard',S.diff(ph3,t)-ph2**2-sign*t)
ph2=1+t+t*t+t**3/3;ph3=1+t+t*t+t**3+2*t**4/3+t**5/3+t**6/9+t**7/63
zero('5.1.3 Picard',S.diff(ph3,t)-ph2**2)
# Chapter 4 scalar characteristic polynomials and particular solutions
r=S.symbols('r')
for n,P,fact in [(1,r*r+4,(r-2*S.I)*(r+2*S.I)),(2,r**3-r*r+2*r-2,(r-1)*(r*r+2)),(3,r**4+4,(r*r-2*r+2)*(r*r+2*r+2)),(4,r**4-2*r**3+2*r-1,(r-1)**3*(r+1)),(5,r*r+4*r+4,(r+2)**2),(6,r*r+2*r+4,(r+1)**2+3),(7,r**3+4*r,r*(r*r+4)),(8,r**4+8*r*r+16,(r*r+4)**2)]:zero(f'4.1.1({n}) factor',P-fact)
def op(Y,coeff):return sum(c*S.diff(Y,t,j) for j,c in enumerate(coeff))
for n,Y,coeff,f in [
 (1,t**3/3-t*t+3*t,[0,1,1],1+t*t),
 (2,t*S.sin(2*t)/4-S.cos(4*t)/12,[4,0,1],S.cos(2*t)+S.cos(4*t)),
 (3,-t*t*S.cos(2*t)/8+t*S.sin(2*t)/16,[4,0,1],t*S.sin(2*t)),
 (4,t**3/9+4*t*t/9+26*t/27,[0,3,-4,1],t*t),
 (5,-S.exp(2*t)*S.sin(S.exp(-t)),[2,-3,1],S.sin(S.exp(-t))),
 (6,S.exp(3*t)/2,[-4,8,-5,1],S.exp(3*t)),
 (7,S.exp(t*t),[-2,0,1],4*t*t*S.exp(t*t)),
 (8,t**3*S.exp(t)/6,[1,-2,1],t*S.exp(t))]:zero(f'4.2.1({n})',op(Y,coeff)-f)
# Vector eigensystems: all 7 systems including real/complex basis vectors.
mats=[S.Matrix([[-3,48,-28],[-4,40,-22],[-6,57,-31]]),S.Matrix([[0,1],[1,0]]),S.Matrix([[-5,-10,-20],[5,5,10],[2,4,9]]),S.Matrix([[3,-1,0],[-4,-1,0],[4,-8,-2]]),S.Matrix([[9,-5,0],[0,-1,5],[0,-1,5]]),S.Matrix([[3,-2,0],[-2,3,0],[0,0,5]]),S.Matrix([[2,1,3],[0,2,-1],[0,0,2]])]
lp=1+2*S.sqrt(2);lm=1-2*S.sqrt(2)
def v(l):return [l+2,(3-l)*(l+2),8*l-20]
spec=[[(1,[3,2,3]),(2,[4,1,1]),(3,[2,2,3])],[(1,[1,1]),(-1,[1,-1])],[(5,[-2,0,1]),(2+S.I,[-3-S.I,-2+S.I,2])],[(-2,[0,0,1]),(lp,v(lp)),(lm,v(lm))],[(0,[25,45,9]),(4,[1,1,1]),(9,[1,0,0])],[(1,[1,1,0]),(5,[1,-1,0]),(5,[0,0,1])],[(2,[1,0,0])]]
for i,(mat,sp) in enumerate(zip(mats,spec),1):
 for j,(lam,vec) in enumerate(sp):
  z=mat*S.Matrix(vec)-lam*S.Matrix(vec)
  for m,el in enumerate(z):zero(f'4.3.3({i}) vector{j} row{m}',el)
# Triangular repeated-root system, checked as a full fundamental matrix.
mat=mats[-1];F=S.exp(2*t)*S.Matrix([[1,t,3*t-t*t/2],[0,1,-t],[0,0,1]])
for j,el in enumerate(F.diff(t)-mat*F):zero('4.3.3(7) full matrix '+str(j),el)
zero('4.3.3(7) determinant',F.det()-S.exp(6*t))
# Full higher-order coupled example, not only eliminant.
x1=A*S.exp(t)+B*S.cos(t)+C*S.sin(t)-t-2+S.Rational(2,5)*S.exp(2*t)
x2=2*A*S.exp(t)+(B-C)*S.cos(t)+(B+C)*S.sin(t)-3*t-3+S.Rational(3,5)*S.exp(2*t)
zero('4.3.1 row1',S.diff(x1,t)-S.diff(x2,t)+x1+t)
zero('4.3.1 row2',S.diff(x1,t,2)-S.diff(x2,t)+3*x1-x2-S.exp(2*t))
# Initial conditions for every explicitly written IVP.
for name,Y,t0,y0 in [('1.2.1',2*S.exp(-3*t)+2*t+1,0,3),('2.1.6(2)',-S.sqrt(1+2*t*t),0,-1),('2.1.6(4)',S.Rational(3,2)*S.exp(S.cos(t)-1),0,S.Rational(3,2)),('2.1.6(5)',S.log(t*t/2+t**4/4+S.E-S.Rational(3,4)),1,1),('2.1.6(6)',S.Rational(1,2)+S.Rational(3,2)*S.exp(1-t*t),1,2),('5.1.6',2*S.exp(t)-t-2,0,0),('5.3.5(1)',t*S.log(t),1,0),('5.3.5(2)',(1+S.exp(t))/(1-S.exp(t)),S.log(2),-3)]:zero(name+' IV',Y.subs(t,t0)-y0)
# Coefficient recurrence verified by finite polynomial residual through all determined orders.
a0,a1=S.symbols('a0 a1');arr=[a0,a1,0]
for n in range(12):arr.append(arr[n]/((n+3)*(n+2)))
pol=sum(a*t**j for j,a in enumerate(arr))
for j in range(len(arr)-2):zero('3.5.1 coeff'+str(j),S.expand(S.diff(pol,t,2)-t*pol).coeff(t,j))
arr=[S.Integer(10),S.Integer(3)]
for n in range(12):arr.append(S.Rational(n+3,n+2)*arr[n])
pol=sum(a*t**j for j,a in enumerate(arr))
for j in range(len(arr)-2):zero('3.5.2 coeff'+str(j),S.expand((t*t-1)*S.diff(pol,t,2)+5*t*S.diff(pol,t)+3*pol).coeff(t,j))
for n in range(8):
 H=S.factorial(n)*sum((-1)**j*(2*t)**(n-2*j)/(S.factorial(j)*S.factorial(n-2*j)) for j in range(n//2+1))
 zero('3.5.3 Hermite n='+str(n),S.diff(H,t,2)-2*t*S.diff(H,t)+2*n*H)
report={'count':len(checks),'passed':sum(c['passed'] for c in checks),'checks':checks}
(R/'qa'/'symbolic-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('SYMBOLIC',report['passed'],'/',report['count'])
assert report['passed']==report['count']
