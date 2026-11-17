from pathlib import Path
p=Path(__file__).with_name('补齐衔接中的证明依据.py')
text=p.read_text(encoding='utf-8')
prefix=text[:text.index("edit('arnold-models.tex'")]
start=text.index("edit('qualitative-volume.tex',r'固定初值")
exec(compile(prefix+text[start:],str(p),'exec'))
