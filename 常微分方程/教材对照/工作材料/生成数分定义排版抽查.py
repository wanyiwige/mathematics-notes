from pathlib import Path
import json,re,fitz
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[2]
p=r/'教材对照/整合记录与清单索引.md';s=p.read_text(encoding='utf-8')
block='## 数分前置定义补全\n\n2026-10-30，对照分析学152个源码文件，补写39个定义和8段证明，并检查定义先于使用。新增内容仍直接写入各章正文。数分笔记源码未修改。详见[数分前置知识对照与定义补全](数分前置知识对照与定义补全.md)。\n\n'
if '## 数分前置定义补全' not in s:s=s.replace('## 校验',block+'## 校验',1)
p.write_text(s,encoding='utf-8')
pdf=fitz.open(r/'main.pdf');aux='\n'.join(p.read_text(encoding='utf-8') for p in (r/'chapters').glob('*.aux'))
f=json.loads((r/'教材对照/最终校验记录.json').read_text(encoding='utf-8'));offset=f['cover_pages'][0]-1
keys=['def:support-test','lem:symmetric-spectral-elementary','def:banach-operator','def:vector-bundle','def:forms-coordinate','prop:forms-stokes-calculus','def:variation-functional','def:frechet-derivative','lem:nonnegative-elliptic-positive']
pages=[]
for key in keys:
    m=re.search(r'\\newlabel\{'+re.escape(key)+r'\}\{\{[^}]+\}\{([^}]+)\}',aux)
    assert m,key
    pages.append(int(m[1])+offset)
sheet=Image.new('RGB',(1650,2370),'#ddd')
for j,num in enumerate(pages):
    pix=pdf[num-1].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((530,750))
    sheet.paste(im,(j%3*550+(550-im.width)//2,j//3*790+10))
    ImageDraw.Draw(sheet).text((j%3*550+12,j//3*790+766),f'PDF page {num}',fill='black')
sheet.save(r/'教材对照/数分前置定义排版抽查.jpg',quality=93)
f['analysis_prerequisites_revision']['sample_pages']=pages
(r/'教材对照/最终校验记录.json').write_text(json.dumps(f,ensure_ascii=False,indent=2),encoding='utf-8')
print({'pages':len(pdf),'new_definitions':39,'sample_pages':pages,'overfull':f['overfull_hboxes']})
