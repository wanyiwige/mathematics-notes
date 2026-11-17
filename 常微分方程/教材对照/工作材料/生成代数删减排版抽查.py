from pathlib import Path
import re,json,hashlib,fitz
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[2]
p=r/'教材对照/整合记录与清单索引.md';s=p.read_text(encoding='utf-8')
if '## 与代数笔记重复内容删减' not in s:
    s=s.replace('## 校验','## 与代数笔记重复内容删减\n\n2026-10-30，以代数笔记为已有基础，删去对偶空间、Hamilton--Cayley定理、正交对角化、正定平方根、群及群作用等重复的定义和证明；保留微分方程及几何应用。详见[删减清单](与代数笔记重复内容删减清单.md)。此前补全数字为对应修订时的历史状态。\n\n## 校验',1)
    p.write_text(s,encoding='utf-8')
pdf=fitz.open(r/'main.pdf');d=json.loads((r/'教材对照/最终校验记录.json').read_text(encoding='utf-8'))
aux='\n'.join(p.read_text(encoding='utf-8') for p in (r/'chapters').glob('*.aux'))
offset=d['cover_pages'][0]-1;pages=[]
for key in ['sec:quasipolynomials','sec:linear-evolution','sec:normal-modes','def:quotient-circle']:
    m=re.search(r'\\newlabel\{'+re.escape(key)+r'\}\{\{[^}]+\}\{([^}]+)\}',aux);assert m,key;pages.append(int(m[1])+offset)
for key in ['向量场的对称','四元数的标准基']:
    found=next((i+1 for i,pg in enumerate(pdf) if i>8 and key in ''.join(pg.get_text().split())),None);assert found,key;pages.append(found)
sheet=Image.new('RGB',(1650,1580),'#ddd')
for j,num in enumerate(pages):
    pix=pdf[num-1].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((530,750))
    sheet.paste(im,(j%3*550+(550-im.width)//2,j//3*790+10))
    ImageDraw.Draw(sheet).text((j%3*550+12,j//3*790+766),f'PDF page {num}',fill='black')
sheet.save(r/'教材对照/代数重复内容删减排版抽查.jpg',quality=94)
d['algebra_dedup_revision']['sample_pages']=pages
assert hashlib.sha256((r/'main.pdf').read_bytes()).hexdigest()==d['pdf_sha256']
p=r/'教材对照/最终校验记录.json';p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for label in d['algebra_dedup_revision']['removed_labels']:
    assert r'\newlabel{'+label+'}' not in aux,label
print({'pages':len(pdf),'sample_pages':pages,'removed_labels_absent':True,'overfull':d['overfull_hboxes']})
