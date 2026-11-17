from pathlib import Path
import fitz
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
doc=fitz.open(root/'build/tikz-review/review.pdf')
assert len(doc)==17
for group in range(2):
    sheet=Image.new('RGB',(1560,1100),'#ddd')
    for j,i in enumerate(range(group*9,min((group+1)*9,len(doc)))):
        pix=doc[i].get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((510,340))
        x=(j%3)*520;y=(j//3)*365
        sheet.paste(im,(x+(520-im.width)//2,y))
        ImageDraw.Draw(sheet).text((x+8,y+344),f'TikZ {i+1}',fill='black')
    sheet.save(root/f'教材对照/TikZ配图预览{group+1}.jpg',quality=95)
