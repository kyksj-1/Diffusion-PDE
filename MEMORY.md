# MEMORY · 项目活档案

> 这是项目的"活档案"——决策、状态、风险随时间演化。**每次重大决策、阶段切换、风险更新时维护**；不是每次 session 必须改。
> 若与 `MISSION.md` 冲突，以 `MISSION.md` 为准（MISSION 是命令，MEMORY 是日志）。

---

## A. 角色选择（首次：2026-04-26）

### A.1 当前角色：Anima Anandkumar 教授（Caltech / NVIDIA）

### A.2 选择理由（CLAUDE.md "角色扮演"要求"该任人物真实存在并说明理由"）

1. **"AI4PDE" 这个术语的旗手**——她在 NVIDIA 主推的 "AI for Science" 路线把 AI4PDE 从学术兴趣点推成顶会标准方向。
2. **实验室产出全覆盖**：FNO（NeurIPS 2021 spotlight）、PINO（数据 + 物理混合训练）、GNO（图神经算子）、Diffusion-FNO、CFO（flow-matching for PDE）—— 是当今"diffusion / flow + PDE"产线最完整的实验室。
3. **写作风格符合 NeurIPS 评委偏好**：理论先行 → 设计精巧 → 实验干净 → 卖点包装清晰。她的论文典型节奏正是路径 A 想走的"理论重 / 实验轻"。
4. **领域内权威性**：IEEE Fellow、ACM Fellow、Bren Professor，AI4Science 方向的 Nature 子刊综述常作者。
5. **路径 A 的题材契合度**：她的组在 2024-2025 年发表的 DiffusionPDE / CFO / FunDPS 是我们直接对标的 baseline，"在自己擅长方向打自己" 这种叙事她非常熟悉。

### A.3 备选（仅在用户要求换角色时启用）

- **George Em Karniadakis**（Brown）—— PINN 鼻祖，更偏严谨数学，但写作偏 JCP / SISC 风格而非 NeurIPS。
- **Weinan E**（Princeton / 北大）—— Deep BSDE / 高维 PDE 的奠基人，理论极重；NeurIPS 风格略保守。
- **Maziar Raissi**（CU Boulder）—— PINN 通讯作者，写作普及性强。

---

## B. 决策日志（按日期倒序）

### 2026-04-26 · 路径选定 + 工作区固化

- 用户**确认走路径 A**（Shock-aware diffusion for hyperbolic PDEs，代号 EntroDiff）。
- **目录约定 black/white**：默认 black/，仅讲解时 white/。语义口径已写入 MISSION §2 / CLAUDE 排版规范条款。
- **NeurIPS 排版规范**固化（9 页、双盲、`\begin{equation}` / `\begin{align}`、`booktabs` 无 vrules、`natbib` 用 `\citet/\citep`）。
- **创建 git 分支** `feat/setup-paper-project-20260426` 承载本次基础设施搭建。
- **paper/2026_template/** 已存在官方 NeurIPS 2026 模板（`neurips_2026.tex` / `.sty` / `checklist.tex`）。

### 2026-04-25 · 完成路径 A 的第一性原理解读

- 输出 `Docs/white/路径A_第一性原理解读.md`（用户已学完）。
- 输出 `Docs/black/path_A_method_skeleton.md`（论文骨架 / 5 个核心定理 / 12 周时间表 / 风险簿）。
- 输出 `Docs/black/idea_originality_analysis.md`（IDEA 原创性扫描，给出路径 A/B/C 三选一）。

### 2026-04-21 · 项目初始化

- 创建 git 仓库（commit `2099801` initialization）。
- 用户选择 NeurIPS 投稿方向：AI4S / AI4PDE / Diffusion Model。
- 备齐 16 篇相关论文 PDF 在 `EXAMPLE PAPERS/`。

---

## C. 状态快照（每周 / 每阶段切换时更新一次）

### C.1 当前阶段

- **周次**：W1（12 周时间表的第 1 周）
- **本周主任务**：L1 讲义（扩散模型 ↔ Fokker-Planck 等价性）
- **下一里程碑**：W3 末完成 Theorem 1 的 formal proof（双 Burgers 耦合）

### C.2 已完成

| 类别 | 产物 | 路径 |
|---|---|---|
| 决策 | 路径 A 选定 | `MEMORY.md §B` |
| 文档 | 原创性分析 | `Docs/black/idea_originality_analysis.md` |
| 文档 | 路径 A 方法骨架 | `Docs/black/path_A_method_skeleton.md` |
| 讲义 | 路径 A 第一性原理解读 | `Docs/white/路径A_第一性原理解读.md` |
| 模板 | NeurIPS 2026 官方模板 | `paper/2026_template/` |
| 基建 | 双轨目录约定（black/white） | `MISSION.md §2` |

### C.3 进行中

- 论文 LaTeX 工作区搭建（`paper/black/`）
- 代码工作区搭建（`PROJECT/black/`）

### C.4 阻塞中

- 暂无

### C.5 下一步（W1-W2）

1. L1 讲义：扩散模型 ↔ Fokker-Planck 等价性
2. L2 讲义：Optimal Transport / Wasserstein 几何
3. 论文 sections 占位骨架（intro / method / theory）

---

## D. 风险簿（来自 path_A_method_skeleton §7，定期复评）

| 风险 ID | 描述 | 概率 | 冲击 | 对策 | 状态 |
|---|---|---|---|---|---|
| R1 | Theorem 3（主定理）证不出，$\exp(\Lambda) \to \mathcal O(1)$ 退化论证不够 | 中 | **高** | 备用：退而求次证 $\exp(\Lambda/2)$，仍对 baseline 有改进 | 监控中 |
| R2 | BV-aware parameterization 在 2D 上工程难 implement | 中 | 中 | 先 1D 跑通；2D 用 mesh-based $\phi$ 替代 signed distance | 待 W6 验证 |
| R3 | DiffusionPDE / FunDPS 作者作 reviewer 挑实验 | 高 | 中 | 主实验直接用他们公开数据 + 代码作 baseline | 写作时落实 |
| R4 | Score Shocks 的 VP-VE 等价性假设在实模型不严格成立 | 低 | 中 | 论文声明只在 VE 设定下证明，VP 留 future work | 写作时落实 |
| R5 | 12 周紧，实验未必能跑出来 | 中 | 高 | E1+E2 必做（最小工作量），E3-E5 增量；理论章节做厚 | 监控中 |
| R6 | Reviewer 认为"只是 Score Shocks 的应用" | 中 | 中 | Intro 强调三大原创：Theorem 1 耦合 + Theorem 3 收敛率 + Theorem 5 JKO 桥梁 | 写作时落实 |
| R7 | 用户作为物理系学生，弱解 / OT / BV 数学工具不熟，影响进度 | 中 | 中 | L1-L5 讲义系列预热；用户每周读一份 | 推进中 |

---

## E. 关键检索索引（high-traffic 跳转）

| 想找... | 去这里 |
|---|---|
| 路径 A 方法骨架 / 5 大定理 / 12 周计划 | `Docs/black/path_A_method_skeleton.md` |
| 为什么走路径 A（vs B/C） | `Docs/black/idea_originality_analysis.md` §3 |
| 第一性原理拆解（讲给学生） | `Docs/white/路径A_第一性原理解读.md` |
| NeurIPS 2026 排版细节 | `paper/black/CONVENTIONS.md`（待建） + `MISSION.md §3` |
| LaTeX 主控 / 各 section | `paper/black/neurips_2026.tex`（待建） |
| 代码模块结构 | `PROJECT/black/README.md`（待建） |
| 多环境开发（PC / Colab / 服务器） | `Docs/black/多环境开发指南_从第一天就做对.md` |
| 16 篇相关论文 | `EXAMPLE PAPERS/` |
| 角色 / 写作风格 | 本文件 §A |

---

## F. 维护规则（请认真维护，否则我会问你"现在到哪儿了"）

### F.1 触发更新的事件（其一发生即更新对应小节）

| 触发事件 | 应更新 |
|---|---|
| 用户做出**重大决策**（路径切换 / 方法变更 / 投稿目标变更 / 角色切换） | §A、§B |
| 完成一个**里程碑**（讲义 / 定理证明 / 实验 / 章节初稿） | §C.2、§B |
| 风险**新增 / 状态变化**（缓解 / 升级 / 解除） | §D |
| 用户提出**新的偏好或约束** | §B + 视情况更新 `MISSION.md` 或 `CLAUDE.md` |
| 启动新的**周阶段**（每周 / 每两周） | §C.1、§C.5 |

### F.2 不写进 MEMORY 的事

- 普通文件编辑、bug 修复细节（git log 自带）
- 临时调试 / 探索（用 git stash 或临时分支）
- 一次性问答（用对话上下文即可）

### F.3 与其他文件的分工

| 文件 | 主管什么 |
|---|---|
| `MISSION.md` | 命令 / 当前应该做什么（指令性） |
| `MEMORY.md`（本文件） | 历史 / 状态 / 风险（描述性） |
| `CLAUDE.md` | 协议 / 规范（约束性） |
| `EXPERIENCE.md` | 跨 session 的工具调用经验（可被其他 agent 提取） |

---

> **若你正在读这份文件却不知道接下来该做什么——读 `MISSION.md §4`。**
