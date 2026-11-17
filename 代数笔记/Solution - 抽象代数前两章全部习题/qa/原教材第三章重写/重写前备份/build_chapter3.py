"""只生成第三章与新的前三章总入口；不重新生成已有前两章。"""
from pathlib import Path
import re, json, hashlib
from chapter3_data import DATA

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
SOURCE = ROOT / 'chapters' / 'Part 2'
MAIN = '抽象代数前三章全部习题详解.tex'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

protected = [SOURCE/f'chapter{c}{s}.tex' for c in (1,2,3) for s in ('','-exercises')]
protected += [OUT/'chapter1.tex',OUT/'chapter2.tex',OUT/'抽象代数前两章全部习题详解.tex']
protected += list((ROOT/'Solution - 抽象代数集中测验复习').glob('*.tex'))
baseline = OUT/'qa'/'第三章整理前原文件哈希.json'
baseline.parent.mkdir(exist_ok=True)
if not baseline.exists():
    baseline.write_text(json.dumps({str(p):digest(p) for p in protected},ensure_ascii=False,indent=2),encoding='utf-8')

src=(SOURCE/'chapter3-exercises.tex').read_text(encoding='utf-8-sig')
starts=list(re.finditer(r'\\begin\{problem\}',src))
original={}
for j,m in enumerate(starts):
    block=src[m.end():starts[j+1].start() if j+1<len(starts) else len(src)]
    head=block.split(r'\end{problem}',1)[0].strip()
    n=int(re.search(r'习题(\d+)：',head)[1])
    q=re.sub(r'^\\textbf\{习题\d+：\}', '',head).strip()
    original[n]={'question':q,'line':src[:m.start()].count('\n')+1}
assert list(original)==list(range(1,69))

# 这四题已在期中复习册逐步展开；只转换引用与普通证明标题。
review=(ROOT/'Solution - 抽象代数集中测验复习'/'chapter3.tex').read_text(encoding='utf-8-sig')
toolmap={'r-ring-laws':'ringlaws','r-unit-laws':'unit','r-homomorphism':'ringiso','r-quotients':'ideal'}
for n in (1,2,3,8):
    m=re.search(r'\\subsection\{习题'+str(n)+r'：',review)
    end=review.find(r'\subsection{',m.end())
    block=review[m.start():end if end>=0 else len(review)]
    title=re.search(r'\\subsection\{习题\d+：([^\n]+)\}\\label',block)[1]
    idea=block.split(r'\paragraph{考点与思路}',1)[1].split(r'\textbf{原文依据：}',1)[0].strip()
    proof=re.search(r'\\begin\{proof\}\[详细证明\](.*?)\\end\{proof\}',block,re.S)[1].strip()
    hint=block.split(r'\paragraph{复习提示}',1)[1].strip()
    proof=re.sub(r'习题(\d+)',lambda m:r'\exref{3}{'+m[1]+'}',proof)
    hint=re.sub(r'习题(\d+)',lambda m:r'\exref{3}{'+m[1]+'}',hint)
    if n==2:
        proof=proof.replace(r'\textbf{第一步：证明条件 (1) 与条件 (2) 等价。}',r'\begin{enumerate}\item 证明条件(1)与条件(2)等价。')
        proof=proof.replace(r'\textbf{第二步：证明条件 (1) 与条件 (3) 等价。}',r'\item 证明条件(1)与条件(3)等价。')
        proof+='\n'+r'\end{enumerate}'
    if n==8:
        for i,t in enumerate(('i','ii','iii','iv','v','vi')):
            verdict='成立' if i in (0,4) else '不成立'
            before=r'\textbf{('+t+') '+verdict+'。}'
            after=(r'\begin{enumerate}[label=(\roman*)]\item ' if i==0 else r'\item ')+verdict+'。'
            assert before in proof
            proof=proof.replace(before,after)
        proof+='\n'+r'\end{enumerate}'
    DATA[n]=dict(title=title,idea=idea,proof=proof,hint=hint,refs='ringlaws,unit' if n!=8 else 'ringiso,ideal',question=None)
assert sorted(DATA)==list(range(1,69))

# 以实际源码中的具名小节、环境起始行定位；注释内容不伪造当前PDF编号。
locations={
 'c3correspondence':(130,'环的同态定理','环的对应定理'),
 'c3isomorphism':(169,'环的同态定理','第三同构定理及其证明'),
 'c3direct':(254,'环的直和','直和定义、分量理想与内直和'),
 'c3product':(332,'环的直和','理想积的定义与分配律'),
 'c3comaximal':(356,'环的直和','互素理想的积等于交'),
 'c3crt':(379,'环的直和','中国剩余定理及证明'),
 'c3principal':(442,'环的直和','生成理想与主理想的定义及表达式'),
 'c3anti':(469,'环的反同构','反同构、反同态与反自同构定义'),
 'c3conjugate':(498,'环的反同构','四元数共轭与乘法表'),
 'c3prime':(564,'素理想和极大理想','素理想、极大理想及商环判据'),
 'c3maxexists':(708,'素理想和极大理想','极大理想存在性与佐恩引理构造'),
 'c3nil':(717,'素理想和极大理想','幂零元等于全部素理想之交'),
 'c3fraction':(758,'商域和分式环','商域的存在与分式表示'),
 'c3poly':(1149,'交换环上的多项式环','多项式环的定义、系数唯一性和代入'),
 'c3multi':(1296,'交换环上的多项式环','多元多项式环的定义'),
 'c3algebraic':(1340,'交换环上的多项式环','代数关系与代数无关的定义'),
 'c3polyquot':(1366,'交换环上的多项式环','系数取商诱导的多项式商环同构'),
 'c3degree':(1392,'整环上的一元多项式环','次数法则、整环性与单位'),
 'c3division':(1429,'整环上的一元多项式环','带余除法与因式定理'),
 'c3roots':(1473,'整环上的一元多项式环','非零多项式的根数上界'),
 'c3qroots':(1490,'整环上的一元多项式环','四元数二次方程的共轭根构造'),
 'c3finite':(1517,'整环上的一元多项式环','有限乘法子群循环、有限域非零元的幂'),
 'c3minimal':(1569,'整环上的一元多项式环','极小多项式定义与商环刻画'),
 'c3irred':(1587,'整环上的一元多项式环','不可约定义与极大理想、商域的等价性'),
 'c3nilideal':(1699,'整环上的一元多项式环','幂零理想定义'),
 'c3functions1':(1746,'多项式函数','一元多项式函数与形式多项式的对应'),
 'c3functionsN':(1802,'多项式函数','无限域的多元零函数判据及有限域低次数代表的唯一性'),
}
source_lines=(SOURCE/'chapter3.tex').read_text(encoding='utf-8-sig').splitlines()
for key,(line,sec,name) in locations.items():
    assert source_lines[line-1].lstrip('%').startswith(r'\begin'),(key,line)

def reftext(refs):
    out=[]
    for key in refs.split(','):
        if key.startswith('ex'):
            c,n=key[2:].split(':');out.append(r'\exref{'+c+'}{'+n+'}')
        else:out.append(r'\noteref{'+key+'}')
    return '；'.join(out)

pieces=['% !TEX root = '+MAIN+'\n',r'\clearpage\section{第3章：环}',r'''
本章收录原习题1--68题。涉及$1$、可逆元、素理想和极大理想时，以幺环为背景；交换性及非零条件在需要处说明。幂零元也称零幂元，$r(R)$为幂零根，$J(R)$为全部极大理想之交。第26--29题的若尔当同态统一采用第26题明确给出的三重乘积条件。新补的推导沿现有习题解答展开，不声称已经另行核对原教材书页。
''']
for n in range(1,69):
    d=DATA[n];base=original[n]
    question=d['question'] or base['question']
    if n in (2,8):
        block_start=re.search(r'\\subsection\{习题'+str(n)+r'：',review).start()
        bb=review[block_start:]
        question=bb.split(r'\paragraph{题目}',1)[1].split(r'\paragraph{考点与思路}',1)[0].strip()
    pieces += [r'\subsection{习题'+str(n)+'：'+d['title']+'}',
               r'\label{ex:3:'+str(n)+'}',r'\paragraph{题目}',question,
               r'\paragraph{考点与思路}',d['idea'],
               r'\paragraph{所用结论与原文依据}',reftext(d['refs'])+'。原解位置：'+r'\path{chapters/Part 2/chapter3-exercises.tex}'+f'，第{base["line"]}行起。'+('本题沿用期中复习册第三章已经展开的证明。' if n in (1,2,3,8) else '本题在现有习题解答的思路内补齐推导。'),
               '% 原题和原解来源同上；新增中间推导为本册补写。',
               r'\begin{proof}',d['proof'].strip(),r'\end{proof}',
               r'\paragraph{复习提示}',d['hint'],'']
chapter='\n\n'.join(pieces)+'\n'
(OUT/'chapter3.tex').write_text(chapter,encoding='utf-8')

# 总入口由现有前两章入口扩充；保留前两章所有手工内容和引用表。
s=(OUT/'抽象代数前两章全部习题详解.tex').read_text(encoding='utf-8-sig')
s=s.replace('第一章与第二章习题分别通过 input 加载','第一、二、三章习题分别通过 input 加载')
s=s.replace('抽象代数前两章习题详解','抽象代数前三章习题详解')
s=s.replace(r'第二章1--57题}',r'第二章1--57题\quad 第三章1--68题}')
s=s.replace(r'\date{2026年11月4日}',r'\date{}')
old='本册收录现有代数笔记抽象代数第一章45题、第二章57题，共102题，保留原题号。'
assert old in s
s=s.replace(old,'本册收录现有代数笔记抽象代数第一章45题、第二章57题、第三章68题，共170题，保留原题号。')
s=s.replace('期中复习册已经展开的41题作为本次详解的基础，其余61题重新展开。','前两章沿用已经整理的102题；第三章以现有68题及期中复习册已展开的4题为依据补齐证明。')
s=s.replace('这里的第一、二章均指抽象代数部分','这里的第一、二、三章均指抽象代数部分')
registry=[]; rows=[]
for key,(line,sec,name) in locations.items():
    commented=source_lines[line-1].startswith('%')
    state='，现为源码注释' if commented else '，当前正文'
    label='原笔记第3章“'+sec+'”节（'+name+state+'）'
    registry.append(r'\registerref{'+key+'}{'+label+'}')
    rows.append(r'\phantomsection\label{note:'+key+'}原笔记第3章“'+sec+'”节 & '+name+'；'+('现为源码注释，按源码回查。' if commented else '当前正文。')+r'\newline\path{chapters/Part 2/chapter3.tex}，第'+str(line)+r'行起。\\')
s=s.replace(r'\title{','\n'.join(registry)+'\n\n'+r'\title{',1)
s=s.replace(r'\input{chapter2}',r'\input{chapter2}'+'\n\n'+r'\input{chapter3}',1)
note='第三章引用按具名小节和源码行号定位：其中原笔记已注释的小节明确标为“现为源码注释”，不为其编造当前PDF定理编号。已有前两章的引用及题目内容沿用原文件。'
s=s.replace(r'\tableofcontents',note+'\n\n'+r'\tableofcontents',1)
end=r'\bottomrule\end{longtable}\normalsize'
assert s.count(end)==1
s=s.replace(end,'\n'.join(rows)+'\n'+end,1)
end2=r'\bottomrule\end{longtable}\end{document}'
assert s.count(end2)==1
index='\n'.join('3 & '+r'\hyperref[ex:3:'+str(n)+']{'+str(n)+'：'+DATA[n]['title']+r'}\\' for n in range(1,69))
s=s.replace(end2,index+'\n'+end2,1)
(OUT/MAIN).write_text(s,encoding='utf-8')

# 旧生成器仍仅负责旧入口；新增生成器不覆盖旧入口与前两章。
for p,h in json.loads(baseline.read_text(encoding='utf-8')).items():
    assert digest(Path(p))==h, f'受保护文件已变化：{p}'
print(json.dumps({'第三章题数':68,'新入口':MAIN,'chapter3行数':len(chapter.splitlines()),'原文件哈希检查':'通过'},ensure_ascii=False))
