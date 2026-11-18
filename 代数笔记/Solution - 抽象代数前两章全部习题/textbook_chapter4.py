"""《代数学引论》第三版书页157--161，逐页按扫描原题转录。"""
QUESTIONS={}
def q(n,page,text):QUESTIONS[n]=dict(book_page=page,pdf_page=page+10,text=text.strip())

q(1,157,r'''设$D$为一个主理想整环而且包含在一个整环$R$内，设$a,b\in D$。证明，若$d$是$a,b$在$D$中的最大公因子，则$d$也是$a,b$在$R$内的最大公因子。''')
q(2,157,r'''设$D$为主理想整环，$a\in D$，$a\ne0$。若$a$为素元，则$D/(a)$为一域。''')
q(3,157,r'''设$D$为一主理想整环，$F$为$D$的商域。证明：$F$内任一包含$D$的子环$D'$仍为主理想整环（域看作主理想整环），而且$D'$是$D$关于某一乘性子集的分式环。反之，$D$的任一分式环是$F$的一个子环，因而仍是主理想整环。''')
q(4,157,r'''设$m$是一个无平方因子的整数且$m\ne0,1$，令
\[
F=\Q(\sqrt m)=\{a+b\sqrt m\mid a,b\in\Q\},
\]
则$F$是一域，叫做有理数域$\Q$上的二次域。$F$中有一个子集$R$定义如下：
当$m\equiv2$或$3\pmod4$时，$R=\{a+b\sqrt m\mid a,b\in\Z\}$；
当$m\equiv1\pmod4$时，$R=\{a+b(1+\sqrt m)/2\mid a,b\in\Z\}$。
证明$R$是$F$的一个子环。$R$以后分别记作$\Z[\sqrt m]$、$\Z[(1+\sqrt m)/2]$（即$\S2$中的$R_m$），$R$叫做$F$的代数整数环。''')
q(5,157,r'''假设$\Q(\sqrt m)$、$\Z[\sqrt m]$或$\Z[\tfrac12(1+\sqrt m)]$如习题4。$\Z[\sqrt m]$或$\Z[\tfrac12(1+\sqrt m)]$统记作$R_m$。$R_m$的单位乘法群记作$R_m^*$。证明：
\begin{enumerate}[label=(\roman*)]
\item $R_{-1}^*=\{\pm1,\pm\sqrt{-1}\}$；
\item $R_{-3}^*=\{\pm1,\pm\omega,\pm\omega^2\}$，其中$\omega=\tfrac12(-1+\sqrt{-3})$，$\omega$是一个三次单位根；
\item 当$m<0$但$m\ne-1,-3$时，$R_m^*=\{\pm1\}$。
\end{enumerate}''')
q(6,158,r'''设$H$为四元数体，令$D=\{a_0+a_1I+a_2J+a_3K\mid a_0,\ldots,a_3\text{ 或全为整数或全为奇整数的一半}\}$。证明：$D$是$H$的一个子环，并确定$D$的单位群。''')
q(7,158,r'''设$H,D$如题6。证明$D$的每个理想是一个主理想。''')
q(8,158,r'''证明：域$F$上一元形式幂级数环$F[[x]]$是一个主理想整环，而且$F[[x]]$只有一个非零的素理想$(x)$，因而它也是唯一的极大理想。试问$F[[x]]$的其它理想取什么形式？''')
q(9,158,r'''证明$\Z[x]$的任一个主理想都非极大。''')
q(10,158,r'''证明$\Z[\sqrt{-5}]$满足因子链条件。进一步证明，习题5中的环$R_m$都满足因子链条件。''')
q(11,158,r'''$F$为一域，$\Q^+$表示非负有理数全体，$\Q^+$是一个加法半群（也是乘法半群）。用$D$表示一元多项式
\[
a_1x^{\alpha_1}+a_2x^{\alpha_2}+\cdots+a_nx^{\alpha_n}
\]
的全体，其中$a_1,\ldots,a_n\in F$，而$x$的次数$\alpha_1,\ldots,\alpha_n$允许取$\Q^+$中的任意数，即允许取任意非负有理数。这样两个多项式相等规定为同类单项式的系数一一相等；它们相加规定为同类单项式的系数一一相加；它们相乘规定为：先按分配律展开，然后单项式相乘
\[
a_ix^{\alpha_i}b_jx^{\beta_j}=a_ib_jx^{\alpha_i+\beta_j},
\]
最后按加法求和。证明$D$构成一个整环，并且$D$不满足因子链条件。''')
q(12,158,r'''证明$\Z[\tfrac12(1+\sqrt5)]$为欧几里得整环。''')
q(13,158,r'''设$D$为一欧几里得整环，证明：若$D$的$d$函数满足：
\begin{enumerate}[label=(\roman*)]
\item $d(ab)=d(a)d(b)$；
\item $d(a+b)\le\max(d(a),d(b))$，
\end{enumerate}
则$D$是一个域或者是某域上一元多项式环。''')
q(14,158,r'''设$p$为一奇素数。证明：在整数环$\Z$内$x^2\equiv-1\pmod p$有解的充要条件是$p\equiv1\pmod4$。''')
q(15,158,r'''设$R_m$为习题5所定义的。$R_m$中不属于$\Z$的元素$\pi$是一个不可约元的充要条件是范数$N(\pi)$是$\Z$的一个素数。''')
q(16,158,r'''设$p$为一素数。证明：
\begin{enumerate}[label=(\roman*)]
\item 若$p\equiv1\pmod4$，则$p$在高斯整数环$R_{-1}=\Z[\sqrt{-1}]$内可分解成两个共轭的不可约元的乘积。由此证明，若$p\equiv1\pmod4$，则$p$可表成两个整数的平方和；
\item 若$p\equiv-1\pmod4$，则$p$也是$R_{-1}$的不可约元；
\item 在$R_{-1}$内$2$与一个不可约元的平方相伴，即
\[
2=(1+\sqrt{-1})(1-\sqrt{-1})=-\sqrt{-1}(1+\sqrt{-1})^2,
\]
其中$1+\sqrt{-1}$是不可约元。
\end{enumerate}''')
q(17,158,r'''根据习题16定出高斯整数环$\Z[\sqrt{-1}]$的全部不可约元。''')
q(18,159,r'''证明：一个正整数$m$可以表成两个整数的平方和，其充要条件是在$m$的标准分解中出现的$4k+3$形式的素数的幂指数为偶数。''')
q(19,159,r'''设$R$为一个有$1$的交换环，$P$为它的一个素理想。在多项式环$R[x_1,\ldots,x_n]$中，如果一个多项式$f(x_1,\ldots,x_n)$（假设同类项都已合并）的系数在$R$内生成的理想与$P$互素，则$f(x_1,\ldots,x_n)$叫做关于$P$的本原多项式。证明：两个关于$P$的本原多项式的乘积仍是关于$P$的本原多项式。''')
q(20,159,r'''设$R$为一个唯一因子分解整环，$S$是由$R$的一些不可约元生成的乘法半群。证明：$S^{-1}R$仍为一唯一因子分解整环。''')
q(21,159,r'''证明$f(x)=x^{p-1}+x^{p-2}+\cdots+1$在$\Z[x]$内不可约，其中$p$为素数。''')
q(22,159,r'''判定下列多项式在高斯整数环$R_{-1}=\Z[\sqrt{-1}]$上是否可约：
\begin{enumerate}[label=(\roman*)]
\item $f(x)=x^{p-1}+x^{p-2}+\cdots+1$，$p$为素数；
\item $f(x)=x^4+(8+i)x^3+(3-4i)x+5$，其中$i=\sqrt{-1}$。
\end{enumerate}''')
q(23,159,r'''设$D$为主理想整环。证明：若$D$不是域，则$D[x]$不是主理想整环。''')
q(24,159,r'''证明：主理想整环的商环的每个理想仍为主理想。''')
q(25,159,r'''在$R_{10}=\Z[\sqrt{10}]$中证明：
\begin{enumerate}[label=(\roman*)]
\item $\varepsilon=\sqrt{10}+3$是一个单位；
\item $R_{10}$的任一个单位$u$可写成$u=\pm\varepsilon^r$，$r\in\Z$。因此$R_{10}$的单位群$U$等于一个$2$阶群$\langle-1\rangle$和一个无限循环群$\langle\varepsilon\rangle$的直积。$\pm\varepsilon^{\pm1}$叫做$R_{10}$的基本单位。（注意，若$v=a+b\sqrt{10}$是$R_{10}$的单位，则$\pm v^{\pm1}=\pm a\pm b\sqrt{10}$也都是$R_{10}$的单位。）
\item $R_{10}$不是唯一因子分解整环。
\end{enumerate}''')
q(26,159,r'''设$p$为一素数，$S$表示与$p$互素的整数全体，则$S$为$\Z$的一个乘性子集。作$\Z$对$S$的分式环$S^{-1}\Z$，记作$\Z_S$。
\begin{enumerate}[label=(\roman*)]
\item 决定$\Z_S$的单位群$U$；
\item 证明$P=\Z_S\setminus U$是$\Z_S$的唯一极大理想；
\item 证明$\Z_S$的每个非零理想是$P$的一个方幂。
\end{enumerate}''')
q(27,159,r'''设$S$为交换环$R$的一个子环而且$S$与$R$有相同的单位元素。证明：$R$的任一个素理想$P$与$S$的交$P\cap S$是$S$的一个素理想。问$R$的任一极大理想$M$与$S$的交$M\cap S$是不是$S$的极大理想？''')
q(28,159,r'''在$R_2=\Z[\sqrt2]$中，证明：
\begin{enumerate}[label=(\roman*)]
\item $\varepsilon=1+\sqrt2$是一个单位；
\item $R_2$的每个单位$u$可表成$u=\pm\varepsilon^r$，$r\in\Z$。因此$\pm\varepsilon^{\pm1}$是基本单位而且$R_2$的单位群$U=\langle-1\rangle\times\langle\varepsilon\rangle$。
\end{enumerate}''')
q(29,159,r'''在第4题的假设下，证明：
\begin{enumerate}[label=(\roman*)]
\item 当$m\equiv2$或$3\pmod4$时（$R_m=\Z[\sqrt m]$），$\sqrt m$的极小多项式是$x^2-m$；
\item 当$m\equiv1\pmod4$时（$R_m=\Z[\tfrac12(1+\sqrt m)]$），$\tfrac12(1+\sqrt m)$的极小多项式为$x^2-x+\tfrac14(1-m)$。
\end{enumerate}''')
q(30,160,r'''承上题。设$P$为$R_m$的一个非零素理想，证明：
\begin{enumerate}[label=(\roman*)]
\item 交$P\cap\Z$是$\Z$的一个非零素理想，因而$P\cap\Z=p\Z$，$p$是含于$P$内的唯一的素数；
\item 商环$F=R_m/P$是一个整环而且包含$F_p=\Z/p\Z$作为子域；
\item $F=F_p[\alpha]$，$\alpha$表示陪集$\sqrt m+P$或陪集$\tfrac12(1+\sqrt m)+P$，按照$m\equiv2$或$3\pmod4$或$m\equiv1\pmod4$而定，而且$\alpha$在$F_p$上的极小多项式是$x^2-m\pmod P$的因式，或是$x^2-x+\tfrac14(1-m)\pmod P$的因式，按照上述两种情况而定。总之$F$是$p$个元素或$p^2$个元素的有限整环，因而$F$是一个域。由此可知，$R_m$的任一非零素理想是极大理想。
\end{enumerate}''')
q(31,160,r'''承29题。设$p$为一素数，$p$在$R_m$内生成的理想记作$R_mp$，证明：
\begin{enumerate}[label=(\roman*)]
\item $R_mp\cap\Z=p\Z$，而且商环$R=R_m/R_mp$包含$F_p=\Z/p\Z$作为子域；
\item $R=F_p[\gamma]$，$\gamma$表示陪集$\sqrt m+R_mp$或陪集$\tfrac12(1+\sqrt m)+R_mp$，按照$m\equiv2$或$3\pmod4$或$m\equiv1\pmod4$而定。按照这两种情况，$\gamma$的极小多项式是$x^2-m\pmod{p\Z}$或$x^2-x+\tfrac14(1-m)\pmod{p\Z}$。总之，$R$是含$p^2$个元素的有限环；
\item 设$m\equiv2$或$3\pmod4$，$x^2-m\pmod{p\Z}$可约，若
\[
x^2-m\equiv(x-a)(x-b)\pmod{p\Z},
\]
其中$a,b\in\Z$而且$a\not\equiv b\pmod{p\Z}$，则$R_m$的理想
\[
P_1=(p,\sqrt m-a),\qquad P_2=(p,\sqrt m-b)
\]
是素理想，而且$R_mp=P_1\cap P_2=P_1P_2$；
\item 设$m$同于(iii)，$x^2-m\pmod{p\Z}$可约。若
\[
x^2-m\equiv(x-a)^2\pmod{p\Z},\qquad a\in\Z,
\]
则$R_m$的理想$P=(p,\sqrt m-a)$是素理想，而且$R_mp=P^2$。这种情况仅当$p=2$或$p\mid m$时才出现；
\item 设$m$同于(iii)，若$x^2-m\pmod{p\Z}$不可约，则$R_mp$是$R_m$的素理想；
\item 在情况(iii)--(v)中用$x^2-x+\tfrac14(1-m)$替代$x^2-m$，结论仍然成立。此时(iv)仅当$p\mid m$时才出现。
\end{enumerate}
因此，明显地决定了$R_m$的一切素理想。''')
q(32,160,r'''承29题。证明：
\begin{enumerate}[label=(\roman*)]
\item 设$d$为任一正整数，则商环$R_m/R_md$是含$d^2$个元素的有限环；
\item 设$A$为$R_m$的任一非零理想，则交$A\cap\Z$是$\Z$的一个非零理想。令$A\cap\Z=d\Z$，则商环$R_m/A$的元素的个数不超过$d^2$；
\item $R_m$是一个诺特环。
\end{enumerate}''')
q(33,161,r'''证明：
\begin{enumerate}[label=(\roman*)]
\item 诺特环的商环为诺特环；
\item 有限多个诺特环的直和为诺特环；
\item 诺特环的分式环为诺特环；
\item 举例说明诺特环的子环不一定是诺特环。
\end{enumerate}''')
q(34,161,r'''举例说明一个唯一因子分解整环$R$模它的一个素理想得到的商环不一定是唯一因子分解整环。''')
q(35,161,r'''举例说明唯一因子分解整环的子环不一定是唯一因子分解整环。''')
q(36,161,r'''证明诺特环的诣零根$N$是幂零的，即存在一个正整数$r$使得$N^r=(0)$。''')
q(37,161,r'''设$R$为一诺特环。证明$R$上形式幂级数环$R[[x]]$也是诺特环。''')
