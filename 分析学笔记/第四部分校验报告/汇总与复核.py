from pathlib import Path
import csv, hashlib, json, re, runpy
root=Path(__file__).resolve().parent.parent
out=Path(__file__).resolve().parent
for n in range(1,8):
    runpy.run_path(str(out/f'校验{n:02d}.py'))
baseline=list(csv.DictReader((out/'源文件哈希基线.csv').read_text(encoding='utf-8-sig').splitlines()))
changed=[]
for row in baseline:
    p=Path(row['Path'])
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest().upper()!=row['Hash']:
        changed.append(str(p))
verification={'checked':len(baseline),'unchanged':len(baseline)-len(changed),'changed':changed,'source_modified_by_audit':False}
(out/'源文件完整性复核.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')
titles=['Fourier级数的基本性质','Fourier级数的收敛性','Fourier级数的一些应用','R上的Fourier变换','R^d上的Fourier变换','有限Fourier分析','Dirichlet定理']
rows=['| 章 | 内容与报告 | 源码行数 | 数学环境记录 | A | B | C |','|---|---|---:|---:|---:|---:|---:|']
totals=[0]*5
for n,title in enumerate(titles,1):
    report=out/f'第{n:02d}章_第一轮校验报告.md'
    text=report.read_text(encoding='utf-8')
    counts=[len(re.findall(r'^### \d+-\d+ \['+c+r'\]',text,re.M)) for c in 'ABC']
    source=root/'chapters'/'part4'/f'chapter{n}.tex'
    line_count=len(source.read_text(encoding='utf-8-sig').splitlines())
    body=text.split('## 逐项检查记录',1)[1].split('## 核验边界',1)[0]
    blocks=len(re.findall(r'^\| \[\d+行\]',body,re.M))
    for i,val in enumerate([line_count,blocks,*counts]): totals[i]+=val
    # Validate every cited source line and referenced issue ID.
    for line in re.findall(r'chapter\d+\.tex:(\d+)',text):
        assert 1<=int(line)<=line_count
    ids=set(re.findall(r'^### (\d+-\d+)',text,re.M))
    for ref in re.findall(r'见 (\d+-\d+)',text): assert ref in ids
    assert text.count('```')%2==0
    rows.append(f'| {n} | [{title}](<{report.as_posix()}>) | {line_count} | {blocks} | {counts[0]} | {counts[1]} | {counts[2]} |')
rows.append('| 合计 | | '+' | '.join(map(str,totals))+' |')
index='''# 第四部分第一轮校验总览

本轮仅审查当前第四部分7章源码，并生成独立报告，没有修改笔记正文、主文件、配置或图片。逐章通读并核验定义、结论、证明、正文公式及相关插图；数学环境表提供具体检查记录，正文覆盖见每章按节说明。

分级：A为定义/结论/计算式错误，B为证明缺口或条件不足，C为表述/符号/引用问题。计数按问题条目，不是错误定理数量；不少A项是中间计算式错误，目标结论仍正确。数学环境数包括证明等环境，不能与定理数量等同。

'''+ '\n'.join(rows)+'''

## 优先处理的问题

- 第一章：实/复三角系数混用，固定部分和张成断言错误，Tauber证明缺绝对值与无限尾项，最后一致版本需要额外依据。
- 第二章：实三角Parseval归一化错误，高阶导数相位及Hölder积分等号错误，圆周连续逼近需补。
- 第三章：曲线及弧长参数范围过宽，等周计算误标位置/导数系数，Weyl逼近误写阶梯函数，Fejér核导数估计需展开。
- 第四章：两种适度下降条件并不等价；特征值结论须排除零函数。
- 第五章：非整数Bessel自变量及复幂范围、Radon反演的分数算子作用域需明确。
- 第六章：主要证明通过；FFT基例混用单位根与指数下标等记号问题。
- 第七章：主证明链通过；指数尾和积分和平方根求和常数的两处计算式错误。

各报告分别注明已有证明成立、正确但需补充、仅陈述未证明及引用边界。未发现问题表示本轮审读通过，不表示经过形式化证明；不是根据关键词检索或既有PDF判断覆盖。本轮没有启用主文件中注释的第四部分，也没有编译。

## 文件保护

'''+f'检查前后的SHA-256基线共{len(baseline)}个源项目文件，其中{len(baseline)-len(changed)}个一致。'+('全部一致。' if not changed else '变化路径见复核JSON，目标部分如有变化须重新审读。')+'''

[哈希基线](源文件哈希基线.csv) · [完整性复核](源文件完整性复核.json)

本轮新增文件全部位于“第四部分校验报告”目录；报告及其生成脚本为审查产物。第3章2张数学插图、第7章2张数学插图已单独查看；第1章TikZ示意的数学信息从源码核验。装饰性封面不作为数学证明依据。
'''
(out/'第四部分_第一轮校验总览.md').write_text(index,encoding='utf-8')
print(json.dumps({'totals':totals,'hashes':verification,'index':str(out/'第四部分_第一轮校验总览.md')},ensure_ascii=False))
