from pathlib import Path
import json,re,zipfile,hashlib
root=Path(__file__).resolve().parents[2]
record=root/'教材对照/最终校验记录.json'
data=json.loads(record.read_text(encoding='utf-8'))
backup=root.parent/'常微分方程备份/排版调整前-20261029-084816.zip'
z=zipfile.ZipFile(backup)
assert z.testzip() is None
counts={'before':0,'after':0}; changed=[]
for p in (root/'chapters').glob('*.tex'):
    names=[name for name in z.namelist() if name.split('/')[-1]==p.name]
    assert len(names)==1,(p.name,names)
    old=z.read(names[0]).decode('utf-8-sig');new=p.read_text(encoding='utf-8')
    if old.replace('\r\n','\n')!=new.replace('\r\n','\n'):changed.append(p.name)
    for key,text in [('before',old),('after',new)]:
        counts[key]+=len(re.findall(r'\\\[|\\begin\{(?:align\*?|equation\*?|gather\*?|multline\*?)\}',text))
    for env in ('proof','theorem','proposition','definition','aligned','align*'):
        assert new.count('\\begin{'+env+'}')==new.count('\\end{'+env+'}'),(p.name,env)
data.update({'layout_revision':{'backup':str(backup),'changed_chapter_sources':changed,'display_blocks':counts,'overfull_hboxes':data['overfull_hboxes'],'preview':'行间公式与分行排版抽查.jpg'}})
data['visual_check']='All 15 chapter covers within page; sampled displayed formulas, aligned derivations and proof pagination.'
record.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
pages=data['pdf_pages'];over=data['overfull_hboxes'];inline=data['inline_integrals_with_displaystyle']
text=f'''# 行间公式与分行排版修订

日期：2026-10-29。

本轮将较长的关键等式、估计和定义式移入行间环境，连续计算使用 `aligned` 或 `align*` 按推理步骤对齐；成组条件、矩阵和结论适当分行。简短符号和条件保留行内排版。

主要调整新增章节及扩写后的证明；原第3章和第5章仅对拥挤公式与长行作局部排版调整。数学结论和证明思路沿用现稿。

正文行间公式块由{counts['before']}处增至{counts['after']}处。剩余{inline}处行内积分号均保留 `\\displaystyle`。

最终PDF共{pages}页，XeLaTeX重复编译后目录和交叉引用稳定；Overfull警告{over}处，无未定义引用、重复标签或缺字警告。已抽查行间公式、分步推导、证明分页及章节封面。

[更新后的笔记](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/main.pdf>) · [排版抽查](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/教材对照/行间公式与分行排版抽查.jpg>)

排版前备份：[排版调整前-20261029-084816.zip](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程备份/排版调整前-20261029-084816.zip>)。
'''
(root/'教材对照/行间公式与分行排版修订.md').write_text(text,encoding='utf-8')
index=root/'教材对照/整合记录与清单索引.md'
s=index.read_text(encoding='utf-8');s=s.split('## 校验')[0]+f'''## 校验

最终PDF共{pages}页，目录和交叉引用稳定，无未定义引用、重复标签或缺字警告。根据后续要求，正文中的教材出处说明已清理，39段证明已扩写；本轮进一步增加行间公式并对齐连续推导，现有行宽溢出警告{over}处。原有字体替代提示保留。

详细数据见[最终校验记录](最终校验记录.json)。此前修订见[证明扩写与排版修订记录](证明扩写与排版修订记录.md)，本轮见[行间公式与分行排版修订](行间公式与分行排版修订.md)。
'''
index.write_text(s,encoding='utf-8')
assert hashlib.sha256((root/'main.pdf').read_bytes()).hexdigest()==data['pdf_sha256']
print(json.dumps({'pages':pages,'display_blocks':counts,'changed_files':changed,'overfull':over,'inline_integrals':inline},ensure_ascii=False,indent=2))
