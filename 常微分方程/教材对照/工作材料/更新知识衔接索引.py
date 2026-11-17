from pathlib import Path
import re,json,zipfile,collections
root=Path(__file__).resolve().parents[2]
p=root/'教材对照/整合记录与清单索引.md'
s=p.read_text(encoding='utf-8')
start=s.index('## 原文保留与组织')
end=s.index('## 逐项去向')
s=s[:start]+'''## 原文保留与组织

本轮从整合前完整备份中读取原第1—6章的具体定义、定理、公式和证明，按论证依赖重新安置新增材料。位置由前置知识和后续用途决定；适合在章末展开的内容继续留在章末。

第一章的模型放在求解问题总览之前，正式的捕捞稳定性分析放在第六章稳定性定义之后。第三章的Green响应紧接常数变易公式。第四章的准多项式与共振紧接算子解法；矩阵演化和主振动留在章末，主振动稳定性接在第六章Lyapunov直接法之后。

第五章的压缩映射解释接在Picard证明之后，Euler残差接在Peano构造之后，能量延拓接在延拓判据之后；局部逆与移动坐标仍在本章末。第六章的体积变化接相流，轨道稳定性接极限环定义，微扰闭轨接返回映射与导数判据，非临界能量层和种群闭轨仍接Hamilton系统于章末。

新增章节中，第十一章流形先于第十二章特征线，使切空间和子流形先于其应用。其余章节顺序保留。原第二章本轮未修改；Arnold读书笔记项目仅备份，未改动。

原稿中参数可微性证明的余项估计、Hamilton中心分类证明的闭曲线步骤已在原思路内修正和展开；补出矩阵变分方程、有限维紧集延拓及离散周期点导数判据的证明，供新增内容直接引用。正文统一使用“证明”，不保留教材章节出处说明。

本轮修改前备份：`../常微分方程备份/知识衔接调整前-20261029-185708.zip`。具体审阅与位置理由见[知识衔接审阅与调整记录](知识衔接审阅与调整记录.md)。

'''+s[end:]
mapping={}
for code in ['B04','B05']+[f'B{i:02}' for i in range(13,21)]:mapping[code]=['chapter12.tex']
for i in range(1,18):mapping[f'E{i:02}']=['chapter11.tex']
mapping.update({'B21':['continuity-energy-extension.tex'],'B24':['qualitative-return-perturbation.tex'],
'C18':['arnold-linear-algebra.tex','continuity-mode-stability.tex'],
'C25':['qualitative-volume.tex','qualitative-hamilton-volume.tex'],
'D01':['continuity-banach.tex'],'D02':['continuity-banach.tex'],'D03':['continuity-banach.tex','continuity-euler.tex'],
'D04':['arnold-contraction.tex'],'D06':['arnold-contraction.tex'],
'F01':['arnold-models.tex','continuity-harvest.tex'],'F03':['arnold-models.tex','arnold-linear-algebra.tex'],
'F08':['qualitative-orbital-stability.tex']})
for i in range(19,22):mapping[f'C{i:02}']=['linear-quasipolynomials.tex']
base='C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程/chapters/'
for code,files in mapping.items():
    for f in files:assert (root/'chapters'/f).exists()
    links='、'.join(f'[{f}](<{base}{f}>)' for f in files)
    s,n=re.subn(r'(\| '+code+r' \| )[^\n]+?( \| [^\n]+ \|)',lambda m:m[1]+links+m[2],s)
    assert n==1,(code,n)
p.write_text(s,encoding='utf-8')
p=root/'教材对照/工作材料/TikZ配图记录.json'
data=json.loads(p.read_text(encoding='utf-8'))
for item in data['figures']:
    if item['name']=='return-map':item['chapter']='qualitative-return-perturbation.tex';item['anchor']=None
    if item['name']=='stereographic':item['chapter']='chapter11.tex'
    if item['name'] in ('burgers-characteristics','jet-cusp'):item['chapter']='chapter12.tex'
    if item['name']=='lv-levels':item['anchor']=None
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
backup=root.parent/'常微分方程备份/知识衔接调整前-20261029-185708.zip'
assert zipfile.ZipFile(backup).testzip() is None
def expand(path,seen):
    path=path.resolve();assert path not in seen,path
    seen.add(path)
    t=path.read_text(encoding='utf-8')
    def sub(m):
        name=m[1]
        if name.startswith('chapters/'):
            p=root/(name if name.endswith('.tex') else name+'.tex')
            return expand(p,seen)
        return m[0]
    return re.sub(r'\\(?:input|include)\{([^}]+)\}',sub,t)
seen=set();text=expand(root/'main.tex',seen)
labels=re.findall(r'\\label\{([^}]+)\}',text)
dups=[k for k,v in collections.Counter(labels).items() if v>1];assert not dups,dups
old=zipfile.ZipFile(backup)
oldlabels=set()
for name in old.namelist():
    if name.endswith('.tex'):oldlabels.update(re.findall(r'\\label\{([^}]+)\}',old.read(name).decode('utf-8-sig')))
assert oldlabels<=set(labels),oldlabels-set(labels)
chains=[['thm:有限维Picard存在唯一性定理','sec:picard-contraction','thm:Peano存在性定理'],
['prop:compact-extension-vector','thm:energy-global-extension'],
['thm:C1依赖性定理','prop:matrix-variation','cor:Cr依赖性推论','thm:local-inverse'],
['def:动力系统与流','thm:nonlinear-liouville','def:Lyapunov稳定性','prop:harvest-threshold'],
['sec:normal-modes','thm:Lyapunov稳定性判据','prop:normal-mode-stability'],
['def:Poincare映射','prop:discrete-derivative-test','sec:perturbed-oscillation'],
['def:Hamilton系统','thm:Hamilton函数沿轨道守恒','cor:hamilton-volume','thm:regular-energy-level'],
['chap:manifolds','chap:characteristics']]
for chain in chains:
    pos=[text.index('\\label{'+k+'}') for k in chain]
    assert pos==sorted(pos),chain
envs=('definition','theorem','proof','proposition','example','lemma','corollary')
baseline='\n'.join((root/f'教材对照/工作材料/整合前原稿/chapter{i}.tex').read_text(encoding='utf-8') for i in range(1,7))
result={'active_chapter_files':sorted(p.name for p in seen if p.parent.name=='chapters'),
'retained_labels':len(oldlabels),'current_labels':len(labels),'dependency_chains_checked':chains,
'new_environments':{e:text.count('\\begin{'+e+'}')-baseline.count('\\begin{'+e+'}') for e in envs},
'backup_crc_valid':True,'chapter2_unchanged_this_revision':(root/'chapters/chapter2.tex').read_bytes()==old.read('chapter2.tex')}
(root/'教材对照/工作材料/知识依赖核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
