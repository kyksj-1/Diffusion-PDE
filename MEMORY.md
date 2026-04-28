# MEMORY · 项目活档案（给 AI 看）

> **阅读对象 · AI**。给人看的进度报告在 `REPORT.md`；当前阶段指令在 `MISSION.md`；持续性协议在 `CLAUDE.md`。
> **维护节奏**：重大决策 / 里程碑 / 风险变化 / 阶段切换时更新；普通编辑不更新。

---

## A · 角色选择（首次 2026-04-26）

### A.1 当前角色：Anima Anandkumar 教授（Caltech / NVIDIA）

### A.2 选择理由（CLAUDE.md "角色扮演"要求"该人物真实存在并说明理由"）

1. **AI4PDE 这个术语的旗手**——她在 NVIDIA 主推的 "AI for Science" 路线把 AI4PDE 从学术兴趣点推成顶会标准方向
2. **实验室产出全覆盖**：FNO（NeurIPS 2021 spotlight）、PINO、GNO、Diffusion-FNO、CFO（flow-matching for PDE）—— 是当今 "diffusion / flow + PDE" 产线最完整的实验室
3. **写作风格符合 NeurIPS 评委偏好**：理论先行 → 设计精巧 → 实验干净 → 卖点包装清晰
4. **领域内权威性**：IEEE / ACM Fellow，Bren Professor，AI4Science 方向 Nature 子刊综述常作者
5. **路径 A 题材契合度**：她的组在 2024–2025 年发表的 DiffusionPDE / CFO / FunDPS 是直接对标的 baseline

### A.3 备选角色（仅在用户要求换角色时启用）

- George Em Karniadakis（Brown）—— PINN 鼻祖；偏 JCP / SISC 风格
- Weinan E（Princeton / 北大）—— Deep BSDE / 高维 PDE 奠基；理论极重
- Maziar Raissi（CU Boulder）—— PINN 通讯作者；普及性强

---

## B · 决策日志（按日期倒序）

### 2026-04-28（W3）· 论文前三节精修 + 定理附录完整迁入 LaTeX

- **本 session 任务**：用户 5 点指令——(1) 完善 §1/§2/§5 + 定理入附录，(2) NeurIPS 2026 格式，(3) 更新进度文档，(4) 继写 §6 Theory，(5) 已知证明在 `Docs/proof/`。
- **执行策略**：顺序执行（宏 → 精修 §1/§2 → 实写 §5 → 定理迁入 LaTeX → §6 proof sketch → 刷新文档），定理迁入用 3 个并行 sub-agent 同步完成。
- **产出**：
  1. `macros/notation.tex`：落地全部 11 个 `[planned]` 宏（`\physsolvis / \rhotphys / \errsc / \dShock / \phisbg / \phissh / \jumpamp / \unat / \uhat / \muth / \abs / \norm`）；同步 SYMBOL.md §12（删 `[planned]` 标记）+ §15 变更日志
  2. `01_intro.tex`：精修 GAP 段（补齐 central-diff 诊断）、Insight 段（精确 eq ref）、Contribution 列表换用 `T_{d}`
  3. `02_related_work.tex`：精修 VE-SDE prelim 段（补热方程 → Cole-Hopf 链）、全面使用 `\initdat / \physsol` 宏
  4. `05_method.tex`：完整实写 4 子节——§5.0 Overview（5 行 lead-in）、§5.1 Viscosity-matched schedule（10 行 + eq）、§5.2 BV-aware parameterization（18 行 + eq + 3 子网络说明）、§5.3 Loss family（12 行 + eq + Table 1 + \Rent 定义）、§5.4 Sampler（14 行 + eq:reverse-ode + Godunov flux + Algorithm 1）
  5. `A1_proofs.tex`：5 个 `proofs/thmN_proof.tex` 子文件全部从 `Docs/proof/` Markdown 迁入 LaTeX（Thm 1: 290 行 / Thm 2: 391 行 / Thm 3: 635 行 / Thm 4: 357 行 / Thm 5: 471 行），主控 `A1_proofs.tex` 完成 `\input` 编排
  6. `06_theory.tex`：5 个 proof sketch 段全部替换 `\todo`（每段 6–8 行思想线 + 附录 ref）
  7. `REPORT.md`：§1 摘要完成度更新（理论 85% / 论文 65%）、§2.3 刷新、§3.2 百分比全表更新、§4 下一步建议、§6 里程碑
  8. `PLAN/W3_sections_refine_plan.md`：新计划文档
- **未做**：§7/§8 仍占位；本地编译未跑（用户 Overleaf）；未合并分支
- **论文完成度**：从 ~24% 提升至 ~65%（§1/§2/§5/§6/A1 全部实写，仅 §7/§8/A2/A3 待写）

### 2026-04-26（W2 · session #N+1）· 首次进入论文实写

- **本 session 任务范式**：从"基础设施 + 文档"切换到 LaTeX 实写。MISSION 指令"完成 introduction 和 related work 的写作"。
- **用户决策（AskUserQuestion 收齐）**：
  - **Q1 = C**（同步重构方案 Y）：本步在写 01/02 的同时完成结构精简——删除 03_preliminaries.tex 与 04_double_burgers.tex 作独立 section；prelim 内容并入 §2.1 Background；double-Burgers structure 含 Thm 1 statement 实写为 §6.1。
  - **Q2 = 顺手补全**：用 `pdf-vision` 工具读 6 篇核心 PDF 封面，更新 `references.bib` 至接近 final。
- **产出（在 `paper/intro-relwork-restruct-20260426` 分支）**：7 个原子 commit
  1. `docs(plan)` PLAN/W2_intro_relwork_plan.md
  2. `docs(symbol)` 建立 SYMBOL.md 全文符号 master sheet（含 11 个 `[planned]` 宏）
  3. `paper(refs)` 校验 6 篇 PDF 封面 + 新增 bhola2025fmo / armegioiu2026
  4. `refactor(paper)` 删 03/04 + 改 neurips_2026.tex `\input`
  5. `paper(02)` 重写 §2 为 Related Work and Background（4 + 3 段）
  6. `paper(06)` 在 §6.1 实写 Double-Burgers Coupling 桥段 + Thm 1 statement
  7. `paper(01)` 实写 §1 Introduction（Gap / Insight / Contribution）
- **架构层面**：main body 由 8 sections 精简为 6（§1 / §2 / §5 / §6 / §7 / §8）。intro 中所有 `\ref` 锚已迁移到位。
- **未做**：`05_method.tex` / `07_experiments.tex` / `08_conclusion.tex` 仍占位；附录全部 `\todo`；本地未编译（用户 Overleaf）。

### 2026-04-27（W2 · session #N+2）· Theorem 2 严谨证明草稿完成

- **任务**：用户提供 Theorem 2 证明思路（~353 行），要求提取严谨化为 formal proof draft
- **产出**：`Docs/proof/Theorem 2 draft.md`（18 KB）
  - 完整 9 步证明：同步耦合 → 传播误差 → score 误差 → 期望 → 测度修复 → 合并不等式 → Cauchy–Schwarz → Gronwall → W₁ 上界
  - 5 条假设 (A1)–(A5)：score Lipschitz / schedule 有界 / 训练误差 L² / 分布稳定性（KR 对偶）/ 网络 Lipschitz
  - 关键技术步：**测度不一致修复**（Step 5）通过 Kantorovich–Rubinstein 控制将 `E_{\hat{u}}` 转为 `E_{u^♮}` + O(δ) 修正，闭合 Gronwall 循环
  - PDE Connection 节：Kruzhkov L¹-收缩性确保数值解误差不传播
  - 符号完全对齐 SYMBOL.md / notation.tex / 已有 Theorem 1 draft 格式
- **未做**：未迁入 LaTeX 附录（与 Thm 1/3/4/5 的迁入同步进行）；未本地编译
- **依赖**：需用户 review 确认假设 (A4)–(A5) 的表述与物理含义，以及 Gronwall 反向方向正确性

### 2026-04-26（晚）· 第二次重组：MISSION 瘦身 + 新增 REPORT

- **关键决策**：
  - 任务范式从"写讲义"切换到"**论文撰写 + 跑实验**"。L1–L8 旧讲义保留作 reference（迁到 `Docs/black/lectures/`）
  - **MISSION 瘦身**：只保留"当前阶段指令"（即写即用即换），持续性内容迁到 `CLAUDE.md`
  - **新增 `REPORT.md`**：给人看的诚实进度报告（"完成 / 未完成 / 阻塞"）。AI 的动作清单在本文件 / MISSION
  - 12 周时间表更新：W1 已完成（基础设施搭建），W2 起为"论文+实验"双线
  - **用户的 critique**：之前的"任务完成"声明 over-claim 了——骨架不等于完成。本次起所有进度叙述要对照 REPORT 的诚实状态

### 2026-04-26（白天）· 路径选定 + 工作区固化

- **决策**：路径 A（Shock-aware diffusion for hyperbolic PDEs，代号 EntroDiff）
- **目录约定 black/white**：默认 black/，仅讲解时 white/
- **NeurIPS 排版规范**固化（9 页、双盲、equation/align、booktabs、natbib）
- **5 commits 合并到 main**：MISSION（27590f9）/ MEMORY（730206a）/ CLAUDE（84639a4）/ paper（2df5ccc）/ PROJECT（d48c8e4）/ merge（a7a718a）
- **paper/2026_template/** 已存在官方 NeurIPS 2026 模板

### 2026-04-25 · 完成路径 A 的第一性原理解读

- 输出 `Docs/white/路径A_第一性原理解读.md`
- 输出 `Docs/black/path_A_method_skeleton.md`（论文骨架 / 5 大定理 / 12 周时间表）
- 输出 `Docs/used/idea_originality_analysis.md`（IDEA 原创性扫描）
- **用户已开始 Theorem 3 证明**：`Docs/proof/Theorem 3 draft.md`（符号统一 v2）+ `Docs/proof/Theorem 3 证明改进.md`（critique）

### 2026-04-21 · 项目初始化

- git init，commit 2099801
- 投稿方向锁定 NeurIPS / AI4S / AI4PDE / Diffusion Model
- 16 篇相关论文 PDF 备齐在 `EXAMPLE PAPERS/`

---

## C · 状态快照（每周 / 每阶段切换时刷新）

### C.1 当前阶段

- **周次**：W3（12 周时间表的第 3 周；W0–2 已完成）
- **本阶段主任务**：论文撰写 + 实验启动**双线**
- **本 session（W3）已完成**：§1/§2 精修；§5 Method 完整实写；§6 Theory proof sketch 全部实写；A1_proofs.tex 附录 5 大定理全部迁入；notation.tex 全部宏落地
- **下一里程碑**：(i) 用户 review Thm 3 证明完整性；(ii) §7 Experiments 实写；(iii) §8 Conclusion 实写

### C.2 已完成（详见 REPORT.md §2）

- 决策：路径 A 选定
- 文档：原创性分析、方法骨架、第一性原理解读
- 模板：NeurIPS 2026 官方模板
- 工作区：paper/black + PROJECT/black 双骨架
- 元数据：MISSION / CLAUDE / MEMORY 三件套；REPORT 体系
- 用户独立产出：Theorem 1/3/4/5 初稿 + Theorem 3 revised + critique（在 `Docs/proof/`）
- **W2 session #N+1（2026-04-26）**：SYMBOL.md / references.bib 校验 / §1 §2 §6.1 实写 / 结构精简
- **W2 session #N+2（2026-04-27）**：Theorem 2 严谨证明草稿（AI 产出）
- **W3（2026-04-28）**：
  - notation.tex 全部 11 个 `[planned]` 宏落地；SYMBOL.md 同步
  - §1/§2 精修（强化 GAP 诊断、符号统一、macro 对齐）
  - §5 Method 完整实写（4 子节 + Table + Algorithm 1）
  - A1_proofs.tex 5 大定理完整 LaTeX 证明（5 子文件 + 主控）
  - §6 Theory 5 段 proof sketch 全部实写
  - REPORT.md / MEMORY.md 全面刷新

### C.3 进行中

- 用户 review Thm 3 LaTeX 证明（`proofs/thm3_proof.tex`）← **关键瓶颈**

### C.4 阻塞中

- 暂无

### C.5 下一步（W3/W4 优先级）

1. **Thm 3 最终 review**：用户在 Overleaf 验证 `proofs/thm3_proof.tex` 的 6 阶段证明闭合性
2. **§7 Experiments 实写**：E1-E3 实验描述 + baseline 方法 + 指标
3. **§8 Conclusion 实写**：限制 + future work
4. **全文 `\todo` 清除**：grep 剩余 `\todo`，逐项处理

---

## D · 风险簿（来自 path_A_method_skeleton §7，定期复评）

| ID | 描述 | 概率 | 冲击 | 对策 | 状态 |
|---|---|---|---|---|---|
| R1 | Theorem 3 证不出，$\exp(\Lambda) \to \mathcal O(1)$ 退化论证不够 | 中 | **高** | 备用：退而求次证 $\exp(\Lambda/2)$，仍对 baseline 有改进。**用户已有 v2 草稿**，正在按 critique 修订 | 推进中 |
| R2 | BV-aware parameterization 在 2D 上工程难 implement | 中 | 中 | 先 1D 跑通；2D 用 mesh-based $\phi$ 替代 signed distance | 待 W6 验证 |
| R3 | DiffusionPDE / FunDPS 作者作 reviewer 挑实验 | 高 | 中 | 主实验直接用他们公开数据 + 代码作 baseline | 写作时落实 |
| R4 | Score Shocks 的 VP-VE 等价性假设在实模型不严格成立 | 低 | 中 | 论文声明只在 VE 设定下证明，VP 留 future work | 写作时落实 |
| R5 | 12 周紧，实验未必能跑出来 | 中 | 高 | E1+E2 必做（最小工作量），E3-E5 增量；理论章节做厚 | 监控中 |
| R6 | Reviewer 认为"只是 Score Shocks 的应用" | 中 | 中 | Intro 强调三大原创：Theorem 1 耦合 + Theorem 3 收敛率 + Theorem 5 JKO 桥梁 | 写作时落实 |
| R7 | 用户作为物理系学生，弱解 / OT / BV 数学工具不熟 | 中 | 中 | ~~L1-L5 讲义系列~~ 用户已**主动跳过**讲义阶段，直接进入论文+实验 | 解除 |
| **R8（新）** | **AI over-claim "任务完成"** | 中 | 中 | 所有进度叙述对照 REPORT.md 的诚实状态；commit 信息只描述"做了什么"不写"完成" | **监控中** |

---

## E · 关键检索索引（high-traffic 跳转）

| 想找... | 去这里 |
|---|---|
| 路径 A 完整方法骨架 / 5 大定理 / 12 周计划 | `Docs/black/path_A_method_skeleton.md` |
| Theorem 3 草稿 + critique | `Docs/proof/Theorem 3 draft.md`, `Docs/proof/Theorem 3 证明改进.md`（**待迁 `Docs/black/proofs/`**）|
| 旧 lecture L1–L8 | `Docs/black/lectures/` |
| 第一性原理拆解（讲给学生） | `Docs/white/路径A_第一性原理解读.md` |
| 原创性扫描 | `Docs/used/idea_originality_analysis.md` |
| NeurIPS 排版细节 | `paper/black/CONVENTIONS.md` + `CLAUDE.md §NeurIPS 排版规范` |
| LaTeX 主控 | `paper/black/neurips_2026.tex` |
| 论文符号宏 | `paper/black/macros/notation.tex` |
| 代码模块结构 | `PROJECT/black/README.md` |
| 多环境开发 | `Docs/black/多环境开发指南_从第一天就做对.md` |
| 16 篇相关论文 | `EXAMPLE PAPERS/` |
| 进度（给人看） | `REPORT.md` |

---

## F · 维护规则

### F.1 触发更新事件

| 事件 | 应更新 |
|---|---|
| 重大决策（路径切换 / 方法变更 / 投稿目标 / 角色切换）| §A、§B |
| 完成里程碑（讲义 / 定理 / 实验 / 章节初稿） | §C.2、§B；同步刷 REPORT |
| 风险新增 / 状态变化 | §D |
| 用户提出新偏好或约束 | §B + 视情况更新 MISSION / CLAUDE |
| 启动新阶段（每周 / 每两周） | §C |

### F.2 不写进 MEMORY 的事

- 普通文件编辑、bug 修复细节（git log 自带）
- 临时调试 / 探索（用 git stash 或临时分支）
- 一次性问答（用对话上下文即可）
- **进度数字 / 完成百分比** → 去 REPORT.md（给人看的）

### F.3 与其他文件分工

| 文件 | 主管什么 |
|---|---|
| `MISSION.md` | 当前阶段指令（即写即用即换） |
| `CLAUDE.md` | 持续性协议 |
| `MEMORY.md`（本文件） | AI 视角的决策 / 状态 / 风险 |
| `REPORT.md` | 人视角的诚实进度（完成 / 未完成 / 阻塞） |
| `EXPERIENCE.md` | 跨 session 的工具 / 模式经验（可被其他 agent 提取） |

---

## G · AI 行动 hints（加载 MEMORY 时的"应该如何继续"）

> 这是给 AI 的"读完 MEMORY 后该想什么"。每次加载本文件时按这些 hints 校准行为。

### G.1 当前应该有的态度

- **诚实记账**：不 over-claim 完成，commit message 用"做了什么"，REPORT 用诚实进度
- **理论优先**：Theorem 3 是论文命门；任何"实验进展"在它定稿前都是辅助
- **双线作战**：论文 / 代码可并行，但**不**牺牲理论换实验数量

### G.2 不要做

- ❌ 写新讲义（用户已决定跳过此阶段；旧讲义保留作 reference）
- ❌ 自动合并到 main（始终用户审批，CLAUDE.md §Git 工作流）
- ❌ 把 `Docs/proof/`、`Docs/used/`、`copilot/` 当成自己的工作区（这些是用户独立产物或归档）
- ❌ 用 `$$...$$` 写公式（NeurIPS 禁；CLAUDE.md §排版规范）
- ❌ 从 main 创建分支后忘记 commit（CLAUDE.md §Git 工作流）

### G.3 应该做

- ✅ 启动 session 时按"`MISSION → REPORT → MEMORY → CLAUDE`"顺序读
- ✅ 完成里程碑后同步刷 REPORT + MEMORY §C
- ✅ 调用 `path_A_method_skeleton.md` 作为符号 / Theorem 编号唯一来源
- ✅ 论文符号修改时同步 `paper/black/macros/notation.tex` 与 `path_A_method_skeleton.md §3.1`
- ✅ 遇到不确定时用 `AskUserQuestion`（90% 把握以下不动）

---

> 若你正在读这份文件却不知接下来该做什么——读 `MISSION.md`。
