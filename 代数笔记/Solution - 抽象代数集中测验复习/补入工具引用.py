from pathlib import Path
import re

root=Path(__file__).resolve().parent
mapping={
0:{4:['n-relations'],5:['n-relations'],6:['n-recursion','n-induction'],
7:['n-recursion','n-induction'],8:['n-order','n-recursion','n-induction'],
13:['n-gcd','n-prime-factor','n-congruence'],
14:['n-prime-factor','n-binomial-count'],
23:['n-gcd','n-bezout','n-congruence'],24:['n-crt','n-bezout','n-congruence']},
3:{1:['r-ring-laws','r-unit-laws'],2:['r-ring-laws','r-unit-laws'],
3:['r-ring-laws','r-unit-laws','n-induction'],8:['r-homomorphism','r-quotients']}}
for chapter,items in mapping.items():
    path=root/f'chapter{chapter}.tex'
    text=path.read_text(encoding='utf-8')
    pieces=re.split(r'(?=\\subsection\{习题\d+)',text)
    for i,piece in enumerate(pieces):
        m=re.match(r'\\subsection\{习题(\d+)',piece)
        if not m: continue
        n=int(m[1])
        # 为当前题建立稳定标签，以便直接引用已经完成的习题结论。
        label=f'\\label{{exercise:{chapter}:{n}}}'
        if label not in piece:
            end=piece.index('\n')
            piece=piece[:end]+label+piece[end:]
        intro='\\paragraph{所用结论}'+'、'.join('\\toolref{'+k+'}' for k in items[n])+'。'
        if chapter==0 and n==7:
            intro+='另使用前题已证明的加法结合律与乘法交换律（第零章习题6）。'
        if chapter==3 and n==3:
            intro+='并使用本章习题2（\\ref{exercise:3:2}）已经证明的“右逆不唯一推出非单位”；不将本题结论作为前提。'
        if r'\paragraph{所用结论}' in piece:
            piece=re.sub(r'\\paragraph\{所用结论\}[\s\S]*?(?=\\begin\{proof\})',lambda _:intro+'\n',piece,count=1)
        else:
            piece=piece.replace(r'\begin{proof}',intro+'\n'+r'\begin{proof}',1)
        pieces[i]=piece
    path.write_text(''.join(pieces),encoding='utf-8')
print('第零章、第三章已补入编号引用。')
