from pathlib import Path
import re
files=list(Path('chapters').glob('arnold-*.tex'))+[Path('chapters/chapter'+str(i)+'.tex') for i in range(7,16)]
rows=[(len(m.group(1)),p.name,m.group(1)) for p in files for m in re.finditer(r'(?<!\\)\$([^\$]+)\$',p.read_text(encoding='utf-8')) if len(m.group(1))>65 and '=' in m.group(1)]
for n,p,s in sorted(rows,reverse=True): print(n,p,s)
