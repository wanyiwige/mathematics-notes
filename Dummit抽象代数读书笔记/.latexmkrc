# 始终编译 main.tex
@default_files = ('main.tex');

# 使用 xelatex
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode %O %S';
$pdf_mode = 5;
