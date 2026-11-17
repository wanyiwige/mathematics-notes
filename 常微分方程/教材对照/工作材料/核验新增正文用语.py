from pathlib import Path
import re,collections,json,zipfile,hashlib
r=Path(__file__).resolve().parents[2]
p=r/'教材对照/工作材料/新增正文用语调整记录.json'
d=json.loads(p.read_text(encoding='utf-8'));z=zipfile.ZipFile(d['backup'])
checks={'labels_unchanged':True,'environment_order_unchanged':True,'display_formulas_unchanged':True,'original_inline_formulas_retained':True,'tikz_code_unchanged':True,'chapter1_and_chapter2_unchanged':True}
display=lambda s:re.findall(r'\\\[.*?\\\]|\\begin\{(?:align\*?|equation\*?|gather\*?)\}.*?\\end\{(?:align\*?|equation\*?|gather\*?)\}',s,re.S)
inline=lambda s:collections.Counter(re.findall(r'(?<!\\)\$(?!\$)(.+?)(?<!\\)\$',s,re.S))
for n in range(1,16):
    name=f'chapters/chapter{n}.tex'
    a=z.read(name).decode('utf-8-sig').replace('\r\n','\n');b=(r/name).read_text(encoding='utf-8')
    assert re.findall(r'\\label\{[^}]+\}',a)==re.findall(r'\\label\{[^}]+\}',b),name
    assert re.findall(r'\\(?:begin|end)\{[^}]+\}',a)==re.findall(r'\\(?:begin|end)\{[^}]+\}',b),name
    assert display(a)==display(b),name
    assert not inline(a)-inline(b),(name,inline(a)-inline(b))
    assert re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',a,re.S)==re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',b,re.S),name
    if n<3:assert z.read(name)==(r/name).read_bytes()
    assert r'\input{' not in b
    assert '演化' not in b and '离散步进' not in b
checks['all_chapter_inputs_absent']=True
d['checks']=checks;d['backup_crc_valid']=z.testzip() is None
assert hashlib.sha256(Path(d['backup']).read_bytes()).hexdigest()==d['backup_sha256']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'revised_passages':len(d['changes']),'checks':checks},ensure_ascii=False))
