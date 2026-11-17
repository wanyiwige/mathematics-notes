from pathlib import Path
import json,re,shutil,zipfile,hashlib
import fitz
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
data=json.loads((root/'教材对照/最终校验记录.json').read_text(encoding='utf-8'))
figs=json.loads((root/'教材对照/工作材料/TikZ配图记录.json').read_text(encoding='utf-8'))['figures']
backup=root.parent/'常微分方程备份/TikZ配图前-20261029-141104.zip'
if not backup.exists():backup=Path(data['revision_backup'])
assert zipfile.ZipFile(backup).testzip() is None
pdf=fitz.open(root/'main.pdf')
items=[]
aux='\n'.join(p.read_text(encoding='utf-8') for p in (root/'chapters').glob('*.aux'))
offset=data['cover_pages'][0]-1
for f in figs:
    m=re.search(r'\\newlabel\{fig:ode-tikz-'+re.escape(f['name'])+r'\}\{\{([^}]+)\}\{([^}]+)\}',aux)
    assert m,f['name']
    number,page=m.groups();physical=int(page)+offset
    assert any(('图'+number).replace(' ','') in ''.join(pdf[i].get_text().split()) for i in [physical-1]),(f['name'],number,physical)
    item={**f,'figure_number':number,'printed_page':int(page),'pdf_page':physical}
    items.append(item)
    assert 'body' not in item
sample=[items[i]['pdf_page'] for i in (0,2,5,8,14,16)]
sheet=Image.new('RGB',(1650,2370),'#ddd')
for j,pageno in enumerate(sample):
    page=pdf[pageno-1];pix=page.get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False)
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((530,750))
    x=j%3*550;y=j//3*790;sheet.paste(im,(x+(550-im.width)//2,y+12))
    ImageDraw.Draw(sheet).text((x+12,y+766),f'PDF page {pageno}',fill='black')
sheet=sheet.crop((0,0,1650,1580))
sheet.save(root/'教材对照/TikZ正文排版抽查.jpg',quality=94)
pdf.close()
data.update({'tikz_revision':{'added_figures':17,'source_directory':'figure/tikz','backup':str(backup),'figures':items},'visual_check':'17 TikZ diagrams reviewed; 15 chapter covers within page; sampled in-context diagram pages.'})
(root/'教材对照/最终校验记录.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
if (root/'build/tikz-review/review.pdf').exists():
    shutil.copy2(root/'build/tikz-review/review.pdf',root/'教材对照/TikZ数学配图预览.pdf')
rows=[]
for f in items:
    rows.append(f"| {f['figure_number']} | {f['caption']} | PDF第{f['pdf_page']}页 | [{f['name']}.tex](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/figure/tikz/{f['name']}.tex>) |")
text=f'''# TikZ数学配图修订记录

2026-10-29新增17幅数学配图，全部以TikZ源码绘制，插入相应论述附近。每图使用 `center` 排版，图题采用 `captionof`，标签紧随图题；正文均有交叉引用。

覆盖集中脉冲与Green响应、能量层、Lotka--Volterra闭轨、返回映射、向量场直化、实吹起、Sturm零点、单周期乘子、环面运动、特征线交叉、jet投影尖点、立体投影、奇点指标、相对椭圆轨道、光学测地线、稳定流形及Gibbs密度。

原章节封面图片继续保留。新增数学图均为矢量路径，未以位图代替TikZ。

配图已单独编译检查，并核对曲线、向量方向、关键恒等式和归一化条件。最终整本PDF共{data['pdf_pages']}页；行宽溢出警告{data['overfull_hboxes']}处，无未定义引用、重复标签或缺字警告。

| 图号 | 内容 | 位置 | 源码 |
| --- | --- | --- | --- |
'''+ '\n'.join(rows)+f'''

[更新后的笔记](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/main.pdf>) · [17幅图独立预览](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/教材对照/TikZ数学配图预览.pdf>) · [正文排版抽查](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/教材对照/TikZ正文排版抽查.jpg>)

本轮备份：[{backup.name}](<{backup.as_posix()}>)。
'''
(root/'教材对照/TikZ数学配图修订记录.md').write_text(text,encoding='utf-8')
index=root/'教材对照/整合记录与清单索引.md';s=index.read_text(encoding='utf-8')
s=s.split('## 校验')[0]+f'''## 校验

最终PDF共{data['pdf_pages']}页，目录和交叉引用稳定，无未定义引用、重复标签或缺字警告。正文中的教材出处说明已清理；新增内容已按具体定义和证明的依赖重新安置，保留适当的章末专题，详见[知识衔接审阅与调整记录](知识衔接审阅与调整记录.md)。已增加行间公式和对齐推导，并新增17幅TikZ数学配图。行宽溢出警告{data['overfull_hboxes']}处；原有字体替代提示保留。

修订记录：[证明扩写](证明扩写与排版修订记录.md) · [公式分行](行间公式与分行排版修订.md) · [TikZ配图](TikZ数学配图修订记录.md)。详细数据见[最终校验记录](最终校验记录.json)。
'''
index.write_text(s,encoding='utf-8')
assert hashlib.sha256((root/'main.pdf').read_bytes()).hexdigest()==data['pdf_sha256']
print(json.dumps({'pages':data['pdf_pages'],'figures':17,'sample_pages':sample,'overfull':data['overfull_hboxes']},ensure_ascii=False))
