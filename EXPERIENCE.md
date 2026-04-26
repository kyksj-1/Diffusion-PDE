# EXPERIENCE.md · 跨 session 可复用工具与模式

> **阅读对象**：跨 session 的 AI（不是每次会话都更新；只记录"值得别的 agent 复用"的）。
> **首版**：2026-04-26（W2，session #N+1 收）。

---

## 1 · `AskUserQuestion` 用 ASCII preview 对比候选架构

**触发场景**：任务存在多个可行的实施路径（重构方案 / 引擎选型 / 章节结构 / API 设计），用户单看文字描述难以选。

**模式**：

- 在 `options[].preview` 字段写**多行 ASCII** 把每个方案的关键产物可视化（章节列表、目录结构、API shape）。`preview` 仅在单选模式下生效。
- 末尾用 1–2 行总结 trade-off（"工作量 1.8×；ref 锚全部稳定"等）。
- 推荐选项标 `(Recommended)` 后缀，但**不**预设答案——用户经常选非推荐项。

**示例**（本仓库 W2 session）：3 个章节重构方案的 ASCII 章节树对比，让用户立即看清"删 03/04 后 main body 变成什么样"，避免反复来回澄清。

---

## 2 · `pdf-vision` 批量校验 BibTeX 封面页

**触发场景**：补 `references.bib` 中带 `note = {TODO}` 的占位条目（author / venue / year）。

**模式**：

```text
load_pdf  →  load_pdf  →  ...  (并行 N 个 sessionId)
        ↓
get_current_page (默认 page 1, 即封面)  ×N  (并行)
        ↓
读图：作者列表 / 机构 / venue / arXiv id / 投稿年份
        ↓
patch references.bib
```

**实战要点**：

- `load_pdf` 一次性返回页数 + sessionId，不消耗 image token；只有 `get_current_page` 才返回 image。所以 N 个 PDF 的 load 几乎零成本，可以全部并行。
- `get_current_page` 默认是 page 1 = 封面页；不需要先 `go_to_page(1)`。
- 对 `arXiv 2YYY` 类年份，注意：**arXiv post date** 与 **venue 年份**可能不同。例如 `stochastic_interpolants.pdf` 的 arXiv 是 2303，但 JMLR 26 (2025) 出版，应取 2025 作为 BibTeX year。
- 不要在 `pdf-vision` session 上多取页：每页都是 image，token 量大。封面 + （可选）intro 第 1 页就够。

**反模式**：用 `WebFetch` 去 arXiv 抓 abstract——慢、风险大、不如本地 PDF 直读。

---

## 3 · 在 dirty working tree 上创建子分支并精确 staging

**触发场景**：用户在 `main` 上有未 commit 的修改（元数据微调、独立产物），但 AI 需要在干净分支上做新任务。

**模式**：

1. `git checkout -b <new-branch>`：在 dirty 状态下也合法；working tree 跟随。
2. 后续 commit 时**禁用 `git add -A` / `git add .`**；改用具体文件名：`git add path/to/my/file.tex`。这样用户 dirty 文件不会进入我的 commit。
3. 在最终汇报时主动声明："用户 main 上还有 X / Y / Z 的 dirty 改动，未纳入本分支"。

**陷阱**：

- 当本任务必须 patch 一个**用户也 dirty** 的文件（如 `REPORT.md / MEMORY.md`），AI 的 commit 会**连带把用户的 dirty 改动一起 commit**。这时要在 commit message 里诚实标注"包含用户先前 formatting 微调"。
- Windows 上的 `LF will be replaced by CRLF` 警告可忽略：仓库默认 LF（CLAUDE.md），autocrlf 在 working tree 转换不影响 HEAD。

---

## 4 · 论文符号三处同步规则

**触发场景**：每次写一个新 section、引入新数学符号时。

**同步链**：

```
SYMBOL.md (master)  ←→  paper/black/macros/notation.tex  ←→  Docs/path_A_method_skeleton.md §3.1
   (实操字典)              (LaTeX 宏定义)                     (高层快照)
```

**规则**：

- **SYMBOL.md 是唯一权威**（CONVENTIONS.md §3 与 SYMBOL.md §13 都这么说）。
- 新增宏的标准流程：
  1. 在 SYMBOL.md 对应 block 加一行，标 `[planned]`；
  2. 当某 section 实际首次用到时，把宏加到 `notation.tex`，把 `[planned]` 改成已定义；
  3. **同一个 commit** 一并修改 SYMBOL.md + notation.tex，避免漂移。
- `path_A_method_skeleton.md §3.1` 是高层骨架，原则上不必每次同步；只在重大符号变更（更名 / 删除）时手动对齐。

---

## 5 · NeurIPS 双盲与 `\citet` postnote 用法

**触发场景**：写论文中需要精确指向 baseline 的某个 Theorem / Proposition。

**正确模式**：

```latex
\citet[Proposition~5.4]{sarkar2026scoreshocks}
% 渲染：Sarkar (2026, Proposition 5.4)

\citep[Proposition~5.4][]{sarkar2026scoreshocks}
% 渲染：(Sarkar, 2026, Proposition 5.4)
```

**反模式**：

```latex
[\citet{sarkar2026scoreshocks}, Proposition~5.4]
% 渲染：[Sarkar (2026), Proposition 5.4]  — 双层括号丑
```

**双盲注意**：

- 引用本组前作（如 FunDPS / Anandkumar et al.）时**仍然用 `\citet`**，不是 "Anonymous et al." —— 因为该论文已经发表、作者公开，与本投稿的匿名性互不冲突。CONVENTIONS.md 的"第三人称"指的是**叙述方式**（"the framework of \citet{yao2025fundps}"），而不是隐藏作者名。

---

## 6 · `\todo` 占位的 grep self-check

每次 commit 前跑一遍：

```bash
grep -nE '\$\$' paper/black/sections/*.tex     # 必空（comment 行不计；过滤 ^\s*%）
grep -nE '\\cite\{' paper/black/sections/*.tex  # 必空（用 \citet/\citep）
grep -cE '\\todo' paper/black/sections/*.tex    # 列出每文件 todo 数，最终投稿前必清零
```

`\$\$` 命中如果只在 `% comment` 行可忽略——LaTeX 不渲染 comment。
