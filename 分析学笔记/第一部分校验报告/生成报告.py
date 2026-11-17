from pathlib import Path
import re, json, hashlib, csv

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
KINDS='definition theorem lemma proposition corollary proof example construction axiom remark prp note ill problem solution'.split()

def render(n,title,summary,sections,issues,notes='',unproved=()):
    src=ROOT/'chapters'/'part1'/f'chapter{n}.tex'
    lines=src.read_text(encoding='utf-8-sig').splitlines()
    link=lambda a:f'[{a}行](<{src.as_posix()}:{a}>)'
    counts={s:sum(i[0]==s for i in issues) for s in ('A','B','C')}
    chunks=[f'# 第一部分第{n}章第一轮数学校验报告\n\n{title}\n\n日期：2026-10-14。审查对象：当前源码，共{len(lines)}行。笔记源文件未修改。\n\n## 总体结论\n\n{summary}\n\n问题分级：A为定义/结论/公式错误；B为证明缺口或条件不足；C为表述、符号与引用问题。计数按问题条目，不按错误字符或定理数量：A {counts["A"]}项，B {counts["B"]}项，C {counts["C"]}项。建议均仅写在报告中。\n\n## 按节覆盖\n\n| 范围 | 内容 | 核验结果 |\n|---|---|---|']
    for a,b,name,verdict in sections: chunks.append(f'| {link(a)}—{b} | {name} | {verdict} |')
    chunks.append('\n## 问题与核验依据\n')
    for j,(level,a,b,name,detail,fix,check) in enumerate(issues,1):
        chunks.append(f'### {n:02d}-{j:02d} [{level}] {name}\n\n位置：{link(a)}—{b}。\n\n{detail}\n\n建议：{fix}\n\n复核：{check}\n')
    chunks.append('\n## 逐项检查记录\n\n下表按源码顺序列出全部数学环境。相邻正文、推导、图表及未使用环境的数学论述也已纳入上面的按节覆盖和问题表。证明判定以已声明的局部约定为依据；前置定义有错误时，局部推导通过不代表整条构造链已经成立。合理省略不会自动计为数学错误。\n\n| 行号 | 类型 | 内容定位 | 状态 |\n|---|---|---|---|')
    stack=[]; blocks=[]
    for k,line in enumerate(lines,1):
        clean=re.split(r'(?<!\\)%',line)[0]
        for m in re.finditer(r'\\(begin|end)\{('+ '|'.join(KINDS)+r')\}',clean):
            action,kind=m.groups()
            if action=='begin': stack.append((kind,k))
            else:
                for ix in range(len(stack)-1,-1,-1):
                    if stack[ix][0]==kind:
                        kd,a=stack.pop(ix); blocks.append((a,k,kd)); break
    ordered=sorted(blocks)
    for a,b,kd in ordered:
        refs=[f'{n:02d}-{j:02d}' for j,it in enumerate(issues,1) if it[1]<=b and it[2]>=a]
        first=' '.join(x.strip() for x in lines[a-1:min(b,a+3)])
        first=re.sub(r'\\(?:begin|end)\{\w+\}','',first)
        first=first.replace('|',' / ').replace('\n',' ')[:85]
        if refs: status='有问题，见 '+', '.join(refs)
        elif a in unproved: status='仅陈述未证明（本轮不补写）'
        elif kd in ('proof','solution'): status='已有证明/解答成立（允许可直接补出的省略）'
        elif kd in ('theorem','proposition','lemma','corollary'):
            later=[it for it in ordered if it[0]>b]
            inside=[it for it in ordered if it[2]=='proof' and a<it[0]<=b]
            proof=inside[0] if inside else (later[0] if later and later[0][2]=='proof' else None)
            status=('结论复核通过；已有证明见'+link(proof[0])) if proof else '结论复核通过；未见独立证明环境（正文推导/引用见按节说明）'
        else: status='定义/论述复核通过（遵循本章约定）'
        chunks.append(f'| {link(a)}—{b} | {kd} | {first} | {status} |')
    chunks.append('\n## 核验边界与源文件保护\n\n采用逻辑逐步检查与反例/边界检查；关键构造另作独立推导。有限数值检查只验证具体反例，不代替一般证明。本报告属于人工数学审读，不是形式化验证。没有运行会改写笔记的排版、编译或格式化操作。\n')
    if notes: chunks.append(notes+'\n')
    baseline=list(csv.DictReader((OUT/'源文件哈希基线.csv').read_text(encoding='utf-8-sig').splitlines()))
    changed=[]
    for row in baseline:
        p=Path(row['Path'])
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest().upper()!=row['Hash']: changed.append(row['Path'])
    relevant=[p for p in changed if not ('\\chapters\\part2\\' in p or '\\chapters\\part4\\' in p or '\\chapters\\partm\\' in p)]
    if relevant: raise RuntimeError('本次对象发生变化，须重新审读：'+repr(relevant))
    chunks.append(f'\n保护验证：与检查开始前的 SHA-256 基线逐一比对，共{len(baseline)}个文件，{len(baseline)-len(changed)}个一致。本次对象（第一部分源码、主文件、配置、图片与参考文献）没有变化。基线见同目录“源文件哈希基线.csv”。\n')
    if changed: chunks.append('另观察到本次范围外的文件更新，未由本次检查改写，未覆盖：\n\n'+'\n'.join('- '+p for p in changed)+'\n')
    dest=OUT/f'第{n:02d}章_第一轮校验报告.md'
    dest.write_text('\n'.join(chunks),encoding='utf-8')
    print(json.dumps({'report':str(dest),'issues':counts,'blocks':len(blocks),'protected_files':len(baseline)},ensure_ascii=False))
