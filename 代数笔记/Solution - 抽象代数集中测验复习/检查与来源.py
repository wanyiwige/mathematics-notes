"""核对作业题号覆盖，并保存第零章扫描题面的可追溯记录。"""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parent
expected = {
    0: [4,5,6,7,8,13,14,23,24],
    1: [1,2,4,6,7,8,9,10,12,18,21,22,29,30,32,34,39,43,44],
    2: [7,8,10,11,12,15,29,30,31,32,36,38,39,40,41,42,43,44,45,46,47,49],
    3: [1,2,3,8],
}
lines = ['# 范围与结构检查', '', '此检查核对题号覆盖和解答结构，不代替数学审查。', '']
for chapter, numbers in expected.items():
    source = (root / f'chapter{chapter}.tex').read_text(encoding='utf-8')
    found = [int(x) for x in re.findall(r'\\subsection\{习题(\d+)', source)]
    assert found == numbers, (chapter, found, numbers)
    proofs = source.count(r'\begin{proof}')
    assert proofs == len(numbers), (chapter, proofs)
    assert source.count(r'\textbf{原文依据：}') == len(numbers), (chapter, '原文依据数量')
    assert source.count(r'\end{proof}') == proofs
    for heading in ['题目', '考点与思路', '所用结论', '复习提示']:
        assert source.count('\\paragraph{' + heading + '}') == len(numbers), (chapter, heading)
    env = []
    for kind, name in re.findall(r'\\(begin|end)\{([^}]+)\}', source):
        if kind == 'begin':
            env.append(name)
        else:
            assert env and env.pop() == name, (chapter, name)
    assert not env, (chapter, env)
    assert not re.search(r'待补|待确认|TODO|FIXME', source), chapter
    lines.append(f'- 第{chapter}章：{len(numbers)}题，题号、题目/思路/证明/提示和环境配对检查通过。')

tool_sources = '\n'.join(p.read_text(encoding='utf-8') for p in sorted(root.glob('tools-*.tex')))
tool_keys = re.findall(r'\\label\{tool:([^}]+)\}', tool_sources)
assert len(tool_keys) == len(set(tool_keys)), '重复工具标签'
refs = []
for p in [*root.glob('chapter[0-3].tex'), *root.glob('tools-*.tex')]:
    refs.extend(re.findall(r'\\toolref\{([^}]+)\}', p.read_text(encoding='utf-8')))
assert set(refs) <= set(tool_keys), ('缺失工具', set(refs)-set(tool_keys))
lines += ['', f'工具目录共{len(tool_keys)}条，编号标签唯一，全部{len(refs)}处工具引用均有定义。',
          '共54题，每题均标明原文依据与所用结论。题面已对照教材习题页；第二章12已据教材订正。',
          '数学独立审查结果、编译结果及残余警告见 README.md。']
(root/'范围检查.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')

source0 = (root/'chapter0.tex').read_text(encoding='utf-8')
pages = {30: [], 31: [], 32: []}
md = ['# 第零章指定习题题面', '',
      '来源：聂灵沼、丁石孙《代数学引论》第三版，书页20—22，扫描PDF第30—32页。',
      '扫描页无文本层；由页面图像读取。仅提取本次作业指定习题，证明另见 chapter0.tex。', '']
for match in re.finditer(r'\\subsection\{习题(\d+)：([^\n]+?)\}(?:\\label\{[^}]+\})?\s*\\paragraph\{题目\}([\s\S]*?)(?=\\paragraph\{考点与思路\})', source0):
    number, title, question = int(match[1]), match[2], match[3].strip()
    # 习题4的起始题干在PDF30，四项条件在PDF31；其余按实际题面所在页记录。
    page = 31 if number <= 14 else 32
    pages[page].append({'type':'paragraph', 'exercise':number, 'title':title,
                        'text_latex':question, 'note':'vision',
                        'additional_page':30 if number == 4 else None})
    md += [f'## 习题{number}：{title}', f'扫描PDF第{page}页' + ('（题干起于第30页）' if number==4 else ''), '', question, '']
assert sum(len(v) for v in pages.values()) == 9, '第零章题面提取漏题'
record = {'source':r'D:\四川大学学习资料\四川大学大二教材\代数学引论, 第三版 -- 聂灵沼, 丁石孙 .pdf',
          'scope':'第零章指定9题；不包含这些页面上的其他题目与正文',
          'pages':[{'page':p,'book_page':p-10,'route':'scanned','needs_vision':False,
                    'render':f'source-p{p}.png','elements':v} for p,v in pages.items()]}
(root/'第零章题面来源.md').write_text('\n'.join(md), encoding='utf-8')
(root/'第零章题面来源.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print('\n'.join(lines))
