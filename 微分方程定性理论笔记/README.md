# 微分方程定性理论 · LaTeX 重排本

张芷芬、丁同仁、黄文灶、董镇喜《微分方程定性理论》（科学出版社）的
**忠实 LaTeX 重排工程**。目标：将扫描版原书逐页、逐节录入为可编译的
LaTeX 源码，版式 / 公式 / 符号尽量与原书一致。

> 当前进度：第一章 §1「解的存在性、唯一性及对初值(或参数)的依赖性」、§2「解的延拓」、
> §3「动力系统的一般概念」、§4「平面上的动力系统」已完整转录，章末参考文献已录入；
> 第二至八章为占位 stub（见 `chapters/chapter0X.tex`）。

---

## 1. 编译方式

引擎 **XeLaTeX**，参考文献用 **biber**。用 `latexmk` 一条命令即可
（会自动识别 `.bcf` 并调用 biber，再回环编译交叉引用）：

```bash
latexmk -xelatex main
```

产物为 `main.pdf`。需要清缓存时：

```bash
latexmk -c          # 清辅助文件（保留 pdf）
latexmk -C          # 清全部生成文件
```

> 注：不要手动跑 `bibtex`；本项目用 `biblatex` + `biber`
> （`backend=biber`），`latexmk -xelatex` 已自动处理。

---

## 2. 目录结构

```
微分方程定性理论笔记/
├── main.tex                主文件：加载 preamble、封面、正文 \include、参考文献
├── preamble/
│   ├── packages.tex        宏包加载（ctex / xeCJK / tcolorbox / thmtools / biblatex …）
│   ├── colors.tex          配色方案（绛紫 + 香槟金）与兼容别名
│   ├── commands.tex        自定义数学命令（\vect, \dd, \norm, \R …）
│   ├── theorems.tex        定理环境体系（tcolorbox + thmtools）
│   ├── geometry.tex        版心 / 边距
│   ├── chapter.title.tex   章节标题样式
│   ├── part.title.tex       Part 标题样式
│   └── cover.tex           封面（\makecover / \booktitle …）
├── chapters/
│   ├── chapter01.tex        第一章（§1 已完成，§2–§4 占位）
│   └── chapter02–08.tex     其余章节占位
├── bibliography/
│   └── references.bib      参考文献（照原书录入，style=ieee）
└── README.md
```

---

## 3. 设计系统

### 配色方案 D：绛紫 + 香槟金（Deep Purple & Champagne Gold）

定义在 `preamble/colors.tex`，全部为具名颜色，便于统一替换：

| 角色 | 颜色名 | HEX | 用途 |
|------|--------|-----|------|
| 主结构色 | `PurpleMain` `#3B2A45` | 绛紫 | 定理 / 推论 / 引理 边框、章节彩带 |
| 深结构色 | `PurpleDeep` `#2D1F36` | 深绛紫 | 注记 / 问题 边框、定义标题文字 |
| 浅结构色 | `PurpleLight` `#8B6F95` | 浅绛紫 | 构造 / 记号 / 说明 边框 |
| 淡紫底 | `PurplePale` `#F0EAF0` | 淡紫 | 定义环境底色 |
| 强调金 | `GoldMain` `#C9A86A` | 香槟金 | 定义边框、装饰线 |
| 淡金底 | `GoldPale` `#F5E8D0` | 淡金 | 示例底色 |
| 暖金 | `TealMain` | 香槟金变体 | 示例边框 |

为兼容旧模板的版式文件（`cover.tex` / `chapter.title.tex` / `part.title.tex`），
`colors.tex` 末尾提供了一组**颜色别名**（`BlueMain→PurpleMain`、
`LogicBlue→PurpleMain`、`GreenMain→PurpleMain`、`TealMain→GoldMain!85!white` 等）。
**改配色只需动 `colors.tex`，不必改几何/封面文件。**

### 字体

`ctex` + `xeCJK` 中文默认字体；正文数学用 `fontspec` 加载的字体族
（`\theoremFont` / `\proofFont` 在 `preamble` 中设定）。如需指定字体，
在 `packages.tex` 或 `main.tex` 内用 `\setCJKmainfont` / `\setmainfont`。

### 定理盒子

每个定理环境是一条 `tcolorbox` 彩条框：顶部彩条写「环境名 + 编号 +
（有自定义小标题时）冒号 + 小标题」。

---

## 4. 定理环境使用规范

定义在 `preamble/theorems.tex`，基于 `\newtcbtheorem`。
**每个环境接受两个参数**：`{自定义小标题}{交叉引用标签}`。

```latex
\begin{theorem}{存在唯一性定理}{thm:exist}
  设 $f$ 在区域 $G$ 上连续且关于 $x$ 满足 Lipschitz 条件，则初值问题存在唯一解。
\end{theorem}

由定理 \ref{thm:exist} 可知 ……      % 交叉引用用 \ref{中文标签}
```

- 编号采用**章内计数**（`number within=chapter`），与原书「定理 1.x」约定一致。
- 小标题留空也合法：`\begin{theorem}{}{thm:foo}`，此时彩条不显示冒号。
- 交叉引用统一用 `\ref{标签}`，**不要手填编号**。

### 可用环境

| 类别 | 环境 | 彩条色 | 底色 |
|------|------|--------|------|
| 绛紫（主） | `theorem` 定理 / `corollary` 推论 / `proposition` 命题 / `prp` 原理 | 绛紫边框 | 白 |
| 深绛紫 | `axiom` 公理 / `problem` 问题 / `lemma` 引理 / `remark` 注记 | 深绛紫边框 | 白 |
| 香槟金 | `definition` 定义 | 金边框 + 深紫标题字 | 淡紫 |
| 浅绛紫 | `construction` 构造 / `note` 记号 / `ill` 说明 | 浅绛紫边框 | 白 |
| 暖金 | `example` 示例 | 金边框 | 淡金 |

- 证明：`\begin{proof}` … `\end{proof}`（可带小标题
  `\begin{proof}[证明（充分性）]`），结尾自动落 □。
- 解：`\begin{solution}` … `\end{solution}`，无编号。

### 无编号的「附注 / 命名定理 / 命名引理」

原书的「附注 1/2/3」「Cauchy-Peano 定理」「Gronwall 引理」等：

- **附注**用 `\fuzhu{编号}{内容}`（行内加粗「附注 1」）。
- **命名定理 / 命名引理**（如 Cauchy-Peano、Gronwall）一律写成**带编号的真实环境**
  `\begin{theorem}{Cauchy-Peano 存在定理}{thm:cauchy-peano}` /
  `\begin{lemma}{Gronwall 引理}{lem:gronwall}`，
  不要再用旧的 `\namedthm{}` / `\namedlem{}` 无编号包装宏——
  真实环境能自动编号、可被 `\ref` 引用，且与全书的编号体系一致。

---

## 5. 数学命令约定

定义在 `preamble/commands.tex`，转录时统一使用，不要手敲等价符号：

| 命令 | 含义 |
|------|------|
| `\vect{x}` | 向量（`\boldsymbol{x}`），用于 $\vect{x},\vect{\mu}$ |
| `\dd t` | 微分号 $\dd t$ |
| `\norm{\vect{x}}` / `\abs{x}` | 向量范数 / 绝对值 |
| `\R` `\C` `\Z` `\N` `\Q` | 数域黑体 $\R,\C,\Z,\N,\Q$ |
| `\parder{f}{x}` | 偏导 $\partial f/\partial x$ |
| `\flow` | 流 $\Phi$ |

---

## 6. ⚠️ 已知坑（必读）

### 上下标里的带参宏必须加外层花括号

**现象**：在 `tcolorbox` 定理体内写 `$(E_\vect{\mu})$` 或 `$(E_0^\vect{\mu})$`
会报 `! Missing { inserted.` / `! Missing } inserted.` / `\begingroup`
类错误，且错误往往延迟到下一个定理才被抛出来，极难定位。

**原因**：`\vect` 是 `\boldsymbol{#1}`——一个**需要参数的宏**。
写成 `E_\vect{\mu}` 时，`_` 只捕获宏名 `\vect` 本身，后面的 `{\mu}`
被留在外层成为**悬空分组**，导致整个定理体的花括号计数失衡。

**正确写法**（务必加一层花括号把整个参数包成上下标原子）：

```latex
$(E_{\vect{\mu}})$        % ✅ 下标：把 \vect{\mu} 整体括起来
$(E_0^{\vect{\mu}})$      % ✅ 上标：同样整体括起来
```

**通用规则**：凡上下标是「宏 + 参数」（`\vect{}`、`\mat{}`、`\frac{}{}` 等），
一律用 `{...}` 把整个上下标内容包起来；单个字符（`x_i`、`t^2`）可不加。

> 这条是本项目第 1.2 节编译不过的根因，已修复。以后转录带向量下标/上标的
> Cauchy 问题记号（如 $E_{\vect{\mu}}$、$E_0^{\vect{\mu}}$、$E_{\vect{\eta}}$）
> 务必照此写。

---

## 7. 转录约定（忠实重排）

1. 正文分节与原书小节一一对应；章末习题与参考文献照原书录入。
2. 公式编号沿用原书式号（如 `(1.1)`–`(1.25)`），用 `\tag{1.x}` 标注。
3. 原书插图先留 `\fbox{\parbox{...}{图~x.x …}}` 占位，待补 `figure/` 图后替换。
4. 编译每写完一节检查 `main.log`，要求 **0 错误、0 警告**（至少 0 错误）。
5. 新增一章：复制 `chapters/chapter01.tex` 骨架，在 `main.tex` 取消对应
   `\include` 注释。
