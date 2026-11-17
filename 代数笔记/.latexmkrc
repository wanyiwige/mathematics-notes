# 始终编译 main.tex
@default_files = ('main.tex');

# 使用 xelatex
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode %O %S';
$pdf_mode = 5;

# 降低无损压缩等级。注意：这一行只对 latexmk 生效；直接调用 xelatex 时
# xdvipdfmx 仍用默认最高档压缩。封面图已改为 JPEG（原样嵌入、不再重压缩），
# 因此现在无论用哪种方式编译，PDF 生成都只需约 1 秒。这一行留作兜底。
$xdvipdfmx = 'xdvipdfmx -E -z 1 -o %D %O %S';
