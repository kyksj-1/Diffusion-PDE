# PLAN · W2 · 完成 Introduction 与 Related Work

> 起草：2026-04-26（W2，session #N+1）
> 主控对应：`MISSION.md §本阶段任务（W2）`、`CLAUDE.md §角色扮演 / NeurIPS 排版规范 / 工作区目录约定`
> 角色：**Anima Anandkumar 教授**（项目级 CLAUDE.md 钦定）
> 目标章节：`paper/black/sections/01_intro.tex`、`paper/black/sections/02_related_work.tex`
> 状态：**Final**（用户决策于 2026-04-26 晚收齐，见 §11）

---

## 1 · 本步任务边界（精确到文件级）

### 包含

| 操作 | 路径 | 说明 |
|---|---|---|
| 新建 | `SYMBOL.md` | MISSION 强制：本轮开始时建立全文符号 master sheet |
| 直接编辑 | `paper/black/sections/01_intro.tex` | ≈1 页正文，三段式 Gap / Insight / Contribution + `(C1)(C2)(C3)` 列表 |
| 直接编辑 | `paper/black/sections/02_related_work.tex` | ≈0.5 页，四组 (a)(b)(c)(d) |
| 增补 | `paper/black/references.bib` | 仅当 intro/related 引入新 key |
| 增补 | `paper/black/macros/notation.tex` | 仅当确认要落地新符号 |
| 同步 | `Docs/path_A_method_skeleton.md §3.1` | 与 macros 同步 |
| 状态刷新 | `REPORT.md §2.6 / 3.2`、`MEMORY.md §B/C` | 完成后强制更新 |

### 不包含（推迟）

- ❌ `03_preliminaries.tex / 04_double_burgers.tex / 05_method.tex / 06_theory.tex / 07_experiments.tex / 08_conclusion.tex` 的实写
- ❌ 任何附录（`A1_proofs / A2_extra_experiments / A3_implementation_details`）
- ❌ `\todo{}` 占位的总体清理（只清本次写过的两节内的）
- ❌ 本地 LaTeX 编译（CLAUDE.md：用户 Overleaf 编译）
- ❌ 自动合并 `main`
- ❌ 实装 PROJECT/ 下任何核心代码

---

## 2 · 写作风格基线

### 2.1 角色视角（项目 CLAUDE.md §角色扮演）

**Anima Anandkumar 教授**：
- 理论先行：intro 第一段就锚定 mathematical structure，不停留在工程动机
- 卖点显式：contribution 必须可数、可点单
- 节制对比：不诋毁 baseline；用"saturate"/"do not address"代替"fail"
- `\citet`/`\citep` 自然交错，不堆引

### 2.2 标杆参照（**写作前精读 intro/relwork 节奏**）

| 论文 | 用途 | 路径 |
|---|---|---|
| DiffusionPDE [Huang+24] | 直接对标 baseline，关于 PDE 的 intro 结构 | `EXAMPLE PAPERS/diffusion_pde_generative_solver.pdf` |
| FunDPS [Yao+25] | function-space 框架的 related work 范式 | `EXAMPLE PAPERS/guided_diffusion_function_spaces_pde.pdf` |
| Score Shocks [Sarkar 26] | 理论钥匙引用方式（intro / relwork 都要重引） | `EXAMPLE PAPERS/score_shocks_burgers_structure.pdf` |
| EDM [Karras+22] | VE-SDE 标准引法 | （已知 venue：NeurIPS 2022）|

### 2.3 NeurIPS 排版强制（CLAUDE.md / CONVENTIONS.md）

- 双盲：禁 `[final]` / `[preprint]`；引用本组前作严禁第一人称
- 公式：必须用 `equation` / `align`，禁 `$$...$$`
- 引用：`natbib` + `\citet{}`/`\citep{}`，禁 `\cite{}`
- 符号：必须经 `macros/notation.tex` 宏调用，禁直接写裸 LaTeX
- intro ≤ 1 页，related work ≤ 0.5 页（合计 ≤ 1.5 页 / 9 页正文）

---

## 3 · SYMBOL.md 规划（master sheet）

> 全文符号唯一来源。SYMBOL.md ←→ `macros/notation.tex` ←→ `Docs/path_A_method_skeleton.md §3.1` 三处同步。
> 颗粒度：**全文 master**（不局限本步用到的）。

### 3.1 设计原则

1. 一处定义、全文引用；不允许 sections 内出现裸 `W_1`、`s_\theta` 等
2. 与 `macros/notation.tex` 行号一一对应（同步表见 SYMBOL.md §映射）
3. 标注每个符号的"作用域"（哪一节首引）
4. `Theorem 3 revised.md` 中的细化符号（如 $u^\natural$ / $\hat u$ / $\mu_\theta$ / $d_\Gamma$）一并纳入

### 3.2 分块（草案）

- A. 数集 / 概率（`\R, \N, \E, \Prob, \Law`）
- B. 概率距离 / 测度论（`\Wass{p}, \KL, \Ent, \TV, \BV, \Lip`）
- C. 扩散模型时间轴（$\tau \in [0, T_d]$, $\sigma(\tau)$, $G_\tau$, $p_\tau$, $\rho_t$, $\rho^\star$）
- D. 扩散模型 score（$s_\tau, \sth, D_\theta, e = \sth - s$）
- E. PDE 物理时间轴（$x \in \Omega$, $t \in [0, T]$, $f(u)$, $\dt, \dx, \physvis$, $\mathbf{u}^\star, \mathbf{u}^\nu$）
- F. 几何对象（$\Sigma_{\mathrm{phys}}, \Sigma_{\mathrm{score}}, d_\Gamma$）
- G. 训练误差与放大因子（$\varepsilon, \Lambda, \mathrm{SNR}$）
- H. 损失（$\Ldsm, \Lent, \Lbv, \Lburg, \Rent$ + 总 $\mathcal L$ 与 $\lambda_*$ 系数）
- I. BV-aware 参数化（$\phi^{\mathrm{sm}}_\theta, \phi^{\mathrm{sh}}_\theta, \kappa_\theta$）
- J. 轨迹（$u^\natural(\tau), \hat u(\tau), u^\theta = \hat u(0), \mu_\theta = \Law(u^\theta)$）

### 3.3 与 `Theorem 3 revised.md` 的对齐

`Docs/proof/Theorem 3 revised.md` 已用更细的符号（$u^\natural$ vs $\hat u$，$\Sigma$ 用 $\Gamma$）。本规划**采纳论文版主流**：
- 论文正文用 `\sth, \Dth, \score, \Sigma_{\mathrm{phys}}, \Sigma_{\mathrm{score}}` 等已有宏
- 附录 A1（Theorem 3 完整证明）保留 `Theorem 3 revised.md` 引入的细化符号 $u^\natural, \hat u, d_\Gamma$
- 在 SYMBOL.md 中注明"正文 / 附录 A1"两套作用域，避免冲突

### 3.4 本步实际新增符号（最小集）

预期 intro / related work 用到的全部为已有宏（`\score, \sth, \rhotrue, \physvis, \amp, \Wass{1}, \BV, \Shockphys, \Shockscore`），**预计无需新增**。SYMBOL.md 仍按全文 master 规划写，作为后续章节的参照基准。

---

## 4 · `01_intro.tex` 段落计划（≈1 页）

### §1.1 GAP（约 10–12 行）

**论点链**（topic sentence → 证据 → 结论）：

1. **Topic**：Generative diffusion models have become the dominant paradigm for solving PDEs in function space, but their successes concentrate on regimes where solutions remain smooth.
2. **State of the art**：DiffusionPDE [Huang+24] and FunDPS [Yao+25] achieve SOTA on Darcy / Helmholtz / viscous Navier–Stokes.
3. **Concrete miss**：DiffusionPDE 的 Burgers 实验取 $\physvis = 10^{-2}$（绕开 inviscid limit）；FunDPS 五个 benchmark 中无双曲。
4. **Theoretical miss**：现有 $W_2$/TV/$L^2$ 收敛分析（[Chen+23, Benton+24] 类）未涵盖 weak solution / shock。
5. **Bridge**：The shock regime is therefore both an empirical and a theoretical blind spot.

**引用**：`\citep{huang2024diffusionpde, yao2025fundps}`；可选用 `\citep{kruzhkov1970}` 锚定 weak solution 概念。

### §1.2 INSIGHT（约 10–12 行）

**论点链**：

1. **Topic**：A recent identity changes the landscape: the score field of a VE-SDE diffusion model itself satisfies a viscous Burgers equation in diffusion time.
2. **方程**：写出 (★) `\partial_\tau \score + 2\,\score \cdot \nabla \score = \Delta \score`（带 `\eqref` 锚到 §4 的 `eq:score-burgers`，**或者**在 intro 直接显式）
   → 决策：**intro 不重复方程，仅文字描述 + 指 §\ref{sec:double-burgers}**（保 1 页限）
3. **Double-Burgers picture**：the target hyperbolic conservation law is itself a Burgers-type structure on $(x,t)$; the score satisfies a Burgers structure on $(u, \tau)$. The two are *coupled* through the shock-set correspondence $\Shockphys \leftrightarrow \Shockscore$.
4. **Lever**：This coupling is not just a curiosity—it is the structural lever that lets us turn shock geometry into an architectural prior and into a sharp convergence rate.

**引用**：`\citep{sarkar2026scoreshocks}`（理论钥匙）；`\citep{karras2022edm}`（VE-SDE 锚）；可选 `\citep{pdeperspective2025}`。

### §1.3 CONTRIBUTION（5–7 行 + 三 item 列表）

**桥段一句**：We turn this observation into both an algorithm and a theoretical guarantee.

**列表 item**（与 sections/01_intro.tex 已有占位锚一致）：

- **(C1) Double-Burgers coupling (Theorem~\ref{thm:double-burgers})**：we formalize the geometric correspondence between $\Shockphys(t)$ and $\Shockscore(\tau)$ as a coupled Burgers system, giving a structural foundation for the rest of the paper.
- **(C2) BV-aware score parameterization (§\ref{sec:method})**：we embed the exact $\tanh$ interfacial profile of [Score Shocks Prop. 5.4] into the network, decomposing $\sth$ into a smooth potential plus a shock layer. This severs the $\exp(\amp T)$ amplification source identified by [Score Shocks Thm. 6.3].
- **(C3) Improved Wasserstein rate $\Wass{1} \le \mathcal O(\varepsilon^{1/2})$ (Theorem~\ref{thm:improved-rate})**：under (C2) and a BV regularizer, we prove the generated distribution converges to the Kruzhkov entropy solution at rate $\varepsilon^{1/2}$, with constants independent of $\amp$.

**收口一句**：We empirically validate (C1)–(C3) on inviscid Burgers, Buckley–Leverett, and 1D Euler/Sod (§\ref{sec:experiments}).

---

## 5 · `02_related_work.tex` 段落计划（≈0.5 页）

四组每组一个 paragraph。

### (a) Function-space diffusion solvers（≈4–5 行）

- 列：DDO [Lim+23]、DiffusionPDE [Huang+24]、FunDPS [Yao+25]
- ack：Banach-space framework，PDE-residual guidance，SOTA on smooth regimes
- gap：do not address shock-containing hyperbolic PDEs; their PDE-residual term is undefined across discontinuities
- 我们的位置：interfacial-aware structural prior + Kruzhkov-consistent guidance

### (b) Flow matching for PDE / function spaces（≈3–4 行）

- 列：Stochastic Interpolants [Albergo+24]、Functional Mean Flow [Kerrigan+24]、CFO [2025]、UniFluids [2025]
- ack：alternative generative paradigm over function spaces
- 我们的位置：orthogonal — these works vary the *generative dynamics*; we keep VE-SDE and instead exploit its *Burgers structure*

### (c) PDE perspective on diffusion（≈3–4 行）

- 列：Score Shocks [Sarkar 26]（理论钥匙）、PDE perspective on diffusion [2025]
- ack：identifies that diffusion-model dynamics correspond to PDE flows
- 我们的位置：**identify → leverage**: turn the score-Burgers identity into both an architectural prior (C2) and a sharp convergence rate (C3)

### (d) Hyperbolic conservation laws (numerics)（≈2–3 行）

- 列：Kruzhkov [70]、Kuznetsov [76]、WENO5 [Shu]、DG [Cockburn-Shu+01]、JKO [98]
- 用法：仅作 ground-truth generator + 在 entropy-solution 意义下作 comparator
- 不做 baseline 对比（neural method 才比较）

---

## 6 · 待用户决策（**进入执行前必须先 AskUserQuestion**）

### Q1（关键）· 章节结构调整的时机

> MISSION 写："03 Preliminaries 和 04 Double-Burgers 不要单独开一个 section，部分内容合并到 02 部分内容合并到 Theory 部分"

但本步任务又限定为"完成 introduction 和 related work 的写作"。两者的优先级关系不明：

- **A. 推迟（推荐）**：本步只写 01/02。`03/04` 的 `\label{}` 锚原位保留，intro 中的 `\ref{thm:double-burgers}` 等照旧，下一步专门做结构重构。
  - 优点：ref 链不断，本步可以最快交付，符合 MISSION "本步=intro+relwork"
  - 缺点：保留临时占位多 1 周
- **B. 同步重构**：本步在写 01/02 的同时完成 03/04 的合并。`thm:double-burgers` 转移到 06 Theory 开头；prelim 的核心 Setting 写入 02 末尾或新建一个 §3 "Background & Setup"。
  - 优点：一步到位
  - 缺点：本步工作量翻倍；intro 引用锚需要重定位；与 MISSION "这一步=intro+relwork" 字面冲突

### Q2（次要）· 章节最终结构（无论本步是否动手，写 intro 时都要心里有谱）

候选三种：

- **方案 X**（保守）：1.Intro / 2.Related / 3.Prelim / 4.Double-Burgers / 5.Method / 6.Theory / 7.Exp / 8.Concl（**当前结构**）
- **方案 Y**（最忠实于 MISSION 字面）：1.Intro / 2.Related Work + Notation 段 / 3.Method（含 Double-Burgers Setup 子节）/ 4.Theory（含 Thm 1）/ 5.Exp / 6.Concl
- **方案 Z**（NeurIPS 顶会最常见）：1.Intro / 2.Related / 3.Background & Double-Burgers / 4.Method / 5.Theory / 6.Exp / 7.Concl

### Q3（轻量）· `\citep{...}` 暂用占位的容忍度

- references.bib 中 `huang2024diffusionpde / yao2025fundps / sarkar2026scoreshocks / cfo2025 / unifluids2025 / pdeperspective2025` 等 6 项的 `author = {TODO}` 暂时**不补**？还是顺手从 EXAMPLE PAPERS 抄过来？
  - 默认：**暂不补**（不属于本步主线，提交前 W11 统一抄）。

---

## 7 · 操作顺序（用户确认 §6 后启动）

```
(0)  写本 PLAN（已完成）
(1)  AskUserQuestion 确认 §6 决策
(2)  创建子分支：paper/intro-relwork-20260426（基于 main）
(3)  起草 SYMBOL.md（master sheet）→ commit
(4)  扫读 DiffusionPDE / FunDPS 的 intro 节奏（pdf-vision 各取前 3 页）
(5)  写 01_intro.tex → commit
(6)  写 02_related_work.tex → commit
(7)  同步 references.bib（如需）→ commit
(8)  同步 macros/notation.tex（如需）→ commit
(9)  同步 Docs/path_A_method_skeleton.md §3.1（如符号变化）→ commit
(10) 更新 REPORT.md §2.6/3.2 + MEMORY.md §B/C → commit
(11) 报告用户：分支变更摘要 + 是否合并 main（人工审批）
```

每步对应一个原子 commit；commit message 格式：`{paper|docs|chore}({模块}): {做了什么}`，不写"完成"。

---

## 8 · 风险与对策

| ID | 风险 | 对策 |
|---|---|---|
| W2-R1 | intro 写过长（>1 页） | 严控三段；contribution 列表用 itemize 紧凑式；不重复 §4/§5/§6 的内容 |
| W2-R2 | related work 堆砌作者名导致碎片化 | 每组一个连贯段落，作者名只在 `\citet{}` 时显式出现 |
| W2-R3 | references.bib `note = {TODO}` 残留 | 本步不强行补；`\todo`/`[Placeholder]` 在最终提交前 W11 统一清 |
| W2-R4 | SYMBOL.md 与 macros/notation.tex 漂移 | 一处改三处同步：SYMBOL.md / notation.tex / path_A_skeleton §3.1 |
| W2-R5 | "完成"声明过早（违反 R8） | commit message 用动词性描述，REPORT 进度严格按真实状态 |
| W2-R6 | intro 内嵌方程超出 1 页 | (★) 不在 intro 显式写，仅 ref 到 §4 `eq:score-burgers` |

---

## 9 · 提交前 self-check（CONVENTIONS.md §8 子集）

- [ ] `grep -n '\\\$\\\$' paper/black/sections/0[12]_*.tex` 必空
- [ ] `grep -n '\\\\cite{' paper/black/sections/0[12]_*.tex` 必空（禁裸 `\cite`）
- [ ] `grep -n '\\\\todo' paper/black/sections/0[12]_*.tex` 列出剩余 todo（可有，但要明确）
- [ ] 章节首句必须是 topic sentence
- [ ] 每段 < 8 行（NeurIPS 视觉密度）
- [ ] 双盲：搜索 "Anonymous" 与作者名残留

---

## 10 · 不做的事（边界保护）

- ❌ 写 markdown 草稿后再迁 LaTeX（用户明确：tex 直接写）
- ❌ 触碰 05/07/08 的实写内容（除 ref 锚修复）
- ❌ 修改 PROJECT/black/ 下任何文件
- ❌ 本地 latexmk / pdflatex
- ❌ 自动合并 main
- ❌ 写新讲义（CLAUDE.md / MEMORY.md G.2 明令）
- ❌ 触碰 `Docs/proof/`、`copilot/`（用户独立产物）
- ❌ 把用户在 main 上 dirty 的元数据（CLAUDE/MEMORY/MISSION/REPORT/Theorem 3 系列）纳入我的 commit；只精确 `git add` 我修改的文件

---

## 11 · 用户决策（确认 · 2026-04-26 晚）

### Q1 = C（同步重构 + 写桥段骨架）

**本步实际范围**（覆盖 §1 / §7 草案）：

新增 / 修改文件：
- `SYMBOL.md`（新建，全文 master sheet）
- `paper/black/sections/01_intro.tex`（实写三段 + (C1)(C2)(C3) 列表）
- `paper/black/sections/02_related_work.tex` → 重命名章节为 **"Related Work and Background"**，写 4 组 + 末尾一段 minimal notation/setup
- `paper/black/sections/06_theory.tex` → 在文件顶部插入 **§6.0 Double-Burgers Coupling**（实写桥段 ~10 行 + `\begin{theorem}[Double-Burgers coupling] ... \end{theorem}` 的 statement，proof sketch 留 `\todo`）
- `paper/black/neurips_2026.tex`（删除两行 `\input{sections/03_preliminaries.tex}` 与 `\input{sections/04_double_burgers.tex}`）
- `paper/black/references.bib`（补 6 篇 PDF 封面信息）
- `paper/black/macros/notation.tex`（如出现 SYMBOL.md 新增符号则同步）
- `Docs/path_A_method_skeleton.md §3.1`（如符号变化则同步）

删除文件：
- `paper/black/sections/03_preliminaries.tex`
- `paper/black/sections/04_double_burgers.tex`

`\label{}` 处理：
- `eq:scalar-law`（原 03 prelim §3.2）→ 转移到 02 末尾的 background 段
- `eq:reverse-sde`（原 03 prelim §3.1）→ 同上转移到 02
- `eq:score-burgers`（原 04）→ 转移到 06.0 Double-Burgers Coupling 段
- `thm:double-burgers`（原 04）→ 转移到 06.0 段（保 ref 链）

### Q2 = 顺手补全

用 pdf-vision 读 6 篇 PDF 第 1 页（含作者列表、机构、venue、year），更新 `references.bib`：

| BibTeX key | EXAMPLE PAPERS 文件名 |
|---|---|
| huang2024diffusionpde | diffusion_pde_generative_solver.pdf |
| yao2025fundps | guided_diffusion_function_spaces_pde.pdf |
| sarkar2026scoreshocks | score_shocks_burgers_structure.pdf |
| albergo2024interpolants | stochastic_interpolants.pdf |
| cfo2025 / unifluids2025 | flow_matching_operators_residual_augmented.pdf（实际是哪一篇待 PDF 确认）|
| pdeperspective2025 | （EXAMPLE PAPERS 中可能未含；fallback 保留 TODO） |

### 修订后操作顺序

```
(1)  更新 PLAN 为 final（已完成）
(2)  创建分支：paper/intro-relwork-restruct-20260426
(3)  起草 SYMBOL.md → commit
(4)  pdf-vision 批量读 6 篇 PDF 封面
(5)  更新 references.bib → commit
(6)  重构：删 03/04 + 改 neurips_2026.tex \input → commit
(7)  写 02_related_work.tex（4 组 + notation/setup 段）→ commit
(8)  写 06_theory.tex §6.0 Double-Burgers Coupling 桥段 → commit
(9)  写 01_intro.tex（三段 + 列表）→ commit
(10) 如有新符号：同步 macros/notation.tex + path_A_skeleton §3.1 → commit
(11) self-check: grep `$$` / `\cite{` / `\todo` 分布
(12) 更新 REPORT.md §2/3 + MEMORY.md §B/C → commit
(13) 报告用户：分支变更摘要 + 是否合并 main（人工审批）
```
