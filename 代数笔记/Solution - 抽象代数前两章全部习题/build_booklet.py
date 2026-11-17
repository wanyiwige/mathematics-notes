from pathlib import Path
import re, json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
REVIEW = ROOT / 'Solution - 抽象代数集中测验复习'
P = ROOT / 'chapters' / 'Part 2'
proofs, ideas, hints, questions, deps = {}, {}, {}, {}, {}

def add(c,n,idea,proof,hint,question=None,refs=''):
    k=(c,n); ideas[k]=idea; proofs[k]=proof; hints[k]=hint
    if question: questions[k]=question
    if refs: deps[k]=refs

# 以下扩写保留原习题文件中的构造和推理顺序。
add(1,3,'先用有限集上单射等价于满射，构造单侧单位元，再把它们合并为双侧单位元。',r'''
记给定集合为$G$。固定$a\in G$，由左右消去律，映射$x\mapsto ax$及$x\mapsto xa$均为$G$到自身的单射。$G$有限，故这两个映射也满射，因而存在$e,f\in G$满足$ae=a$、$fa=a$。

任取$x\in G$，结合律给出
\begin{align*}
a(ex)&=(ae)x=ax,\\
(xf)a&=x(fa)=xa.
\end{align*}
分别使用左、右消去律，得$ex=x$及$xf=x$。所以$e$是整个集合的左单位元，$f$是右单位元。于是$ef=f$且$ef=e$，从而$e=f$为双侧单位元。

对任意$g\in G$，左右乘$g$的映射满射，故可取$b,c\in G$使$gb=e$、$cg=e$。由
\[
c=ce=c(gb)=(cg)b=eb=b
\]
可知$gb=bg=e$。每个元素都有双侧逆元，故$G$为群。

有限性不能删去：正整数集在加法下结合且满足两侧消去律，但没有加法单位元，故不是群。''',r'尚未构造出群时，只能使用题设的消去律和结合律，不能预先使用逆元。',refs='group,glaws')
add(1,5,'沿原解选取两个相邻对换，分别计算两个表达式。',r'''
在$S_3$中取$x=(12)$、$y=(23)$。它们都是对换，所以$x^2=y^2=e$，从而$x^2y^2=e$。

按右边先作用的约定，$xy$将$1,2,3$依次映为$2,3,1$，故$xy=(123)$。因此
\[
(xy)^2=(132)\ne e=x^2y^2.
\]
这说明一般群中平方公式$(xy)^2=x^2y^2$不成立。''',r'计算置换乘积时始终从右边开始作用。',r'举例说明群中一般不成立$(xy)^2=x^2y^2$。',refs='cycles')
add(1,11,'先用乘法关系验证子群，再用元素的阶排除与四次单位根群同构。',r'''
令$u=(12)(34)$、$v=(13)(24)$、$w=(14)(23)$。分别作用于$1,2,3,4$可得
\[
u^2=v^2=w^2=e,\qquad uv=vu=w.
\]
由于$w=uv$且$u,v$交换，还可得到$uw=wu=v$、$vw=wv=u$。所以$B=\{e,u,v,w\}$对乘法封闭，每个元素的逆元仍属于$B$；由子群判别法，$B\leq S_4$。这就是克莱因四元群，记作$V_4$。

另一方面，四次单位根群$U_4=\{1,i,-1,-i\}$含有4阶元素$i$，而$B$中三个非单位元的阶均为2。同构保持元素的阶，因此$B\not\cong U_4$。''',r'两个群阶相同，只是同构的必要条件；还需比较元素阶或具体乘法。',refs='subgroup,iso,cycles')
add(1,13,'按取逆把元素配对，再利用群阶的奇偶性。',r'''
设$|G|$为偶数。令$T=\{x\in G:x\ne x^{-1}\}$。若$x\in T$，则$x^{-1}\in T$；取逆将$T$分成互不相交的二元集合$\{x,x^{-1}\}$，所以$|T|$为偶数。

因此$G\setminus T=\{x\in G:x=x^{-1}\}$的元素个数也是偶数。该集合已含单位元$e$，故其元素个数是正偶数，至少为2。可取$a\ne e$使$a=a^{-1}$，于是$a^2=e$。

$a\ne e$排除了1阶情形，而$a^2=e$说明其阶整除2，故$\ord(a)=2$。''',r'取逆的不动点包括单位元，须由偶数计数证明还存在另一个不动点。',r'证明偶数阶有限群中存在2阶元素。',refs='order,glaws')
add(1,14,'核对矩阵满足二面体群的关系，并证明所列的两类矩阵恰有$2n$个。',r'''
直接进行矩阵乘法可得
\[
A^2=E,\qquad B^n=E,\qquad AB=B^{-1}A.
\]
$\zeta$的阶为$n$，故$B$的阶也为$n$。令$H=\{B^k,AB^k:0\leq k<n\}$。由$B^iA=AB^{-i}$，任意两个规定形状的矩阵相乘，分别有
\begin{align*}
B^iB^j&=B^{i+j},& B^i(AB^j)&=AB^{j-i},\\
(AB^i)B^j&=AB^{i+j},&(AB^i)(AB^j)&=B^{j-i}.
\end{align*}
指数均可模$n$化简，所以$H$对乘法封闭。又$(B^i)^{-1}=B^{-i}$，且$(AB^i)^2=E$，所以$H$对取逆封闭，且含$E$，故为群。

$B^0,\ldots,B^{n-1}$两两不同；左乘可逆矩阵$A$可知$AB^0,\ldots,AB^{n-1}$也两两不同。前一类是可逆对角矩阵，后一类是可逆反对角矩阵，两类不交，因而$|H|=2n$。

原笔记中$D_n$的元素为$T^k,ST^k$，并满足$T^n=S^2=e$及$ST=T^{-1}S$。定义$T^k\mapsto B^k$、$ST^k\mapsto AB^k$，所得映射为双射；两边乘法的四种情形均由上述相同关系给出，所以它保持乘法，故$D_n\cong H$。''',r'验证同构时，既要核对关系，也要说明正规形的唯一性和映射的双射性。',refs='dihedral,subgroup,iso')
add(1,15,'分别比较相邻的两个指数公式，得到$a$与$b^i,b^{i+1}$交换。',r'''
任取$a,b\in G$。比较指数$i$和$i+1$的公式，得到
\[
a^{i+1}b^{i+1}=(ab)^{i+1}=(ab)^i ab=a^ib^iab.
\]
在等式两边先左消去$a^i$，再右消去$b$，即得$ab^i=b^ia$。再把$i$换为$i+1$，比较指数$i+1,i+2$，同样得$ab^{i+1}=b^{i+1}a$。

由$a$与$b^i$交换，有$a(b^i)^{-1}=(b^i)^{-1}a$。于是
\begin{align*}
ab&=a(b^i)^{-1}b^{i+1}\\
&=(b^i)^{-1}ab^{i+1}\\
&=(b^i)^{-1}b^{i+1}a=ba.
\end{align*}
因为$a,b$任意，$G$为交换群。''',r'只比较两个相邻指数先得到与某个幂交换；第三个指数使这两个幂的指数差为1。',refs='glaws,powers')
add(1,16,'直接计算两个矩阵的幂，再把乘积的所有正整数次幂写出来。',r'''
首先$\det A=\det B=1$，故$A,B\in\SL_2(\Q)$。矩阵乘法给出
\[
A^2=-E,\quad A^4=E,\qquad
B^2=\begin{pmatrix}-1&-1\\1&0\end{pmatrix},\quad B^3=E.
\]
$A\ne E$且$A^2\ne E$，所以$A$的阶恰为4；$B\ne E$且$B^3=E$，所以$B$的阶恰为3。

另一方面，
\[
AB=\begin{pmatrix}1&1\\0&1\end{pmatrix}.
\]
对$m$归纳：当$m=1$公式成立；若$(AB)^m=\left(\begin{smallmatrix}1&m\\0&1\end{smallmatrix}\right)$，则再乘$AB$得$(AB)^{m+1}=\left(\begin{smallmatrix}1&m+1\\0&1\end{smallmatrix}\right)$。因此对每个正整数$m$，
\[
(AB)^m=\begin{pmatrix}1&m\\0&1\end{pmatrix}\ne E.
\]
故$AB$为无限阶元素。''',r'群中两个有限阶元素的积未必有有限阶，交换性在相关结论中不能省略。',refs='order')
add(1,17,'使用子群判别法；有限阶元素之差的乘法记号是$ab^{-1}$。',r'''
记$T$为$G$中全部有限阶元素的集合。单位元有1阶，故$T\ne\varnothing$。

任取$a,b\in T$，存在正整数$m,n$使$a^m=b^n=e$。由于$G$交换，$a$与$b^{-1}$也交换，故
\[
(ab^{-1})^{mn}=a^{mn}b^{-mn}=(a^m)^n(b^n)^{-m}=e.
\]
因此$ab^{-1}$的阶有限，属于$T$。由子群判别法，$T\leq G$。

交换性不能去掉：第一章习题16中$A,B$均为有限阶，但$AB$为无限阶。因此在该非交换群中，全部有限阶元素组成的集合对乘法不封闭。''',r'证明有限阶只需找到一个正幂等于单位元，不必计算其最小正指数。',refs='subgroup,powers')
add(1,19,'先分清只含旋转的子群与含反射的子群，再用正规性限制参数。',r'''
沿用$D_n=\{T^k,ST^k:0\leq k<n\}$及$ST=T^{-1}S$。设$H\leq D_n$。

先说明旋转子群中的子群形式。设$K\leq\langle T\rangle$，因为$T^n=e\in K$，可取最小正整数$d$使$T^d\in K$。若$T^l\in K$，把$l$写成$qd+r$，$0\leq r<d$，则$T^r=T^l(T^d)^{-q}\in K$。由$d$的最小性只能$r=0$，所以$K=\langle T^d\rangle$；对$l=n$使用同一结论得$d\mid n$。

若$H\subseteq\langle T\rangle$，由上段可写$H=\langle T^d\rangle$，$d\mid n$。用$T$共轭不改变该子群，用$S$共轭把$T^d$变为$T^{-d}$，仍生成同一子群。由于$S,T$生成$D_n$，这样的子群全都正规。

若$H$含反射$ST^k$，写$H\cap\langle T\rangle=\langle T^d\rangle$，$d\mid n$。对$H$中任意另一反射$ST^l$，有
\[
(ST^k)(ST^l)=T^{l-k}\in H\cap\langle T\rangle,
\]
所以$d\mid l-k$。因此
\[
H=\langle T^d,ST^k\rangle,
\]
且$k$只需模$d$取值。这也证明上述形式已穷尽含反射的子群。

若这样的$H$正规，则$T(ST^k)T^{-1}=ST^{k-2}\in H$，由刚才的判据得$d\mid2$。若$d=1$，则$H=D_n$；若$d=2$，须$n$为偶数，且$k$模2只有0、1两种，得到
\[
\langle T^2,S\rangle,\qquad\langle T^2,ST\rangle.
\]
这两个子群均有$n$个元素，指数为2，由第一章习题12可知它们正规。

综上，全部正规子群为$\langle T^d\rangle$（$d\mid n$）、$D_n$，以及$n$为偶数时另有的上述两个指数2子群。''',r'必要条件$d\mid2$得到候选后，还须验证每个候选确实正规。',refs='dihedral,cyclic,normal')
add(1,20,'用集合取逆公式证明必要性，再分别验证乘法和取逆封闭。',r'''
若$HK$为子群，则它对取逆封闭，因而
\[
HK=(HK)^{-1}=K^{-1}H^{-1}=KH.
\]
这里使用$H^{-1}=H$、$K^{-1}=K$。

反之，设$HK=KH$。$e=ee\in HK$，故$HK$非空。集合乘法的结合律给出
\begin{align*}
(HK)(HK)&=H(KH)K=H(HK)K\\
&=(HH)(KK)=HK.
\end{align*}
所以$HK$对乘法封闭。又$(HK)^{-1}=KH=HK$，故对取逆封闭。由子群判别法，$HK$为子群。''',r'集合相等$HK=KH$不要求每个$h\in H$与每个$k\in K$交换。',refs='setproduct,subgroup')
add(1,23,'先分别验证两个子群，再将中心化子中的元素作共轭。',r'''
两集合均含$e$。若$x,y\in C_G(S)$，则对任意$a\in S$，$y^{-1}a=ay^{-1}$，从而
\[
(xy^{-1})a=xay^{-1}=axy^{-1}.
\]
故$xy^{-1}\in C_G(S)$，子群判别法给出$C_G(S)\leq G$。

若$x,y\in N_G(S)$，则$x^{-1}Sx=S$、$y^{-1}Sy=S$，后式也给出$ySy^{-1}=S$。于是
\[
(xy^{-1})^{-1}S(xy^{-1})=y(x^{-1}Sx)y^{-1}=ySy^{-1}=S.
\]
所以$N_G(S)$也是子群。若$c\in C_G(S)$，则对所有$a\in S$有$c^{-1}ac=a$，故$c^{-1}Sc=S$，说明$C_G(S)\leq N_G(S)$。

最后任取$n\in N_G(S)$、$c\in C_G(S)$。因为$n^{-1}an\in S$，对每个$a\in S$都有
\begin{align*}
(ncn^{-1})a&=nc(n^{-1}an)n^{-1}\\
&=n(n^{-1}an)cn^{-1}=a(ncn^{-1}).
\end{align*}
故$ncn^{-1}\in C_G(S)$。由正规性判别，$C_G(S)\trianglelefteq N_G(S)$。''',r'正规化子只要求共轭后整个集合不变；中心化子要求其中每个元素都被固定。',refs='subgroup,normal')
add(1,24,'用拉格朗日定理确定非单位元的阶，直接写出同构。',r'''
设$G=\{e,a\}$。由拉格朗日定理，$\ord(a)\mid2$；$a\ne e$，所以$\ord(a)=2$，即$a^2=e$。

定义$\varphi:G\to\{1,-1\}$为$\varphi(e)=1$、$\varphi(a)=-1$。它是双射。涉及$e$的乘积显然保持；剩下的$a^2=e$对应$(-1)^2=1$，所以$\varphi$也保持这一乘积，故为群同构。''',r'两元素群的乘法由单位元性质和$a^2=e$唯一确定。',r'证明任意2阶群均同构于乘法群$\{1,-1\}$。',refs='lagrange,iso')
add(1,25,'按是否存在4阶元素分类；不存在时确定全部乘法。',r'''
设$|G|=4$。若存在4阶元素$a$，则$\langle a\rangle$已有4个元素，所以$G=\langle a\rangle\cong\Z/4\Z$。

若不存在4阶元素，由拉格朗日定理，每个非单位元都只能为2阶，故所有$x\in G$均满足$x^2=e$。第一章习题2给出$G$交换。取两个不同的非单位元$a,b$。若$ab=e$，则$b=a^{-1}=a$，矛盾；若$ab=a$或$ab=b$，消去得$b=e$或$a=e$，也矛盾。因此$e,a,b,ab$两两不同，已穷尽$G$。

由$a^2=b^2=e$及$ab=ba$，映射
\[
(\bar i,\bar j)\longmapsto a^ib^j\quad
\text{从 }(\Z/2\Z)\times(\Z/2\Z)\text{ 到 }G
\]
良定义、保乘法且为双射，故$G\cong V_4$。

$\Z/4\Z$含4阶元素，而$V_4$没有，两者不同构。这证明4阶群恰有上述两种同构类型。''',r'分类必须穷尽，并且最后要证明两个候选不同构。',r'确定4阶群的全部同构类型。',refs='lagrange,cyclic,iso')
add(1,26,'素数阶使每个非单位元都生成全群，再写出循环群的同构。',r'''
设$|G|=p$，其中$p$为素数。任取$a\ne e$，由拉格朗日定理有$\ord(a)\mid p$，且$\ord(a)\ne1$，所以$\ord(a)=p$。因此$G=\langle a\rangle$。

定义$\varphi:\Z/p\Z\to G$，$\varphi(\bar k)=a^k$。若$k\equiv l\pmod p$，则$a^{k-l}=e$，所以$a^k=a^l$，映射良定义。又
\[
\varphi(\bar k+\bar l)=a^{k+l}=a^ka^l,
\]
故为同态。它满射；若$a^k=e$，则$p\mid k$，故核为$\{\bar0\}$，所以也单射。因此$G\cong\Z/p\Z$，任意两个$p$阶群均同构。''',r'素数阶结论中的素数$p$须相同，才可断言两个群同构。',r'证明任意两个相同素数阶的群同构。',refs='lagrange,cyclic,iso')
add(1,27,'沿原笔记把整数对嵌入矩阵环，借子环结构验证环公理。',r'''
令
\[
\varphi(a,b)=\begin{pmatrix}a&b\\b&a\end{pmatrix},\qquad
S=\left\{\begin{pmatrix}a&b\\b&a\end{pmatrix}:a,b\in\Z\right\}.
\]
$S$含零矩阵，两个此类矩阵之差仍有同样形状，而
\[
\begin{pmatrix}a&b\\b&a\end{pmatrix}
\begin{pmatrix}c&d\\d&c\end{pmatrix}
=\begin{pmatrix}ac+bd&ad+bc\\ad+bc&ac+bd\end{pmatrix}\in S.
\]
故由子环判别法，$S\leq M_2(\Z)$。映射$\varphi$是$\Z\times\Z$到$S$的双射，并且按题设两种运算有
\[
\varphi((a,b)+(c,d))=\varphi(a,b)+\varphi(c,d),\qquad
\varphi((a,b)(c,d))=\varphi(a,b)\varphi(c,d).
\]
所以题设运算使$\Z\times\Z$成为与$S$同构的环。

由乘法公式交换两对参数不改变结果，环是交换的；加法零元为$(0,0)$，负元为$(-a,-b)$，乘法单位元为$(1,0)$。但
\[
(1,1)(1,-1)=(0,0),
\]
两个因子均非零，故此环有零因子，不是整环。''',r'使用矩阵模型前，必须确认像确实为子环，并且模型保持题设的两种运算。',refs='subring,ringiso,zerodiv')
add(1,28,'先检查新加法能否构成交换群，任何一个公理失败即可否定。',r'''
若$\Z$在新运算下为环，则$(\Z,\oplus)$必须为交换群。由于$a\oplus b=ab$，新加法的单位元必须是整数$1$：它满足$a\oplus1=1\oplus a=a$。

然而整数$0$没有新加法逆元，因为对任意$x\in\Z$都有$0\oplus x=0x=0\ne1$。因此$(\Z,\oplus)$不是群，题设两种运算不能使$\Z$成环。''',r'环的零元指加法单位元，换运算后应重新确定，不能沿用整数0。',refs='ring,group')
add(1,31,'分别验证三项结论，严格区别左单位元、右单位元和双侧单位元。',r'''
\begin{enumerate}
\item 设$e$为左单位元、$f$为右单位元。由$e$的性质得$ef=f$，由$f$的性质得$ef=e$，所以$e=f$。这个共同元素同时满足两侧单位元条件。

\item 设$R$无零因子且$e$为左单位元。若$R=\{0\}$，唯一元素就是双侧单位元。若$R\ne\{0\}$，固定$b\ne0$。对任意$a\in R$，
\[
(ae-a)b=a(eb)-ab=ab-ab=0.
\]
因为$b\ne0$且无零因子，必有$ae-a=0$。所以$ae=a$对每个$a$成立，$e$也为右单位元。

\item 设$e$为左单位元，而$R$没有右单位元。若所有$a$均满足$ae=a$，则$e$就是右单位元，矛盾。因此存在$a$使$d=a-ae\ne0$。对任意$x\in R$，
\[
dx=(a-ae)x=ax-a(ex)=0.
\]
于是$(e+d)x=ex+dx=x$。所以$e+d$也是左单位元，且因$d\ne0$有$e+d\ne e$，从而左单位元至少有两个。
\end{enumerate}''',r'无零因子的消去必须有一个非零因子；第二项要单独交代零环。',r'''设$e_La=a$对所有$a\in R$成立时称$e_L$为左单位元，右单位元类似。证明：
\begin{enumerate}
\item 若环同时有左单位元和右单位元，则两者相等，为双侧单位元。
\item 无零因子的环若有左单位元，则它也为右单位元。
\item 若环有左单位元而无右单位元，则左单位元不唯一。
\end{enumerate}''',refs='unit,zerodiv,ringlaws')
add(1,33,'逐项验证理想条件；非交换反例仍取矩阵单位。',r'''
设$R$交换，$a\in R$固定。$0=0a\in Ra$，且对$r,s\in R$，
\[
ra-sa=(r-s)a\in Ra.
\]
因此$Ra$为加法子群。对任意$t\in R$，结合律及交换律给出
\[
t(ra)=(tr)a\in Ra,\qquad (ra)t=(rt)a\in Ra.
\]
所以$Ra$是双边理想。

在非交换环$R=M_2(\Q)$中取$a=E_{11}$，其中$E_{ij}$表示仅第$(i,j)$个位置为1、其余为0的矩阵。直接计算$XE_{11}$可知，$Ra$恰为第二列为零的矩阵集合。$E_{11}\in Ra$，但
\[
E_{11}E_{12}=E_{12}\notin Ra.
\]
所以$Ra$不一定是双边理想。

若$R$没有单位元，不能直接断言$a\in Ra$；本题证明理想条件没有使用这一断言。''',r'$Ra$总有左吸收性；要成为双边理想，还要检查右吸收性。',refs='ideal,ringlaws')
add(1,35,'非零元素生成的主理想只能等于全环，因而可以解出逆元。',r'''
设$R$为交换幺环，$1\ne0$，且只有$\{0\}$与$R$两个理想。任取$a\ne0$。由第一章习题33，$Ra$为理想；它含$a=1a\ne0$，所以$Ra\ne\{0\}$，只能$Ra=R$。

因此$1\in Ra$，存在$r\in R$使$ra=1$。由交换性也有$ar=1$，故$a$可逆。每个非零元素均可逆，按域的定义，$R$为域。

条件$1\ne0$不能略去：零环也只有平凡理想，但不是域。''',r'这里需要幺元来保证$a\in Ra$，需要交换性来把单侧逆变为双侧逆。',refs='ideal,field')
add(1,36,'从理想中一个非零矩阵的非零系数出发，用左右矩阵单位取得所有矩阵单位。',r'''
设$I$为$M_n(\Q)$的非零双边理想，取$0\ne A=(a_{ij})\in I$。存在$i,j$使$a_{ij}\ne0$。记$E_{kl}$为矩阵单位，满足$E_{ij}E_{kl}=\delta_{jk}E_{il}$。

任取$k,l$，理想的两侧吸收性给出
\[
E_{ki}AE_{jl}=a_{ij}E_{kl}\in I.
\]
再左乘矩阵$a_{ij}^{-1}E_{kk}$，得$E_{kl}\in I$。因此所有矩阵单位都属于$I$。

对任意有理矩阵$X=(x_{kl})$，有$x_{kl}E_{kl}=(x_{kl}E_{kk})E_{kl}\in I$。理想对有限和封闭，所以
\[
X=\sum_{k,l}x_{kl}E_{kl}\in I.
\]
因此$I=M_n(\Q)$，不存在非零真双边理想。''',r'不能直接把理想当作有理向量子空间；数乘封闭应由母环矩阵的吸收性推出。',refs='ideal')
add(1,37,'按$ba$是否为零分类，保证出现的另一个零乘积因子非零。',r'''
若$ba=0$，因为$b\ne0$、$a\ne0$，按右零因子的定义，$a$是右零因子。

若$ba\ne0$，则由结合律及题设，$a(ba)=aba=0$。此时$a$与$ba$均非零，按左零因子的定义，$a$是左零因子。

上述两种情形穷尽所有可能，故结论成立。''',r'本笔记称$ab=0$中的$a$为左零因子；引用时沿用这一左右约定。',refs='zerodiv')
add(1,38,'构造有限几何级数，并分别核对左右乘积。',r'''
令$u=1+a+\cdots+a^{n-1}$。由分配律及幂法则，
\begin{align*}
(1-a)u&=(1+a+\cdots+a^{n-1})-(a+a^2+\cdots+a^n)\\
&=1-a^n=1,\\
u(1-a)&=(1+a+\cdots+a^{n-1})-(a+a^2+\cdots+a^n)\\
&=1-a^n=1.
\end{align*}
所以$u$是$1-a$的双侧逆元，即$(1-a)^{-1}=1+a+\cdots+a^{n-1}$。这里不要求$R$交换，因为计算中只出现同一个元素$a$的幂，它们彼此交换。''',r'非交换环中必须核对双侧逆元；同一元素的幂仍可按通常幂法则计算。',refs='unit,ringlaws')
add(1,40,'将单侧逆转为有限集合上的单侧逆映射，再使用有限性。',r'''
在集合$R$上定义$L_x(r)=xr$、$L_y(r)=yr$。由结合律及$xy=1$，对每个$r\in R$都有
\[
L_xL_y(r)=x(yr)=(xy)r=r,
\]
故$L_xL_y=\mathrm{id}_R$，特别地$L_x$满射。由于$R$有限，$L_x$也单射。

于是对任意$r$，从
\[
L_x(L_yL_x(r))=(L_xL_y)L_x(r)=L_x(r)
\]
由$L_x$的单射性得到$L_yL_x(r)=r$。令$r=1$，便得$yx=1$。''',r'有限性用在满射推出单射，不能在无限环中照搬这一步。',refs='unit,ringlaws')
add(1,41,'沿原解构造一列右逆，再用适当次幂右乘来区分它们。',r'''
令$c=1-ba$，则$c\ne0$，且
\[
ac=a-aba=0,\qquad cb=b-bab=0.
\]
对每个整数$n\geq0$定义$x_n=b+ca^n$。于是
\[
ax_n=ab+(ac)a^n=1,
\]
所以每个$x_n$都是$a$的右逆。

若存在$0\leq i<j$使$x_i=x_j$，则$ca^i=ca^j$。由$ab=1$，逐次消去相邻$ab$可得$a^jb^j=1$及$a^ib^j=b^{j-i}$。在上述等式右边乘$b^j$，得到
\[
cb^{j-i}=c.
\]
但$j-i\geq1$且$cb=0$，故左边为0，推出$c=0$，矛盾。因此$x_0,x_1,\ldots$两两不同，$a$有无穷多个右逆。''',r'不能只给出无穷多个公式，还须证明公式表示的元素两两不同。',refs='unit,ringlaws')
add(1,42,'先由广义逆的唯一性排除零因子，再构造左右单位元。',r'''
\begin{enumerate}
\item 固定$a\ne0$，取唯一的$b$使$aba=a$。若$ax=0$，则
\[
a(b+x)a=aba+(ax)a=a.
\]
由$b$的唯一性，$b+x=b$，故$x=0$。若$xa=0$，同样有$a(b+x)a=a+a(xa)=a$，仍得$x=0$。这说明$R$无左右零因子。

\item 由$aba=a\ne0$知$b\ne0$，又
\[
a(bab-b)=(aba)b-ab=ab-ab=0.
\]
因为$a\ne0$且环无零因子，$bab=b$。

\item 任取$r\in R$，有
\[
a(bar-r)=(aba)r-ar=0,\qquad
(rab-r)a=r(aba)-ra=0.
\]
由无零因子得$bar=r$、$rab=r$。故$ba$是左单位元，$ab$是右单位元。第一章习题31第一项给出$ba=ab=1_R$，此元素是整个环的双侧单位元。

\item 对每个非零$a$重复上述构造，都得到双侧逆元$b$。单位元唯一，故各次构造得到的是同一个$1_R$。环至少有两个元素，故$1_R\ne0_R$；否则$r=1_Rr=0_R$对所有$r$成立，环只有一个元素。按体的定义，$R$为体。
\end{enumerate}''',r'单位元属于整个环，不能只证明它对所选的$a$起作用。',refs='zerodiv,unit,field')

add(2,1,'同时利用元素在原群和商群中的阶，以及两个阶数的互素性。',r'''
设$m=\ord(a)$、$d=\ord(aN)$。由$m\mid|N|$，$m$有限；自然同态保持幂，故
\[
(aN)^m=a^mN=N.
\]
所以$d\mid m$，从而$d\mid|N|$。另一方面，$aN$是有限群$G/N$的元素，由拉格朗日定理，$d\mid|G/N|$。

因此$d$是$|N|$和$|G/N|$的公因子。题设两数互素，故$d=1$，即$aN=N$。陪集相等的判据于是给出$a\in N$。''',r'商群的单位元是陪集$N$，不是原群元素$e$。',refs='order,lagrange,quotient')
add(2,2,'先用贝祖等式分解指数1，再使用幂的阶公式。',r'''
由$\gcd(r,s)=1$，存在整数$u,v$使$us+vr=1$。定义$a=c^{us}$、$b=c^{vr}$。显然$a,b\in\langle c\rangle$，并且
\[
ab=c^{us+vr}=c.
\]
由$us\equiv1\pmod r$知$\gcd(u,r)=1$；由$vr\equiv1\pmod s$知$\gcd(v,s)=1$。因而
\begin{align*}
\gcd(rs,us)&=s\gcd(r,u)=s,\\
\gcd(rs,vr)&=r\gcd(s,v)=r.
\end{align*}
按原笔记的幂的阶公式，
\[
\ord(a)=\frac{rs}{\gcd(rs,us)}=r,\qquad
\ord(b)=\frac{rs}{\gcd(rs,vr)}=s.
\]
这就得到题设要求的分解；$r=1$或$s=1$时同一计算仍适用。''',r'指数$u,v$可以为负数；群中的整数幂已经有定义。',refs='powerorder,powers')
add(2,3,'把循环群中的幂方程化成指数的同余方程。',r'''
由贝祖等式，存在整数$u,v$使$ku+mv=1$。取$x=a^u$，则$x\in\langle a\rangle$，且
\[
x^k=a^{ku}=a^{1-mv}=a(a^m)^{-v}=a.
\]
所以解存在。

若$y\in\langle a\rangle$也满足$y^k=a$，可写$y=a^t$。则$a^{kt-1}=e$，由$\ord(a)=m$得$m\mid kt-1$。另一方面$m\mid ku-1$，相减得$m\mid k(t-u)$。因为$\gcd(k,m)=1$，故$m\mid t-u$，于是$y=a^t=a^u=x$。因此解唯一。''',r'唯一性仅在题设指定的循环子群内讨论，不可直接扩大到整个群。',refs='order,powers')
add(2,4,'沿原笔记用共轭联系两个乘积，比较所有使幂等于单位元的正指数。',r'''
由结合律，$a^{-1}(ab)a=ba$。对每个正整数$m$，相邻的$aa^{-1}$消去，得到
\[
(ba)^m=(a^{-1}(ab)a)^m=a^{-1}(ab)^ma.
\]
若$(ab)^m=e$，右边等于$e$，所以$(ba)^m=e$；反之，若$(ba)^m=e$，在等式两边左乘$a$、右乘$a^{-1}$，得到$(ab)^m=e$。

因此两者满足正幂等于单位元的正整数集合相同。该集合非空时，最小正整数相同，即有限阶相同；该集合为空时，两者都为无限阶。''',r'只比较有限阶还不够，要交代一个乘积无限阶时另一个也无限阶。',refs='order,glaws')
add(2,5,'在所有$n$阶元素组成的集合中按取逆配对，利用$n>2$排除不动点。',r'''
令$X=\{a\in G:\ord(a)=n\}$。若$\ord(a)=n$，则$(a^{-1})^m=e$当且仅当$a^m=e$，故$\ord(a^{-1})=n$。所以取逆把$X$映入自身，且连续取两次逆得到原元素。

若$a=a^{-1}$，则$a^2=e$，所以$\ord(a)\mid2$，这与$n>2$矛盾。因此$X$中的元素按$\{a,a^{-1}\}$分成不相交的二元集合。$G$有限，所以$X$有限，其元素个数为偶数；$X$为空时其元素个数为0，也符合结论。''',r'需要配对的集合是阶恰为$n$的元素，不能把阶整除$n$混在一起。',refs='order,glaws')
add(2,6,'中心元素与每个对换交换，因而保持每个二元子集。',r'''
设$\sigma\in Z(S_n)$。对任意不同的$i,j$，由共轭公式及中心的定义，
\[
(\sigma(i)\ \sigma(j))=\sigma(ij)\sigma^{-1}=(ij).
\]
两个对换相同当且仅当它们交换的是同一个二元集合，因此
\[
\{\sigma(i),\sigma(j)\}=\{i,j\}.
\]
固定任意$i$。由于$n>2$，可选择两个与$i$不同且彼此不同的$j,k$。上式分别用于$\{i,j\}$及$\{i,k\}$，得到
\[
\sigma(i)\in\{i,j\}\cap\{i,k\}=\{i\}.
\]
所以$\sigma(i)=i$。$i$任意，故$\sigma=e$。反之恒等置换属于中心，因而$Z(S_n)=\{e\}$。''',r'条件$n>2$保证可以选取第三个点；$S_2$本身交换，中心并不平凡。',refs='center,conjugation')
add(2,9,'先由幂集合的周期性证明群有限，再证明各西罗子群唯一且循环。',r'''
\textbf{必要性。}设$G=\langle a\rangle$为有限循环群，$H\leq G$。循环群的子群分类给出$H=\langle a^d\rangle$，其中$d\mid|G|$。又
\[
G^d=\{(a^t)^d:t\in\Z\}=\langle a^d\rangle=H.
\]
平凡子群对应$d=|G|$，所以每个子群均是某个$G^k$。

\textbf{充分性。}设每个子群均为某个$G^k$。对平凡子群，有正整数$E$使$G^E=\{e\}$。故$g^E=e$对每个$g\in G$成立，并有$G^{k+E}=G^k$。不同幂集合至多$E$个，因而不同子群也只有有限多个。每个循环子群的阶整除$E$，均有限；又
\[
G=\bigcup_{g\in G}\langle g\rangle,
\]
故$G$是有限多个有限循环子群的并，因而有限。

固定素数$p\mid|G|$。从全部$p$幂阶元素中选择阶最大的$a$，记$\ord(a)=p^r$。这种元素存在：西罗第一定理给出$p$阶子群，而$G$有限。题设给出$\langle a\rangle=G^k$，$k\geq1$。因为$a\in G^k$，可取$b\in G$使$b^k=a$。

若$p\mid k$，写$\ord(b)=p^su$、$p\nmid u$，以及$k=p^tv$、$p\nmid v$、$t\geq1$。幂的阶公式说明$b^k$的阶中$p$的指数为$\max(s-t,0)=r$，所以$s=r+t>r$。但$b^u$的阶恰为$p^s$，与$a$的选取矛盾。因此$p\nmid k$。

任取$p$幂阶元素$x$，设$\ord(x)=p^l$。存在整数$v$使$kv\equiv1\pmod{p^l}$，故
\[
x=(x^v)^k\in G^k=\langle a\rangle.
\]
所以所有$p$幂阶元素均属于$\langle a\rangle$。西罗第二定理保证有西罗$p$子群$P$包含$\langle a\rangle$；而$P$的每个元素都是$p$幂阶，反向也属于$\langle a\rangle$。故$P=\langle a\rangle$。同理任何西罗$p$子群都等于它，所以该西罗子群唯一、正规且循环。

对不同素数$p,q$，对应的正规西罗子群交平凡；两个因子元素的换位子同时属于两子群，故为$e$，所以两因子逐元素交换。它们的乘积是子群，反复使用第一章习题21的计数公式，其阶等于$|G|$，故等于$G$。各循环因子的阶两两互素，由原笔记互素阶交换元素乘积的阶的引理，各生成元的积具有$|G|$阶，因而生成$G$。所以$G$为有限循环群。

这里$k$限定为正整数。无限循环群的任何$G^k$都非平凡，不能表示平凡子群，所以结论应写作有限循环群版本。''',r'幂集合$G^k$一般未必为子群；本题仅由题设知道指定的幂集合等于某个子群。',refs='cyclic,powerorder,sylow1,sylow2,internal,coprime')
add(2,13,'交换关系使置换完全由一个点的像决定，再用轨道稳定子定理计数。',r'''
若$\tau\in C_{S_n}(\sigma)$，则$\tau\sigma=\sigma\tau$。反复使用这一等式，对$j\geq0$有
\[
\tau(\sigma^j(1))=\sigma^j(\tau(1)).
\]
因为$\sigma$为$n$轮换，$1,\sigma(1),\ldots,\sigma^{n-1}(1)$穷尽全部$n$个点。因此$\tau$完全由$\tau(1)$决定。

存在唯一$0\leq k<n$使$\tau(1)=\sigma^k(1)$，代入上式得
\[
\tau(\sigma^j(1))=\sigma^{j+k}(1)=\sigma^k(\sigma^j(1)).
\]
所以$\tau=\sigma^k$。反之，$\sigma$的每个幂都与$\sigma$交换，故$C_{S_n}(\sigma)=\langle\sigma\rangle$，其阶为$n$。

对共轭作用，$\sigma$的稳定子就是其中心化子。由轨道稳定子定理，$\sigma$的共轭类大小为
\[
[S_n:C_{S_n}(\sigma)]=\frac{n!}{n}=(n-1)!.
\]''',r'证明中心化子相等要给出两个包含；共轭类大小由中心化子的指数决定。',refs='centerizer,orbit,cycles')
add(2,14,'按轮换类型列共轭类，再利用正规子群的阶及乘法封闭性筛选。',r'''
共轭把轮换中的符号逐个替换，所以同一轮换类型的置换共轭，反之共轭也保持轮换类型。5的分拆对应七种类型，其代表与类大小为
\[
\begin{array}{c|rrrrrrr}
\text{代表}&e&(12)&(12)(34)&(123)&(123)(45)&(1234)&(12345)\\\hline
\text{类大小}&1&10&15&20&20&30&24
\end{array}
\]
计数依据如下：对换有$\binom52=10$个；双对换先选固定点，再把余下四点分成两对，有$5\cdot3=15$个；3-轮换先选三点，再选两种循环方向，有$\binom53\cdot2=20$个；$(3,2)$型同样选三点及方向，余下两点的对换唯一，亦有20个；4-轮换有$\binom54\cdot3!=30$个；5-轮换有$4!=24$个。总数为120，已穷尽$S_5$。

正规子群$N$必须含$e$，并为共轭类的并；其阶还须整除120。将类大小$10,15,20,20,30,24$分别记为$10\epsilon_1,15\epsilon_2,20\epsilon_3,20\epsilon_4,30\epsilon_5,24\epsilon_6$，其中$\epsilon_i\in\{0,1\}$。核对这$2^6$种和与120的因子，可能阶数只有$1,40,60,120$。其中40只能是$1+15+24$，60只能是$1+15+20+24$。

40阶候选含全部双对换，但
\[
((12)(34))((12)(35))=(354)
\]
是3-轮换，不在该候选内，所以不对乘法封闭。60阶候选同样含全部双对换，上式说明它还必须包含3-轮换类；因此两个大小为20的类中只能选择3-轮换类。所得集合恰为所有偶置换，即$A_5$，确为正规子群，因为它是符号同态的核。

故$S_5$的全部正规子群为$\{e\},A_5,S_5$。''',r'共轭类大小相加得到的阶符合整除条件，只能作为候选，还要检查乘法封闭。',r'列出$S_5$的所有共轭类，计算各类大小，并确定全部正规子群。',refs='conjugation,cycles,normal,lagrange,sign')
add(2,16,'先用同一个代表元写出所需交集，再说明非空交集的一般形式。',r'''
任取$g\in G$。由集合元素的写法，
\[
g(H_1\cap H_2)=gH_1\cap gH_2.
\]
具体地，若$x=gh$且$h\in H_1\cap H_2$，则$x$同时属于$gH_1,gH_2$。反之，若$x=gh_1=gh_2$，其中$h_i\in H_i$，则由左消去律$h_1=h_2$，故$x\in g(H_1\cap H_2)$。这已证明题设结论。

若还考虑两个任意左陪集$aH_1,bH_2$，其交非空时取$x$属于交。由陪集相交即相等，有$aH_1=xH_1$、$bH_2=xH_2$，所以
\[
aH_1\cap bH_2=x(H_1\cap H_2).
\]
因此任意两个此类左陪集的交，或为空，或为交子群的一个左陪集。''',r'两个任意陪集的交可能为空，写成某个陪集前须检查非空。',refs='cosets,glaws')
add(2,17,'把交子群的陪集映入两个陪集集合的笛卡尔积，并验证良定义和单射。',r'''
记$\mathcal L_G(H)=\{gH:g\in G\}$为左陪集集合，不要求$H$正规。定义
\[
\theta:\mathcal L_G(H_1\cap H_2)\longrightarrow
\mathcal L_G(H_1)\times\mathcal L_G(H_2),\quad
g(H_1\cap H_2)\longmapsto(gH_1,gH_2).
\]
若$g(H_1\cap H_2)=g'(H_1\cap H_2)$，则$g^{-1}g'\in H_1\cap H_2$，故$gH_i=g'H_i$对$i=1,2$均成立。这说明映射不依赖代表元，因而良定义。

若$\theta(g(H_1\cap H_2))=\theta(g'(H_1\cap H_2))$，则$gH_i=g'H_i$，故$g^{-1}g'\in H_i$对$i=1,2$成立，从而$g^{-1}g'\in H_1\cap H_2$。所以源陪集相同，$\theta$为单射。

题设保证右侧有限，其元素个数为$[G:H_1][G:H_2]$。因此源陪集集合也有限，并有
\[
[G:H_1\cap H_2]\leq[G:H_1][G:H_2].
\]''',r'有限指数不意味着群本身有限；这里计数的是陪集集合。',refs='cosets')
add(2,18,'沿原解构造左陪集作用，按作用的核是否平凡分类。',r'''
令$G$作用于$H$的$n$个左陪集：$g\cdot(xH)=gxH$。该式良定义，且单位元及乘积的作用满足群作用公理，故给出同态$\rho:G\to S_n$。设$K=\ker\rho$，则$K\trianglelefteq G$。

若$k\in K$，则$k$特别固定陪集$H$，即$kH=H$，故$k\in H$。因此$K\leq H<G$，所以$K$一定为真子群。

若$K\ne\{e\}$，它是非平凡真正规子群。由第一同构定理及拉格朗日定理，
\[
[G:K]=|G/K|=|\rho(G)|\mid|S_n|=n!.
\]
若$K=\{e\}$，则$\rho$单射，所以$G\cong\rho(G)\leq S_n$。两种情况已穷尽，故结论成立。''',r'核不可能为整个群，因为它包含于真子群$H$。',refs='action,firstiso,lagrange')
add(2,19,'由陪集作用的像的阶，同时整除$|G|$和$p!$来限制像。',r'''
令$G$作用于$H$的$p$个左陪集，记对应同态为$\rho:G\to S_p$，核为$K$、像为$Q$。与第二章习题18同样，$K\leq H$。第一同构定理及拉格朗日定理给出
\[
|Q|\mid|G|,\qquad |Q|\mid p!.
\]
因为$p$是$|G|$的最小素因子，$|Q|$的任何素因子都不小于$p$。另一方面$p!$中唯一不小于$p$的素因子是$p$，且它的指数为1。所以$|Q|$只能为1或$p$。

陪集作用传递：任意$xH,yH$，元素$yx^{-1}$把前者映到后者。故$Q$在这$p$个陪集上的轨道大小为$p$，由轨道稳定子定理得$p\mid|Q|$。因此$|Q|=p$。

于是$[G:K]=p=[G:H]$。又$K\leq H$，指数乘法公式给出$[H:K]=1$，故$K=H$。因为$K$为核，$H\trianglelefteq G$。''',r'最小素因子的条件用来排除$p!$中的较小素因子。',refs='action,firstiso,lagrange,orbit')
add(2,20,'先由中心非平凡证明交换，再按是否存在$p^2$阶元素分类。',r'''
有限$p$群的中心非平凡，所以$|Z(G)|$只能为$p$或$p^2$。若为$p^2$，则$G=Z(G)$，已经交换。若为$p$，则$G/Z(G)$为$p$阶循环群。取生成元的提升$a\in G$，每个群元素都可写成$a^iz$，其中$z\in Z(G)$。因而任意两个元素满足
\begin{align*}
(a^iz)(a^jw)&=a^{i+j}zw\\
&=a^{j+i}wz=(a^jw)(a^iz).
\end{align*}
所以$G$仍交换。

若有$p^2$阶元素，则它生成$G$，故$G\cong C_{p^2}$。否则每个非单位元的阶都是$p$。选$a\ne e$，再选$b\notin\langle a\rangle$。两个$p$阶子群$\langle a\rangle,\langle b\rangle$的交只能为$\{e\}$：若交非平凡，任一非单位元便生成两个子群，使它们相等，与$b$的选取矛盾。

因为$G$交换，由第一章习题21，$|\langle a\rangle\langle b\rangle|=p^2$，故乘积等于$G$。映射$C_p\times C_p\to G$，$(\bar i,\bar j)\mapsto a^ib^j$为同态且满射；核平凡，因为$a^i=b^{-j}$必须属于两个因子的交。故$G\cong C_p\times C_p$。

这两个群因是否存在$p^2$阶元素而不同构，所以恰为两种类型。''',r'中心商群循环推出交换的计算在这里已经给出，不把后面的习题39作为未证前提。',refs='pcenter,lagrange,cyclic,internal')
add(2,21,'唯一的3阶子群给出正规循环因子，再由2阶元素的共轭作用决定乘法。',r'''
西罗第三定理给出$n_3\mid2$、$n_3\equiv1\pmod3$，所以$n_3=1$。记唯一的3阶子群为$\langle a\rangle$，它正规。西罗第一定理给出2阶元素$b$。

两个子群的交平凡，由第一章习题21，它们的集合乘积有$3\cdot2=6$个元素，故为整个$G$。特别地$a,b$生成$G$。

共轭$b$保持$\langle a\rangle$，且保持$a$的阶，所以$bab^{-1}$只能为$a$或$a^{-1}$。若为$a$，则$a,b$交换，由它们生成的$G$也交换，与题设矛盾。因此
\[
a^3=b^2=e,\qquad bab^{-1}=a^{-1}.
\]
由此每个元素可唯一写成$a^ib^j$，$0\leq i<3$、$0\leq j<2$。唯一性来自两个不同陪集$\langle a\rangle$和$\langle a\rangle b$，各自有三个不同元素。

定义$a^ib^j\mapsto(123)^i(12)^j$。$S_3$中对应元素满足相同关系，所以化简两个正规形乘积所得公式一致，映射保乘法；两边均有六个不同正规形，故为双射。因此$G\cong S_3$。''',r'仅列出几个成立的关系不足以直接判定同构，需补充正规形和双射的说明。',refs='sylow1,sylow3,cyclic,dihedral,iso')
add(2,22,'两种西罗子群都唯一，正规性和互素阶使其逐元素交换。',r'''
由西罗第三定理，
\begin{align*}
n_5\mid3,\quad n_5\equiv1\pmod5&\quad\Longrightarrow\quad n_5=1,\\
n_3\mid5,\quad n_3\equiv1\pmod3&\quad\Longrightarrow\quad n_3=1.
\end{align*}
设这两个唯一的西罗子群为$P=\langle a\rangle$、$Q=\langle b\rangle$，其中$a$为3阶、$b$为5阶。它们均正规，且交平凡，因为交的阶同时整除3和5。

对$x\in P,y\in Q$，正规性说明$[x,y]$同时属于$P$和$Q$，所以$[x,y]=e$，即$xy=yx$。又第一章习题21给出$|PQ|=15$，故$G=PQ$。

因此$a,b$交换，且阶互素。由原笔记互素阶交换元素乘积的阶的引理，$\ord(ab)=15$，所以$ab$生成$G$，故$G\cong C_{15}$。''',r'两个循环子群的乘积未必循环；这里生成元的阶互素且彼此交换才推出循环。',refs='sylow3,normal,coprime')
add(2,23,'根据2阶元素在唯一5阶子群上的共轭作用分类。',r'''
由$n_5\mid2$及$n_5\equiv1\pmod5$，得$n_5=1$。设唯一的5阶子群为$\langle a\rangle$，取2阶元素$b$。两个子群交平凡，由计数可得$G=\langle a\rangle\langle b\rangle$，所以$a,b$生成$G$。

由于$\langle a\rangle$正规，$bab^{-1}=a^t$，其中$\gcd(t,5)=1$。由$b^2=e$，再次共轭得
\[
a=b(a^t)b^{-1}=a^{t^2},
\]
所以$t^2\equiv1\pmod5$。因5为素数，$5\mid(t-1)(t+1)$推出$t\equiv1$或$-1\pmod5$。

若$t\equiv1$，则$a,b$交换，互素阶乘积的阶公式给出$\ord(ab)=10$，故$G\cong C_{10}$。

若$t\equiv-1$，则$a^5=b^2=e$且$bab^{-1}=a^{-1}$。每个元素唯一写为$a^i$或$a^ib$，$0\leq i<5$。将它们分别映到$D_5$中的$T^i$和$T^iS$，由相同的关系核对乘法，得到同构$G\cong D_5$。

$C_{10}$交换，$D_5$不交换，所以两者不同构；$t$的两种可能已穷尽，分类完成。''',r'先证明共轭只剩两种，再分别识别两个群，才能说明分类没有遗漏。',refs='sylow1,sylow3,coprime,dihedral')
add(2,24,'对较大素数的西罗子群计数，排除非唯一的可能。',r'''
设$|G|=pq$，$p<q$为素数。西罗$q$子群的个数$n_q$满足
\[
n_q\mid p,\qquad n_q\equiv1\pmod q.
\]
所以$n_q$只能为1或$p$。若$n_q=p$，则$q\mid p-1$，但$0<p-1<q$，不可能。因此$n_q=1$，唯一的西罗$q$子群$Q$正规。

由于$1<q<pq$，$Q$既非平凡子群也非整个群，所以$G$不是单群。''',r'单性排除的是非平凡真正规子群，须交代候选子群既非1阶也非全群。',refs='sylow3,simple')
add(2,25,'先用西罗数的整除和同余约束缩小到12阶，再直接数元素。',r'''
若$n_p=1$，已得到正规西罗子群。否则$n_p\mid q$给出$n_p=q$，再由$n_p\equiv1\pmod p$得$q>p$。

若$n_q=1$，同样已完成。反设$n_q\ne1$。由$n_q\mid p^2$，它只能为$p$或$p^2$。因$p<q$，$p$不可能模$q$余1，故$n_q=p^2$，于是
\[
q\mid p^2-1=(p-1)(p+1).
\]
$q$为素数，必整除$p-1$或$p+1$；前者因$0<p-1<q$不可能。因此$q\mid p+1$。又$q>p$，只能$q=p+1$。两个相邻整数都为素数，只可能$p=2,q=3$，故剩下12阶情形。

此时反设给出$n_2=3$、$n_3=4$。不同3阶子群交平凡，所以四个3阶子群共有$4(3-1)=8$个3阶元素。群中余下恰有四个元素，包含$e$。

任一西罗2子群有四个元素，其中的元素阶整除4，不能是3阶元，故它只能恰好等于这四个剩余元素组成的集合。因此西罗2子群唯一，与$n_2=3$矛盾。故至少有一个西罗子群正规。''',r'12阶时要说明每个西罗2子群都被同一个四元素集合容纳，才能推出唯一。',refs='sylow3,lagrange')
add(2,26,'保留原解的单位上三角矩阵群和二面体群两个构造。',r'''
在$\F_3$上记
\[
X(a,b,c)=\begin{pmatrix}1&a&c\\0&1&b\\0&0&1\end{pmatrix},\qquad
H=\{X(a,b,c):a,b,c\in\F_3\}.
\]
直接计算可得
\begin{align*}
X(a,b,c)X(a',b',c')&=X(a+a',b+b',c+c'+ab'),\\
X(a,b,c)^{-1}&=X(-a,-b,ab-c).
\end{align*}
所以$H$含单位矩阵，对乘法和取逆封闭，因而是$\GL_3(\F_3)$的子群，阶为$3^3=27$。

每个$X\in H$可写为$E+N$，其中$N$严格上三角，故$N^3=0$。由于$E$与$N$交换，且域特征为3，
\[
X^3=(E+N)^3=E+3N+3N^2+N^3=E.
\]
然而
\begin{align*}
(E+E_{12})(E+E_{23})&=E+E_{12}+E_{23}+E_{13},\\
(E+E_{23})(E+E_{12})&=E+E_{12}+E_{23}.
\end{align*}
所以$H$非交换，是第一个例子。

第二个例子取$D_4$。由二面体群的元素形式，旋转是$T$的幂，阶整除4；反射$ST^k$满足$(ST^k)^2=e$。所以每个元素$x$均满足$x^4=e$。又原笔记已证明$D_4$阶为8且不交换，故满足要求。''',r'矩阵群的封闭性与逆元应先验证，再讨论其阶和元素的幂。',refs='subgroup,dihedral')
add(2,27,'把双陪集分解成右陪集，再准确比较两个右陪集何时相等。',r'''
令$L=a^{-1}Ha\cap K$。它是$K$的子群。双陪集可写为
\[
HaK=\bigcup_{k\in K}Hak,
\]
每个$Hak=H(ak)$都是$H$的一个右陪集。对$k_1,k_2\in K$，右陪集相等的判据给出
\begin{align*}
Hak_1=Hak_2
&\iff (ak_1)(ak_2)^{-1}\in H\\
&\iff ak_1k_2^{-1}a^{-1}\in H\\
&\iff k_1k_2^{-1}\in a^{-1}Ha\cap K=L\\
&\iff Lk_1=Lk_2.
\end{align*}
所以不同$Hak$的个数等于$L$在$K$中的右陪集数，即$[K:L]$。不同的$H$右陪集两两不交，每个均有$|H|$个元素。因此
\[
|HaK|=|H|[K:a^{-1}Ha\cap K].
\]''',r'这里使用右陪集的判据$Hx=Hy\iff xy^{-1}\in H$，次序不能写反。',refs='cosets')
add(2,28,'仍用左正则表示，把一个2阶元素对应为奇置换，再取符号同态的核。',r'''
因为西罗2子群阶为2，可写$|G|=2m$，其中$m$为奇数。取该子群中的非单位元$a$，则$a^2=e$。原笔记的凯莱定理给出左正则表示
\[
\rho:G\longrightarrow S(G),\qquad \rho(g)(x)=gx.
\]
若$ax=x$，右消去$x$得$a=e$，矛盾。因此$\rho(a)$没有不动点。又$a^2=e$，所以$\rho(a)$的每个轨道都有两个元素，正是$\{x,ax\}$。这些轨道把$G$分成$m$对，故$\rho(a)$为$m$个不相交对换的积。

由于$m$为奇数，$\sgn(\rho(a))=(-1)^m=-1$。因此复合同态$\varepsilon=\sgn\circ\rho:G\to\{1,-1\}$满射。令$N=\ker\varepsilon$，由第一同构定理，
\[
G/N\cong\{1,-1\},\qquad [G:N]=2.
\]
所以$G$有指数2的子群，且这个子群正规。''',r'构造符号同态后须证明它非平凡，才能确定核的指数恰为2。',r'设有限群$G$的西罗2子群阶为2。证明$G$存在指数2的子群。',refs='cayley,sign,firstiso')

add(2,33,'在正规子群$N$内使用西罗共轭定理，将任意$g$分解为两个指定因子的乘积。',r'''
任取$g\in G$。由于$N\trianglelefteq G$，$gPg^{-1}\leq N$；共轭保持阶，故$gPg^{-1}$与$P$同阶，也是$N$的西罗$p$子群。

在群$N$内使用西罗第二定理，存在$n\in N$使
\[
gPg^{-1}=nPn^{-1}.
\]
于是$(n^{-1}g)P(n^{-1}g)^{-1}=P$。按正规化子的定义，$n^{-1}g\in N_G(P)$，从而$g=n(n^{-1}g)\in NN_G(P)$。由于$g$任意，$G\subseteq NN_G(P)$；反过来，两个因子均在$G$中，故$NN_G(P)\subseteq G$。因此$G=NN_G(P)$。''',r'共轭元$n$必须取在$N$中，故西罗共轭定理是在群$N$内使用。',refs='sylow2,normalizer')
add(2,34,'先用共轭使$N$的一个西罗子群落入$P$，再计算商群中的阶。',r'''
\begin{enumerate}
\item 取$N$的西罗$p$子群$Q$。把$Q$视为$G$的$p$子群，由西罗第二定理可知它包含于$G$的某个西罗$p$子群$P_1$。同一定理又给出$g\in G$使$gP_1g^{-1}=P$。

因为$N$正规，$gQg^{-1}\leq N$；又$Q\leq P_1$，故$gQg^{-1}\leq P$。所以
\[
gQg^{-1}\leq P\cap N.
\]
左边与$Q$同阶，已经是$N$的西罗$p$子群。右边是$N$的$p$子群，阶不能更大。因此两者阶相同，$P\cap N$也是$N$的西罗$p$子群。

\item 写$|G|=p^rm$、$|N|=p^sn$，其中$p\nmid mn$。由第一项，$|P\cap N|=p^s$。因$N$正规，$PN$为子群，商群$PN/N$有定义；第二同构定理给出
\[
PN/N\cong P/(P\cap N),\qquad |PN/N|=p^{r-s}.
\]
另一方面，$|G/N|=|G|/|N|$中素因子$p$的指数恰为$r-s$。所以$PN/N$具有商群阶中的全部$p$因子，按定义是$G/N$的西罗$p$子群。
\end{enumerate}''',r'第一项不要求$P\cap N$正规；它的西罗性质通过阶数达到最大值证明。',r'''设$G$为有限群，$P$为其西罗$p$子群，$N\trianglelefteq G$。证明：
\begin{enumerate}
\item $P\cap N$为$N$的西罗$p$子群；
\item $PN/N$为$G/N$的西罗$p$子群。
\end{enumerate}''',refs='sylow2,sylowdef,secondiso')
add(2,35,'先使$H$的西罗子群包含于$P$的某个共轭，再比较交子群的阶。',r'''
取$H$的西罗$p$子群$Q$。$Q$也是$G$的$p$子群，由西罗第二定理，存在$a\in G$使$Q\leq aPa^{-1}$。因此
\[
Q\leq aPa^{-1}\cap H\leq H.
\]
$aPa^{-1}\cap H$作为$p$群$aPa^{-1}$的子群，其阶为$p$的幂；又它属于$H$，所以其阶至多为$|H|$中最大的$p$幂，即$|Q|$。结合它包含$Q$，得两者阶相同，故
\[
aPa^{-1}\cap H=Q.
\]
所以该交为$H$的西罗$p$子群。''',r'不必要求$H$正规；共轭$P$的位置可以随$H$选择。',refs='sylow1,sylow2,lagrange')
add(2,37,'先确定中心的阶，再利用交换商群的判别限制换位子群。',r'''
因为$G$为非平凡$p$群，$Z(G)\ne\{e\}$。由拉格朗日定理，其阶只能为$p,p^2,p^3$。

若$|Z(G)|=p^3$，则$G$交换，与题设矛盾。若$|Z(G)|=p^2$，则$G/Z(G)$为$p$阶循环群。取其生成元的提升$a$，任意两个群元素可写成$a^iz,a^jw$，其中$z,w\in Z(G)$，并有
\[
(a^iz)(a^jw)=a^{i+j}zw=a^{j+i}wz=(a^jw)(a^iz).
\]
仍推出$G$交换，矛盾。因此$|Z(G)|=p$。

商群$G/Z(G)$阶为$p^2$，由第二章习题20，它为交换群。将原笔记的交换商群判别用于自然满同态$G\to G/Z(G)$，得$G^{(1)}\leq Z(G)$。由于$G$非交换，$G^{(1)}\ne\{e\}$；而$p$阶循环群$Z(G)$没有非平凡真子群，所以$G^{(1)}=Z(G)$，两者阶均为$p$。''',r'先在本题补写中心商循环的交换性计算，避免依赖尚未出现的习题39。',refs='pcenter,abelianization,lagrange')
add(2,48,'将自同构限制到三个非单位元，证明任意三点置换都保持乘法。',r'''
记$V_4=\{e,a,b,c\}$，其中$a^2=b^2=c^2=e$、$ab=ba=c$，其余不同非单位元的乘积也等于第三个非单位元。

自同构固定$e$，且是双射，所以必置换集合$\{a,b,c\}$。定义限制映射
\[
\Phi:\Aut(V_4)\to S(\{a,b,c\}).
\]
限制保持复合，故$\Phi$为同态。若限制为恒等置换，自同构既固定三个非单位元又固定$e$，所以为恒等自同构，故$\Phi$单射。

任取$\pi\in S(\{a,b,c\})$，将它延拓为固定$e$的双射$\widetilde\pi:V_4\to V_4$。若一个因子为$e$，乘法显然保持；若两个因子为同一个非单位元，乘积为$e$，像的乘积也为$e$；若为两个不同非单位元，乘积是余下的第三个，置换后仍满足这一规则。所以$\widetilde\pi$保乘法，为自同构。因此$\Phi$满射。

由$S(\{a,b,c\})\cong S_3$，得$\Aut(V_4)\cong S_3$。''',r'一个任意的元素置换通常不保持群乘法，本题需用$V_4$的特殊乘法逐类验证。',refs='aut,iso')
add(2,50,'先证明内自同构群是唯一极小非平凡正规子群，再把自同构在它上的限制消去。',r'''
设$A=\Aut(G)$、$S=\Inn(G)$。因为$G$非交换且单，中心作为正规子群只能为$\{e\}$：若中心为$G$，群便交换。因此原笔记的内自同构群定理给出$S\cong G$，所以$S$也是非交换单群，且$S\trianglelefteq A$。

由原笔记无中心群的自同构定理，$C_A(S)=\{e_A\}$且$Z(A)=\{e_A\}$。这里$C_A(S)$指$A$中与$S$每个元素交换的自同构所成的子群。

先证明$S$是$A$的特征子群。任取非平凡正规子群$M\trianglelefteq A$。交$M\cap S$为$S$的正规子群，由$S$的单性，只能平凡或等于$S$。若交平凡，因$M,S$均在$A$中正规，对$m\in M,s\in S$，换位子$[m,s]$同时落在$M,S$中，故为单位元。于是$M\leq C_A(S)=\{e_A\}$，矛盾。故每个非平凡正规子群$M$都包含$S$。

$S$自身没有非平凡真正规子群，所以它是$A$中唯一的极小非平凡正规子群。任意$A$的自同构都把极小非平凡正规子群映为同类子群，因此必须保持$S$，故$S$为特征子群。

任取$\beta\in\Aut(A)$。因$S$特征，$\beta|_S$为$S$的自同构。通过同构$G\to S$、$g\mapsto c_g$（$c_g(x)=gxg^{-1}$），该限制对应某个$a\in\Aut(G)=A$。在$A$中有
\[
ac_ga^{-1}=c_{a(g)},
\]
所以由$a$诱导的内自同构$\gamma_a$与$\beta$在$S$上相同。令$\delta=\gamma_a^{-1}\beta$，则$\delta$逐元素固定$S$。

对$x\in A,s\in S$，因$S\trianglelefteq A$，$xsx^{-1}\in S$，从而
\[
\delta(x)s\delta(x)^{-1}=\delta(xsx^{-1})=xsx^{-1}.
\]
因此$x^{-1}\delta(x)$与所有$s\in S$交换，属于$C_A(S)=\{e_A\}$，故$\delta(x)=x$。所以$\delta$恒等，$\beta=\gamma_a$为内自同构。结合$Z(A)$平凡，按定义$A$为完全群。''',r'关键是先证明$S$特征，才能把$A$的任意自同构限制为$S$的自同构。',refs='inner,autcenterless,characteristic,complete,simple')
add(2,51,'沿原笔记用$S_4$的完全性把整个群分解成它与中心化子的直积，再取换位子群。',r'''
反设$N=S_4=G^{(1)}$。换位子群正规，所以$N\trianglelefteq G$；由第二章习题49，$N$中心平凡且为完全群。

任取$g\in G$。由于$N$正规，$x\mapsto gxg^{-1}$限制到$N$为自同构。$N$完全，故存在$n\in N$使$gxg^{-1}=nxn^{-1}$对所有$x\in N$成立。因此$n^{-1}g\in C_G(N)$，即$g\in NC_G(N)$。于是$G=NC_G(N)$。

记$C=C_G(N)$。由定义$N$与$C$逐元素交换，且$N\cap C=Z(N)=\{e\}$。故乘法映射$N\times C\to G$、$(n,c)\mapsto nc$是满同态；若$nc=e$，则$n=c^{-1}\in N\cap C$，所以$n=c=e$，核平凡。因而$G\cong N\times C$。

对直积逐分量计算换位子，并分别用$[(n_1,e),(n_2,e)]$、$[(e,c_1),(e,c_2)]$取得两因子的生成换位子，得到
\[
G^{(1)}=N^{(1)}C^{(1)}.
\]
因为$C^{(1)}\leq G^{(1)}=N$且$C^{(1)}\leq C$，得$C^{(1)}\leq N\cap C=\{e\}$。所以$G^{(1)}=N^{(1)}$。

最后说明$N^{(1)}=A_4$：符号同态使所有换位子落入$A_4$；另一方面两个对换的换位子可给出3-轮换，例如$[(12),(23)]=(132)$，对符号作共轭替换即可得到全部3-轮换。原笔记已证明3-轮换生成$A_4$，故$N^{(1)}=A_4$。于是$G^{(1)}=A_4\ne S_4$，与假设矛盾。''',r'直积分解后还要证明中心化子因子的导群平凡，不能直接省略这一因子。',refs='complete,characteristic,internal,derived,threecycles,sign')
add(2,52,'保留原解的两个双对换，直接计算它们的换位子。',r'''
任取不同的$a,b,c$。因$n\geq5$，还可选取与它们不同且彼此不同的$d,e$。令
\[
x=(ab)(de),\qquad y=(bc)(de).
\]
两个置换均为两个对换之积，故$x,y\in A_n$。它们又满足$x^{-1}=x$、$y^{-1}=y$。不相交支集上的置换交换，所以
\[
xy=(ab)(bc)(de)^2=(abc).
\]
按本笔记的换位子约定，
\[
[x,y]=x^{-1}y^{-1}xy=(xy)^2=(acb),\qquad
[y,x]=(abc).
\]
因此每个3-轮换都是$A_n$中某两个元素的换位子，属于$A_n^{(1)}$。

全部3-轮换生成$A_n$，所以$A_n\leq A_n^{(1)}$。反向包含由换位子群是原群的子群而成立。因此$A_n^{(1)}=A_n$。''',r'附加的两个点保证构造的$x,y$都是偶置换，这解释了$n>4$的用途。',refs='derived,threecycles,cycles')
add(2,53,'按原解取一个对换和一个3-轮换，用共轭取得星形对换。',r'''
取$a=(12)$、$b=(234)$。它们分别为2阶和3阶，故$a^2=b^3=e$。逐点作用可知$ab$把$1,2,3,4$依次映到$2,3,4,1$，所以$ab=(1234)$，从而$(ab)^4=e$。

设$K=\langle a,b\rangle$。共轭公式给出
\[
bab^{-1}=(13),\qquad b^2ab^{-2}=(14).
\]
因此$K$含$(12),(13),(14)$。由第二章习题10，这三个星形对换生成$S_4$，所以$S_4\leq K$；反向包含成立，故$K=S_4$。

由此构造出了满足要求的生成元。这里证明的是这两个具体置换生成$S_4$，并未把题中的三个等式单独视为任意群的完整展示。''',r'验证所列等式和证明两个元素生成全群，是两个分别需要完成的步骤。',refs='conjugation,cycles,generated')
add(2,54,'先计算关系，再让三个共轭双对换构成$V_4$并用子群乘积计数。',r'''
取$a=(12)(34)$、$b=(123)$。显然$a^2=b^3=e$。按右边先作用计算，$ab$固定1，并将$2,4,3$依次映到$4,3,2$，所以$ab=(243)$，从而$(ab)^3=e$。

设$K=\langle a,b\rangle$。$a,b$均为偶置换，所以$K\leq A_4$。由共轭公式，
\[
bab^{-1}=(23)(14),\qquad b^2ab^{-2}=(13)(24).
\]
这两者连同$a$恰为$V_4$的三个非单位元，所以$V_4\leq K$。又$\langle b\rangle$阶为3，$V_4$阶为4，两者的交的阶同时整除3和4，故交平凡。

由第一章习题21，集合$V_4\langle b\rangle$有$4\cdot3=12$个元素，并且包含于$K$。而$K\leq A_4$、$|A_4|=12$，所以只能$K=A_4$。''',r'不必预先证明$V_4\langle b\rangle$为子群；集合乘积的计数已足够比较阶。',refs='conjugation,sign,lagrange')
add(2,55,'先说明生成关系的读法，再用八个正规形识别四元数群，并按元素阶列尽子群。',r'''
若只要求题设等式成立而不作其他限定，$V_4$中两个不同非单位元$a,b$也满足这些等式，却不与$Q_8$同构。因此先在$a^2\ne e$的条件下证明，再说明完整展示的情形。

由$b^{-1}ab=a^{-1}$得$ab=ba^{-1}$；将$a$换成$a^{-1}$又得$ba=a^{-1}b$。利用这些关系可以把每个字中的$b$移到右边，并用$b^2=a^2$、$a^4=e$化简，故每个元素都能写成
\[
a^ib^j,\qquad0\leq i<4,\quad0\leq j<2.
\]
所以$|G|\leq8$。$a^2\ne e$与$a^4=e$说明$a$阶为4。若$b\in\langle a\rangle$，则$b$与$a$交换，由共轭关系得$a=a^{-1}$，与4阶矛盾。因此$b\notin\langle a\rangle$，两个右陪集$\langle a\rangle$、$\langle a\rangle b$不交，每个均有四个元素，故$|G|=8$，所列正规形两两不同。

在四元数体中，$Q_8=\{\pm1,\pm I,\pm J,\pm K\}$是乘法群，其中$I^2=J^2=K^2=-1$、$IJ=K=-JI$。元素$I,J$满足与$a,b$相同的关系。将$a^ib^j$映到$I^iJ^j$，两边八个正规形唯一，故为双射。化简乘积时均使用$ba=a^{-1}b$或$JI=I^{-1}J$及平方关系，所得乘法一致，所以映射为同构，$G\cong Q_8$。

若将题设关系理解为完整展示，设相应展示群为$\widetilde G$。同样的化简证明$|\widetilde G|\leq8$。$I,J$满足全部关系，由自由群商构造的泛性质，$a\mapsto I,b\mapsto J$诱导$\widetilde G\twoheadrightarrow Q_8$，所以$|\widetilde G|\geq8$，从而也与$Q_8$同构。

最后列出全部子群。$Q_8$只有一个2阶元素$-1$，六个其余非单位元均为4阶，它们分别生成
\[
\langle I\rangle=\{1,-1,I,-I\},\quad
\langle J\rangle=\{1,-1,J,-J\},\quad
\langle K\rangle=\{1,-1,K,-K\}.
\]
由拉格朗日定理，真子群的阶只能为1、2或4。1阶子群只有$\{1\}$；2阶子群只能为$\{1,-1\}$；4阶子群不可能所有非单位元都为2阶，因为全群只有一个2阶元，故必须含4阶元，只能为上述三个循环子群之一。因此连同全群$Q_8$，已穷尽全部子群。

三个4阶子群指数为2，均正规；$\{1,-1\}$包含于中心，也正规；平凡子群及全群本来就正规。所以$Q_8$的每个子群均正规。''',r'仅有若干成立的等式，与把它们指定为完整生成关系，是两种不同假设。',r'''设$G=\langle a,b\rangle$，满足
\[
a^4=b^4=e,\qquad a^2=b^2,\qquad b^{-1}ab=a^{-1}.
\]
在$a^2\ne e$的条件下，证明$G\cong Q_8$，列出全部子群并证明每个子群正规。若将上述关系理解为完整展示，也证明展示群为$Q_8$。仅要求等式成立时，说明为何须加限定。''',refs='dihedral,quaternion,lagrange,free')
add(2,57,'选定有限左陪集代表，从一个字的右端递推代表元，得到有限个施赖尔生成元。',r'''
设$G=\langle g_1,\ldots,g_n\rangle$。令$S=\{g_1^{\pm1},\ldots,g_n^{\pm1}\}$，它有限，且每个群元素都是$S$中元素的有限乘积。取$H$的$m$个左陪集代表组成集合$T$，规定$e$代表陪集$H$。对$x\in G$，用$\overline x\in T$表示$xH$的唯一选定代表。

对每个$s\in S,t\in T$，由$stH=\overline{st}H$知
\[
b_{s,t}=\overline{st}^{\,-1}st\in H.
\]
令$\mathcal B=\{b_{s,t}:s\in S,t\in T\}$，则$\mathcal B\subseteq H$且$|\mathcal B|\leq|S|m$，所以$\langle\mathcal B\rangle\leq H$。

任取$h\in H$，写$h=s_1\cdots s_r$，$s_i\in S$。$r=0$时$h=e$已属于$\langle\mathcal B\rangle$。以下设$r\geq1$，从右端递归定义
\[
t_{r+1}=e,\qquad t_i=\overline{s_it_{i+1}}quad(i=r,r-1,\ldots,1).
\]
由反向归纳可知$t_iH=s_i\cdots s_rH$：起点$t_{r+1}H=H$；若$t_{i+1}H=s_{i+1}\cdots s_rH$，则
\[
t_iH=s_it_{i+1}H=s_i\cdots s_rH.
\]
因为$h\in H$，有$t_1H=H$，按代表元的选取，$t_1=e$。

令$b_i=t_i^{-1}s_it_{i+1}$。由$t_i=\overline{s_it_{i+1}}$，每个$b_i$均为$\mathcal B$的元素。相邻代表元消去，得到
\begin{align*}
b_1\cdots b_r
&=t_1^{-1}s_1t_2\,t_2^{-1}s_2t_3\cdots t_r^{-1}s_rt_{r+1}\\
&=t_1^{-1}s_1\cdots s_rt_{r+1}=h.
\end{align*}
故$H\leq\langle\mathcal B\rangle$，结合反向包含，得$H=\langle\mathcal B\rangle$，所以$H$有限生成。''',r'写成$a_j^{-1}g_i a_k$时，$a_j$必须代表$g_i a_kH$，不能让三个下标完全独立。',refs='generated,cosets')

add(1,45,'先确认嵌套逆元全部存在，再沿原解选择$d=a-aba$并核对左乘积。',r'''
令$c=b^{-1}-a$。若$c=0$，则$a=b^{-1}$，所以$ab=1$，与题设矛盾。故$c\ne0$，$c^{-1}$存在。

令$d=cba$。由$a,b,c$均非零且体无零因子，$d\ne0$，所以$d$可逆。展开得
\[
d=(b^{-1}-a)ba=a-aba.
\]
保留乘法次序，计算
\begin{align*}
(a^{-1}+c^{-1})d
&=a^{-1}(a-aba)+c^{-1}(cba)\\
&=(1-ba)+ba=1.
\end{align*}
右乘$d^{-1}$，得$a^{-1}+c^{-1}=d^{-1}$。所以$a^{-1}+c^{-1}$确实非零且可逆，其逆为$d$。从而
\[
a-\bigl(a^{-1}+(b^{-1}-a)^{-1}\bigr)^{-1}
=a-d=aba.
\]
原笔记还给出辅助恒等式。对$x\ne0,1$，由$x^{-1}-1=x^{-1}(1-x)$及乘积取逆反序公式，
\begin{align*}
(x^{-1}-1)^{-1}&=(1-x)^{-1}x\\
&=(1-x)^{-1}\bigl(1-(1-x)\bigr)\\
&=(1-x)^{-1}-1.
\end{align*}
这些计算均未交换不同元素的乘法次序。''',r'嵌套表达式每一层取逆都必须先说明对象非零，不能只在形式上变形。',refs='field,unit,ringlaws')

def read_original(c):
    s=(P/f'chapter{c}-exercises.tex').read_text(encoding='utf-8-sig')
    starts=list(re.finditer(r'\\begin\{problem\}',s)); result={}
    for j,m in enumerate(starts):
        block=s[m.end(): starts[j+1].start() if j+1<len(starts) else len(s)]
        head,body=block.split(r'\end{problem}',1)
        number=int(re.search(r'习题(\d+)',head).group(1))
        title=re.search(r'\\textbf\{习题[^：]+：(.+?)\}',head).group(1).rstrip('。')
        q=re.sub(r'^\s*\\textbf\{习题[^\n]+?\}', '',head).strip()
        # 标题中可能含数学花括号，按括号层级去除最外层 textbf。
        start=head.index(r'\textbf{')+len(r'\textbf{');level=1;pos=start
        while level:
            if head[pos]=='{':level+=1
            elif head[pos]=='}':level-=1
            pos+=1
        fulltitle=head[start:pos-1]
        title=fulltitle.split('：',1)[1].rstrip('。')
        q=head[pos:].strip()
        pm=re.search(r'\\begin\{(proof|solution)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}',body,re.S)
        proof=pm.group(2).strip() if pm else ''
        # 少数题先给解答再证明，须保留第二个环境。
        allp=list(re.finditer(r'\\begin\{(proof|solution)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}',body,re.S))
        proof='\n\n'.join(x.group(2).strip() for x in allp)
        proof=proof.replace(r'\textit{补充解答。}','')
        result[number]={'title':title,'question':q,'proof':proof,'line':s[:m.start()].count('\n')+1}
    return result

original={c:read_original(c) for c in [1,2]}

# 第56题沿原有六步证明；增补有限阶数核对表，原有计数、归纳及识别路线不变。
p56=original[2][56]['proof']
p56=p56.replace('其中$v_p(n)$表示$n$中素因子$p$的指数。','其中$v_p(n)$表示$n$中素因子$p$的指数。若西罗$p$子群正规且非平凡、真包含于群，则与单性矛盾。')
groups={}
for n in range(4,60):
    fac=[p for p in range(2,n+1) if n%p==0 and all(p%d for d in range(2,int(p**.5)+1))]
    if len(fac)<=1:continue
    p=max(fac);m=n
    while m%p==0:m//=p
    allowed=[d for d in range(1,m+1) if m%d==0 and d%p==1]
    if allowed==[1]:groups.setdefault(p,[]).append(n)
table='\n'+r'\begin{center}\begin{tabular}{c|p{11cm}}'+'\n'+r'$p$ & 最大素因子为$p$且西罗数被迫为1的阶数$n$\\\hline'+'\n'
for p,ns in groups.items():table+=f'${p}$ & $'+','.join(map(str,ns))+r'$\\'+'\n'
table+=r'\end{tabular}\end{center}'+'\n'
p56=p56.replace('例如$n=45$时',table+'例如$n=45$时')
p56=p56.replace('但$A_5$的西罗2子群只有五个：','但$A_5$中不存在4阶元素：5个点上的4阶置换只能含一个4-轮换，而4-轮换为奇置换。因此它的4阶西罗2子群都为$V_4$。这些子群只有五个：')
add(2,56,'保留原笔记的六步路线：用单群的置换作用排除小阶情形，以归纳证明可解性，再从60阶单群的西罗子群作用识别$A_5$。',p56,
    '在假设单群时作用核只有两种可能，先证明作用非平凡才能推出忠实；计数时还要防止不同4阶子群的2阶元重复。',refs='simple,action,firstiso,sylow1,sylow2,sylow3,pcenter,solvable,an')

# 引用注册表：定位实际正文环境；统一计数器包括例、注记等，不能只数定理。
locations={
 'group':(1,51,'群的定义'),'glaws':(1,77,'单位元、逆元与反序取逆'),'cancel':(1,90,'方程、消去律'),
 'powers':(1,109,'整数指数法则'),'abelianpowers':(1,134,'交换元素的乘积幂'),
 'dihedral':(1,163,'二面体群及其阶数与乘法关系'),'cycles':(1,208,'轮换与对换'),'cycledecomp':(1,222,'不相交轮换分解'),
 'subgroup':(1,260,'子群判别法'),'cosets':(1,315,'陪集相等的判据与陪集划分'),'lagrange':(1,342,'拉格朗日定理'),
 'order':(1,357,'元素的阶与幂的判据'),'iso':(1,387,'群同构及同构不变量'),'cayley':(1,406,'凯莱定理及左正则表示'),
 'sign':(1,293,'符号同态与交错群的阶'),'hom':(1,481,'群同态、像与核'),'normal':(1,577,'正规子群的等价判据'),
 'setproduct':(1,615,'集合乘积及取逆公式'),'quotient':(1,680,'商群及自然同态'),'firstiso':(1,730,'群同态基本定理'),
 'ring':(1,780,'环的定义'),'ringlaws':(1,790,'环中零元、负元和分配律的运算'),
 'subring':(1,889,'子环判别法'),'ringiso':(1,922,'环同构及其性质'),'unit':(1,953,'幺环、单位及双侧逆元'),
 'zerodiv':(1,987,'左右零因子、无零因子的消去律'),'field':(1,1033,'域与体'),'quaternion':(1,1091,'四元数体的矩阵模型'),
 'ideal':(1,1200,'理想的定义'),'idealunit':(1,1234,'含有单位的理想'),
 'correspondence':(2,18,'子群对应定理'),'secondiso':(2,111,'群的第二同构定理'),
 'generated':(2,142,'生成子群与有限生成群'),'derived':(2,172,'换位子与换位子群'),'abelianization':(2,176,'交换同态像与换位子群'),
 'cyclic':(2,228,'循环群及其子群分类'),'powerorder':(2,254,'幂的阶的公式'),'coprime':(2,276,'互素阶交换元素乘积的阶'),
 'simple':(2,331,'单群的定义'),'threecycles':(2,347,'对换与3-轮换的生成结论'),'conjugation':(2,366,'轮换的共轭公式'),
 'an':(2,398,'交错群的单性'),'derivedseries':(2,503,'导出列'),'solvabledef':(2,521,'可解群的定义'),
 'solvable':(2,681,'可解群的子群、像与扩张'),'aut':(2,717,'自同构与自同构群'),'cyclicaut':(2,740,'循环群的自同构'),
 'inner':(2,819,'内自同构群与中心商群'),'center':(2,807,'群的中心'),'autcenterless':(2,854,'无中心群的自同构定理'),
 'complete':(2,884,'完全群'),'characteristic':(2,890,'特征子群及其性质'),
 'action':(2,923,'群作用及对应的置换表示'),'orbit':(2,1060,'轨道稳定子定理'),'pcenter':(2,1140,'有限$p$群的中心非平凡'),
 'centerizer':(2,1161,'元素的中心化子'),'classeq':(2,1165,'类方程'),'normalizer':(2,1207,'子群的正规化子'),
 'sylow1':(2,1259,'西罗第一定理'),'sylowdef':(2,1286,'西罗子群的定义'),'sylow2':(2,1290,'西罗第二定理'),
 'sylow3':(2,1341,'西罗第三定理'),'internal':(2,1542,'内直和分解定理'),'free':(2,1958,'自由群的泛性质与生成关系')}

envs='theorem lemma corollary proposition definition remark example construction problem axiom prp note ill algo'.split()
cn={'theorem':'定理','lemma':'引理','corollary':'推论','proposition':'命题','definition':'定义','remark':'注记','example':'例','construction':'构造'}
records={}
for c in [1,2]:
    lines=(P/f'chapter{c}.tex').read_text(encoding='utf-8-sig').splitlines()
    sec=0; count=0; secname=''; current=None
    for i,line in enumerate(lines,1):
        sm=re.match(r'\\section\{(.+)\}',line)
        if sm:sec+=1;count=0;secname=sm.group(1);current=None
        em=re.search(r'\\begin\{('+ '|'.join(envs)+r')\}',line)
        if em:count+=1;current=(f'{c}.{sec}.{count}',cn.get(em.group(1),'条目'),i)
        records[c,i]=(sec,secname,current)
    for key,value in list(locations.items()):
        cc,line,name=value[:3]
        if cc!=c:continue
        # definition前置文字的定位保留节号，不假造命题编号。
        sec,secname,item=records[c,line]
        if key=='generated':item=None
        label=f'原笔记第{c}章第{sec}节'
        if item:label+='，'+item[1]+' '+item[0]
        locations[key]=(c,line,name,label,secname)

reviewdeps={
1:{1:'cancel',2:'glaws',4:'group',6:'dihedral',7:'powers,glaws',8:'glaws,hom',9:'subgroup,cosets',10:'iso,ringiso',12:'cosets,normal',18:'cyclic',21:'cosets',22:'normal,firstiso,setproduct',29:'ringiso,ring',30:'subring,unit',32:'ideal,field,idealunit',34:'ideal,ringlaws',39:'ideal,ringlaws',43:'ideal,zerodiv,idealunit',44:'iso'},
2:{7:'generated,cyclic',8:'generated,powers,abelianpowers',10:'threecycles,conjugation',11:'conjugation,generated',12:'conjugation,threecycles',15:'correspondence,normal,quotient',29:'setproduct,glaws',30:'orbit,normalizer,cosets',31:'sylow1,sylow3,orbit,cycles',32:'sylow1,sylow3,lagrange',36:'sylow1,sylow2,sylow3,orbit',38:'cyclicaut,firstiso,lagrange',39:'center,cosets,powers',40:'cayley,sign,firstiso',41:'normal,derived',42:'derivedseries,derived,solvabledef',43:'solvable,sylow3,pcenter',44:'classeq,pcenter,solvable',45:'firstiso,derivedseries,solvable,internal',46:'inner,cyclic',47:'inner,aut,glaws',49:'inner,complete,conjugation,threecycles'}}
for c,items in reviewdeps.items():
    for n,keys in items.items():deps[c,n]=keys

def reftext(keys):
    return '；'.join(r'\noteref{'+k+'}' for k in keys.split(',') if k)

def get_review(c):
    s=(REVIEW/f'chapter{c}.tex').read_text(encoding='utf-8-sig')
    starts=list(re.finditer(r'\\subsection\{习题(\d+)：',s));res={}
    for i,m in enumerate(starts):
        b=s[m.start(): starts[i+1].start() if i+1<len(starts) else len(s)]
        n=int(m.group(1))
        q=b.split(r'\paragraph{题目}',1)[1].split(r'\paragraph{考点与思路}',1)[0].strip()
        idea=b.split(r'\paragraph{考点与思路}',1)[1].split(r'\textbf{原文依据：}',1)[0].strip()
        pr=re.search(r'\\begin\{proof\}(?:\[[^\]]*\])?(.*?)\\end\{proof\}',b,re.S).group(1).strip()
        hint=b.split(r'\paragraph{复习提示}',1)[1].strip()
        res[n]={'question':q,'idea':idea,'proof':pr,'hint':hint}
    return res

review={c:get_review(c) for c in [1,2]}
assert len(proofs)==61,(len(proofs),sorted(proofs))

# 将仅在旧标题中出现的条件完整移入题面，保证每题可单独阅读。
questions.update({
 (1,11):r'证明$B=\{e,(12)(34),(13)(24),(14)(23)\}$为$S_4$的子群，并证明$B$不同构于四次单位根乘法群$U_4=\{1,i,-1,-i\}$。',
 (1,17):r'设$G$为交换群。证明$G$中全部有限阶元素组成一个子群，并说明交换性不能删去。',
 (2,4):r'设$a,b$为群$G$的任意两个元素，证明$ab$与$ba$具有相同的阶，包括无限阶的情形。',
 (2,20):r'设$p$为素数，$|G|=p^2$。证明$G$交换，并证明$p^2$阶群恰有$C_{p^2}$与$C_p\times C_p$两种同构类型。',
 (2,23):r'证明10阶群恰有$C_{10}$与$D_5$两种同构类型。',
 (2,25):r'设$p,q$为不同的素数，$|G|=p^2q$。证明$G$至少有一个正规的西罗子群。',
})

def plain_title(t):
    for a,b in [(r'\cong','同构于'),(r'\Z','Z'),(r'\Q','Q'),(r'\F','F'),(r'\GL','GL'),(r'\SL','SL'),(r'\Aut','Aut')]:t=t.replace(a,b)
    t=re.sub(r'\\[A-Za-z]+','',t)
    return t.replace('$','').replace('{','').replace('}','').replace('^','').replace('_','').replace('\\','')

def numbered_proof(pr,c,n):
    # 原复习册的多项题改为与最终题面一一对应的 enumerate。
    if (c,n)==(1,30):
        pr=pr.replace(r'\textbf{(i)}',r'\begin{enumerate}\item ',1)
        for x in ['ii','iii','iv']:pr=pr.replace(r'\textbf{('+x+')}',r'\item ',1)
        pr+='\n'+r'\end{enumerate}'
    if (c,n)==(1,43):
        pr=pr.replace(r'\textbf{(i) 真理想具有公共零点。}',r'\begin{enumerate}\item',1)
        pr=pr.replace(r'\textbf{(ii) 零因子的必要性。}',r'\item\textbf{必要性。}',1)
        pr=pr.replace(r'\textbf{(ii) 零因子的充分性。}',r'\textbf{充分性。}',1)
        pr+='\n'+r'\end{enumerate}'
    if (c,n)==(1,34):
        pr=pr.replace('因为环交换，可以使用二项式展开：','若环无单位元，下面求和的两个端项分别指$(-s)^N$与$r^N$，不使用零次幂。因为环交换，可以使用二项式展开：')
    if (c,n)==(1,39):
        pr=pr.replace('展开$(a-b)^{n+m-1}$','若环无单位元，二项式展开的端项直接表示$(-b)^{n+m-1}$与$a^{n+m-1}$，不使用零次幂。展开$(a-b)^{n+m-1}$')
    names={'拉格朗日定理':'lagrange','子群判别法':'subgroup','正规性判别':'normal',
        '第一同构定理':'firstiso','同态基本定理':'firstiso','第二同构定理':'secondiso',
        '轨道稳定子定理':'orbit','西罗第一定理':'sylow1','西罗第二定理':'sylow2','西罗第三定理':'sylow3',
        '西罗共轭定理':'sylow2','共轭公式':'conjugation','子环判别法':'subring','幂的阶公式':'powerorder','凯莱定理':'cayley'}
    for name,key in names.items():
        pr=pr.replace(name,r'\proofref{'+key+'}{'+name+'}',1)
    return pr

header=r'''% !TEX program = xelatex
% 本文件含全部102题；正文不通过 input 加载其他习题或工具文件。
\documentclass[UTF8,a4paper,11pt,fontset=windows]{ctexart}
\usepackage[margin=2.2cm]{geometry}
\usepackage{amsmath,amssymb,amsthm,enumitem,booktabs,longtable,array}
\usepackage[unicode,hidelinks]{hyperref}
\usepackage{xurl,fancyhdr}
\setlength{\headheight}{15pt}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{抽象代数前两章习题详解}\fancyhead[R]{题目、思路与证明}\fancyfoot[C]{\thepage}
\setlength{\parindent}{2em}\setlength{\parskip}{0.35em}
\setlist[enumerate]{itemsep=0.35em,topsep=0.4em}
\renewcommand{\proofname}{证明}
\newcommand{\Z}{\mathbb Z}\newcommand{\Q}{\mathbb Q}
\newcommand{\R}{\mathbb R}\newcommand{\C}{\mathbb C}
\newcommand{\N}{\mathbb N}\newcommand{\F}{\mathbb F}
\DeclareMathOperator{\GL}{GL}\DeclareMathOperator{\SL}{SL}
\DeclareMathOperator{\Aut}{Aut}\DeclareMathOperator{\Inn}{Inn}
\DeclareMathOperator{\lcm}{lcm}\DeclareMathOperator{\ord}{ord}
\DeclareMathOperator{\sgn}{sgn}\DeclareMathOperator{\Ker}{Ker}
\newcommand{\noteref}[1]{\hyperref[note:#1]{\csname notename@#1\endcsname}}
\newcommand{\proofref}[2]{\hyperref[note:#1]{#2}}
\newcommand{\exref}[2]{\hyperref[ex:#1:#2]{第#1章习题#2}}
\newcommand{\registerref}[2]{\expandafter\gdef\csname notename@#1\endcsname{#2}}
'''
pieces=[header]
for key,(c,line,name,label,secname) in locations.items():
    pieces.append(r'\registerref{'+key+'}{'+label+'（'+name+'）}\n')
pieces.append(r'''
\title{抽象代数前两章习题详解\\\large 第一章1--45题\quad 第二章1--57题}
\author{}\date{2026年11月4日}
\begin{document}\maketitle
本册收录现有代数笔记抽象代数第一章45题、第二章57题，共102题，保留原题号。原来合写的第一章24--26题分别列出。题面以现有习题文件为基础，必要的限定和已知订正放在相应题目内；证明沿用原笔记的构造、顺序和方法，在原有路线中补齐理由。期中复习册已经展开的41题作为本次详解的基础，其余61题重新展开。

各题按题目、考点与思路、所用结论、证明、复习提示组织。普通证明标题统一为“证明”。题中引用的原笔记定义、定理、命题和证明，以原笔记第一、二章各自的章号、节号和现有统一计数器编号定位；点击引用可跳至文末原笔记定位表，表中列出源文件和源码行号。原笔记正文不在本册重排，也不另建K编号的定理目录。

这里的第一、二章均指抽象代数部分，与线性代数部分的章号无关。编号以本次读取的原章节源码顺序为准，不采用当前只启用第三章的主PDF中的临时章号。源码行号仅供本次版本定位，后续手动增删会使其移动。

\paragraph{记号与约定}
群的单位元记为$e$，元素阶记为$\ord(a)$；$H\leq G$表示子群，$N\trianglelefteq G$表示正规子群，$[G:H]$表示左陪集个数。置换乘积从右至左作用。$D_n$为$2n$阶二面体群。$C_m$表示$m$阶循环群，$V_4$表示克莱因四元群。有关定义的正式位置分别见\noteref{group}、\noteref{cosets}、\noteref{order}、\noteref{normal}、\noteref{dihedral}、\noteref{cyclic}。

环不预设有乘法单位元，一般环同态不预设保幺；子环也不要求与母环共用单位元。域指交换的除环，体指不要求交换的除环。零因子必须非零：若$ab=0$且$a,b\ne0$，称$a$为左零因子、$b$为右零因子，沿用\noteref{zerodiv}的左右约定。$E$为单位矩阵，$E_{ij}$为仅第$(i,j)$个位置为1的矩阵单位。

\paragraph{补充工具的归属}
整数带余除法、贝祖等式、有限集计数、数学归纳法，以及线性代数与闭区间紧致性，是原解已经使用的前置工具，不冒充抽象代数正文中另有编号的定理。具体使用时交代条件与计算；不能从原笔记中找到的独立陈述，不赋予原笔记编号。第一章44题逐列计数和第二章47题的有限基构造均在题内展开。第二章12题中沿原笔记补出的附加点引理也在该题内证明。

\tableofcontents\clearpage
''')

supp={(1,7):'数学归纳法。',(1,21):'有限满射的等纤维计数（证明中给出纤维双射）。',(1,34):'交换环的二项式展开；无幺环中的端项不使用零次幂。',(1,39):'交换环的二项式展开。',(1,43):'闭区间紧致性、连续函数的非零邻域及连续倒数，均为分析前置工具。',(1,44):'线性代数中可逆矩阵与有序基的等价判别，以及有限集的乘法计数原理。',(2,2):'整数贝祖等式。',(2,3):'整数贝祖等式与互素整除。',(2,7):'整数贝祖等式。',(2,29):'有限集合并集的计数。',(2,30):'有限集合并集的上界。',(2,47):'有限维二元域向量空间的基构造，在本题具体展开。',(2,56):'有限阶数分类与关于群阶的数学归纳法。'}
extra={(1,17):[(1,16)],(1,19):[(1,12)],(1,22):[(1,20)],(1,25):[(1,2)],(1,35):[(1,33)],(1,39):[(1,34)],(1,42):[(1,31)],
 (2,11):[(2,10)],(2,21):[(1,21)],(2,22):[(1,21)],(2,23):[(1,21)],(2,31):[(1,25)],(2,36):[(1,44),(1,38)],(2,37):[(2,20)],(2,43):[(2,25),(2,20)],(2,45):[(2,42)],(2,46):[(2,39)],(2,49):[(2,6),(2,31)],(2,51):[(2,49)],(2,53):[(2,10)],(2,54):[(1,11),(1,21)],(2,55):[(1,12)],(2,56):[(2,20),(2,32)]}

all_questions=[]
for c,maxn,title in [(1,45,'代数基本概念'),(2,57,'群')]:
    pieces.append(r'\clearpage\section{第'+str(c)+'章：'+title+'}\n')
    for n in range(1,maxn+1):
        k=c,n
        base=original[c].get(n,original[c][24] if c==1 and n in [25,26] else None)
        assert base is not None,k
        if n in review[c]:
            item=review[c][n];q=item['question'];idea=item['idea'];pr=item['proof'];hint=item['hint']
        else:
            assert k in proofs,k
            q=questions.get(k,base['question']);idea=ideas[k];pr=proofs[k];hint=hints[k]
        if k in proofs:pr=proofs[k];idea=ideas[k];hint=hints[k];q=questions.get(k,q)
        pr=numbered_proof(pr,c,n)
        title={ (1,24):'2阶群',(1,25):'4阶群的分类',(1,26):'素数阶群'}.get(k,base['title'])
        # 部分原题只有短标题，补出完整的量词和任务。
        if not q:q=questions.get(k,title+'。')
        source=f'第{c}章原习题{n}'
        refs=reftext(deps[k])
        if k in extra:refs+='；'+'、'.join(r'\exref{'+str(a)+'}{'+str(b)+'}' for a,b in extra[k])
        if k in supp:refs+='。补充前置工具：'+supp[k]
        pieces.extend([
            r'\subsection{习题'+str(n)+'：'+r'\texorpdfstring{'+title+'}{'+plain_title(title)+'}}\n'+r'\label{ex:'+str(c)+':'+str(n)+'}\n',
            r'\paragraph{题目}'+'\n'+q+'\n',
            r'\paragraph{考点与思路}'+'\n'+idea+'\n',
            r'\paragraph{所用结论与原文依据}'+'\n'+refs+'。\n',
            f'% 原解来源：chapters/Part 2/chapter{c}-exercises.tex:{base["line"]}；{source}。\n',
            r'\begin{proof}'+'\n'+pr.strip()+'\n'+r'\end{proof}'+'\n',
            r'\paragraph{复习提示}'+'\n'+hint+'\n\n'])
        all_questions.append((c,n,title,base['line']))

pieces.append(r'''\clearpage\section*{原笔记引用定位}\addcontentsline{toc}{section}{原笔记引用定位}
下表只记录原笔记条目的位置，不重抄定理和定义。原笔记未启用前两章时，可直接按源文件行号回查。正文引用链接指向本表；每项均保留原章节的实际编号或节内位置。
\small\begin{longtable}{p{6.3cm}p{8.0cm}}
\toprule 原笔记条目 & 原文位置与内容范围\\\midrule\endhead
''')
for key,(c,line,name,label,secname) in locations.items():
    pieces.append(r'\phantomsection\label{note:'+key+'}'+label+' & '+name+'；第'+str(c)+'章“'+secname+'”。'+r'\newline\path{chapters/Part 2/chapter'+str(c)+'.tex}，第'+str(line)+r'行起。\\'+'\n')
pieces.append(r'\bottomrule\end{longtable}\normalsize'+'\n')
pieces.append(r'''\clearpage\section*{题号与证明入口}\addcontentsline{toc}{section}{题号与证明入口}
\small\begin{longtable}{cp{13.5cm}}
\toprule 章 & 题号及主题（点击跳转）\\\midrule\endhead
''')
for c,n,title,line in all_questions:
    pieces.append(str(c)+' & '+r'\hyperref[ex:'+str(c)+':'+str(n)+']{'+str(n)+'：'+title+r'}\\'+'\n')
pieces.append(r'\bottomrule\end{longtable}\end{document}'+'\n')
s='\n'.join(pieces)
s=s.replace('。。','。').replace('；。','。')
# 全部跨题引用都明确章别；先处理已有显式章别，再处理本章简称。
for c in [1,2]:
    pass
def link_questions(text,c):
    text=re.sub(r'第([12])章习题(\d+)(?![\d])',lambda m:r'\exref{'+m[1]+'}{'+m[2]+'}',text)
    text=re.sub(r'(?<!章)习题(\d+)(?![\d])',lambda m:r'\exref{'+str(c)+'}{'+m[1]+'}',text)
    return text
# 只处理题内段落，避免改变标题、源码注释及 label。
chunks=re.split(r'(\\subsection\{习题\d+：[^\n]*\}\n\\label\{ex:[12]:\d+\})',s)
for i in range(1,len(chunks),2):
    c=int(re.search(r'ex:([12]):',chunks[i]).group(1))
    chunks[i+1]=link_questions(chunks[i+1],c)
s=''.join(chunks)
# 所有普通证明统一无自定义标题，题面订正避免沿用复习册对来源的未核验措辞。
s=s.replace('题目按教材书页98核正','题目采用期中复习册已经核正的版本')
s=s.replace('原书要求同构；','期中复习册题面要求同构；')
target=OUT/'抽象代数前两章全部习题详解.tex'
chapter1_start=s.index(r'\clearpage\section{第1章：代数基本概念}')
chapter2_start=s.index(r'\clearpage\section{第2章：群}')
appendix_start=s.index(r'\clearpage\section*{原笔记引用定位}')
root_comment='% !TEX root = 抽象代数前两章全部习题详解.tex\n'
(OUT/'chapter1.tex').write_text(root_comment+s[chapter1_start:chapter2_start],encoding='utf-8')
(OUT/'chapter2.tex').write_text(root_comment+s[chapter2_start:appendix_start],encoding='utf-8')
main=s[:chapter1_start]+r'\input{chapter1}'+'\n\n'+r'\input{chapter2}'+'\n\n'+s[appendix_start:]
main=main.replace('% 本文件含全部102题；正文不通过 input 加载其他习题或工具文件。','% 主文件；第一章与第二章习题分别通过 input 加载。')
target.write_text(main,encoding='utf-8')
print('WROTE',target,'lines',len(s.splitlines()),'chars',len(s),'questions',len(all_questions))
