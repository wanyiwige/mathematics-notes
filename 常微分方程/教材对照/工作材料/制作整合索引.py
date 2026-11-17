from pathlib import Path
import re

root=Path(__file__).resolve().parents[2]
source=(root/'教材对照/Arnold教材相对现有笔记的新增知识清单.md').read_text(encoding='utf-8')
ids=re.findall(r'^\| ([A-F]\d+) \|',source,re.M)
mapping={}
for key in ids:
    g=key[0]; n=int(key[1:])
    if g=='A': target={1:'arnold-models',2:'chapter9',3:'chapter9',4:'chapter9',5:'arnold-green',6:'arnold-green'}.get(n,'chapter7')
    if g=='B': target='chapter7' if n in [1,2,3,6,7,8,9,10,11,12] else ('chapter11' if n in [4,5,13,14,15,16,17,18,19,20] else 'arnold-energy')
    if g=='C': target='arnold-linear-algebra' if n in [1,2,3,4,5,18,19,20,21] else ('chapter10' if n in [6,7,8,9,10,11,13,14,15,16,17] else ('chapter15' if n==12 else ('chapter8' if n in [26,27,28,29] else ('arnold-energy' if n==25 else 'chapter9'))))
    if g=='D': target='chapter15' if n==5 else 'arnold-contraction'
    if g=='E': target='chapter12' if n<=17 else 'chapter13'
    if g=='F': target={1:'arnold-models',2:'arnold-energy',3:'arnold-models',4:'chapter14',5:'chapter14',6:'arnold-linear-algebra',7:'chapter14',8:'arnold-energy',9:'chapter14',10:'chapter15',11:'chapter14',12:'chapter14',13:'chapter15',14:'chapter15'}[n]
    mapping[key]='chapters/'+target+'.tex'
quoted={
 'E06':'一般嵌入定理沿原书作为引用；正则方程子流形另有证明。',
 'E07':'一般流形分类沿原书作为引用。',
 'E11':'S2 障碍在第13章证明；全体球面的可平行化分类作为深层引用。',
 'E26':'一般 Poincare--Hopf 指标和定理作为引用；球面、射影空间、环面计算有证明。',
 'F10':'沿原书反对称方法证明；完全谱与最低特征函数正性列明为分析前提。',
 'F13':'折叠和正规形的类型计算有证明；Cibrario/Davydov 全分类作为原书引用。',
 'F14':'给出定义、约化机制和奇点模型；全分类及模参数理论保留引用属性。',
}
lines=['# Arnold 内容整合记录与清单索引','','日期：2026-10-29。','','## 备份','',
'完整备份目录：`C:/Users/WANYIWIGE/Desktop/我的笔记/常微分方程备份/Arnold内容整合前-20261029-073418/`。',
'其中两个 ZIP 分别保存两套笔记完整原稿，`备份校验.csv` 记录 SHA-256。主笔记22个 TeX 源文件已逐一与备份内容核对。','',
'## 原文保留与组织','',
'原第1、3、4、5、6章以末尾 input 接入补充文件，原正文保留；第2章字节未改。第6章原有势能相图补了缺失的 label，修复原有悬空引用。原空白第7—13章用于新增专题，另新增第14—15章。主文件已接入全部15章。Arnold 读书笔记项目仅备份，未改动。','',
'正文统一使用“证明”环境，不标“补充证明”。每章或节标教材节号；已有知识通过现有标签引用。原书略去的初等步骤已展开；原书只引用的深层分类保持引用属性，不虚构证明。','',
'## 逐项去向','','| 原清单编号 | 源文件 | 说明 |','|---|---|---|']
for key in ids:
    file=mapping[key]
    note=quoted.get(key,'已在正文组织定义、结论与相应论证；同义扩展与已有结论衔接。')
    lines.append(f'| {key} | [{Path(file).name}](<{(root/file).as_posix()}>) | {note} |')
lines+=['','## 封面','',
'第7—15章各选一张既有未使用二次元图，另存 JPEG 2280×1500，精确比值1.52:1。记录见 `工作材料/新增章节封面记录.json`；预览为 `新增章节封面预览.jpg`。',
'经确认图像及引用后，按用户授权删除对应9张原PNG；这些PNG仍完整保存在整合前ZIP中。','',
'## 校验','',
'源码定理环境成对，标签无新增重复；原前6章正文与备份核对无删改。编译、页数及排版检查结果在最终校验后记录。']
(root/'教材对照/整合记录与清单索引.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('INDEXED',len(ids),'TARGETS_EXIST',all((root/p).exists() for p in mapping.values()))
