from pathlib import Path
import re,json
BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/'chapters'
KINDS={'mydefinition':('定义','def'),'mytheorem':('定理','th'),'proposition':('命题','prop'),'mycorollary':('推论','cor'),'mylemma':('引理','lem')}
TOPICS={1:{1:'events',2:'probability',3:'conditional',4:'independence',5:'product'},2:{1:'cdf',2:'discrete',3:'continuous',4:'transform'},3:{1:'joint',2:'rvindependence',3:'conditionaldist',4:'order',5:'jacobian'}}
def brace(s,pos):
    assert s[pos]=='{',s[pos:pos+30]
    depth=0
    for k in range(pos,len(s)):
        if s[k]=='{' and (k==0 or s[k-1]!='\\'):depth+=1
        if s[k]=='}' and (k==0 or s[k-1]!='\\'):
            depth-=1
            if not depth:return s[pos+1:k],k+1
    raise ValueError('unclosed brace')
def env_end(s,pos,env):
    pattern=re.compile(r'\\(begin|end)\{'+re.escape(env)+r'\}')
    depth=0
    for m in pattern.finditer(s,pos):
        depth+=1 if m[1]=='begin' else -1
        if depth==0:return m.end()
    raise ValueError(env)

# Plain source paragraphs are not captured by the environment scanner. Keep the
# necessary notation beside its first use, reading the actual source each run.
# Boundaries are unique text anchors rather than fragile source line numbers.
CONTEXT={
    (1,'section','events'):[
        (r'\item \textbf{互斥（互不相容）事件}',r'\end{enumerate}',True),
        ('事件的运算性质就是集合的运算性质。',r'\subsection*{古典概率模型（高中内容）}',False)],
    (1,'after','measure-space'):[
        ('若存在两两互斥的事件列 $A_1,A_2,',r'\textbf{注：}当 $\mu(\Omega)=1$',False)],
    (1,'section','product'):[
        ('设子试验 $1$ 和子试验 $2$ 的概率空间分别为',r'\begin{example}[掷骰子与独立取球]',False)],
    (2,'before','continuous-distribution-properties'):[
        (r'\textbf{注：}\quad “几乎处处”是指',r'\textbf{注：}\quad 因为各端点的单点概率为 $0$',False)],
    (2,'before','standard-normal-symmetry'):[
        ('标准正态分布的密度和分布函数分别记为',r'\begin{proposition}{标准正态分布的对称公式}',False)],
    (3,'after','random-vector'):[
        (r'记 $\sigma(\mathcal C)$ 为包含集合族',r'\begin{proof}',False)],
    (3,'before','continuous-vector-joint-density'):[
        ('记 $m_n(B)$ 为集合 $B$ 的 $n$ 维体积',r'\begin{proposition}{联合密度与联合分布函数}',False)],
    (3,'example','独立指数变量的部分和'):[
        (r'\textbf{注：}\quad 设随机向量 $\boldsymbol X=(X_1,\ldots,X_n)$ 的密度为 $f_{\boldsymbol X}$',
         '% 补足多维密度变换的积分证明。',False)],
}

def source_context(s,ch,stage,key):
    result=[]
    for start,stop,list_items in CONTEXT.get((ch,stage,key),[]):
        if s.count(start)!=1:
            raise ValueError(f'context start must be unique: {start}')
        begin=s.index(start)
        finish=s.index(stop,begin+len(start))
        fragment=s[begin:finish].strip()
        if list_items:
            fragment='\\begin{enumerate}\n'+fragment+'\n\\end{enumerate}'
        result.append('\n'+fragment+'\n')
    return ''.join(result)

manifest=[]
for ch in range(1,4):
    p=SOURCE/f'chapter{ch}.tex';s=p.read_text(encoding='utf8')
    chunks=[f'% !TEX root = 概率论期中复习.tex\n% 自动抽取自 chapters/chapter{ch}.tex；原例题及其解答保留。\n']
    sec=0;ex=0
    pattern=re.compile(r'\\section\{|\\begin\{(example|'+ '|'.join(KINDS)+r')\}')
    cursor=0
    for m in pattern.finditer(s):
        if m.start()<cursor:continue
        line=s.count('\n',0,m.start())+1
        if m[0].startswith('\\section'):
            title,end=brace(s,m.end()-1);sec+=1
            key=TOPICS[ch][sec]
            chunks.append(f'\n\\clearpage\\section{{{title}}}\\label{{k:{key}}}\n')
            if key=='cdf': chunks.append(r'\label{sec:random-variables-and-distribution-functions}'+'\n')
            if key=='events': chunks.append(r'事件的全集为$\Omega$；$AB=A\cap B$，$A^c=\Omega\setminus A$。并表示至少一个发生，交表示同时发生，差表示前者发生而后者不发生。'+'\n')
            if key=='probability': chunks.append(r'事件列$A_n\uparrow A$表示$A_n\subseteq A_{n+1}$且$A=\bigcup_nA_n$；$A_n\downarrow A$表示$A_{n+1}\subseteq A_n$且$A=\bigcap_nA_n$。'+'\n')
            if key=='order':chunks.append(r'本节公式中的样本$X_1,\ldots,X_n$独立同分布，公共分布函数为$F$；涉及密度时假设公共分布连续型且密度为$f$。'+'\n')
            chunks.append(source_context(s,ch,'section',key))
            cursor=end;continue
        env=m[1];end=env_end(s,m.start(),env)
        block=s[m.start():end]
        title='';key=''
        if env=='example':
            ex+=1;head=re.match(r'\\begin\{example\}(?:\[([^\n]*)\])?',block)
            title=head[1] or '抽取方式与排列计数'
            chunks.append(source_context(s,ch,'example',title))
            plain=title.replace('$','').replace(r'\sigma','sigma')
            heading=r'\texorpdfstring{'+title+'}{'+plain+'}' if '$' in title else title
            body=block[head.end():-len(r'\end{example}')]
            gap=re.match(r'(?:\s|%[^\n]*\n)*',s[end:]);ps=end+gap.end()
            if s.startswith(r'\begin{proof}',ps):
                end=env_end(s,ps,'proof');body+='\n'+s[ps:end]
            chunks.append(f'\n\\subsection{{例题：{heading}}}\\label{{note:c{ch}:e{ex}}}\n')
            chunks.append(f'\\basis{{原笔记第{ch}.{sec}节，例“{title}”；源码\\texttt{{chapters/chapter{ch}.tex}}第{line}行。}}\n')
            chunks.append(body.strip()+'\n')
            key=f'note:c{ch}:e{ex}'
        else:
            pos=len('\\begin{'+env+'}')
            if not block[pos:].lstrip().startswith('{'):
                title='事件列极限的存在';key='event-limit-exists'
                block=block[:pos]+'{'+title+'}{'+key+'}'+block[pos:]
            else:
                pos=pos+len(block[pos:])-len(block[pos:].lstrip());title,pos=brace(block,pos);key,pos=brace(block,pos)
            chunks.append(source_context(s,ch,'before',key))
            chunks.append('\n'+block+'\n')
            chunks.append(f'\\origin{{原笔记第{ch}.{sec}节，{KINDS[env][0]}“{title}”；源码第{line}行。}}\n')
            chunks.append(source_context(s,ch,'after',key))
        manifest.append({'chapter':ch,'section':sec,'kind':env,'title':title,'label':key,'source':str(p.relative_to(BASE.parent)),'start_line':line,'end_line':s.count('\n',0,end)+1})
        cursor=end
    (BASE/f'notes{ch:02d}.tex').write_text('\n'.join(line.rstrip() for line in ''.join(chunks).splitlines())+'\n',encoding='utf8')
    print('chapter',ch,'examples',ex)
(BASE/'qa'/'原笔记抽取清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
