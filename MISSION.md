# MISSION · 项目总命令

> 每个 session 开始前必读 3 件：本文件 → `MEMORY.md` → `CLAUDE.md`。

---

## 0. 一句话现状

走路径 A：**Shock-aware diffusion for hyperbolic PDEs**（项目代号 **EntroDiff**），投 **NeurIPS 2026**，**重理论 / 轻实验**。

---

## 1. 决策快照

| 维度 | 决策 |
|---|---|
| 领域 | AI4S → AI4PDE × Diffusion Model |
| 路径 | A（详见 `Docs/black/path_A_method_skeleton.md`） |
| 项目代号 | EntroDiff |
| 投稿目标 | NeurIPS 2026（main conference） |
| 论文风格 | NeurIPS 偏好：理论重 + 实验轻 |
| 实验定位 | 仅作 **toy example 验证**；benchmark 留到 rebuttal 补 |
| 角色扮演 | **Anima Anandkumar**（Caltech / NVIDIA），AI4PDE 旗手；理由见 `MEMORY.md §角色` |
| 用户身份 | 物理系学生：扩散模型懂概念但没写过代码；PDE 有基础但弱解 / OT / BV 等高阶工具未学；对论文"理论高级度"有强诉求（NeurIPS 偏好） |

---

## 2. 工作区目录约定

| 目录 | 用途 |
|---|---|
| `paper/` | 论文写作、理论推导、图表（**LaTeX 工作区**） |
| `paper/2026_template/` | 官方 NeurIPS 2026 模板（**只读**，不直接改） |
| `paper/black/` | 论文工作主目录（**默认归位**） |
| `paper/white/` | 用户讲解版（仅在用户说"讲解"时启用） |
| `PROJECT/` | 代码工作区 |
| `PROJECT/black/` | 主开发版（**默认归位**） |
| `PROJECT/white/` | 白盒注释版（讲解时启用） |
| `Output/balck/` | 实验输出（**默认归位**，拼写沿用既有目录） |
| `Output/white/` | 用户白盒展示用 |
| `Docs/black/` | 内部讲义 / 笔记 / 决策日志（**默认归位**） |
| `Docs/white/` | 用户讲解版（讲解类输出去这里） |
| `Docs/lectures/` | 系列讲义（L1, L2, ...）默认归位时落 `Docs/black/lectures/` |
| `Docs/proofs/` | 定理证明稿件 |
| `EXAMPLE PAPERS/` | 16 篇相关 PDF（**只读引用**） |

### 归位规则（强制）

- **默认所有产物 → `black/`**
- **仅当用户显式说"为我讲解 / 解读 / 教学 / 给我讲清"时 → `white/`**
- 元数据 / 协议（`MISSION.md`、`MEMORY.md`、`CLAUDE.md`、`EXPERIENCE.md`）放项目根目录，不分 black/white

---

## 3. NeurIPS 2026 排版规范

- **主控文件**：`paper/black/neurips_2026.tex`
- **样式包**：`paper/black/neurips_2026.sty`（从 `paper/2026_template/` 拷贝）
- **页数**：正文（含图表）**≤ 9 页**；references / checklist / technical appendices 不计
- **匿名性**：双盲提交，**严禁** `[final]` / `[preprint]` 选项；引用本组工作用第三人称（"In the previous work of Jones et al. [4]"）
- **公式**：必须用 `\begin{equation}` / `\begin{align}` 等环境，**严禁** `$$...$$`
- **表格**：使用 `booktabs` 宏包，**严禁**垂直分割线（`|`）
- **图表 caption**：必须包含 *Key take-away message*（一句话告诉读者"这张图说明了什么"）
- **引用**：使用 `natbib` 包，文内统一用 `\citet{}`（作者(年份)叙述式）或 `\citep{}`（(作者,年份)括号式）
- **详细约定**：参见 `paper/black/CONVENTIONS.md`

---

## 4. 当前阶段（W1 of 12 周时间表）

> 时间表完整版见 `Docs/black/path_A_method_skeleton.md §6`。

| 周 | 阶段 | 主任务 | 关键产物 |
|---|---|---|---|
| **W1（当前）** | 理论基石 | L1 + L2 讲义（Fokker-Planck & Optimal Transport） | `Docs/black/lectures/L1.md`, `L2.md` |
| W2 | 理论基石 | L3 + L4 讲义（JKO & 熵解） | `L3.md`, `L4.md` |
| W3 | 理论基石 | L5 讲义（Score–Burgers）+ Theorem 1 formal proof | `L5.md`, `Docs/black/proofs/thm1.md` |
| W4 | 理论突破 | Theorem 2 + 3 证明 | `thm2.md`, `thm3.md` |
| W5 | 代码基建 | 复现 EDM + DiffusionPDE baseline | `PROJECT/black/baseline/` |
| W6 | 代码主体 | BV-aware parameterization + $\mathcal L_3$ | `PROJECT/black/entrodiff/` |
| W7 | 实验 E1 | Inviscid Burgers 完整跑通 | `Output/balck/E1/` |
| W8 | 实验 E2 + Theorem 4 | Buckley-Leverett + R-H 验证 | `Output/balck/E2/`, `thm4.md` |
| W9 | 实验 E3 + Theorem 5 | Euler/Sod + JKO 对应证明 | `Output/balck/E3/`, `thm5.md` |
| W10 | 写作 | Intro + Method + Theory 章节初稿 | `paper/black/v1.pdf` |
| W11 | 实验 E4（可选） | Shallow-water | `Output/balck/E4/` |
| W12 | 冲刺 | 消融 + 写作 + 投稿 | `paper/black/final.pdf` |

---

## 5. 用户痛点 / 期望（保留自旧版 MISSION）

- **代码侧**：没写过扩散模型代码 → 需要明确告知"用哪些库的哪一部分"
- **知识侧**：PDE 谱分析、流形 / 微分几何、流匹配进阶 — 都需补
- **工程侧**：多环境（PC / Colab / 服务器）开发，参考 `Docs/black/多环境开发指南_从第一天就做对.md`
- **对讲解的语言要求**：拒绝"行业黑话"、第一性原理讲清；输出归位 `Docs/white/`
- **对论文的语言要求**：严谨专业、高度符号化、与上下文符号 / 思路对齐
- **对所有任务的核心硬要求**：理论高级度（NeurIPS 偏好）

---

## 6. 旧版 IDEA 的最终归宿

> 路径 A 已涵盖以下原始 IDEA 中的所有"故事点"，无需另起：

| 原始 IDEA | 在路径 A 中的承载 |
|---|---|
| 解视作分布 | Theorem 1 双 Burgers 耦合（solution-level Liouville） |
| 高斯 → 解分布的逐步去噪 | EDM 反向 ODE，加 viscosity-matched schedule |
| 范式转移 "loss → push distribution" | Intro 一句话 motivation（不作 novelty） |
| 高维 / 尖锐解 PDE | 路径 A 锁定**尖锐解**（hyperbolic / shock）；高维留作 future work |
| 等离子体 / 核聚变数据 | E5 Vlasov-Poisson 加分项 |
| 流形角度 | 暂不进路径 A，留作 future work |

---

## 7. 协议优先级

1. 本 `MISSION.md`（任务命令）
2. `CLAUDE.md`（项目协议 / 排版 / 归位 / git 工作流）
3. `MEMORY.md`（决策日志 / 状态快照 / 风险簿）
4. `~/.claude/CLAUDE.md`（用户全局协议，被项目协议覆盖时以项目为准）
