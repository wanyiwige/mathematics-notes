"""One-shot, source-preserving mechanical split; run from the project root."""
from pathlib import Path
import re, json, hashlib, zipfile

ROOT = Path.cwd()
BUILD = ROOT / 'codex-build-section-layout-20261028'
PART_NAMES = {'part1': '第一部分：单变量分析学', 'part2': '第二部分：多变量分析学',
              'part4': '第四部分：Fourier 分析', 'partm': '短篇'}
SECTION = re.compile(rb'(?m)^[ \t]*\\section(?:\*)?(?=[\s\[{])')
LEGACY = 'chapters/part2/section3-4.tex'
LEGACY_INPUT = b'\\input{chapters/part2/section3-4}'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def title(data, command):
    text = data.decode('utf-8-sig')
    match = re.search(r'(?m)^[ \t]*\\' + command + r'\*?\s*(?:\[[^\]]*\])?\s*\{', text)
    if not match:
        return ''
    start = i = match.end()
    depth = 1
    while i < len(text):
        if text[i] == '\\':
            i += 2
            continue
        if text[i] == '{': depth += 1
        if text[i] == '}':
            depth -= 1
            if not depth: return text[start:i].replace('\n', ' ').replace('\r', '')
        i += 1
    raise ValueError('Unbalanced title')

def main():
    if BUILD.exists():
        raise RuntimeError('Build directory exists; do not rerun migration over user edits')
    files = sorted(p for p in (ROOT/'chapters').glob('*/*.tex')
                   if re.fullmatch(r'(chapter|article)\d+\.tex', p.name))
    originals = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in files}
    originals[LEGACY] = (ROOT/LEGACY).read_bytes()
    changes, sections, expected = {}, [], {}
    for rel, raw in originals.items():
        if rel == LEGACY: continue
        path = Path(rel)
        part, stem = path.parent.name, path.stem
        number = int(re.search(r'\d+', stem)[0])
        folder = path.parent / f'section{number:02d}'
        if (ROOT/folder).exists(): raise RuntimeError(f'Existing destination: {folder}')
        flat = raw.replace(LEGACY_INPUT, originals[LEGACY]) if rel == 'chapters/part2/chapter3.tex' else raw
        nl = b'\r\n' if flat.count(b'\r\n') > flat.count(b'\n')/2 else b'\n'
        chapter_title = title(flat, 'chapter')
        matches = list(SECTION.finditer(flat))
        # Unsectioned articles keep their heading and move the body, without inventing sections.
        if not matches:
            chapter_line = re.search(rb'(?m)^.*\\chapter\*?\{[^\r\n]*\}[^\r\n]*(?:\r?\n|$)', flat)
            start = chapter_line.end() if chapter_line else len(flat)
            chunks = [(start, len(flat), 'body.tex', '正文（原文未分节）')] if flat[start:].strip() else []
        else:
            chunks = [(m.start(), matches[i+1].start() if i+1<len(matches) else len(flat),
                       f'section{i+1:02d}.tex', title(flat[m.start():], 'section')) for i,m in enumerate(matches)]
        prefix = flat[:chunks[0][0]] if chunks else flat
        part_note = PART_NAMES.get(part, part)
        chapter_note = f'{part_note} / {"短篇" if stem.startswith("article") else "第"}{number}{"" if stem.startswith("article") else "章"}：{chapter_title}'
        note = f'% ===== {chapter_note} ====='.encode('utf-8') + nl
        aggregator = note + prefix
        entries = []
        for idx,(a,b,name,heading) in enumerate(chunks, 1):
            dest = (folder/name).as_posix()
            section_note = f'{number}.{idx} {heading}' if matches else heading
            meta = (f'% !TEX root = ../../../main.tex\n% 所属：{chapter_note}\n'
                    f'% {"节" if matches else "内容"}：{section_note}\n% 正文按原文件顺序保存；由 ../{path.name} 调用。\n').encode('utf-8').replace(b'\n', nl)
            changes[dest] = meta + flat[a:b]
            aggregator += f'% {"第"+str(idx)+"节" if matches else "正文"}：{heading}'.encode('utf-8') + nl
            aggregator += f'\\input{{{dest[:-4]}}}%'.encode('utf-8') + nl
            entry = {'part': part, 'chapter': number, 'chapter_name': chapter_title,
                     'section': idx if matches else None, 'section_name': heading,
                     'entry': rel, 'file': dest, 'metadata_bytes': len(meta),
                     'body_sha256': digest(flat[a:b])}
            sections.append(entry); entries.append(entry)
        changes[rel] = aggregator if chunks else note + flat
        expected[rel] = {'sha256':digest(flat), 'prefix':prefix, 'entries':entries,
                         'original_sha256':digest(raw), 'note':note}
    # Compatibility path retained: no deletion and no duplicate source of truth.
    changes[LEGACY] = (b'% !TEX root = ../../main.tex\n'
        + '% 兼容旧路径：第二部分第三章第四节「反常重积分」。\n'.encode('utf-8')
        + '% 正文已迁至 section03/section04.tex；请在新位置编辑。\n'.encode('utf-8')
        + b'\\input{chapters/part2/section03/section04}%\n')
    BUILD.mkdir()
    with zipfile.ZipFile(BUILD/'sources-before-split.zip', 'x', zipfile.ZIP_DEFLATED) as z:
        for p in sorted((ROOT/'chapters').rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(ROOT))
        z.write(ROOT/'main.tex','main.tex')
    # Detect edits since inspection before modifying originals.
    for rel,raw in originals.items():
        if (ROOT/rel).read_bytes() != raw: raise RuntimeError(f'Concurrent edit: {rel}')
    for rel,data in changes.items():
        p=ROOT/rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
    # Independently reconstruct the original flattened bytes, with no whitespace normalization.
    results=[]
    for rel,item in expected.items():
        data=(ROOT/rel).read_bytes()
        if item['entries']:
            reconstructed=item['prefix']
            for e in item['entries']:
                chunk=(ROOT/e['file']).read_bytes()[e['metadata_bytes']:]
                assert digest(chunk)==e['body_sha256'],e['file']
                reconstructed+=chunk
        else:
            reconstructed=data[len(item['note']):]
        assert digest(reconstructed)==item['sha256'],rel
        results.append({'file':rel,'expanded_sha256':digest(reconstructed),'unchanged':True})
    manifest={'chapter_count':len(files),'numbered_sections':sum(e['section'] is not None for e in sections),
              'body_files':sum(e['section'] is None for e in sections),'entries':sections,'checks':results,
              'main_sha256':digest((ROOT/'main.tex').read_bytes())}
    (BUILD/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 章节文件索引','', '章入口仍使用原来的 chapterN.tex，主文件无需改动。',
      '目录 sectionNN 对应本部分的第 NN 章；其中 sectionMM.tex 对应该章第 MM 节。',
      '没有分节的短篇正文放在 body.tex，不人为增加节标题。',
      '图片仍使用项目根目录下的 figure/ 路径，从项目根目录编译 main.tex。',
      '节文件顶部含主文件定位注释、所属章名和本节名称。','',
      '旧路径 part2/section3-4.tex 仅作兼容转发，实际正文在 part2/section03/section04.tex。','']
    for rel in expected:
        p=Path(rel); label=title(originals[rel],'chapter')
        lines += [f'## {PART_NAMES[p.parent.name]} / {p.stem}：{label}', '',f'章入口：[{p.name}]({rel.removeprefix("chapters/")})','']
        es=expected[rel]['entries']
        if not es: lines += ['本章目前仅有章标题，尚无正文或节标题。','']
        for e in es:
            sec=f'{e["chapter"]}.{e["section"]}' if e['section'] else '正文'
            lines += [f'- {sec} {e["section_name"]} — [{Path(e["file"]).name}]({e["file"].removeprefix("chapters/")})']
        lines += ['']
    (ROOT/'chapters/README.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('entries','checks')},ensure_ascii=False))
    print('PASS: all chapter bodies reconstructed byte-for-byte; original chapter/main paths retained.')

if __name__=='__main__': main()
