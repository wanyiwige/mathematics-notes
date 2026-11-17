import os, json, time, threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import fitz
from rapidocr_onnxruntime import RapidOCR

ROOT=Path(__file__).parent
SOURCE=r'C:\Users\WANYIWIGE\Desktop\UTX - Ordinary Differential Equations.pdf'
local=threading.local()
def run(p):
    target=ROOT/f'page_{p:03d}.json'
    if target.exists(): return p
    if not hasattr(local,'engine'):
        local.engine=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1)
    doc=fitz.open(SOURCE)
    pix=doc[p-1].get_pixmap(matrix=fitz.Matrix(1.65,1.65))
    result,_=local.engine(pix.tobytes('png'),use_cls=False)
    data={'pdf_page':p,'printed_page':p-4,'elements':result or []}
    target.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    text='\n'.join(x[1] for x in result or [])
    (ROOT/f'page_{p:03d}.txt').write_text(text,encoding='utf-8')
    return p
if __name__=='__main__':
    import sys
    pages=[int(x) for x in sys.argv[1:]] or list(range(10,339))
    with ThreadPoolExecutor(max_workers=4) as pool:
        for p in pool.map(run,pages): print('DONE',p,flush=True)
