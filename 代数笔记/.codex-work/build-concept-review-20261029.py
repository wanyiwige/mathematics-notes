from pathlib import Path
import re, json

root = Path(r'C:\Users\WANYIWIGE\Desktop\我的笔记\代数笔记')
work = root / '.codex-work'
data_path = work / 'concept-review-20261029.tsv'
data = data_path.read_text(encoding='utf-8')
for old, new in [('1;111;', '1;105;'), ('1;112;', '1;106;'),
                 ('1;154;', '1;156;'), ('1;1331;', '1;1328;'),
                 (r'$C_x=\{gxg^{-1}:g\in G\}$', r'$C(x)=\{gxg^{-1}:g\in G\}$')]:
    data = data.replace(old, new)
data_path.write_text(data, encoding='utf-8')
rows = []
for line in data.splitlines():
    ch, number, term, cue = line.split(';', 3)
    rows.append(dict(ch=int(ch), line=int(number), term=term, cue=cue))

snapshots = {}
texts = {}
for ch in (1, 2):
    path = root / f'chapters/Part 2/chapter{ch}.tex'
    raw = path.read_bytes()
    backup = work / f'chapter{ch}-before-concept-anchors-20261029.tex'
    if backup.exists():
        raise RuntimeError(f'备份已存在，避免重复插入：{backup}')
    snapshots[path] = raw
    texts[ch] = raw.decode('utf-8').splitlines(keepends=True)

# 每个已经启用的 definition 环境都必须有复查项，不能只按加粗词收集。
coverage = []
for ch, lines in texts.items():
    start = None
    for i, line in enumerate(lines, 1):
        if line.startswith(r'\begin{definition}'):
            start = i
        if line.startswith(r'\end{definition}'):
            found = [r['term'] for r in rows if r['ch'] == ch and start <= r['line'] <= i]
            if not found:
                raise RuntimeError(f'未覆盖定义环境：第{ch}章 {start}-{i}')
            coverage.append(dict(chapter=ch, start=start, end=i, terms=found))
            start = None

for ch, lines in texts.items():
    targets = sorted({r['line'] for r in rows if r['ch'] == ch})
    for n in targets:
        line = lines[n-1]
        if not line.strip() or line.lstrip().startswith('%'):
            raise RuntimeError(f'跳转目标为空行或注释：{ch}:{n}')
        marker = f'\\phantomsection\\label{{p2:concept:c{ch}-l{n}}}'
        if line.startswith(r'\item '):
            lines[n-1] = r'\item ' + marker + line[len(r'\item '):]
        elif line.startswith(r'\begin{'):
            # 先进入环境，保留原有定理标签，再加独立的定义位置锚点。
            lines[n-1] = line.rstrip('\r\n') + marker + ('\r\n' if line.endswith('\r\n') else '\n')
        else:
            lines[n-1] = marker + line

header = r'''% !TEX root = ../../main.tex
\chapter*{前两章概念复查表}
\phantomsection
\addcontentsline{toc}{chapter}{前两章概念复查表}
\markboth{前两章概念复查表}{前两章概念复查表}

按正文顺序列出第一章、第二章已经引入的概念。复查时先尝试完整说出定义及其条件，再核对要点；点击概念名称或页码可跳转到定义位置。方框可用于打印后勾选。同一处同时定义的相关概念共用跳转位置。

\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.22}
\begin{longtable}{@{}p{0.03\linewidth}>{\raggedright\arraybackslash}p{0.255\linewidth}>{\raggedright\arraybackslash}p{0.55\linewidth}>{\raggedright\arraybackslash}p{0.10\linewidth}@{}}
\hline
 & \textbf{概念} & \textbf{复查要点} & \textbf{定义位置}\\
\hline
\endfirsthead
\multicolumn{4}{r}{\small 前两章概念复查表（续）}\\
\hline
 & \textbf{概念} & \textbf{复查要点} & \textbf{定义位置}\\
\hline
\endhead
\hline
\multicolumn{4}{r}{\small 续下页}\\
\endfoot
\hline
\endlastfoot
'''
out = [header]
last_group = None
chapter_names = {1: '第一章：代数基本概念', 2: '第二章：群'}
for row in rows:
    ch, n = row['ch'], row['line']
    sections = []
    for i, line in enumerate(snapshots[root / f'chapters/Part 2/chapter{ch}.tex'].decode('utf-8').splitlines(), 1):
        match = re.match(r'\\section\{([^}]+)\}', line)
        if match and i <= n:
            sections.append(match.group(1))
    group = (ch, len(sections), sections[-1])
    if group != last_group:
        if last_group is None or last_group[0] != ch:
            out.append(r'\multicolumn{4}{@{}l@{}}{\rule{0pt}{2.4em}\large\textbf{' + chapter_names[ch] + r'}}\\*' + '\n')
        out.append(r'\multicolumn{4}{@{}l@{}}{\rule{0pt}{1.8em}\textbf{' + f'§{ch}.{len(sections)}\quad ' + sections[-1] + r'}}\\*' + '\n')
        last_group = group
    label = f'p2:concept:c{ch}-l{n}'
    out.append(r'$\square$ & \hyperref[' + label + ']{' + row['term'] + '} & ' + row['cue'] +
               r' & \hyperref[' + label + r']{第\pageref*{' + label + r'}页}\\' + '\n')
out.append('\\end{longtable}\n\\endgroup\n')

main_path = root / 'main.tex'
packages_path = root / 'preamble/packages.tex'
main = main_path.read_bytes()
packages = packages_path.read_bytes()
snapshots[main_path] = main
snapshots[packages_path] = packages
main_s = main.decode('utf-8')
needle = r'\tableofcontents'
if main_s.count(needle) != 1:
    raise RuntimeError('目录标记不唯一')
main_s = main_s.replace(needle, needle + '\n\t\\clearpage\n\t\\input{chapters/Part 2/concept-review}')
packages_s = packages.decode('utf-8')
if r'\usepackage{longtable,array}' not in packages_s:
    packages_s = packages_s.replace(r'\usepackage{float}', '\\usepackage{float}\n\\usepackage{longtable,array}')

updates = {root / f'chapters/Part 2/chapter{ch}.tex': ''.join(texts[ch]) for ch in (1, 2)}
updates[main_path] = main_s
updates[packages_path] = packages_s
for path, old in snapshots.items():
    if path.read_bytes() != old:
        raise RuntimeError(f'检测到并发修改：{path}')
for ch in (1, 2):
    path = root / f'chapters/Part 2/chapter{ch}.tex'
    (work / f'chapter{ch}-before-concept-anchors-20261029.tex').write_bytes(snapshots[path])
(work / 'main-before-concept-review-20261029.tex').write_bytes(main)
(work / 'packages-before-concept-review-20261029.tex').write_bytes(packages)
for path, text in updates.items():
    path.write_bytes(text.encode('utf-8'))
(root / 'chapters/Part 2/concept-review.tex').write_text(''.join(out), encoding='utf-8')
(work / 'concept-review-coverage-20261029.json').write_text(json.dumps(dict(rows=len(rows), definitions=coverage), ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(dict(review_rows=len(rows), covered_definition_environments=len(coverage), unique_jump_targets=len({(r['ch'],r['line']) for r in rows})), ensure_ascii=False))
