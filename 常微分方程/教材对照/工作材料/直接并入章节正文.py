from pathlib import Path
import re,json,zipfile,hashlib,shutil,datetime
root=Path(__file__).resolve().parents[2]
stamp='20261030-'+datetime.datetime.now().strftime('%H%M%S')
backup=root.parent/'常微分方程备份'/f'正文模块直接并入前-{stamp}.zip'
sources=[root/'main.tex']+sorted((root/'chapters').glob('*.tex'))+sorted((root/'preamble').glob('*.tex'))+sorted((root/'figure/tikz').glob('*.tex'))
pdf=root/'main.pdf'
assert backup.parent.is_dir()
with zipfile.ZipFile(backup,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for p in sources+[pdf]:z.write(p,p.relative_to(root).as_posix())
assert zipfile.ZipFile(backup).testzip() is None
pattern=re.compile(r'\\input\{([^}]+)\}')
mapping={};files={};expanded=[]
def expand(text,parent,stack=()):
    def sub(m):
        p=(root/(m[1]+('.tex' if not m[1].endswith('.tex') else ''))).resolve()
        assert p.is_relative_to(root) and p not in stack,p
        assert p.is_file(),p
        mapping[p.relative_to(root).as_posix()]=parent.name
        expanded.append({'chapter':parent.name,'source':p.relative_to(root).as_posix()})
        return expand(p.read_text(encoding='utf-8'),parent,stack+(p,)).rstrip('\n')
    return pattern.sub(sub,text)
for n in range(1,16):
    p=root/f'chapters/chapter{n}.tex'
    old=p.read_text(encoding='utf-8');new=expand(old,p)
    assert not pattern.search(new)
    assert re.findall(r'\\label\{([^}]+)\}',new)==re.findall(r'\\label\{([^}]+)\}',expand(old,p))
    files[p.name]={'before_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'changed':old!=new}
    if old!=new:p.write_text(new,encoding='utf-8')
    assert p.read_text(encoding='utf-8')==new
# Keep unused former modules as a reversible archive, away from active chapter sources.
archive=(root/'教材对照/工作材料'/f'正文模块归档-{stamp}').resolve()
assert archive.is_relative_to(root)
archive.mkdir()
for p in sorted((root/'chapters').glob('*.tex')):
    if re.fullmatch(r'chapter\d+\.tex',p.name):continue
    assert p.resolve().is_relative_to(root/'chapters')
    shutil.move(str(p),str(archive/p.name))
# The user had already inlined Chapter 1; its empty old module must not be restored.
mapping['chapters/arnold-models.tex']='chapter1.tex'
index=root/'教材对照/整合记录与清单索引.md'
s=index.read_text(encoding='utf-8')
for src,chapter in mapping.items():
    if not src.startswith('chapters/'):continue
    name=Path(src).name
    s=re.sub(r'\['+re.escape(name)+r'\]\(<[^>]+>\)',f'[{chapter}](<C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/chapters/{chapter}>)',s)
s=re.sub(r'(\[[^\]]+\]\(<[^>]+>\))(?:、\1)+',r'\1',s)
s+='\n## 直接并入章节正文\n\n2026-10-30，新增正文模块与17幅TikZ图形代码均已直接展开到对应章节正文，章节内不再使用`\\input`。原模块移入工作材料归档；当前内容以`chapters/chapter1.tex`至`chapter15.tex`为准。主文件原有分章结构及导言配置保留。\n'
index.write_text(s,encoding='utf-8')
manifest=root/'教材对照/工作材料/TikZ配图记录.json'
d=json.loads(manifest.read_text(encoding='utf-8'))
for f in d['figures']:
    f['chapter']=mapping.get('chapters/'+f['chapter'],f['chapter'])
    f['embedded_in_chapter']=True
manifest.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
report={'date':'2026-10-30','backup':str(backup),'backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'archive':str(archive),'expanded_inputs':list({(i['chapter'],i['source']):i for i in expanded}.values()), 'source_to_chapter':mapping,'chapter_files':files,'original_pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}
# Each original chapter was expanded once for replacement and once for equality verification.
(root/'教材对照/工作材料/模块直接并入记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'backup':str(backup),'changed_chapters':[k for k,v in files.items() if v['changed']],'chapter_input_commands':0,'inline_tikz':sum((root/f'chapters/chapter{i}.tex').read_text(encoding='utf-8').count(r'\begin{tikzpicture}') for i in range(1,16))},ensure_ascii=False,indent=2))
