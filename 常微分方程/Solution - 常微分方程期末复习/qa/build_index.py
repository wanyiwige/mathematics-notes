from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]

def expand(text):
 return re.sub(r'\\input\{([^}]+)\}',lambda m:(ROOT/(m[1]+'.tex')).read_text(encoding='utf-8') if (ROOT/(m[1]+'.tex')).exists() else '',text)
def group(text,start):
 assert text[start]=='{';depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  elif text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i
rows=[];answers=[]
for n in range(1,6):
 text=(ROOT/f'chapter{n}.tex').read_text(encoding='utf-8-sig')
 text=expand(text)
 matches=list(re.finditer(r'\\problem\{([^}]+)\}\{([^}]+)\}',text))
 for j,m in enumerate(matches):
  block=text[m.end():matches[j+1].start() if j+1<len(matches) else len(text)]
  ans=[]
  for a in re.finditer(r'\\ans\{',block):
   body,_=group(block,a.end()-1);ans.append(body)
  rows.append({'id':m[1],'printed_pages':m[2],'chapter':n,'answers':len(ans)})
  if ans:
   answers.append(r'\noindent\textbf{\hyperref[q:'+m[1]+']{习题 '+m[1]+r'}}\quad{\small 第\pageref{q:'+m[1]+r'}页。}')
   answers.extend(r'\[\begin{gathered}'+a+r'\end{gathered}\]' for a in ans)
expected=[]
def simple(sec,nums):expected.extend(sec+'.'+str(n) for n in nums)
def sub(sec,q,n):expected.extend(f'{sec}.{q}({k})' for k in range(1,n+1))
simple('1.1',[1,2]);simple('1.2',range(1,5));sub('1.2',5,3);sub('1.3',1,3);simple('1.3',[2])
simple('2.1',[1]);
for q,n in [(2,13),(3,15),(4,6),(5,3),(6,6),(7,4)]:sub('2.1',q,n)
simple('2.1',[8,9])
for q,n in [(1,9),(2,2),(4,5)]:sub('2.2',q,n)
simple('2.2',range(5,10))
for q,n in [(1,6),(2,6),(3,9)]:sub('2.4',q,n)
simple('2.4',[4,6]);simple('3.1',[1,2,3]);simple('3.2',[1,2,3,4,6]);simple('3.3',[1,2,3]);simple('3.4',range(1,7));simple('3.5',range(1,5))
sub('4.1',1,8);simple('4.1',[2,3]);sub('4.2',1,8);simple('4.2',[2]);simple('4.3',[1]);sub('4.3',3,7);simple('4.3',[4]);simple('4.4',[1,2,3]);simple('5.1',range(1,9));simple('5.2',[1]);simple('5.3',[1,4]);sub('5.3',5,2);simple('5.4',[1,2,3]);simple('5.5',[1,3,4]);simple('5.6',[2,3])
actual=[r['id'] for r in rows]
assert len(actual)==len(set(actual)), 'duplicate question'
assert set(actual)==set(expected),{'missing':sorted(set(expected)-set(actual)),'extra':sorted(set(actual)-set(expected))}
(ROOT/'answers.tex').write_text(r'\section{答案速查}'+'\n'+r'\noindent 本表按题号列出计算结果；条件、符号限制、拼接解与证明见对应正文。'+'\n'+r'\begingroup\small'+'\n'+'\n'.join(answers)+'\n'+r'\endgroup',encoding='utf-8')
(ROOT/'qa'/'coverage.json').write_text(json.dumps({'count':len(rows),'by_chapter':{n:sum(r['chapter']==n for r in rows) for n in range(1,6)},'questions':rows},ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 常微分方程期末复习：范围与核验清单','','题号以所供第二版为准。小问分别计项；3.3.1的两问、4.3.4的三条结论在单一条目内完整对应。','',f'共 {len(rows)} 个题号条目。','','|章|条目数|','|---|---:|']
for n in range(1,6):lines.append(f'|{n}|{sum(r["chapter"]==n for r in rows)}|')
lines+=['','## 纳入原则','','前五章各节习题中的全部具体计算题，以及课堂照片指定的非计算题。建模、消去常数、积分因子的一般公式、解对初值的导数和数值编程题均计入计算范围。','','## 版本差异与原题问题','','- 第二版第2.3节未单列习题。照片明确标注第三版习题2.3第1、2题；没有第三版题面，不虚构对应。第二版2.4的全部计算小问已纳入。','- 1.1.2未指定等腰三角形的两腰，正文区分三种构型。','- 4.4.3的共振指振幅无界，不是电位差在每个足够大时刻都趋无穷。','','## 未纳入的非指定理论题','','2.1：10、11；2.2：3；2.4：5；3.2：5；3.5：5；4.3：2；5.2：2、3、4；5.3：2、3、6；5.4：4、5、6；5.5：2；5.6：1。其余第二版前五章的习题全部进入本册。其中5.4.2虽非照片指定，因涉及具体误差界的推算，保守纳入。','','## 逐题对照','','|题号|教材印刷页|正文中显式结果数|','|---|---|---:|']
lines += [f'|{r["id"]}|{r["printed_pages"]}|{r["answers"]}|' for r in rows]
(ROOT/'范围与核验清单.md').write_text('\n'.join(lines),encoding='utf-8')
print('Coverage passed:',len(rows),'entries;',len(answers),'answer index blocks')
