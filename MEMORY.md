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

- **周次**：W2（12 周时间表的第 2 周；W0–1 已完成）
- **本阶段主任务**：论文撰写 + 实验启动**双线**（不再写讲义）
- **下一里程碑**：Theorem 3 主定理定稿 + E1 Burgers 数据 / baseline 跑通

### C.2 已完成（详见 REPORT.md §2）

- 决策：路径 A 选定
- 文档：原创性分析、方法骨架、第一性原理解读
- 模板：NeurIPS 2026 官方模板
- 工作区：paper/black + PROJECT/black 双骨架
- 元数据：MISSION / CLAUDE / MEMORY 三件套；REPORT 新增中
- 用户独立产出：Theorem 3 草稿 v2 + critique（待迁入 `Docs/black/proofs/`）

### C.3 进行中

- MEMORY / MISSION / CLAUDE 第二次重组（本 session）
- 新建 REPORT.md
- L1–L8 lectures 已迁 `Docs/black/lectures/`

### C.4 阻塞中

- 暂无

### C.5 下一步

详见 `MISSION.md §本阶段任务`。优先级：Theorem 3 修订（A 线）> Burgers ground truth + EDM baseline（C/D 线）。

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
