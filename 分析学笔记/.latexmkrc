# 分析学笔记 编译配置
# 引擎：XeLaTeX（preamble 用到 ctex / fontspec / xeCJK，禁止用 pdflatex）
$pdf_mode = 5;            # 5 = 直接用 XeLaTeX 生成 PDF
# 参考文献：biblatex + Biber（禁止用 BibTeX，否则 main.bbl 为空）
$biber = 'biber %O %S';
