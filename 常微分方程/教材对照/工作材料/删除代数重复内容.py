from pathlib import Path
import re,json,zipfile,hashlib,datetime
r=Path(__file__).resolve().parents[2]
stamp='20261030-'+datetime.datetime.now().strftime('%H%M%S')
backup=r.parent/'常微分方程备份'/f'代数重复内容删减前-{stamp}.zip'
files=[r/'main.tex',r/'main.pdf']+list((r/'chapters').glob('*.tex'))+list((r/'preamble').glob('*.tex'))
with zipfile.ZipFile(backup,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for p in files:z.write(p,p.relative_to(r).as_posix())
assert zipfile.ZipFile(backup).testzip() is None
text={i:(r/f'chapters/chapter{i}.tex').read_text(encoding='utf-8') for i in range(1,16)}
before=text.copy();changes=[]
def change(i,a,b,reason,source):
    assert text[i].count(a)==1,(i,a[:80],text[i].count(a))
    text[i]=text[i].replace(a,b)
    changes.append({'chapter':i,'reason':reason,'algebra_source':source,'before':a,'after':b})
def env(i,marker,end,reason,source,replacement=''):
    a=text[i].index(marker);b=text[i].index(end,a)+len(end)
    change(i,text[i][a:b],replacement,reason,source)
def proved(i,marker,envname,reason,source):
    a=text[i].index(marker);b=text[i].index('\\end{'+envname+'}',a)+len('\\end{'+envname+'}')
    c=text[i].index(r'\begin{proof}',b);assert not text[i][b:c].strip()
    e=text[i].index(r'\end{proof}',c)+len(r'\end{proof}')
    change(i,text[i][a:e],'',reason,source)

env(4,r'\begin{definition}[线性泛函与对偶空间]',r'\end{definition}',
    '删除线性函数、对偶空间及其维数的重复定义；只保留取值映射的应用。','Part 1/chapter7.tex:7-30',
    r'对给定的 $t$，取值映射 $f\mapsto f(t)$ 是函数空间上的线性函数。')
proved(4,r'\begin{lemma}[Cayley--Hamilton 恒等式]','lemma','删除已在代数笔记证明的 Hamilton--Cayley 定理。','Part 1/chapter5.tex:1461-1520')
env(4,r'\begin{definition}[群、子群与一般线性群]',r'\end{definition}',
    '删除群、子群、同态、核及一般线性群的重复定义，只保留本文记号。','Part 2/chapter1.tex:13-143,243-309,480-546',
    r'以下将 $n$ 阶实一般线性群记为 $GL(n,\R)$。')
change(4,r'所有求值泛函若不能张成 $V^*$','所有取值映射若不能张成 $V^*$','沿用代数笔记“线性函数”的名称。','Part 1/chapter7.tex:12-22')
change(4,'因此可从这些泛函选出一组基','因此可从这些线性函数中选出一组基','统一名称。','Part 1/chapter7.tex:12-30')
change(4,r'任意求值泛函都是 $V$ 上的连续线性泛函',r'任意取值映射都是 $V$ 上的连续线性函数','统一名称。','Part 1/chapter7.tex:12-30')
for i in (4,9):
    change(i,'Cayley--Hamilton','Hamilton--Cayley','定理名称与代数笔记一致。','Part 1/chapter5.tex:1399-1520')
env(4,r'\begin{definition}[对称矩阵与正定性]',r'\end{definition}',
    '删去对称、正定和正交矩阵的重复定义，保留不属于这些代数定义的 Hessian 记号。','Part 1/chapter3.tex:850-866; chapter6.tex:698-715,970-1048',
    r'''\begin{definition}[Hessian 矩阵]
对二次连续可微实函数，Hessian 矩阵指 $D^2f=(\partial_i\partial_jf)_{i,j}$；混合偏导相等使它对称。
\end{definition}''')
proved(4,r'\begin{lemma}[实对称矩阵的正交分解]','lemma','删除实对称矩阵正交对角化及正定性判别的重复证明。','Part 1/chapter6.tex:1750-1864; chapter7.tex:1664-1680')
env(4,r'\begin{definition}[正定矩阵的平方根]',r'\end{definition}',
    '删除正定平方根的重复构造；代数笔记还证明了唯一性。','Part 1/chapter7.tex:1773-1800')

change(6,r'''\begin{definition}[商空间、圆周与圆柱]\label{def:quotient-circle}
在集合 $X$ 上，满足自反、对称和传递性的关系称等价关系。
等价类记为 $[x]=\{y:y\sim x\}$，这些类组成商集 $X/{\sim}$，自然投影为 $\pi(x)=[x]$。
若 $X$ 有拓扑，规定''',r'''\begin{definition}[商拓扑、圆周与圆柱]\label{def:quotient-circle}
设 $X$ 是拓扑空间，$X/{\sim}$ 是某等价关系确定的商集，$\pi:X\to X/{\sim}$ 为自然映射。规定''',
    '不复述等价关系和等价类，保留代数商结构之外的商拓扑及圆周相空间。','Part 1/chapter4.tex:274-324; Part 2/chapter1.tex:681-728; chapter2.tex:1025-1042')

change(7,r'''\begin{definition}[群作用与对称性]
群 $G$ 对集合 $M$ 的作用是映射 $(g,x)\mapsto gx$，满足
$ex=x$、$(gh)x=g(hx)$。集合 $Gx$ 称为 $x$ 的轨道。
保持向量场''',r'''\begin{definition}[向量场的对称]
保持向量场''','删除一般群作用与群轨道的重复定义；保留向量场对称这一新概念。','Part 2/chapter2.tex:923-943,1025-1042')
change(7,'作用的两条轨道相交则重合；向量场的对称等价于它与局部相流可交换。','向量场的对称等价于它与局部相流可交换。','删去代数笔记已证明的群轨道相交性质。','Part 2/chapter2.tex:1025-1042')
change(7,r'''先证轨道结论。若 $gx=hy$，则 $y=h^{-1}gx$。
对任意 $k\in G$，有 $ky=kh^{-1}gx\in Gx$，所以 $Gy\subset Gx$。
交换两点的角色也得反向包含，因此两条轨道重合。

''','','删除上述重复性质的证明，不动向量场对称与相流可交换的证明。','Part 2/chapter2.tex:1025-1042')
change(7,r'\begin{definition}[闭子群与陪集]',r'\begin{definition}[拓扑群与闭子群]','标题只保留新的拓扑概念。','Part 2/chapter1.tex:309-339')
change(7,r'子群 $H$ 的加法陪集为 $x+H=\{x+h:h\in H\}$；乘法记号下写为 $gH$。','',
    '删除陪集的重复定义。','Part 2/chapter1.tex:309-339')

change(8,r'\begin{definition}[平方平均空间与正交]',r'\begin{definition}[平方平均空间与完全性]','不再重复有限维内积空间中的正交定义。','Part 1/chapter6.tex:101-120,345-369')
change(8,'内积为零称正交；范数为 1 且两两正交的族称标准正交系。\n其有限线性组合在 $2$ 范数下稠密时，称完全正交系。',
    '一个正交系的有限线性组合在 $2$ 范数下稠密时，称该正交系完全。',
    '删去正交、标准正交系的复述，保留无限维平方平均意义的完全性。','Part 1/chapter6.tex:101-120,345-369')

env(11,r'\begin{definition}[正交群与特殊正交群]',r'\end{definition}',
    '删去正交群、特殊正交群及反对称矩阵的重复定义，保留群的流形结构和连通性证明。','Part 1/chapter3.tex:850-867; chapter6.tex:1043-1048,1156-1161',
    r'下文将实正交群及特殊正交群分别记为 $O(n)$ 和 $SO(n)$。')
change(11,r'这里平方根按定义~\ref{def:positive-matrix-root} 构造，$Q=AP^{-1}$ 满足',
    r'取 $A^TA$ 的正定平方根，并令 $Q=AP^{-1}$，则',
    '删去指向重复定义的引用，直接使用已有正定平方根，保留极分解的应用计算。','Part 1/chapter7.tex:1773-1800')
change(11,r'''\begin{definition}
四元数代数 $\mathbb H$ 的实基为 $1,i,j,k$，乘法满足
$i^2=j^2=k^2=ijk=-1$；共轭把后三个系数变号。''',r'''\begin{definition}[四元数的共轭与范数]
四元数的标准基记为 $1,i,j,k$。对 $q=a+bi+cj+dk$，定义其共轭为
$\overline q=a-bi-cj-dk$。''','删去四元数体的基和乘法表的重复介绍；保留代数笔记未定义的共轭、范数和纯虚部分。','Part 2/chapter1.tex:1090-1147')

change(12,r'切空间 $T_xM$ 上的线性泛函称余向量，全体构成对偶空间 $T_x^*M$。',
    r'记切空间的对偶空间为 $T_x^*M$，其中的元素称余向量。','不重复一般对偶空间的定义，只定义切空间中的新名称。','Part 1/chapter7.tex:12-30')
change(12,r'''这里正交化的具体步骤是：从线性无关的 $a_j$ 出发，依次令
$b_j=a_j-\sum_{i<j}\langle a_j,e_i\rangle e_i$、$e_j=b_j/|b_j|$。
线性无关使分母不为零，故在相应小邻域内这些向量光滑。''',
    '由 Schmidt 正交化可在足够小的邻域内选取这样的标架；由于各次除法的分母不为零，所得向量随参数光滑变化。',
    '删去 Schmidt 正交化的重复公式，仅说明在局部法向标架中的应用。','Part 1/chapter6.tex:290-343')

oldlabels=set(re.findall(r'\\label\{([^}]+)\}','\n'.join(before.values())))
new='\n'.join(text.values());labels=re.findall(r'\\label\{([^}]+)\}',new)
removed=sorted(oldlabels-set(labels));assert removed==sorted(['lem:cayley-hamilton-foundation','def:group-notation','lem:symmetric-spectral-elementary','def:positive-matrix-root'])
assert len(labels)==len(set(labels))
refs=re.findall(r'\\(?:ref|eqref|autoref)\{([^}]+)\}',new)
assert not set(removed)&set(refs)
for i,s in text.items():
    for e in ('definition','theorem','proof','lemma','proposition','corollary'):
        assert s.count('\\begin{'+e+'}')==s.count('\\end{'+e+'}'),(i,e)
    assert r'\input{' not in s
    assert not any(ord(c)<32 and c not in '\n\r\t' for c in s)
# This turn only changes newly added material, never the original six-chapter baseline.
original='\n'.join((r/f'教材对照/工作材料/整合前原稿/chapter{i}.tex').read_text(encoding='utf-8') for i in range(1,7))
for c in changes:
    if c['chapter']<=6 and len(c['before'])>30:
        assert re.sub(r'\s+','',c['before']) not in re.sub(r'\s+','',original),c['reason']
for i,s in text.items():
    if s!=before[i]:(r/f'chapters/chapter{i}.tex').write_text(s,encoding='utf-8')
environments=('definition','theorem','proof','lemma','proposition','example','corollary')
allbefore='\n'.join(before.values())
result={'date':'2026-10-30','backup':str(backup),'backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'changes':changes,
'changed_chapters':[i for i in text if text[i]!=before[i]],'removed_labels':removed,'current_labels':len(labels),
'net_removed_environments':{e:allbefore.count('\\begin{'+e+'}')-new.count('\\begin{'+e+'}') for e in environments},
'new_environments_vs_original':{e:new.count('\\begin{'+e+'}')-original.count('\\begin{'+e+'}') for e in environments},
'no_dangling_removed_references':True}
(r/'教材对照/工作材料/代数重复内容删减记录.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['backup','changed_chapters','removed_labels','net_removed_environments']},ensure_ascii=False,indent=2))
