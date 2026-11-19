"""从各周最终正文生成带题号链接的答案速查；不改写题目和解答。"""
from pathlib import Path
import json
import re

BASE = Path(__file__).resolve().parent


def heading(block):
    start = block.index("{")
    depth = 0
    for pos in range(start, len(block)):
        if block[pos] == "{" and block[pos - 1] != "\\":
            depth += 1
        elif block[pos] == "}" and block[pos - 1] != "\\":
            depth -= 1
            if not depth:
                return block[start + 1:pos]
    raise ValueError("未闭合的小节标题")


parts = ["\\section{作业答案速查}\n"]
manifest = []
for week in range(1, 13):
    path = BASE / f"week{week:02}.tex"
    source = path.read_text(encoding="utf8")
    blocks = re.split(r"(?=\\subsection\{)", source)[1:]
    parts.append(f"\\subsection*{{第{week}周}}\n\\begin{{enumerate}}\n")
    for block in blocks:
        label = re.search(r"\\label\{([^}]+)\}", block)
        answer = re.search(r"\\paragraph\{(?:标准)?答案\}([\s\S]*)", block)
        title = heading(block)
        manifest.append({"week": week, "title": title,
                         "label": label[1] if label else None,
                         "has_answer": bool(answer)})
        if label and answer:
            text = re.sub(r"%[^\n]*", "", answer[1]).strip()
            parts.append("\\item \\hyperref[" + label[1] + "]{" + title + "}：" + text + "\n")
    parts.append("\\end{enumerate}\n")
(BASE / "answers.tex").write_text("".join(parts), encoding="utf8")
(BASE / "qa" / "作业覆盖清单.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf8")
print(f"作业条目{len(manifest)}；有完整答案{sum(x['has_answer'] for x in manifest)}")
