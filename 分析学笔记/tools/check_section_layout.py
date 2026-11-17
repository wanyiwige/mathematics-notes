"""Read-only validation of the actual entry graph against the archived source."""
from pathlib import Path
import json,re,zipfile,hashlib
root=Path.cwd()
build=root/'codex-build-section-layout-20261028'
m=json.loads((build/'manifest.json').read_text(encoding='utf-8'))
metadata={e['file']:e['metadata_bytes'] for e in m['entries']}
pattern=re.compile(rb'(?m)^% (?:\xe7\xac\xac\d+\xe8\x8a\x82|\xe6\xad\xa3\xe6\x96\x87)\xef\xbc\x9a[^\r\n]*\r?\n\\input\{([^}]+)\}%\r?\n')
with zipfile.ZipFile(build/'sources-before-split.zip') as z:
    assert (root/'main.tex').read_bytes()==z.read('main.tex'),'main.tex changed'
    for item in m['checks']:
        name=item['file']
        before=z.read(name)
        if name=='chapters/part2/chapter3.tex':
            before=before.replace(b'\\input{chapters/part2/section3-4}',z.read('chapters/part2/section3-4.tex'))
        after=(root/name).read_bytes()
        after=after.split(b'\n',1)[1] # added chapter comment only
        used=[]
        def expand(match):
            path=match[1].decode('utf-8')+'.tex'
            assert path in metadata,path
            used.append(path)
            return (root/path).read_bytes()[metadata[path]:]
        after=pattern.sub(expand,after)
        assert after==before,f'Content/order mismatch in {name}'
        assert used==[e['file'] for e in m['entries'] if e['entry']==name],name
    for e in m['entries']:
        body=(root/e['file']).read_bytes()[metadata[e['file']]:]
        assert hashlib.sha256(body).hexdigest()==e['body_sha256'],e['file']
print('PASS: actual input order, complete reconstructed bytes, section hashes, and main.tex unchanged.')
