from pathlib import Path
import pymupdf as fitz,json
from PIL import Image,ImageOps,ImageDraw
R=Path(__file__).resolve().parents[1];d=fitz.open(R/'常微分方程期末复习.pdf');out=R/'qa'/'render';out.mkdir(exist_ok=True)
info=[]
for i,p in enumerate(d):
 pix=p.get_pixmap(matrix=fitz.Matrix(.75,.75));pix.save(out/f'p{i+1:03d}.png')
 # Any text beyond usable page width is an independently measured clipping candidate.
 bad=[]
 for b in p.get_text('dict')['blocks']:
  for line in b.get('lines',[]):
   for s in line['spans']:
    x0,y0,x1,y1=s['bbox']
    if x0<35 or x1>p.rect.width-35:bad.append({'text':s['text'],'bbox':s['bbox']})
 info.append({'page':i+1,'chars':len(p.get_text()),'edge_candidates':bad})
for start in range(0,len(d),12):
 sheet=Image.new('RGB',(1600,1740),'#dddddd');draw=ImageDraw.Draw(sheet)
 for j in range(12):
  n=start+j+1
  if n>len(d):break
  im=Image.open(out/f'p{n:03d}.png');im=ImageOps.contain(im,(388,545))
  xx=(j%4)*400+6;yy=(j//4)*580+22;sheet.paste(im,(xx,yy));draw.text((xx,yy-18),f'PAGE {n}',fill='black')
 sheet.save(out/f'sheet_{start+1:03d}.png')
(R/'qa'/'visual-check.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
print('PAGES',len(d),'edge candidates',[(r['page'],len(r['edge_candidates'])) for r in info if r['edge_candidates']])
print('shortpages',[(r['page'],r['chars']) for r in info if r['chars']<100])
