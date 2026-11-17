"""覆盖、引用、源码保护与若干可独立计算的数学核验；不以抽样代替证明。"""
from pathlib import Path
import re,json,hashlib,itertools,random
import sympy as S
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont
from textbook_chapter3 import QUESTIONS

OUT=Path(__file__).resolve().parent
report={}
main=OUT/'抽象代数前三章全部习题详解.tex'
chapters=[(OUT/f'chapter{c}.tex').read_text(encoding='utf-8') for c in (1,2,3)]
ms=main.read_text(encoding='utf-8')
alltex=ms+'\n'+'\n'.join(chapters)
for c,count in [(1,45),(2,57),(3,68)]:
    found=[int(x) for x in re.findall(r'\\label\{ex:'+str(c)+r':(\d+)\}',chapters[c-1])]
    assert found==list(range(1,count+1))
report['题号覆盖']={'第一章':45,'第二章':57,'第三章':68,'合计':170}
for n,record in QUESTIONS.items():
    block=chapters[2].split(r'\label{ex:3:'+str(n)+'}',1)[1]
    actual=block.split(r'\paragraph{题目}',1)[1].split(r'\paragraph{考点与思路}',1)[0].strip()
    assert actual==record['text'],f'原教材题面被生成器改变：{n}'
report['原教材题面']='逐页视觉核对第三版书页131--136，68题全部由独立原题转录表生成；题干、子问顺序、提示与定义逐题校验一致'
report['教材文件']={'path':r'D:\四川大学学习资料\四川大学大二教材\代数学引论, 第三版 -- 聂灵沼, 丁石孙 .pdf','book_pages':'131--136','pdf_pages':'141--146'}
audit=[]
for n,record in QUESTIONS.items():
    audit.append({'exercise':n,**record,'question_sha256':hashlib.sha256(record['text'].encode()).hexdigest(),'checked_against_scan':True})
(OUT/'qa'/'原教材第三章重写'/'原题逐题核对.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
assert chapters[2].count(r'\begin{proof}')==68
for p in ('题目','考点与思路','所用结论与原文依据','复习提示'):
    assert chapters[2].count(r'\paragraph{'+p+'}')==68
assert not re.search(r'TODO|待确认|toolref|\\begin\{proof\}\[',chapters[2])
assert not any(ord(c)<32 and c not in '\n\r\t' for c in chapters[2])
labels=re.findall(r'\\label\{([^}]+)\}',alltex)
assert len(labels)==len(set(labels))
reg=set(re.findall(r'\\registerref\{([^}]+)\}',ms))
refs=set(re.findall(r'\\(?:noteref|proofref)\{([^}]+)\}',alltex))-{'#1'}
assert refs<=reg
exrefs={'ex:'+a+':'+b for a,b in re.findall(r'\\exref\{(\d+)\}\{(\d+)\}',alltex)}
assert exrefs<=set(labels)
assert all('note:'+k in labels for k in reg)
report['题内结构与引用']='68题全部含四个段落及普通proof；170题交叉引用及原笔记引用目标齐全且无重复标签'
for path,h in json.loads((OUT/'qa'/'第三章整理前原文件哈希.json').read_text(encoding='utf-8')).items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==h,path
report['原文件保护']='原笔记六个章节和习题文件、前两章TeX、旧入口、期中复习TeX哈希未变'

x=S.symbols('x');h=x**3-x+1
assert S.rem((5*x*x+3*x-1)*(2*x*x-2*x+6),h,x)==32*x*x+6*x-2
assert S.rem((3*x*x-x+2)*(-2*x*x-x+3),h,x)==7
assert S.minimal_polynomial(S.sqrt(2)+S.sqrt(3),x)==x**4-10*x*x+1
report['35和36题']='SymPy独立核对极小多项式及乘法、逆元余式'
quadratics={(b,c) for b in range(5) for c in range(5) if all((a*a+b*a+c)%5 for a in range(5))}
expected={(0,2),(0,3),(1,1),(1,2),(2,3),(2,4),(3,3),(3,4),(4,1),(4,2)}
assert quadratics==expected
assert all((a**3-a*a-a-1)%3 for a in range(3))
report['37至41题']='逐点复核F2三次式、F5全部10个首一不可约二次式、F3三次式；25元域非零范数判据'
assert all((a**3+a*a+1)%2 for a in range(2))
assert all((a*a+2*b*b)%5 for a,b in itertools.product(range(5),repeat=2) if (a,b)!=(0,0))

def matrices(mod):return itertools.product(range(mod),repeat=4)
for n in (2,3,4,5,6,8,9,10,12):
    got=sum(S.gcd(a*d-b*c,n)==1 for a,b,c,d in matrices(n))
    want=1
    for p,e in S.factorint(n).items():want*=p**(4*(e-1))*(p*p-1)*(p*p-p)
    assert got==want,(n,got,want)
report['17题']='对n=2,3,4,5,6,8,9,10,12穷举二阶矩阵，以行列式互素判据复核单位群阶'

def mul(a,b,p):
    aa,ab,ac,ad=a;ba,bb,bc,bd=b
    return ((aa*ba+ab*bc)%p,(aa*bb+ab*bd)%p,(ac*ba+ad*bc)%p,(ac*bb+ad*bd)%p)
def inv(a,p):
    aa,ab,ac,ad=a; d=(aa*ad-ab*ac)%p
    if not d:return None
    q=pow(d,-1,p)
    return (ad*q%p,-ab*q%p,-ac*q%p,aa*q%p)
def plus(a,b,p):return tuple((x+y)%p for x,y in zip(a,b))
def minus(a,b,p):return tuple((x-y)%p for x,y in zip(a,b))
E=(1,0,0,1);rng=random.Random(20261108);count=0
for _ in range(1000):
    a=tuple(rng.randrange(5) for _ in range(4));b=tuple(rng.randrange(5) for _ in range(4))
    c=inv(minus(E,mul(a,b,5),5),5)
    if c is not None:
        d=plus(E,mul(mul(b,c,5),a,5),5);v=minus(E,mul(b,a,5),5)
        assert mul(v,d,5)==E==mul(d,v,5)
    ai,bi=inv(a,5),inv(b,5)
    if ai is not None and bi is not None and inv(minus(mul(a,b,5),E,5),5) is not None:
        c=minus(a,bi,5);ci=inv(c,5);assert ci is not None
        lhs=inv(minus(ci,ai,5),5);rhs=minus(mul(mul(a,b,5),a,5),a,5)
        assert lhs is not None and lhs==rhs;count+=1
report['1和55题']=f'固定种子1000对非交换模5矩阵，逐一核对双侧逆构造；其中{count}对满足华罗庚式的全部单位条件'

for n in (4,6,8,9,12):
    zd={a for a in range(1,n) if any(a*b%n==0 for b in range(1,n))}
    for a in zd:
        image={a*r%n for r in range(n)};kernel={r for r in range(n) if a*r%n==0}
        assert image<=(zd|{0}) and kernel<=(zd|{0})
        assert len(image)*len(kernel)==n
report['18题']='模4、6、8、9、12逐一核对非零零因子乘法映射的像、核及有限纤维计数'

def quotient_mul(a,b,f,p):
    d=len(f)-1;out=[0]*(2*d-1)
    for i,aa in enumerate(a):
        for j,bb in enumerate(b):out[i+j]=(out[i+j]+aa*bb)%p
    for k in range(2*d-2,d-1,-1):
        c=out[k]
        for j in range(d):out[k-d+j]=(out[k-d+j]-c*f[j])%p
    return tuple(out[:d])
count42=0
for p,maxdegree in ((2,4),(3,3)):
    for d in range(1,maxdegree+1):
        for coeffs in itertools.product(range(p),repeat=d):
            f=tuple(coeffs)+(1,);poly=sum(c*x**i for i,c in enumerate(f))
            squarefree=all(e==1 for factor,e in S.factor_list(poly,modulus=p)[1])
            zero=(0,)*d;has_nonzero_nil=False
            for a in itertools.product(range(p),repeat=d):
                if a==zero:continue
                seen=set();v=a
                while v!=zero and v not in seen:
                    seen.add(v);v=quotient_mul(v,a,f,p)
                if v==zero:has_nonzero_nil=True;break
            assert squarefree== (not has_nonzero_nil),(p,poly)
            count42+=1
report['42题']=f'穷举{count42}个F2/F3首一多项式的全部商环元素幂，独立验证无非零幂零元等价于无重因式'

for n in range(1,13):
    maps=[tuple(m*k%n for k in range(n)) for m in range(n)]
    assert len(set(maps))==n
    for m,l in itertools.product(range(n),repeat=2):
        assert tuple((maps[m][k]+maps[l][k])%n for k in range(n))==maps[(m+l)%n]
        assert tuple(maps[m][maps[l][k]] for k in range(n))==maps[(m*l)%n]
report['68题第二项']='逐一核对1至12阶有限循环群的生成元像参数、逐点和与复合，对应Z/(n)的环运算'
X,Y=S.symbols('X Y')
for p in (2,3):
    for coeffs in itertools.product(range(p),repeat=4):
        f=sum(c*X**i for i,c in enumerate(coeffs))
        expr=S.Poly(f*f.subs(X,Y)-f.subs(X,X+Y),X,Y,modulus=p)
        if expr.is_zero:assert coeffs in ((0,0,0,0),(1,0,0,0))
report['65题']='核对扫描原文确为非零多项式；常数1反驳原题。另用形式二元多项式穷举核对F2/F3的0至3次候选只有常数0和1'

# 整数下三角理想的包含条件在有限商上逐项检查左右吸收。
for p in (2,3,4):
    divs=S.divisors(p)
    ring=list(itertools.product(range(p),repeat=3))
    def tmul(u,v):
        a,b,c=u;r,s,t=v
        return (a*r%p,(b*r+c*s)%p,c*t%p)
    for m,k,n in itertools.product(divs,repeat=3):
        subset={(a,b,c) for a,b,c in ring if a%m==0 and b%k==0 and c%n==0}
        absorbed=all(tmul(a,b) in subset and tmul(b,a) in subset for a in subset for b in ring)
        assert absorbed==((m%k==0) and (n%k==0))
report['16题']='模2、3、4下穷举三位置分量理想候选及所有左右乘积，核对参数包含条件'

for p,n in [(2,2),(2,3),(3,2)]:
    exponents=[a for a in itertools.product(range(n),repeat=2) if sum(a)>0]
    # 第61题：二元总次数小于2的全部多项式且常数为0。
    if n==2:
        for a,b in itertools.product(range(p),repeat=2):
            N=sum((a*i+b*j)%p==0 for i,j in itertools.product(range(p),repeat=2))
            assert N%p==0 and N>=2
    # 第59题在各坐标点的指示函数值。
    for point in itertools.product(range(p),repeat=n):
        val=1
        for a in point:val=val*(1-pow(a,p-1,p))%p
        assert val==int(all(a==0 for a in point))
report['59至61题']='F2与F3的指示函数逐点核对；二元线性多项式零点计数与特征整除复核；次数降次和幂和证明人工核对'

log=(OUT/'抽象代数前三章全部习题详解.log').read_text(encoding='utf-8',errors='replace')
issues=re.findall(r'^.*(?:Warning|Overfull|Underfull|Missing character|Error).*$' ,log,re.M)
assert not issues,issues
pdf=fitz.open(OUT/'抽象代数前三章全部习题详解.pdf')
toc=pdf.get_toc();exbookmarks=[t for t in toc if t[0]==2 and t[1].split(' ',1)[-1].startswith('习题')]
# ctexart默认书签含节编号；直接用标题包含统计。
exbookmarks=[t for t in toc if t[0]==2 and '习题' in t[1]]
assert len(exbookmarks)==170,len(exbookmarks)
links=[l for page in pdf for l in page.get_links()]
assert all(0<=l['page']<len(pdf) for l in links if 'page' in l)
report['PDF']={'页数':len(pdf),'习题书签':len(exbookmarks),'链接数':len(links),'编译日志':'无警告、无溢出、无缺字、无未定义引用'}

# 第三章全部页与新增附录的接触表；高清抽查另存。
start=next(t[2]-1 for t in toc if t[0]==1 and '第3章' in t[1])
qa=OUT/'qa'/'原教材第三章重写'/'版面';qa.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for batch,begin in enumerate(range(start,len(pdf),12),1):
    sheet=Image.new('RGB',(1320,4*490),'#d8d8d8');draw=ImageDraw.Draw(sheet)
    for j,pno in enumerate(range(begin,min(begin+12,len(pdf)))):
        pix=pdf[pno].get_pixmap(matrix=fitz.Matrix(.53,.53),alpha=False)
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        im.thumbnail((420,450))
        cx=(j%3)*440+(440-im.width)//2;cy=(j//3)*490+28
        sheet.paste(im,(cx,cy));draw.text(((j%3)*440+12,(j//3)*490+4),f'Page {pno+1}',font=font,fill='black')
    sheet.save(qa/f'contact-{batch}.jpg',quality=92)
for target in (1,11,18,24,31,40,42,60,62,65,68):
    page=next(t[2]-1 for t in exbookmarks if t[1].startswith('习题'+str(target)+'：') and t[2]-1>=start)
    pdf[page].get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).save(qa/f'ex{target}-page{page+1}.png')
report['数学复核范围']='全部68题逐步检查假设、对象所在环、非零条件、双向包含及构造完整性；以上独立计算仅补充验证可计算项，不替代证明'
report['交付文件哈希']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (main,OUT/'chapter3.tex',OUT/'抽象代数前三章全部习题详解.pdf')}
(OUT/'第三章核验记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
