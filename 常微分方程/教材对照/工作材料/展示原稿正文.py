from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[2]
chapter=int(sys.argv[1]);start=int(sys.argv[2]);end=int(sys.argv[3])
text=(root/f'教材对照/工作材料/整合前原稿/chapter{chapter}.tex').read_text(encoding='utf-8')
lines=text.splitlines();text='\n'.join(lines[start-1:end])
text=re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}','[此处原有TikZ示意图，图题和邻近说明保留]',text,flags=re.S)
text=re.sub(r'^\s*%.*$','',text,flags=re.M)
text=re.sub(r'\n\s*\n\s*\n','\n\n',text)
print(text)
