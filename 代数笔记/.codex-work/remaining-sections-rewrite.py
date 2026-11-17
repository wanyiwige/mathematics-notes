from pathlib import Path

root = Path(r'C:\Users\WANYIWIGE\Desktop\我的笔记\代数笔记')
p = root / 'chapters/Part 2/chapter2.tex'
work = root / '.codex-work'

def replace_section(title, next_title, fragment):
    text = p.read_text(encoding='utf-8')
    start = text.index('\\section{' + title + '}')
    end = text.index('\\section{' + next_title + '}', start) if next_title else text.index('%\\section{章末习题中的知识与解法}', start)
    content = (work / fragment).read_text(encoding='utf-8')
    p.write_text(text[:start] + content.rstrip() + '\n\n' + text[end:], encoding='utf-8')

if __name__ == '__main__':
    import sys
    replace_section(*sys.argv[1:])
