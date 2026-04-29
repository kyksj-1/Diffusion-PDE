# paper/black · 论文写作工作区

> EntroDiff · NeurIPS 2026 主控目录。
> 所有内部草稿、推导、图表都在这里；最终投稿前生成 `white/` 镜像版本。

## 目录结构

```
paper/black/
├── neurips_2026.tex      ← 主控文件（LaTeX 入口）
├── neurips_2026.sty      ← 官方样式（从 paper/2026_template/ 拷贝，禁改）
├── checklist.tex         ← NeurIPS Reproducibility Checklist
├── references.bib        ← 文献库（占位，写作期填充）
├── CONVENTIONS.md        ← 排版与符号约定（写之前必读）
├── README.md             ← 本文件
├── macros/
│   └── notation.tex      ← 全文统一符号宏（与 path_A_method_skeleton 对齐）
├── sections/
│   ├── 01_intro.tex
│   ├── 02_related_work.tex
│   ├── 03_preliminaries.tex
│   ├── 04_double_burgers.tex
│   ├── 05_method.tex
│   ├── 06_theory.tex          ← 主体（Theorem 2-5）
│   ├── 07_experiments.tex
│   ├── 08_conclusion.tex
│   ├── A1_proofs.tex          ← 完整证明（不计入 9 页）
│   ├── A2_extra_experiments.tex
│   └── A3_implementation_details.tex
├── figures/              ← 所有 PDF / PNG 图（filename 与 \includegraphics 对齐）
└── proofs/               ← Markdown 推导稿（先用 md 推导，再迁到 .tex）
```

## 编译命令

```bash
cd paper/black
pdflatex neurips_2026
bibtex   neurips_2026
pdflatex neurips_2026
pdflatex neurips_2026
```

或（推荐）使用 `latexmk`：

```bash
cd paper/black
latexmk -pdf neurips_2026.tex
```

## 写作流程（推荐）

1. **先 Markdown 后 LaTeX**：复杂推导先在 `paper/black/proofs/<thmN>.md` 写 Markdown 草稿（你能直接看 Markdown 数学），定稿后迁到 `sections/A1_proofs.tex`。
2. **小步提交**：每完成一个 section / theorem，单独 commit（参考 `CLAUDE.md §Git 工作流`）。
3. **图表先占位**：`sections/*.tex` 里所有 `\begin{figure}` 当前是 `\fbox` 占位；实际图待 `figures/*.pdf` 生成后替换为 `\includegraphics`。
4. **每次 push 前**：`latexmk -pdf` 跑通；用 `pdftotext` 检查 9 页限制。

## 约束清单（每次写作前快速校对）

- [ ] **页数**：正文 ≤ 9 页（含图表，不含 references/checklist/appendix）
- [ ] **匿名**：未加 `[final]` 或 `[preprint]`；未提到本组前作（除非用第三人称）
- [ ] **公式**：所有 displayed math 都在 `equation` / `align` 等环境内；**禁** `$$...$$`
- [ ] **表格**：`booktabs` 三线（`\toprule / \midrule / \bottomrule`），**无** `|`
- [ ] **图表 caption**：每个 caption 含 *Key take-away message*
- [ ] **引用**：用 `\citet{}` / `\citep{}`，统一一致

## 元数据

- 投稿目标：NeurIPS 2026 Main Track（双盲）
- 项目代号：EntroDiff
- 论文骨架来源：`Docs/black/path_A_method_skeleton.md`
- 主控分支：见 git log（当前在 `feat/setup-paper-project-20260426`）
