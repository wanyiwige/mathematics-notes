import 扩写证明 as base
import 扩写几何与零点
import 扩写动力学证明
import 扩写进阶证明
import 扩写共轭证明
import re
for file,key,body in base.edits:
    text=(base.root/'chapters'/file).read_text(encoding='utf-8')
    candidates=[m for m in re.finditer(r'\\begin\{proof\}(.*?)\\end\{proof\}',text,re.S) if key in m.group(1)]
    if len(candidates)!=1: raise RuntimeError((file,key,len(candidates)))
base.apply()
