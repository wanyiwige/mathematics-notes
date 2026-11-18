"""生成第四章与前四章入口；不重新生成前三章或改动原笔记。"""
from pathlib import Path
import re,json,hashlib,subprocess
from textbook_chapter4 import QUESTIONS
from chapter4_solutions import DATA

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
NOTES=ROOT/'chapters'/'Part 2'/'chapter4.tex'
MAIN='抽象代数前四章全部习题详解.tex'
SOURCE_PDF=Path(r'D:\四川大学学习资料\四川大学大二教材\代数学引论, 第三版 -- 聂灵沼, 丁石孙 .pdf')
QA=OUT/'qa'/'原教材第四章'
QA.mkdir(parents=True,exist_ok=True)
assert sorted(QUESTIONS)==sorted(DATA)==list(range(1,38))

protected=[ROOT/'main.tex',ROOT/'main.pdf',NOTES,NOTES.with_name('chapter3.tex')]
protected += [OUT/f'chapter{c}.tex' for c in (1,2,3)]
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
snapshot=QA/'开始时原文件哈希.json'
if not snapshot.exists():snapshot.write_text(json.dumps(before,ensure_ascii=False,indent=2),encoding='utf-8')

lines=NOTES.read_text(encoding='utf-8-sig').splitlines()
def find(text):
    return next(i for i,l in enumerate(lines,1) if text in l)
refs={
 'c4div':(find(r'\begin{definition}'),'整除、相伴、不可约元与素元的定义'),
 'c4gcd':(find('若$d\\mid a,d\\mid b$'),'最大公因子与最小公倍数的定义'),
 'c4pidprime':(find(r'\label{p2:pid-primes}'),'主理想整环的不可约元为素元及非零素理想极大'),
 'c4bezout':(find(r'\label{p2:pid-bezout}'),'主理想整环的贝祖表示'),
 'c4chain':(find('理想列$N_1'),'因子降链与链终止的定义'),
 'c4euclid':(find('若存在函数$d:'),'欧几里得整环的除法定义'),
 'c4quadratic':(find('设$m\\ne0,1$为无平方因子'),'二次域、共轭、范数与代数整数环'),
 'c4gaussian':(find('高斯整数环$R_{-1}'),'高斯整数环的范数欧几里得除法'),
 'c4ufd':(find('若整环$R$满足下列条件'),'唯一因子分解整环的定义'),
 'c4ufdcriterion':(find(r'\label{p2:ufd-criterion}'),'素元与因子链条件的唯一分解判据'),
 'c4nonufd':(find(r'$R=\Z[\sqrt{-5}]$不是'),'负五平方根整数环不唯一分解的例子'),
 'c4gauss':(find(r'\label{p2:gauss-primitive}'),'本原多项式乘积的高斯引理'),
 'c4primitive':(find(r'\label{p2:primitive-fraction-field}'),'本原多项式在商域上的相伴与不可约性'),
 'c4polynomial':(find(r'\label{p2:polynomial-ufd}'),'唯一分解整环的多项式扩张'),
 'c4eisenstein':(find(r'\label{p2:eisenstein}'),'艾森斯坦不可约性判别'),
 'c4noeth':(find(r'\label{p2:noetherian-equivalences}'),'诺特性、极大条件和理想有限生成的等价性'),
 'c4hilbert':(find(r'\label{p2:hilbert-basis}'),'希尔伯特基定理及其系数理想证明'),
 'c4zprimes':(find(r'\label{p2:z-polynomial-primes}'),'整数多项式环素理想分类与非零主素理想不极大'),
}
def section(line):
    return [re.search(r'\\section\{(.+)\}',l)[1] for l in lines[:line] if re.match(r'\\section\{',l)][-1]
def reftext(keys):
    parts=[]
    for k in keys.split(','):
        if k.startswith('ex'):
            c,n=k[2:].split(':');parts.append(r'\exref{'+c+'}{'+n+'}')
        else:parts.append(r'\noteref{'+k+'}')
    return '；'.join(parts)

pieces=['% !TEX root = '+MAIN,r'\clearpage\section{第4章：整环的整除性}',
        r'原题据聂灵沼、丁石孙《代数学引论》第三版书页157--161（扫描PDF第167--171页）逐页转录。原题的条件、子问和提示保留；可核实的问题在解答中单独说明。各题的证明为本册解答，引用原笔记的定义、定理与证明。']
audit=[]
for n in range(1,38):
    d=DATA[n];q=QUESTIONS[n]
    source=f'原题：《代数学引论》第三版，书页{q["book_page"]}'+('--161' if n==32 else '')+f'，扫描PDF第{q["pdf_page"]}页'+('起。' if n==32 else '。')
    pieces += [r'\subsection{习题'+str(n)+'：'+d['title']+'}',r'\label{ex:4:'+str(n)+'}',
        r'\paragraph{题目}',q['text'],r'\paragraph{考点与思路}',d['idea'],
        r'\paragraph{所用结论与原文依据}',reftext(d['refs'])+'。'+source,
        '% 原题来自扫描本；下列证明为本册补写，不声称教材提供了原解。',
        r'\begin{proof}',d['proof'],r'\end{proof}',r'\paragraph{复习提示}',d['hint']]
    audit.append({'exercise':n,**q,'question_sha256':hashlib.sha256(q['text'].encode()).hexdigest()})
(OUT/'chapter4.tex').write_text('\n\n'.join(pieces)+'\n',encoding='utf-8')

s=(OUT/'抽象代数前三章全部习题详解.tex').read_text(encoding='utf-8-sig')
s=s.replace('抽象代数前三章习题详解','抽象代数前四章习题详解')
s=s.replace('第一、二、三章习题分别通过 input 加载','第一至第四章习题分别通过 input 加载')
s=s.replace(r'第三章1--68题}',r'第三章1--68题\quad 第四章1--37题}')
s=s.replace('第三章68题，共170题','第三章68题、第四章37题，共207题')
s=s.replace('第三章题面直接按原教材逐页核对','第三、四章题面直接按原教材逐页核对')
s=s.replace('第三章的68题题面直接按原教材书页131--136逐页核对，解答按原题重写。','第三章的68题按教材书页131--136核对，第四章的37题按书页157--161核对，解答按原题展开。')
s=s.replace('这里的第一、二、三章均指抽象代数部分','这里的第一至第四章均指抽象代数部分')
s=s.replace('不采用当前只启用第三章的主PDF中的临时章号','不采用主PDF中因选编章节而产生的临时章号')
s=s.replace(r'\input{chapter3}',r'\input{chapter3}'+'\n\n'+r'\input{chapter4}',1)
registrations=[];rows=[]
for key,(line,name) in refs.items():
    sec=section(line)
    label='原笔记第4章“'+sec+'”节（'+name+'）'
    registrations.append(r'\registerref{'+key+'}{'+label+'}')
    rows.append(r'\phantomsection\label{note:'+key+'}原笔记第4章“'+sec+'”节 & '+name+r'。\newline\path{chapters/Part 2/chapter4.tex}，第'+str(line)+r'行起。\\')
s=s.replace(r'\title{','\n'.join(registrations)+'\n\n'+r'\title{',1)
end=r'\bottomrule\end{longtable}\normalsize'
assert s.count(end)==1
s=s.replace(end,'\n'.join(rows)+'\n'+end,1)
end=r'\bottomrule\end{longtable}\end{document}'
assert s.count(end)==1
idx='\n'.join('4 & '+r'\hyperref[ex:4:'+str(n)+']{'+str(n)+'：'+DATA[n]['title']+r'}\\' for n in range(1,38))
s=s.replace(end,idx+'\n'+end,1)
(OUT/MAIN).write_text(s,encoding='utf-8')

(QA/'原题逐题记录.json').write_text(json.dumps({'source_pdf':str(SOURCE_PDF),'pages':'书页157--161 / PDF167--171','questions':audit},ensure_ascii=False,indent=2),encoding='utf-8')
for p,h in before.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
print(json.dumps({'第四章题数':len(DATA),'总题数':207,'主文件':MAIN,'原笔记与前三章':'生成过程中未改动','检查范围':'仅编译，不渲染输出PDF'},ensure_ascii=False))
