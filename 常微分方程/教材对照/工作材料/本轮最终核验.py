from pathlib import Path
import re,json,hashlib,shutil
import fitz
from PIL import Image,ImageOps,ImageDraw
root=Path(__file__).resolve().parents[2]
build=root/'build/arnold-integration'
log=(build/'main.log').read_text(encoding='utf-8',errors='replace')
assert 'Output written on' in log
for pattern in (r'Reference .* undefined',r'Citation .* undefined',r'Missing character:',r'There were undefined references',r'multiply defined',r'Label\(s\) may have changed'):
    assert not re.search(pattern,log),pattern
ns={}
script=(root/'教材对照/工作材料/行内积分排版.py').read_text(encoding='utf-8')
exec(script.split('report=[]')[0].replace("root=Path(__file__).resolve().parents[2]",'root=None'),ns)
total=0
for p in [root/'main.tex']+list((root/'chapters').glob('*.tex'))+list((root/'preamble').glob('*.tex')):
    text=p.read_text(encoding='utf-8')
    for a,b in ns['inline_ranges'](text):
        block=text[a:b]
        for m in ns['integral'].finditer(block):
            total+=1
            assert re.search(r'\\displaystyle\s*$',block[:m.start()]),(p.name,block)
pdf=fitz.open(build/'main.pdf')
covers=[]
for i,page in enumerate(pdf):
    info=page.get_image_info()
    if i>0 and 0<len(page.get_text())<450 and info:
        largest=max(info,key=lambda x:(x['bbox'][2]-x['bbox'][0])*(x['bbox'][3]-x['bbox'][1]))
        bb=largest['bbox']
        if bb[2]-bb[0]>400 and bb[3]-bb[1]>250:
            covers.append({'page':i+1,'bbox':list(bb)})
assert len(covers)==15, covers
assert all(-1<=c['bbox'][1]<2 for c in covers),covers
keys=['初值导数的矩阵变分方程','有限维紧集延拓判据','法二：利用增量方程','一维周期点的导数判据','隐函数定理说明','局部逆与沿解移动的坐标']
samples=[]
for key in keys:
    for i,page in enumerate(pdf):
        if i<covers[0]['page']:continue
        text=''.join(page.get_text().split())
        if ''.join(key.split()) in text:
            samples.append(i);break
aux='\n'.join(p.read_text(encoding='utf-8') for p in (build/'chapters').glob('*.aux'))
samples=[]
for label in ['prop:compact-extension-vector','prop:matrix-variation','prop:normal-mode-stability','prop:discrete-derivative-test','thm:local-inverse','thm:动能加势能型Hamilton系统平衡点分类']:
    m=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]+\}\{([^}]+)\}',aux)
    assert m,label
    samples.append(int(m[1])+covers[0]['page']-2)
samples.insert(1,samples[1]-1)
samples=list(dict.fromkeys(samples))
thumbs=[]
for i in samples:
    pix=pdf[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
    img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
    img.thumbnail((530,750))
    tile=Image.new('RGB',(550,790),'#ddd')
    tile.paste(img,((550-img.width)//2,25))
    ImageDraw.Draw(tile).text((12,768),f'PDF page {i+1}',fill='black')
    thumbs.append(tile)
sheet=Image.new('RGB',(550*3,790*((len(thumbs)+2)//3)),'white')
for j,img in enumerate(thumbs):sheet.paste(img,((j%3)*550,(j//3)*790))
sheet.save(root/'教材对照/行间公式与分行排版抽查.jpg',quality=92)
old=json.loads((root/'教材对照/最终校验记录.json').read_text(encoding='utf-8'))
old.update({'pdf_pages':len(pdf),'pdf_sha256':hashlib.sha256((build/'main.pdf').read_bytes()).hexdigest(),'overfull_hboxes':log.count('Overfull \\hbox'),'expanded_proofs_this_revision':39,'inline_integrals_with_displaystyle':total,'source_editorial_notes_removed':True,'revision_backup':'../常微分方程备份/证明扩写前-20261029-083340.zip','cover_pages':[c['page'] for c in covers],'proof_sample_pages':[i+1 for i in samples]})
dependency=json.loads((root/'教材对照/工作材料/知识依赖核验.json').read_text(encoding='utf-8'))
old.update({'new_environments':dependency['new_environments'],'revision_backup':'../常微分方程备份/知识衔接调整前-20261029-185708.zip','coherence_revision':dependency})
old.pop('expanded_proofs_this_revision',None)
inline_record=root/'教材对照/工作材料/模块直接并入记录.json'
if inline_record.exists():
    inline=json.loads(inline_record.read_text(encoding='utf-8'))
    old.update({'date':'2026-10-30','revision_backup':inline['backup'],'inline_revision':inline})
prerequisite_record=root/'教材对照/工作材料/数分前置定义补全记录.json'
if prerequisite_record.exists():
    prerequisite=json.loads(prerequisite_record.read_text(encoding='utf-8'))
    old.update({'date':'2026-10-30','revision_backup':prerequisite['backup'],'analysis_prerequisites_revision':prerequisite,'new_environments':prerequisite['total_new_environments_vs_original_notes']})
wording_record=root/'教材对照/工作材料/新增正文用语调整记录.json'
if wording_record.exists():
    wording=json.loads(wording_record.read_text(encoding='utf-8'))
    old.update({'revision_backup':wording['backup'],'wording_revision':wording})
algebra_record=root/'教材对照/工作材料/代数重复内容删减记录.json'
if algebra_record.exists():
    algebra=json.loads(algebra_record.read_text(encoding='utf-8'))
    old.update({'revision_backup':algebra['backup'],'algebra_dedup_revision':algebra,'new_environments':algebra['new_environments_vs_original']})
pdf.close()
(root/'教材对照/最终校验记录.json').write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
for ext in ('pdf','synctex.gz','aux','bbl','bcf','blg','log','out','run.xml','toc'):
    source=build/('main.'+ext)
    if source.exists():shutil.copy2(source,root/source.name)
for p in (build/'chapters').glob('*.aux'):shutil.copy2(p,root/'chapters'/p.name)
print(json.dumps(old,ensure_ascii=False,indent=2))
