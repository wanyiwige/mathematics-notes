from pathlib import Path
import re, json

root=Path(r'C:\Users\WANYIWIGE\Desktop\我的笔记\代数笔记')
work=root/'.codex-work'
backup=work/'linear-concept-review-backup-20261029'
if backup.exists(): raise RuntimeError('备份已存在，须避免重复加锚点。')
rows=[]
for line in (work/'linear-concept-review-20261029.tsv').read_text(encoding='utf-8').splitlines():
    c,n,names=line.split(';',2)
    rows.extend(dict(ch=int(c),line=int(n),name=name,target=f'p1:concept:c{c}-l{n}') for name in names.split('|'))
snapshots={}
updates={}
coverage=[]
exceptions={(1,323):'等式陈述，并未另定义一个概念。',
            (1,385):'最大公因子的另一刻画，概念已收入第101行。',
            (1,1396):'多项式乘积的次数公式，并非新概念。'}
for c in range(1,8):
    path=root/f'chapters/Part 1/chapter{c}.tex'
    raw=path.read_bytes(); snapshots[path]=raw
    s=raw.decode('utf-8'); lines=s.splitlines(keepends=True)
    for m in re.finditer(r'(?m)^[ \t]*\\begin\{definition\}[\s\S]*?\\end\{definition\}',s):
        start=s.count('\n',0,m.start())+1; end=start+m.group().count('\n')
        terms=[r['name'] for r in rows if r['ch']==c and start<=r['line']<=end]
        if not terms and (c,start) not in exceptions:
            raise RuntimeError(f'未检查的定义环境：{c}:{start}')
        coverage.append(dict(ch=c,start=start,end=end,terms=terms,reason=exceptions.get((c,start))))
    for n in sorted({r['line'] for r in rows if r['ch']==c}):
        line=lines[n-1]
        if not line.strip() or line.lstrip().startswith('%'): raise RuntimeError(f'跳转目标无效：{c}:{n}')
        anchor=f'\\phantomsection\\label{{p1:concept:c{c}-l{n}}}'
        ending='\r\n' if line.endswith('\r\n') else '\n'
        if re.match(r'^\s*\\begin\{',line):
            lines[n-1]=line.rstrip('\r\n')+anchor+ending
        elif re.match(r'^\s*\\item\b',line):
            lines[n-1]=re.sub(r'^(\s*\\item(?:\[[^\]]*\])?\s*)',lambda m:m.group()+anchor,line,count=1)
        else:
            indent=re.match(r'^\s*',line).group()
            lines[n-1]=indent+anchor+line[len(indent):]
    updated=''.join(lines)
    assert re.sub(r'\\phantomsection\\label\{p1:concept:c\d-l\d+\}','',updated)==s
    updates[path]=updated.encode('utf-8')

main_path=root/'main.tex'; main=main_path.read_bytes(); snapshots[main_path]=main
main_s=main.decode('utf-8')
needle=r'\input{chapters/Part 2/concept-review}'
if main_s.count(needle)!=1: raise RuntimeError('抽象代数表入口不唯一。')
newmain=main_s.replace(needle,'%\\input{chapters/Part 1/concept-review}\n\t'+needle)
updates[main_path]=newmain.encode('utf-8')
for path,raw in snapshots.items():
    if path.read_bytes()!=raw: raise RuntimeError(f'发现并发修改：{path}')
backup.mkdir()
for path,raw in snapshots.items():
    (backup/(path.parent.name+'-'+path.name)).write_bytes(raw)
for path,raw in updates.items(): path.write_bytes(raw)
(work/'linear-concept-entries-20261029.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'linear-concept-definition-audit-20261029.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(concepts=len(rows),targets=len({r['target'] for r in rows}),checked_definition_environments=len(coverage)),ensure_ascii=False))
