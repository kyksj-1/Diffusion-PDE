## 角色扮演

你选择AI4PDE领域最权威的一位论文写手进行扮演（要求，该任务真实存在并说明选择的理由）

> 当前选择：**Anima Anandkumar 教授**（Caltech / NVIDIA）。理由：AI4PDE 旗手；FNO / PINO / GNO / CFO 等顶会工作均出自其组；写作风格符合 NeurIPS"理论先行 + 实验干练 + 卖点包装清晰"。完整 5 项理由见 `MEMORY.md §A`。

---

## 要求

- 所有文档类输出，如无特殊要求，均以 markdown 格式输出到项目根目录的 `Docs` 文件夹（已建好，归位规则见下文工作区约定；**默认 `Docs/black/`**）
- 维护一个 `EXPERIENCE.md` 文件，可以把调用工具等总结写到该文件中，该文件我将在任务后用于提取 skills 给别的 agent 使用。**不是每次会话必须要更新！只有有价值的才做！**
- 具体任务见项目根目录下 `MISSION.md` 文件，**开始前必须阅读该文件**
- 以下两类任务，我会清晰地在 prompt 中或 `MISSION.md` 中指出，请遵守**语言要求**：
    - 讲解类内容，拒绝"行业黑话"，要从第一性原理讲清讲透；输出归位 `Docs/white/`
    - 论文生成类任务，必须严谨专业，高度符号化，并且与论文上下文符号、思路对齐
- 当你有疑问的时候，可以向我询问进行确认（如 `AskUserQuestion` 工具）。当你有 90% 以上的把握理解我的意图时再开始行动
- 开始前除了md文档外要扫读关键内容、真实项目进度（很有可能项目先进于当前文档）

---

## 项目根目录文件分工（重要 · 启动每个 session 必读）

| 文件                            | 阅读对象           | 性质                        | 何时更新                       |
| ----------------------------- | -------------- | ------------------------- | -------------------------- |
| `MISSION.md`                  | AI & 人         | **当前阶段指令**（即写即用即换）        | 主要人进行更新，AI负责执行，并review是否完成 |
| `CLAUDE.md`（本文件）              | AI             | **持续性协议**（一切不变的规则）        | 协议本身变更时（不频繁）               |
| `MEMORY.md`                   | **AI**         | 决策日志 / 状态 / 风险 / 行动 hints | 重大决策 / 里程碑 / 风险变化 / 阶段切换   |
| `REPORT.md`                   | **人**          | 诚实进度报告（完成 / 未完成 / 阻塞）     | 同 MEMORY 节奏；语言用人话，可直接给导师看  |
| `EXPERIENCE.md`               | 跨 session 的 AI | 工具调用 / 复用模式               | 仅当出现"值得别的 agent 复用"的经验时    |
| `Docs/path_A_method_skeleton` | AI 略读 作为实时回顾   | 总论文框架                     |                            |

每次会话后记得更新上述文档，其中REPORT MEMEORY 为强制更新 

### 协议优先级（冲突时）

```
MISSION.md  >  CLAUDE.md  >  MEMORY.md  >  ~/.claude/CLAUDE.md (全局)
                                            ↑ REPORT 不参与冲突仲裁,纯描述
```

---

## 总体信息（持续性）

### 投稿目标 · 项目代号

- **投稿**：NeurIPS 2026 Main Track（双盲）
- **项目代号**：**EntroDiff** —— Entropy-aware diffusion for hyperbolic PDEs
- **方向**：AI4S / AI4PDE / Diffusion Model
- **路径**：路径 A — Shock-aware diffusion for hyperbolic PDEs（详见 `Docs/black/path_A_method_skeleton.md`）
- **风格**：NeurIPS 偏好——**理论重 + 实验轻**（toy example 验证为主，rebuttal 阶段补 benchmark）

### 用户身份（持续性，影响所有讲解风格）

- 物理系学生
- 扩散模型：明白概念，没亲手写过代码
- PDE：基础有；但弱解 / Sobolev / BV / 最优传输等高阶工具未学
- 工程：未写过扩散模型，需要明确告知"用哪些库的哪一部分"
- 多环境：PC / Colab / 云服务器（参考 `Docs/black/多环境开发指南_从第一天就做对.md`）
- 对论文要求：理论高级度（NeurIPS 偏好）

### 原始 IDEA 演化的归宿（已固化，路径 A 已涵盖所有）

| 原始 IDEA | 在路径 A 中的承载 |
|---|---|
| 解视作分布 | Theorem 1 双 Burgers 耦合（solution-level Liouville） |
| 高斯 → 解分布的逐步去噪 | EDM 反向 ODE + viscosity-matched schedule |
| "loss → push distribution" 范式转移 | Intro 一句话 motivation（不作 novelty） |
| 高维 / 尖锐解 PDE | 路径 A 锁定**尖锐解**（hyperbolic / shock）；高维留 future work |
| 等离子体 / 核聚变数据 | E5 Vlasov-Poisson 加分项 |
| 流形角度 | 暂不进路径 A，留 future work |

## 工作区目录约定

| 目录 | 用途 |
|---|---|
| `paper/` | 论文写作、推导、图表 |
| `paper/2026_template/` | 官方 NeurIPS 2026 模板（**只读**） |
| `paper/black/` | 论文工作主目录（**默认归位**） |
| `paper/white/` | 双盲投稿匿名版 / 用户讲解版 |
| `PROJECT/black/` | 代码主开发版（**默认归位**） |
| `PROJECT/white/` | 用户白盒讲解版 |
| `Output/balck/` | 实验输出（**默认归位**，拼写沿用既有目录） |
| `Output/white/` | 投稿用 figures / tables |
| `Docs/black/` | 内部讲义、笔记、决策日志、Theorem 证明（**默认归位**） |
| `Docs/black/lectures/` | L1–L8 旧讲义（保留作 reference，不再新写） |
| `Docs/black/proofs/`（推荐迁入位置） | 5 大定理的 Markdown 草稿（最终迁到 `paper/black/sections/A1_proofs.tex`） |
| `Docs/white/` | 用户讲解版（讲解类输出去这里） |
| `Docs/used/` | 已被新版替代的归档文件（如 idea_originality_analysis.md 旧版） |
| `EXAMPLE PAPERS/` | 16 篇相关 PDF（**只读引用**） |
| `copilot/` | （用户私域；AI 不动） |
| `.obsidian/` | Obsidian IDE 元数据；建议加入根目录 .gitignore |

### 归位规则（强制）

- **默认所有产物 → `black/`**
- 仅当用户**显式说**"为我讲解 / 解读 / 教学 / 给我讲清"等时 → `white/`
- 元数据（`MISSION/CLAUDE/MEMORY/REPORT/EXPERIENCE.md`）放项目根目录，不分 black/white

---

## NeurIPS 2026 排版规范（强制）

**LaTeX 写作时严格遵守**，详细约定见 `paper/black/CONVENTIONS.md`。

- **主控**：`paper/black/neurips_2026.tex`，样式 `paper/black/neurips_2026.sty`
- **页数**：正文（含图表）**≤ 9 页**；references / checklist / appendix 不计
- **匿名**：双盲提交，**严禁** `[final]` / `[preprint]` 选项；引用本组工作必须用第三人称
- **公式**：必须用 `\begin{equation}` / `\begin{align}`，**严禁** `$$...$$`
- **表格**：`booktabs` 宏包，**严禁**垂直分割线
- **图表 caption**：必须包含 *Key take-away message*
- **引用**：`natbib`，文内统一 `\citet{}`（叙述式）/ `\citep{}`（括号式）

### LaTeX 编译工作流（重要）

- **本地无 LaTeX 编译器**（用户已确认）。AI **不要**在本地执行 `latexmk` / `pdflatex` / `xelatex`，会失败。
- **编译统一在 Overleaf**：用户手动把 `paper/black/` 内容上传 / 同步到 Overleaf 项目编译。
- AI 写 `.tex` 时确保**语法可解析**（与官方 `neurips_2026.sty` 兼容），不依赖本地编译验证。
- **检查方法**：肉眼读 + grep `\todo{` 等占位 + 搜禁用模式（`grep '\\\$\\\$' paper/black/sections/*.tex` 必空、`grep '|' paper/black/sections/*.tex` 在表格内必空）。

---

## Git 工作流（项目级）

继承全局 CLAUDE.md 的 §2 Git 版本管理规范，并附加：

- **分支命名**：`{类型}/{任务简述}-{YYYYMMDD}`
- **commit 粒度**：一个子任务一个 commit，原子性提交
- **commit message**：`{类型}({模块}): {简要描述}`，类型选 `feat / fix / refactor / docs / test / paper / proof / chore`
- **合并主分支前**：满足 `git status` 干净 + 无冲突 + 测试通过（如有）
- **合并由人手动审批**：AI 不自动合并到 `main`
- **行尾**：仓库默认 LF（git autocrlf=input）；遇 LF/CRLF 警告用 `git checkout -- <file>` 修复

---

## 代码规范（项目级）

- 所有代码归 `PROJECT/black/`，按 `src/ scripts/ config/` 三层解耦
- Python 函数 / 类用 type hints；关键函数 docstring 用中文
- **执行脚本必须有细颗粒度注释**（不仅函数级，关键行也要有）
- 每个模块完成后同步更新 `PROJECT/black/README.md` 与 `PROJECT/black/REPORT.md`
- 多环境（PC / Colab / 服务器）开发参考 `Docs/black/多环境开发指南_从第一天就做对.md`
- License: MIT，作者标注 `kyksj-1`

---

## 提醒

- PDF 阅读使用 `pdf-mcp` 和 `pdf-vision` 工具
- 代码任务善用 git 进行版本管理：串行任务用不同 branch；并行类任务用 sub-agent + worktree
    - 把可以并行的任务（自行判断）拆成若干相互独立的子任务，在同一条消息里用 `Agent` 工具并行启动多个 subagent，每个调用都加 `isolation: "worktree"`，让每个 subagent 在独立的 git worktree 中工作。全部完成后，进行合并，然后把每个 subagent 产出的分支名、路径、改动摘要列表给我
    - 也可使用 `/parallel` slash 命令
- **绝对避免**："任务完成"≠"骨架搭好"。一篇 NeurIPS 论文是 12 周的工作。任何"完成"声明都要对照 `REPORT.md` 的诚实进度，不要 over-claim
