# CONVENTIONS.md · `paper/black/` 写作约定

> 写一行 LaTeX 之前**必读**。CLAUDE.md 与 MISSION.md 的"NeurIPS 排版规范"是这份文件的总命令；本文件落实到具体宏、命名、风格细节。

---

## 1. 排版强制约束（不可违反）

| 项 | 规定 |
|---|---|
| 页数 | 正文 ≤ **9 页**（含图表；references / checklist / appendix 不计） |
| 文档类 | `\documentclass{article}` + `\usepackage{neurips_2026}`（不带任何选项；选项即 = 双盲提交） |
| 匿名 | **禁**用 `[final]` / `[preprint]` 选项；引用本组前作用第三人称 |
| 公式 | 所有 displayed math 用 `equation` / `align` / `equation*` / `align*` / `gather` 等环境；**禁** `$$...$$`（NeurIPS 模板明确禁止，且会破坏行号） |
| 表格 | 必须 `booktabs`（`\toprule \midrule \bottomrule`），**禁**垂直分割线 `|` |
| 图表 caption | 必须含 **Key take-away message**（一句话告诉读者"这张图说明了什么") |
| 引用 | `natbib`，文内统一 `\citet{key}`（叙述式，"作者(年份)"）/ `\citep{key}`（括号式，"(作者,年份)"）|

## 2. 文件 / 模块约定

| 角色 | 路径 | 注 |
|---|---|---|
| 主控 | `paper/black/neurips_2026.tex` | 不放正文，仅做 \input 编排 |
| 章节 | `paper/black/sections/NN_<name>.tex` | 序号 `01..06` 对应正文 §1..§6；`A1..A3` 对应附录 |
| 符号宏 | `paper/black/macros/notation.tex` | 改之前同步修改 `Docs/black/path_A_method_skeleton.md §3.1` |
| 引用 | `paper/black/references.bib` | 每条 entry 必须给 venue + year；占位条目带 `note = {TODO: ...}` |
| 推导草稿 | `paper/black/proofs/thmN_proof.tex` | LaTeX 直接写；对应 `\input` 在 `A1_proofs.tex` |
| 图表 | `paper/black/figures/<NN>_<name>.pdf` | 序号与论文中出现顺序一致 |

## 3. 符号统一规则

- **必须通过宏**：所有专业符号（$\Wass{1}$, $\sth$, $\Rent$ 等）通过 `macros/notation.tex` 定义的宏调用，**禁**直接写 `W_1` / `s_\theta` / `\mathrm{R}_{\mathrm{ent}}`。
- **新增宏**：在 `macros/notation.tex` 加宏后，必须同步更新 `Docs/black/path_A_method_skeleton.md §3.1` 的 Notation 表（避免讲义与论文符号漂移）。
- **不冲突原则**：小写罗马字母用作 PDE 解（$u$）、扩散变量；大写 $W$ 用作 Wasserstein；希腊字母 $\sigma, \tau, \rho, \nu$ 用法见 `notation.tex`。

## 4. 引用风格细则

```latex
% 叙述式（作者作主语）
\citet{huang2024diffusionpde} introduced ...
% → "Huang et al. (2024) introduced ..."

% 括号式（事实陈述加来源）
The score field satisfies a Burgers identity \citep{sarkar2026scoreshocks}.
% → "... a Burgers identity (Sarkar, 2026)."

% 多引用
prior work \citep{huang2024diffusionpde, yao2025fundps, lim2023ddo}
```

**禁**：`\cite{}`（不区分括号 vs 叙述）、`Huang et al. \citep{...}`（重复作者名）。

## 5. 图表写法模板

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=0.8\linewidth]{02_burgers_shock_compare}  % no extension
    \caption{Burgers shock comparison. Left: WENO5 ground truth; middle: EDM baseline (visible oscillations); right: EntroDiff (clean shock). \textbf{Key take-away}: BV-aware parameterization captures the shock without TV blow-up, validating Theorem~\ref{thm:improved-rate}.}
    \label{fig:e1-burgers}
\end{figure}
```

```latex
\begin{table}[t]
    \caption{Main results on E1–E3 ($\Wass{1}$ error, lower is better). \textbf{Key take-away}: EntroDiff achieves the lowest error on every shock-containing benchmark.}
    \label{tab:main-results}
    \centering
    \begin{tabular}{lcccc}
        \toprule
        Method & E1 & E2 & E3 ($\rho$) & E3 ($u$) \\
        \midrule
        FNO          & ... & ... & ... & ... \\
        EDM          & ... & ... & ... & ... \\
        DiffusionPDE & ... & ... & ... & ... \\
        \textbf{EntroDiff (ours)} & \textbf{...} & \textbf{...} & \textbf{...} & \textbf{...} \\
        \bottomrule
    \end{tabular}
\end{table}
```

## 6. 写作风格约束（NeurIPS）

- **每段第一句**: topic sentence，明确这一段在论证什么。
- **避免中性叙述**: 永远把 contribution / improvement / surprise 显式说出来。
- **第三人称**: 提到本组前作必须用第三人称（"In the prior work of Anonymous et al."）。
- **公式与文字一一对应**: 每个公式前必须有一句"我接下来要写"的引出，每个公式后必须有一句"它告诉我们什么"的解释。
- **限定词诚实**: 用 *typically* / *under standard regularity* / *empirically observed* 等表明边界，**严禁**虚高（"always" / "guarantees" 不能滥用）。

## 7. 草稿期占位约定

- 暂未写的内容用 `\todo{...}` 宏（红色）— 提交前全文搜索 `\todo` 必须为空。
- 暂用的虚假数字用 `[Placeholder]` 字样标记。
- TODO 评论用 `% TODO[<scope>] · ...` 注释格式（便于 grep）。

## 8. 提交前 checklist

- [ ] `\todo` 与 `[Placeholder]` 全部清除
- [ ] `references.bib` 所有 `note = {TODO}` 已填充
- [ ] 9 页正文上限通过（用 `pdftotext` 验证）
- [ ] 双盲：搜索 author / institution 名，确保无泄漏
- [ ] 表格 `|` 检查：`grep -n '|' paper/black/sections/*.tex` 应当空
- [ ] `$$` 检查：`grep -n '\\\$\\\$' paper/black/sections/*.tex` 应当空
- [ ] 编译无 warning（除可控的 hbox / vbox）
- [ ] checklist.tex 全部回答完毕

---

> 当 CONVENTIONS.md 与 NeurIPS 官方排版有冲突时，以 NeurIPS 官方为准；本文件随时更新。
