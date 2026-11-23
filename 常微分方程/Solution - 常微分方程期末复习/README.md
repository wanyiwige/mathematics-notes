# 常微分方程期末复习

教材：张伟年、杜正东、徐冰《常微分方程》第2版。范围：前五章所有计算题，以及课堂照片指定的其余习题。详见“范围与核验清单.md”。

- 主文件：`常微分方程期末复习.tex`。
- 成品：`常微分方程期末复习.pdf`，77页。
- `methods.tex`：13类方法汇总，包括选法、公式、适用条件及遗漏分支检查。
- `chapter1.tex` 至 `chapter5.tex`：原题数据、逐题推导、答案与必要条件。
- `answers.tex`：可点击回到原题的答案速查。
- 方向场、磁场、Euler折线均由TikZ源码绘制，无外部图片依赖。
- `numerics.py`：数值题的可运行程序，附三种算法、表格生成及独立校验。

## 编译

使用已安装中文字体的Windows TeX Live，在本目录运行两遍；第一次新建目录时可运行三遍以稳定目录和页码：

```powershell
xelatex -interaction=nonstopmode -halt-on-error 常微分方程期末复习.tex
xelatex -interaction=nonstopmode -halt-on-error 常微分方程期末复习.tex
```

其他系统需把主文件的 `fontset=windows` 改为当地可用的中文字体设置。正常编译不需要Python；所有生成的TikZ和表格源码已包含。

## 计算与检查

```powershell
python numerics.py
python qa/verify_symbolic.py
python qa/build_index.py
```

数值脚本需要 `mpmath`；符号验证需要 `sympy`。重新生成示意图需 `numpy`、`scipy`，运行 `python qa/make_figures.py`。重新生成页面检查图需 `pymupdf`、`Pillow`，运行 `python qa/render_review.py`。

## 版本限制

照片写明“习题2.3（第三版）1、2”。所供第二版2.3节没有单独习题，相关计算集中于2.4，已全部作答。未取得第三版题面，未宣称两版的这两道题已一一对应。

## 核验记录

- 180个题号条目通过范围清单检查；3.3.1内两问、4.3.4内三条结论分别对应展开。
- 224项符号校验通过，包括微分残差、势函数、参数解、特征向量、完整方程组、级数系数及初值。校验的具体覆盖项见 `qa/symbolic-check.json`；不是对所有文字证明的自动验证。
- 数值题用高精度积分、独立ODE求解及步长减半核对；报告见 `qa/numerical-check.json`。
- 最终XeLaTeX编译退出码0，无LaTeX警告、缺字、Overfull或Underfull。
- 全77页均作缩略图排版审阅，图表及关键公式另检查；自动文字边界检查未发现靠近纸张边缘的裁切候选。缩略图检查不等于以阅读字号逐字复读所有页面。
- 题面以教材渲染页核对，OCR仅供检索；源PDF摘要与页码偏移见 `qa/source-provenance.json`。

2026年11月24日，经AI辅助整理、计算、核验。原有教材笔记正文和用户已有修改未纳入本次变更。
