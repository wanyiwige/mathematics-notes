from pathlib import Path
import csv, hashlib, re, json

out=Path(__file__).resolve().parent
root=out.parent
titles=['实数理论——从Peano公理到实数的连续性','一元实函数与基本初等函数','实数的八大基本定理','数列极限的应用与一些反例','级数理论','函数的极限与连续性','微分法','Riemann积分与反常积分','一些不定积分的问题','一些定积分的问题','一些反常积分的问题','函数项序列与函数项级数']
focus=['商集良定义、序、Dedekind及集合的势','定义域、反函数分支及不等式证明','拓扑基与实数完备性的互证','序列估计、Fibonacci与进位表示','比较判别、重排及无穷乘积','极限定义、黎曼函数与一致连续','导数条件、凹凸、洛必达及Taylor','积分表、可积性、中值及反常运算','原函数分支与积分函数的区别','不等式、数值/几何公式及Stieltjes','振荡判敛与多个奇点','一致收敛、幂级数表与逼近']
rows=[]; errors=[]
for n in range(1,13):
    src=root/'chapters'/'part1'/f'chapter{n}.tex'
    report=out/f'第{n:02d}章_第一轮校验报告.md'
    s=report.read_text(encoding='utf-8')
    lines=src.read_text(encoding='utf-8-sig').splitlines()
    issues=re.findall(r'^### (\d{2}-\d{2}) \[([ABC])\]',s,re.M)
    assert len({i for i,l in issues})==len(issues),report
    counts=[sum(l==kind for i,l in issues) for kind in 'ABC']
    declared=re.search(r'A (\d+)项，B (\d+)项，C (\d+)项',s)
    assert counts==list(map(int,declared.groups())),report
    for a,b in re.findall(r'位置：\[(\d+)行\].*?—(\d+)。',s):
        if not(1<=int(a)<=int(b)<=len(lines)): errors.append([n,a,b,len(lines)])
    for path,a in re.findall(r'\]\(<([^>]+):(\d+)>\)',s):
        p=Path(path)
        if not p.exists() or int(a)>len(p.read_text(encoding='utf-8-sig').splitlines()): errors.append([n,path,a])
    ledger=s.split('## 逐项检查记录',1)[1].split('## 核验边界',1)[0]
    blocks=sum(line.startswith('| [') for line in ledger.splitlines())
    rows.append({'chapter':n,'lines':len(lines),'issues':counts,'blocks':blocks,'report':report.as_posix()})
assert not errors,errors
baseline=list(csv.DictReader((out/'源文件哈希基线.csv').read_text(encoding='utf-8-sig').splitlines()))
changed=[]
for row in baseline:
    p=Path(row['Path'])
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest().upper()!=row['Hash']: changed.append(row['Path'])
protected=[p for p in changed if not any(('\\chapters\\'+part+'\\') in p for part in ['part2','part4','partm'])]
assert not protected,protected
totals=[sum(r['issues'][k] for r in rows) for k in range(3)]
total_blocks=sum(r['blocks'] for r in rows)
total_lines=sum(r['lines'] for r in rows)
parts=['# 数学分析笔记第一部分：第一轮校验总览',
       '日期：2026-10-14。第一部分12章均已按源码正文顺序审读并分别交付报告。第一轮只写报告，没有修改笔记。',
       f'共审读{total_lines}行源码，逐项登记{total_blocks}个数学环境；环境外数学论述、公式表、计算代码及正文数学图另在按节覆盖和问题条目中记录。共{sum(totals)}个问题条目：A {totals[0]}项，B {totals[1]}项，C {totals[2]}项。条目会合并同一问题的多处表现，不能把此数解释为错误定理的数量。',
       'A：定义、结论或公式错误；B：证明缺口或条件不足；C：表述、符号、引用问题。没有发现问题的记录是数学审读结果，不是形式化认证。',
       '## 逐章报告',
       '| 章 | 内容及报告 | 源码行数 | 数学环境 | A | B | C | 主要核验主题 |\n|---|---|---:|---:|---:|---:|---:|---|']
for r,title,theme in zip(rows,titles,focus):
    a,b,c=r['issues']
    parts[-1] += f'\n| {r["chapter"]} | [{title}](<{r["report"]}>) | {r["lines"]} | {r["blocks"]} | {a} | {b} | {c} | {theme} |'
parts += ['## 最需要优先处理的内容',
          '基础构造方面，第一章的有理数序在负分母下不良定义、分割缺非空条件，整数/有理数商集运算的良定义证明需要补齐。第三章有拓扑基公式和若干完备性互证问题。它们应先于依赖这些基础的后续证明修订。',
          '分析方面，应优先修复第六章极限定义的正半径，第七章可导条件、Jensen权重和Taylor余项，第八章错误积分表、Cauchy否定量词及非法反常积分拆分，第十章Minkowski公式、Cauchy–Schwarz等号条件和跳跃积分因子的可加性，第十二章错误级数表。各报告均给出行号、理由与反例或补证思路。',
          '## 最初关心的黎曼函数证明',
          f'第六章[{576}行](<{(root/"chapters/part1/chapter6.tex").as_posix()}:576>)定义黎曼函数，第595—611行讨论连续性与处处去心极限0。已有有限坏点集的证明思路，但未完整处理无理点、有理基点属于坏点集、端点和严格误差；有理点还被错分为第二类间断。正确结论：所有点的去心极限都是0，无理点连续，有理点可去间断（按本笔记叫第三类）。统一补证见[第六章报告](<{rows[5]["report"]}>)。',
          '第五章与第七章没有另写这两个结论的完整证明；第八章涉及黎曼函数的可积性，另见第八章报告。',
          '## 覆盖边界及待核实项',
          '第九章第9.2、9.3节和第十一章第11.2、11.3节仅有标题。未写出的内容记为未写，未擅自补入笔记。已经陈述而未证明的命题与已有证明成立、结论正确但证明不足分别登记。章首提醒存在问题的“集合的势”一节已在第一章报告中审读。',
          '第九章的三张历史图片已阅读；关于柯西原书的具体版次与页码归属，以及“教材普遍丢失原意”的历史判断仍待核实。数学结论没有依赖未核实的历史说法。',
          '当前main.tex的第一部分12个include仍全部注释，审查不依赖现有PDF。正文外部数学图片已检查；TikZ图按源码的公式、坐标和关系核对。没有运行编译或声称版面已验收。',
          '## 源文件保护与交付复核',
          f'与检查开始前的SHA-256基线比较，共{len(baseline)}个原有文件，{len(baseline)-len(changed)}个一致。第一部分12章源码、主文件、配置、图片和参考文献均与基线一致。本次写入仅发生在“第一部分校验报告”文件夹。',
          '另检测到本次范围外的文件更新，未由本次检查操作改写，也没有覆盖这些更新：\n\n'+'\n'.join('- '+p for p in changed) if changed else '未检测到任何原有文件变化。',
          '12份报告的编号、统计、源码定位范围与链接目标已作结构复核；建议和反例在交付前重新检查，发现误判的内容已更正或保留原有记号约定。数学审读不能保证消除全部隐蔽错误。',
          f'基线文件：[源文件哈希基线.csv](<{(out/"源文件哈希基线.csv").as_posix()}>)。生成脚本和最后复核数据一并保存在本目录，方便追溯；它们不修改笔记源文件。']
(out/'第一轮校验总览.md').write_text('\n\n'.join(parts),encoding='utf-8')
result={'chapters':rows,'total_source_lines':total_lines,'total_math_blocks':total_blocks,'issue_totals':dict(zip('ABC',totals)),'baseline_files':len(baseline),'unchanged_files':len(baseline)-len(changed),'changed_out_of_scope':changed,'source_locations_valid':True,'protected_objects_unchanged':True}
(out/'最终复核记录.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
