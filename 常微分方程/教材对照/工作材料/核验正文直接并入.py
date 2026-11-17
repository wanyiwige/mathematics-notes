from pathlib import Path
import re,json,zipfile,hashlib
import fitz
root=Path(__file__).resolve().parents[2]
rp=root/'教材对照/工作材料/模块直接并入记录.json'
d=json.loads(rp.read_text(encoding='utf-8'))
z=zipfile.ZipFile(d['backup']);assert z.testzip() is None
pattern=re.compile(r'\\input\{([^}]+)\}')
modules=[]
def old_expand(name,parent):
    text=z.read(name).decode('utf-8-sig').replace('\r\n','\n')
    def sub(m):
        src=m[1]+('.tex' if not m[1].endswith('.tex') else '')
        modules.append({'chapter':parent,'source':src})
        return old_expand(src,parent).rstrip('\n')
    return pattern.sub(sub,text)
for i in range(1,16):
    name=f'chapter{i}.tex'
    expected=old_expand('chapters/'+name,name)
    actual=(root/'chapters'/name).read_text(encoding='utf-8')
    assert expected==actual,name
    assert not pattern.search(actual),name
d['expanded_inputs']=modules
d['expanded_text_inputs']=sum(x['source'].startswith('chapters/') for x in modules)
d['expanded_tikz_inputs']=sum(x['source'].startswith('figure/tikz/') for x in modules)
d['chapter_content_exactly_matches_pre_edit_expansion']=True
d['chapter_input_commands']=0
d['chapter1_and_chapter2_untouched']=all((root/f'chapters/chapter{i}.tex').read_bytes()==z.read(f'chapters/chapter{i}.tex') for i in (1,2))
oldpdf=fitz.open(stream=z.read('main.pdf'),filetype='pdf')
d['previous_pdf_pages']=len(oldpdf)
oldhashes=[hashlib.sha256(p.get_text().encode()).hexdigest() for p in oldpdf]
(root/'教材对照/工作材料/直接并入前PDF页面文字哈希.json').write_text(json.dumps(oldhashes),encoding='utf-8')
rp.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
dep=root/'教材对照/工作材料/知识依赖核验.json'
v=json.loads(dep.read_text(encoding='utf-8'))
v['active_chapter_files']=[f'chapter{i}.tex' for i in range(1,16)]
v['modules_directly_embedded']=True
dep.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:d[k] for k in ('expanded_text_inputs','expanded_tikz_inputs','chapter_content_exactly_matches_pre_edit_expansion','chapter1_and_chapter2_untouched','previous_pdf_pages')},ensure_ascii=False))
