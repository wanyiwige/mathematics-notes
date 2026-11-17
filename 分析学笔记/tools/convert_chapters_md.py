from pathlib import Path
import re, subprocess, shutil, json
root=Path(r'C:\Users\WANYIWIGE\Desktop\我的笔记\分析学笔记')
out=Path(r'D:\万的笔记\万的笔记\分析学 多变量分析学')
work=root/'tools'/'md_conversion'
work.mkdir(parents=True,exist_ok=True)
names={'definition':'定义','theorem':'定理','lemma':'引理','corollary':'推论','proposition':'命题','example':'例','problem':'问题','proof':'证明','solution':'解'}
commands=(root/'preamble/commands.tex').read_text(encoding='utf-8')
commands='\n'.join(x for x in commands.splitlines() if not x.lstrip().startswith('%'))
report=[]
for ch,title in [(2,'多元函数微分学'),(3,'重积分')]:
    files=sorted((root/f'chapters/part2/chapter{ch:02}').glob('section*.tex'))
    text='\n\n'.join(p.read_text(encoding='utf-8') for p in files)
    text=re.sub(r'(?m)(?<!\\)%.*','',text)
    # Give references readable, stable names instead of engine-dependent theorem numbers.
    labels={}
    for m in re.finditer(r'\\begin\{('+ '|'.join(names)+r')\}\s*(?:\[([^\]]*)\])?\s*(?:[（(]([^）)]+)[）)])?\s*\\label\{([^}]+)\}',text):
        labels[m[4]]=m[2] or m[3] or (names[m[1]]+'（本节前述）')
    ref_sec=0
    ref_count=0
    for token in re.finditer(r'\\section\{|\\begin\{('+ '|'.join(k for k in names if k not in ('proof','solution'))+r')\}|\\label\{([^}]+)\}',text):
        if token[0].startswith(r'\section'):
            ref_sec+=1
            ref_count=0
        elif token[1]:
            ref_count+=1
        elif token[2]:
            labels[token[2]]=f'{ch}.{ref_sec}.{ref_count}'
    text=re.sub(r'\\(?:eqref|ref)\{([^}]+)\}',lambda m: labels.get(m[1],m[1]),text)
    text=re.sub(r'\\label\{[^}]+\}','',text)
    head_sec=[0,0]
    def heading(m):
        if m[0].startswith(r'\section'):
            head_sec[0]+=1
            head_sec[1]=0
            return m[0]
        number=''
        if m[1] not in ('proof','solution'):
            head_sec[1]+=1
            number=f' {ch}.{head_sec[0]}.{head_sec[1]}'
        return '\n\n\\textbf{'+names[m[1]]+number+('（'+m[2]+'）' if m[2] else '')+'}\n\n'
    text=re.sub(r'\\section\{[^}]+\}|\\begin\{('+ '|'.join(names)+r')\}\s*(?:\[([^\]]*)\])?',heading,text)
    text=re.sub(r'\\end\{('+ '|'.join(names)+r')\}',lambda m:'\n\n'+('$\\square$\n\n' if m[1]=='proof' else ''),text)
    sec=[0]
    def section(m):
        sec[0]+=1
        return '\\section*{§'+str(sec[0])+'　'+m[1]+'}'
    text=re.sub(r'\\section\{([^}]+)\}',section,text)
    text=re.sub(r'\\input\{figure/([^}]+)\.tex\}',lambda m:r'\includegraphics{assets/'+Path(m[1]).name+'.png}',text)
    images=re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',text)
    for img in images:
        if img.startswith('assets/'):
            assert (out/img).exists(), img
            continue
        src=root/img
        if not src.exists(): raise RuntimeError('Missing image '+img)
        dest=out/'assets'/Path(img).name
        dest.parent.mkdir(exist_ok=True)
        shutil.copy2(src,dest)
        text=text.replace('{'+img+'}','{assets/'+dest.name+'}')
    text=text.replace('\\begin{center}','').replace('\\end{center}','')
    tex=work/f'chapter{ch}.tex'
    tex.write_text(commands+'\n\\chapter*{第'+('二' if ch==2 else '三')+'章　'+title+'}\n'+text,encoding='utf-8')
    target=out/f'chapter{ch}.md'
    result=subprocess.run(['pandoc',str(tex),'-f','latex','-t','markdown+tex_math_dollars-raw_tex-header_attributes-link_attributes','--wrap=none','--markdown-headings=atx','-o',str(target)],capture_output=True,text=True,encoding='utf-8')
    if result.returncode: raise RuntimeError(result.stderr)
    md=target.read_text(encoding='utf-8')
    md=re.sub(r'<img src="([^"]+)"[^>]*?/>',lambda m:'![示意图]('+m[1]+')',md)
    # Put display delimiters on their own lines; keep existing math content intact.
    md=re.sub(r'\$\$(.*?)\$\$',lambda m:'\n\n$$\n'+m[1].strip()+'\n$$\n\n',md,flags=re.S)
    md=re.sub(r'\n{3,}','\n\n',md).strip()+'\n'
    md='\n'.join(line.strip() for line in md.splitlines())+'\n'
    target.write_text(md,encoding='utf-8')
    report.append({'chapter':ch,'sections':sec[0],'images':len(images),'source_environments':{k:len(re.findall(r'\\begin\{'+k+r'\}', '\n'.join(p.read_text(encoding='utf-8') for p in files))) for k in names},'warnings':result.stderr})
print(json.dumps(report,ensure_ascii=False,indent=2))
