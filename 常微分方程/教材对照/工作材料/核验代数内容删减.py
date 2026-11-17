from pathlib import Path
import json,hashlib,re,zipfile
r=Path(__file__).resolve().parents[2]
p=r/'教材对照/工作材料/代数重复内容删减记录.json';d=json.loads(p.read_text(encoding='utf-8'))
baseline=json.loads((r/'教材对照/工作材料/代数笔记源文件哈希基线.json').read_text(encoding='utf-8'))
a=r.parent/'代数笔记'
assert all(hashlib.sha256((a/k).read_bytes()).hexdigest()==v for k,v in baseline.items())
z=zipfile.ZipFile(d['backup']);assert z.testzip() is None
assert hashlib.sha256(Path(d['backup']).read_bytes()).hexdigest()==d['backup_sha256']
for name in z.namelist():
    if name.startswith('preamble/') or name=='main.tex':assert z.read(name)==(r/name).read_bytes(),name
for i in (1,2,3,5,10,13,14,15):
    name=f'chapters/chapter{i}.tex';assert z.read(name)==(r/name).read_bytes(),name
text='\n'.join((r/f'chapters/chapter{i}.tex').read_text(encoding='utf-8') for i in range(1,16))
labels=re.findall(r'\\label\{([^}]+)\}',text);refs=re.findall(r'\\(?:ref|eqref|autoref)\{([^}]+)\}',text)
assert len(labels)==len(set(labels));assert not set(d['removed_labels'])&set(refs)
assert not set(refs)-set(labels),set(refs)-set(labels)
assert r'\input{' not in text
for env in ('definition','theorem','proof','lemma','proposition','example','corollary'):
    assert text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}')
for name in ['def:banach-operator','lem:neumann-series','def:l2-completion','def:smooth-one-parameter','thm:arnold-translation','thm:arnold-flowbox','thm:arnold-stable-manifold']:
    assert name in labels,name
for change in d['changes']:
    assert change['algebra_source']
d.update({'algebra_protected_files':len(baseline),'algebra_sources_unchanged':True,'backup_crc_valid':True,
'no_undefined_source_references':True,'current_label_count':len(labels),'original_main_and_preamble_unchanged':True,'math_environments_balanced':True})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:d[k] for k in ['algebra_protected_files','algebra_sources_unchanged','current_label_count','no_undefined_source_references','net_removed_environments']},ensure_ascii=False))
