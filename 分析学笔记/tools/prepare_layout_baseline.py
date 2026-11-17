"""Prepare an isolated, original-source compile baseline from the rollback ZIP."""
from pathlib import Path
import json,zipfile
root=Path.cwd(); b=root/'codex-build-section-layout-20261028'
m=json.loads((b/'manifest.json').read_text(encoding='utf-8'))
wrapper=(b/'all-parts.tex').read_text(encoding='utf-8')
with zipfile.ZipFile(b/'sources-before-split.zip') as z:
 for c in m['checks']:
  rel=c['file']; data=z.read(rel)
  if rel=='chapters/part2/chapter3.tex':
   data=data.replace(b'\\input{chapters/part2/section3-4}',z.read('chapters/part2/section3-4.tex'))
  target=b/'baseline-source'/rel
  target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
  old=rel.removesuffix('.tex')
  new=target.relative_to(root).as_posix().removesuffix('.tex')
  wrapper=wrapper.replace('\\input{'+old+'}', '\\input{'+new+'}')
(b/'baseline.tex').write_text(wrapper,encoding='utf-8')
(b/'baseline.bbl').write_bytes((b/'all-parts.bbl').read_bytes())
print('Isolated original-source baseline prepared; project sources unchanged.')
