from pathlib import Path
import json,hashlib,fitz
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[2]
p=r/'教材对照/整合记录与清单索引.md';s=p.read_text(encoding='utf-8')
if '## 新增正文用语修订' not in s:
    s=s.replace('## 校验','## 新增正文用语修订\n\n2026-10-30，以原有章节的措辞为准调整新增正文121处文字；4.4节改为“矩阵指数与线性递推”，其他章节统一使用解映射、迭代等已经介绍的名称。公式、标签和证明结构保留。详见[语言与用词修订记录](新增内容语言与用词修订记录.md)。\n\n## 校验',1)
    p.write_text(s,encoding='utf-8')
pdf=fitz.open(r/'main.pdf')
keys=['矩阵指数与线性递推','周期解稳定时','解映射的复合关系','Lyapunov二次型与拓扑分类','未确定归一化常数','将零序列代入算子']
pages=[]
for key in keys:
    found=next((i+1 for i,pg in enumerate(pdf) if i>8 and key in ''.join(pg.get_text().split())),None)
    assert found,key
    pages.append(found)
sheet=Image.new('RGB',(1650,1580),'#ddd')
for j,num in enumerate(pages):
    pix=pdf[num-1].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((530,750))
    sheet.paste(im,(j%3*550+(550-im.width)//2,j//3*790+10))
    ImageDraw.Draw(sheet).text((j%3*550+12,j//3*790+766),f'PDF page {num}',fill='black')
sheet.save(r/'教材对照/新增正文用语排版抽查.jpg',quality=94)
pdf[pages[0]-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(r/'教材对照/工作材料/4.4用语修订排版.png')
p=r/'教材对照/最终校验记录.json';d=json.loads(p.read_text(encoding='utf-8'))
d['wording_revision']['sample_pages']=pages
assert hashlib.sha256((r/'main.pdf').read_bytes()).hexdigest()==d['pdf_sha256']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print({'pages':len(pdf),'sample_pages':pages,'revised_passages':121,'overfull':d['overfull_hboxes']})
