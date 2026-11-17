from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[2]
integral=re.compile(r'\\(?:int|iint|iiint|iiiint|idotsint|oint|oiint|oiiint)(?![A-Za-z])')

def escaped(s,i):
    n=0;i-=1
    while i>=0 and s[i]=='\\': n+=1;i-=1
    return n%2==1

def inline_ranges(s):
    i=0; start=None; mode=None
    while i<len(s):
        if s[i]=='%' and not escaped(s,i):
            j=s.find('\n',i); i=len(s) if j<0 else j+1; continue
        if s.startswith('$$',i) and not escaped(s,i):
            if mode is None: mode='display'
            elif mode=='display': mode=None
            i+=2; continue
        if s[i]=='$' and not escaped(s,i):
            if mode is None: mode='dollar';start=i+1
            elif mode=='dollar': yield start,i;mode=None;start=None
            i+=1;continue
        if s.startswith('\\(',i) and not escaped(s,i) and mode is None:
            mode='paren';start=i+2;i+=2;continue
        if s.startswith('\\)',i) and not escaped(s,i) and mode=='paren':
            yield start,i;mode=None;start=None;i+=2;continue
        i+=1
    if mode in ('dollar','paren'): raise ValueError('Unclosed inline math')

report=[]
paths=[root/'main.tex']+sorted((root/'chapters').glob('*.tex'))+sorted((root/'preamble').glob('*.tex'))
for p in paths:
    s=p.read_text(encoding='utf-8'); inserts=[]; total=0
    for a,b in inline_ranges(s):
        block=s[a:b]
        for m in integral.finditer(block):
            total+=1
            if not re.search(r'\\displaystyle\s*$',block[:m.start()]):
                inserts.append(a+m.start())
    for i in reversed(inserts): s=s[:i]+'\\displaystyle'+s[i:]
    if inserts: p.write_text(s,encoding='utf-8')
    if total: report.append({'file':str(p.relative_to(root)),'inline_integrals':total,'inserted':len(inserts)})
(root/'教材对照/工作材料/行内积分排版记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('INLINE_INTEGRALS',sum(x['inline_integrals'] for x in report),'INSERTED',sum(x['inserted'] for x in report),'FILES',sum(x['inserted']>0 for x in report))
