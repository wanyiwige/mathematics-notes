from pathlib import Path
import re,subprocess,concurrent.futures
root=Path(r'C:\Users\WANYIWIGE\Desktop\我的笔记\分析学笔记')
work=root/'tools/md_conversion'
out=Path(r'D:\万的笔记\万的笔记\分析学 多变量分析学')
text='\n'.join(p.read_text(encoding='utf-8') for p in (root/'chapters/part2/chapter03').glob('*.tex'))
imgs=re.findall(r'\\input\{(figure/[^}]+)\}',text)
def render(img):
    src=root/img
    name=src.stem
    tex=work/(name+'.tex')
    tex.write_text(r'\documentclass[border=6pt]{standalone}'+'\n'+r'\usepackage{ctex,amsmath,amssymb,tikz}'+'\n'+r'\usetikzlibrary{arrows.meta,positioning,patterns,calc,decorations.pathreplacing}'+'\n'+r'\begin{document}'+'\n'+src.read_text(encoding='utf-8')+'\n'+r'\end{document}',encoding='utf-8')
    p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',tex.name],cwd=str(work),capture_output=True)
    if p.returncode: return (name,p.stdout.decode('utf-8',errors='replace')[-1700:])
    p=subprocess.run(['pdftoppm','-png','-scale-to','2200','-singlefile',str(work/(name+'.pdf')),str(out/'assets'/name)],capture_output=True)
    return (name,'OK' if p.returncode==0 else str(p.stderr))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for r in pool.map(render,imgs): print(r)

