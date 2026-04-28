# PLAN · W2 · 完成 §5 Method 实写

> 起草：2026-04-26（W2，session #N+2）
> 主控对应：`MISSION.md §本阶段任务`、`CLAUDE.md §角色扮演 / NeurIPS 排版规范 / 工作区目录约定`
> 角色：**Anima Anandkumar 教授**（项目级 CLAUDE.md 钦定）
> 目标章节：`paper/black/sections/05_method.tex`
> 状态：**Draft**（待用户确认 §6 后改 Final）
> 衔接：本步是 W2 session #N+1 的延续。前序 PLAN：`PLAN/W2_intro_relwork_plan.md`（intro / related / §6.1 已实写）

---

## 0 · 输入条件复盘（启动前对齐）

| 项 | 状态 | 备注 |
|---|---|---|
| §1 Introduction | ✓ 实写完毕（W2 #N+1） | (C1)(C2)(C3) 列表锚已就位 |
| §2 Related Work + Background | ✓ 实写完毕（W2 #N+1） | `eq:reverse-sde / eq:scalar-law` 锚已就位 |
| §6 Theory | ✓ §6.1 桥段 + 5 个 Thm statement，§6.2–§6.5 proof sketch 留 `\todo` | `\ref{thm:double-burgers / thm:stability / thm:improved-rate / thm:shock-location / thm:jko}` 链已就位 |
| §5 Method（**本步目标**） | 占位骨架已就 — 4 子节、4 displayed equation、1 表格 caption（全部 `\todo`） | 不动子节顺序，只填内容 |
| `macros/notation.tex` | 已就：`\sth, \Dth, \physvis, \amp, \Wass{1}, \BV, \TV, \Shockphys, \Shockscore, \Ldsm, \Lent, \Lbv, \Lburg, \Rent, \physsol, \initdat, \uth` | §5 需增补 `planned`：`\phisbg, \phissh, \jumpamp, \rhotphys, \physsolvis, \dShock, \unat, \uhat, \muth, \errsc, \abs, \norm`（SYMBOL.md §12 已规划）|
| `references.bib` | 6 篇核心 PDF 封面已校验（W2 #N+1）；§5 还会用到 `karras2022edm, jko1998`（已存在）；可能用到 `kruzhkov1970, kuznetsov1976, shu1999weno, cockburn2001dg`（已存在） | 不需新增 entry |
| `Docs/proof/Theorem 3 revised.md` | A0–A6 假设体系完备 | 可作为 §5.2 / §5.3 写作时的内部参照（**不外泄到正文**） |
| `Docs/proof/Theorem 4 draft.md` | 含 4 引理 + Godunov 弱形式推导，从 §5.4 视角已成型 | 可作为 §5.4 内部参照 |
| `Docs/proof/Theorem 5 draft.md` | 第 1 部分：粒子 ODE → 连续性方程；尚未到 JKO 离散化 | §5 不依赖 §6.5 内容，影响小 |

---

## 1 · 本步任务边界（精确到文件级）

### 包含

| 操作 | 路径 | 说明 |
|---|---|---|
| 直接编辑 | `paper/black/sections/05_method.tex` | ≈2 页正文，4 子节 + 1 表格 + 1 算法环境（视决策）|
| 增补 | `paper/black/macros/notation.tex` | 落地 SYMBOL.md §12 的 11 个 `[planned]` 宏 |
| 同步 | `SYMBOL.md` | §15 变更日志 + §12 把 planned 标记移除 |
| 同步 | `Docs/path_A_method_skeleton.md §3.1` | 仅当 macros 名字与原表冲突时 |
| 状态刷新 | `REPORT.md §2.3 / §3.2`、`MEMORY.md §B/C`  | 完成后强制更新 |

### 不包含（推迟）

- ❌ §6 Theory 5 个 proof sketch 段（W3 任务）
- ❌ §7 Experiments / §8 Conclusion（W3 / W4）
- ❌ 附录 A1/A2/A3（W4 + Theorem 3 完整证明迁入）
- ❌ 本地 LaTeX 编译（CLAUDE.md：用户 Overleaf）
- ❌ 自动合并 main
- ❌ 实装 PROJECT/black/ 下任何核心代码
- ❌ 触碰 `Docs/proof/`（用户独立产物）

---

## 2 · 写作风格基线（Anandkumar）

1. **理论先行**：每个子节首句锁定 mathematical lever，不停留在工程动机
2. **卖点显式**：每个子节给一个 displayed equation 作"锚点公式"，并在公式前后各一句"为何写它 / 它说明什么"（CONVENTIONS.md §6）
3. **限定词诚实**：用 *under standard regularity* / *in the entropy-distribution sense* / *empirically observed*；禁 "always" / "guarantees" 滥用
4. **节制对比**：不诋毁 DiffusionPDE / FunDPS；用 *"is ill-defined across discontinuities"* / *"sidesteps the inviscid limit"* 等中性诊断
5. **引用风格**：natbib，`\citet{}` 叙述式 / `\citep{}` 括号式；本组前作严第三人称
6. **每段 ≤ 8 行**（NeurIPS 视觉密度）；topic sentence 必须显式

---

## 3 · §5 Method 段落计划（≈2 页）

### 3.0 Overview 一段（视用户决策；当前推荐：**写**）

紧接 `\section{Method: EntroDiff}` 与 `\label{sec:method}`，写一段 4–5 行的 lead-in：

- **Topic**：把 §6.1 Theorem 1 的"双 Burgers 几何耦合"翻译为 4 个独立可训练的算法组件
- **Roadmap**：(i) viscosity-matched schedule (§\ref{sec:method:schedule}) → (ii) BV-aware parameterization (§\ref{sec:method:bv-aware}) → (iii) loss family (§\ref{sec:method:loss}) → (iv) Godunov-form sampler (§\ref{sec:method:sampler})
- **承上启下**：每一组件锚定 §6 哪一个 Theorem
- **承下启上**：4 个 component 缺一不可，组合在 §6.3 Theorem 3 给出 $\Wass{1} \le \mathcal O(\varepsilon^{1/2})$ 的可证明保障

### 3.1 §5.1 Viscosity-matched noise schedule（≈10 行 + 1 公式）

**论点链**：

1. **Motivation**：score-level Burgers `eq:score-burgers` 的有效黏性是 $g(\tau)^2/2$（VE-SDE 标准结论）；solution-level 物理 PDE `eq:scalar-law` 的黏性是 $\physvis$。Theorem 1 的几何耦合在两者**同阶**时最紧。
2. **Choice**：所以 EDM 默认 cosine / 多项式调度被替换为
   $$ \sigma^{2}(\tau) = 2\,\physvis\,\tau, \qquad \tau \in [0, T_{d}]. \quad (\text{eq:visc-matched}) $$
3. **What it says**：在此调度下，扩散时间 $\tau$ 与物理黏度 $\physvis$ 之间出现确定性等价关系（Cole–Hopf 视角）
4. **Pay-off**：把 Theorem 1 的耦合从 $\mathcal O(\sigma)$ 邻域升级为 $\mathcal O(\sqrt{\physvis \tau})$ 邻域；同时使 §6.4 Theorem 4 中的 R–H 速度匹配成为可能（speciation alignment）

**用宏**：`\physvis, \sigtau, \dtau`；引用 `\eqref{eq:score-burgers}`、`\ref{thm:double-burgers}`、`\ref{thm:shock-location}`。

**ref 锚**：保留 `eq:visc-matched`。

### 3.2 §5.2 BV-aware score parameterization（≈18 行 + 1 公式 + 架构插入图说明）⭐ 核心 novelty

**论点链**：

1. **Why this is the lever**：Score Shocks `Proposition 5.4` 给出真实 score 在界面层的精确 $\tanh$ 解析剖面（厚度 $\sim \sigma(\tau)$），而 baseline DSM 网络只能渐近恢复——这是 Score Shocks Theorem 6.3 的 $\exp(\amp T)$ 放大的根源
2. **Architectural prior**：把这个 $\tanh$ 形态 **hard-code** 进网络结构，分解为三个子网络
   $$ \sth(u, \tau) = \nabla \phisbg(u, \tau) + \frac{\jumpamp(u, \tau)}{2} \tanh\!\left( \frac{\phissh(u, \tau)}{2\,\sigtau^{2}} \right) \nabla \phissh(u, \tau). \quad (\text{eq:bv-aware}) $$
3. **Three子网络 roles**：
   - $\phisbg$：smooth background potential（小型 MLP / U-Net；与 baseline EDM 同型）
   - $\phissh$：signed-distance to shock manifold（zero on $\Shockscore(\tau)$；满足 $\abs{\nabla \phissh} = 1$）
   - $\jumpamp$：local jump amplitude（受 R–H 约束，由 §5.4 sampler 时刻匹配 Theorem 4 的 $u_L, u_R$）
4. **Theoretical pay-off**：(eq:bv-aware) 在界面层精确匹配 Score Shocks Prop. 5.4 的内部解，使 Theorem 3 的 Gronwall 常数从 $\amp = \sup_\tau \snr/2$ 退化为 $\mathcal O(1)$。组合 §5.3 的 $\TV$ 正则，可实现 Theorem 3 的 $\Wass{1} \le \mathcal O(\varepsilon^{1/2})$ 收敛率
5. **Engineering note**（短句）：1D 用 signed-distance head；2D 留作 future work / rebuttal

**用宏**：`\sth, \phisbg, \phissh, \jumpamp, \sigtau, \abs`；引用 `\citep[Proposition~5.4]{sarkar2026scoreshocks}`、`\citep[Theorem~6.3]{sarkar2026scoreshocks}`、`\ref{thm:improved-rate}`、`\ref{thm:shock-location}`。

**ref 锚**：保留 `eq:bv-aware`。

### 3.3 §5.3 Loss family（≈12 行 + 1 公式 + 1 表格）

**论点链**：

1. **Composite loss**：四项相加，每项打不同的理论靶
   $$ \mathcal L = \Ldsm + \lambda_{\mathrm{ent}}\,\Rent(\Dth) + \lambda_{\mathrm{BV}}\,\TV(\Dth) + \lambda_{\mathrm{Burg}}\,\norm{\dtau \sth + 2\,\sth \cdot \nabla_u \sth - \Lap_u \sth}^{2}. \quad (\text{eq:loss-final}) $$
2. **Per-term role**（用表格 `tab:loss-family`，4 行 × 3 列：Loss / Theoretical role / Empirical role）
   - $\Ldsm$：DSM 标准回归靶；提供采样基线
   - $\Rent$：Kruzhkov 熵选择子；保证 $\hat u$ 落在 admissible 弱解
   - $\TV(\Dth)$：把 Helly 紧致性带回扩散侧（Theorem 3 的 Aulets 阶段 4 直接调用）
   - $\norm{\cdot}^2$ Burg residual：把 $\sth$ 钉在 (eq:score-burgers) 流形上
3. **Pay-off**（一句）：$\TV(\Dth) + $ `eq:bv-aware` 共同保证 Theorem 3 的 BV 球假设 (A0)
4. **Caption Key take-away**：每个正则项对应一个独立的理论假设，缺一不可

**用宏**：`\Ldsm, \Lent, \Lbv, \Lburg, \Rent, \TV, \BV, \Dth, \dtau, \Lap, \norm, \sth`；引用 `\ref{thm:improved-rate}`。

**ref 锚**：保留 `eq:loss-final`、`tab:loss-family`。

**预设 lambda values**：本节不写具体值（属 hyper-param），用文本陈述权重不为零。

### 3.4 §5.4 Reverse-time sampler with Godunov-form guidance（≈14 行 + 1 公式 + 算法伪码视决策）

**论点链**：

1. **Setup**：从 EDM-style probability-flow ODE 出发，叠加 DPS-style guidance 项以匹配观测约束
2. **The structural difference**（与 DiffusionPDE 拉开距离的最强卖点）：DiffusionPDE 的 PDE-residual term 用 central differences 评估——但在 shock 处 central diff 是 ill-defined 的（discrete oscillation source）。我们改用 **Godunov flux** 评估 PDE residual：
   $$ \frac{du}{d\tau} = -\sigtau \dot\sigma(\tau)\,\sth(u, \tau) - \zeta_{\mathrm{obs}} \nabla_u \mathcal L_{\mathrm{obs}}(u) - \zeta_{\mathrm{PDE}} \nabla_u \Lpde^{\mathrm{Godunov}}(u). \quad (\text{eq:reverse-ode}) $$
3. **Why Godunov**（短论证）：Godunov flux 是 entropy-consistent monotone scheme（cf. \citep{shu1999weno, cockburn2001dg}）；它在 shock 处给出 **R–H-respecting** 的离散通量，与 Theorem 4 的 R–H + Lax 条件一致
4. **Discretisation**：Heun 二阶 ODE；$N_\tau$ 步默认 $N_\tau = 50$（具体值 → 附录 A3）
5. **Algorithm 1**（视用户决策；推荐写）：8–12 行伪码，输入 prior 噪声 $u_{T_d} \sim \mathcal N(0, \sigma^2(T_d) I)$，输出 sample $\uth = u_0$。每步显式：(a) network 调用得 $\sth$；(b) Godunov flux 评估 PDE residual；(c) Heun 平均；(d) σ 衰减。

**用宏**：`\sth, \sigtau, \dtau, \uth, \Lpde, \physvis`；引用 `\ref{thm:shock-location}`、`\citep{shu1999weno, cockburn2001dg}`。

**ref 锚**：保留 `eq:reverse-ode`、`alg:reverse-sampler`（视决策）。

---

## 4 · §5 ↔ §6 ↔ §1 Contribution 对接表

| Contribution | §1 锚 | §5 实现 | §6 理论 |
|---|---|---|---|
| (C1) Double-Burgers coupling | (C1) itemize | §5.1 调度让两 Burgers 同 viscous profile | §6.1 Thm 1（已写桥段）|
| (C2) BV-aware score parameterization | (C2) itemize | §5.2 hard-code tanh + 三子网络 | §6.3 Thm 3 的可证关键 step |
| (C3) Improved $\Wass{1} \le \mathcal O(\varepsilon^{1/2})$ | (C3) itemize | §5.2 + §5.3 (BV 正则) + §5.4 (Godunov R-H) | §6.3 Thm 3（statement 已写）|

§5 不直接证 (C3)，但**所有结构性必需条件**（A0 BV 球 / A1 完美匹配 in 界面 / A6 R-H 速度匹配）都由 §5 各组件落地。Theorem 4 / 5 是"加法定理"，其 statement 已写好，proof sketch 在 W3 补。

---

## 5 · 待用户决策（**进入执行前用 AskUserQuestion 收齐**）

### Q1 · §5.0 Overview 段是否写？

- **A. 写**（推荐）：4–5 行 lead-in，提供"4 组件 → 4 Theorems"全貌；与用户选中的 EOF 论文 `Architectural decomposition` 段同型。代价：占 5 行版面，9 页正文还吃得消（intro+related = 1.5 页 / theory ≈ 2 页 / experiments + concl ≈ 2.5 页 / 余约 3 页给 method）
- **B. 不写**：直接进 §5.1。优点是省空间；缺点是读者要从 §5.1 一路读到 §5.4 才看到全貌

### Q2 · §5.4 Algorithm 1 伪码是否写？

- **A. 写**（推荐）：8–12 行 algorithmic 环境，明确 Heun + Godunov 的耦合方式。这是 NeurIPS 论文的强习惯，且让 reviewer 一眼看到 Godunov 在哪里调用、与 DiffusionPDE 的差异点
- **B. 不写**：仅文字 + 一个公式描述。优点：省 ~10 行；缺点：与 DiffusionPDE 的差异点会显得"含糊"，丢卖点

### Q3 · §5.4 Godunov flux 是否在本步实写细节？

> 来自 REPORT.md §7.4：用户曾留口"是否真引入 Godunov flux 替代 central diff，还是 W3 优先省事用 central diff + η-reg，把 Godunov 留到实验阶段"

- **A. 实写 Godunov**（推荐）：与 §6.4 Thm 4 R–H/Lax 严格一致；论文卖点最大。代价：附录 A3 要写 Godunov 实装细节（W4 任务，本步不写）
- **B. 用 central diff + η-regularization**：写作压力小；卖点削弱（reviewer 易问"shock 处 ill-defined 怎么办"）

---

## 6 · 操作顺序

```
(1)  写本 PLAN（已完成 → 现在）
(2)  AskUserQuestion 收齐 Q1 / Q2 / Q3
(3)  从 main 创建子分支：paper/method-impl-20260426
(4)  commit 1 (docs)：PLAN/W2_method_plan.md
(5)  补 macros/notation.tex 的 11 个 planned 宏 → commit 2 (paper)
(6)  实写 §5.0 Overview（如 Q1=A）→ commit 3 (paper) — 可与 §5.1 合并
(7)  实写 §5.1 Viscosity-matched schedule → commit 3-4 (paper)
(8)  实写 §5.2 BV-aware parameterization → commit 5 (paper)
(9)  实写 §5.3 Loss family → commit 6 (paper)
(10) 实写 §5.4 Sampler + （视决策）Algorithm 1 → commit 7 (paper)
(11) self-check：grep $$ / \cite{ / 表格 | / \todo 残留 → 修
(12) 同步 SYMBOL.md §15 变更日志 → commit 8 (docs)
(13) 同步 REPORT §2.3 / §3.2 + MEMORY §B/C → commit 9 (docs)
(14) 报告：分支变更摘要 + dry-run merge 结果，等用户审批
```

每步原子 commit；commit message 格式：`{paper|docs|chore}({模块}): {做了什么}`，禁"完成"。

---

## 7 · 风险与对策

| ID | 风险 | 对策 |
|---|---|---|
| W2M-R1 | §5 写过长（>2 页） | 严控每子节行数；表格用 `[t]` 顶置；4 个 displayed equation 是上限 |
| W2M-R2 | 公式锚 `eq:bv-aware / eq:loss-final / eq:reverse-ode / eq:visc-matched` 与 §6 引用断链 | 全部沿用 `05_method.tex` 当前占位 label，不改名 |
| W2M-R3 | Theorem 3 / 4 的 proof 内部细节误进入 §5 | 严控所有 ref 走 statement 层；`\ref{thm:*}`，禁复述证明步骤 |
| W2M-R4 | 双盲：误用 "we [as the authors of FunDPS]" | 引 FunDPS 强制 `\citet{yao2025fundps}` 第三人称 |
| W2M-R5 | macros 漂移：notation.tex 增宏没同步 SYMBOL.md | 一处改三处同步：notation.tex / SYMBOL.md §12 / path_A_skeleton §3.1 |
| W2M-R6 | "完成"声明过早（违反 R8） | commit message 用动词性描述；REPORT 进度严格按真实状态（"replace placeholder with prose"，不写"finish"）|
| W2M-R7 | 表格用 `\|` 垂直线 | 提交前 `grep -n '\|' paper/black/sections/05_method.tex` 应空 |
| W2M-R8 | Algorithm 环境与 NeurIPS 排版冲突 | 用 `algorithm` + `algorithmic`（neurips_2026.sty 已 load `algorithm`）|

---

## 8 · 提交前 self-check（CONVENTIONS.md §8 子集）

- [ ] `grep -n '\$\$' paper/black/sections/05_method.tex` 必空
- [ ] `grep -n '\\cite{' paper/black/sections/05_method.tex` 必空（禁裸 `\cite`）
- [ ] `grep -n '\\todo' paper/black/sections/05_method.tex` 仅留外文档可显式认领的 `\todo`，否则空
- [ ] `grep -n '|' paper/black/sections/05_method.tex` 应空（表格内禁垂直线）
- [ ] `grep -nE 's_\\theta|\\nu_\\\{?\\mathrm\\\{phys' paper/black/sections/05_method.tex` 应空（裸符号检查）
- [ ] 章节首句必须 topic sentence
- [ ] 每段 ≤ 8 行
- [ ] 双盲：搜 "we propose" / 我组前作不经 \citet 直接称我

---

## 9 · 不做的事（边界保护）

- ❌ 写 markdown 草稿后再迁 LaTeX（用户明确：tex 直接写）
- ❌ 触碰 §6 / §7 / §8 / 附录 实写内容（除 ref 锚解析）
- ❌ 修改 PROJECT/black/ 下任何文件
- ❌ 本地 latexmk / pdflatex
- ❌ 自动合并 main
- ❌ 触碰 `Docs/proof/`、`copilot/`（用户独立产物）
- ❌ 把用户在 main 上 dirty 的元数据（CLAUDE/MEMORY/MISSION/REPORT/Theorem 系列）纳入我的 commit；只精确 `git add` 我修改的文件

---

## 10 · 用户决策（待 AskUserQuestion 后填）

> 决策一旦收齐，本节会落到 Final，并把 §5 决策的预选 (A/B) 改为定值。
