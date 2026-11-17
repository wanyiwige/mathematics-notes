from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
data=json.loads((root/'教材对照/工作材料/TikZ配图记录.json').read_text(encoding='utf-8'))
preview=root/'build/tikz-review';preview.mkdir(exist_ok=True)
s=r'''\documentclass[UTF8]{ctexart}
\usepackage[paperwidth=18cm,paperheight=12cm,margin=1cm]{geometry}
\usepackage{amsmath,amssymb,tikz,xcolor,listings}
\usetikzlibrary{arrows.meta,positioning}
\input{preamble/colors}
\pagestyle{empty}
\begin{document}
'''
for i,f in enumerate(data['figures']):
    if i:s+='\n\\clearpage\n'
    s+='\\begin{center}\n\\input{figure/tikz/'+f['name']+'}\n\\par\\medskip\n'+str(i+1)+'. '+f['caption']+'\n\\end{center}\n'
s+='\\end{document}\n'
(preview/'review.tex').write_text(s,encoding='utf-8')
