from pathlib import Path
import zipfile,re,json
root=Path(__file__).resolve().parents[2]
backup=root.parent/'常微分方程备份/Arnold内容整合前-20261029-073418/常微分方程-完整原稿.zip'
out=root/'教材对照/工作材料/整合前原稿';out.mkdir(exist_ok=True)
z=zipfile.ZipFile(backup)
report={}
for i in range(1,7):
    name=next(n for n in z.namelist() if n.replace('\\','/').endswith(f'chapters/chapter{i}.tex'))
    text=z.read(name).decode('utf-8-sig');(out/f'chapter{i}.tex').write_text(text,encoding='utf-8')
    print('\n===== 原稿 Chapter',i,'字符',len(text),'=====')
    for j,line in enumerate(text.splitlines(),1):
        if re.search(r'\\(?:chapter|section|subsection|subsubsection)\*?\{|\\begin\{(?:definition|theorem|proposition|lemma|corollary)\}',line):print(f'{j}: {line.strip()}')
    report[str(i)]={'characters':len(text),'lines':len(text.splitlines())}
(root/'教材对照/工作材料/原稿阅读清单.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
