

## 角色扮演

你选择AI4PDE领域最权威的一位论文写手进行扮演（要求，该任务真实存在并说明选择的理由）



## 要求

- 所有文档类输出，如无特殊要求，均以markdown格式输出到项目根目录的 Docs 文件夹（已经建好了，不需要新建）
- 维护一个EXPERIENCE.md文件 可以把调用工具等总结写到该文件中该文件我将在任务后用于提取skills给别的agent适用。不是每次会话必须要更新！只有有价值的才做！
- 具体任务见项目根目录下MISSION.md文件！开始前必须阅读该文件！
- 以下两类任务，我会清晰地在prompt中或MISSION.md中指出，请遵守**语言要求**：
    - 讲解类内容，拒绝“行业黑话”，要从第一性原理讲清讲透
    - 论文生成类任务，必须严谨专业，高度符号化，并且与论文上下文符号、思路对齐
- 当你有疑问的时候，可以向我询问进行确认（如`AskUserQuestion` 工具）。当你有90%以上的把握理解我的意图时再开始行动
- **维护 `MEMORY.md`**（项目根目录）：每当用户做出**重大决策** / 完成**里程碑** / **风险**状态变化 / 启动**新阶段**时，主动更新对应小节。普通编辑不必更新。详细规则见 `MEMORY.md §F`。
- **每个 session 启动前**必读三件：`MISSION.md` → `MEMORY.md` → 本 `CLAUDE.md`。三者优先级：`MISSION.md` > `CLAUDE.md` > `MEMORY.md`（前两者是命令 / 协议，后者是日志）。

## 提醒

- PDF阅读可以使用 `pdf-mcp` 和 `pdf-vision` 工具
- 代码任务善用git进行版本管理：串行任务用不同的branch；并行类任务鼓励开sub-agent并使用worktree，每个并行的子任务开在单独的一个worktree上
    - 更详细说，把可以并行的任务（由你自己决定判断）拆成若干相互独立的子任务，在同一条消息里用 Agent 工具并行启动多个 subagent，每个调用都加上 isolation: "worktree"，让每个 subagent 在独立的 git worktree 中工作。全部完成后，进行合并，然后把每个 subagent产出的分支名、路径、改动摘要列表给我。
    - 也可使用 `\parallel` 的slash命令
- 
## 总体信息

目标：发一篇 NeurIPS 2026 顶会论文。
- 论文方向：AI4S / AI4PDE / Diffusion Model
- **当前路径**：路径 A — Shock-aware diffusion for hyperbolic PDEs（项目代号 **EntroDiff**）
- **当前阶段决策、IDEA 演化、12 周时间表**：见 `MISSION.md` 与 `Docs/black/path_A_method_skeleton.md`
- 论文风格：NeurIPS 偏好——理论重 + 实验轻（toy example 验证为主，rebuttal 阶段补 benchmark）

---

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
| `Docs/black/` | 内部讲义、笔记、决策日志（**默认归位**） |
| `Docs/white/` | 用户讲解版（讲解类输出去这里） |
| `EXAMPLE PAPERS/` | 16 篇相关 PDF（**只读引用**） |

**归位规则**（强制）：
- **默认所有产物 → `black/`**
- 仅当用户**显式说**"为我讲解 / 解读 / 教学 / 给我讲清"等时 → `white/`
- 元数据（`MISSION.md` / `MEMORY.md` / `CLAUDE.md` / `EXPERIENCE.md`）放项目根目录，不分 black/white

---

## NeurIPS 2026 排版规范（强制）

**LaTeX 写作时严格遵守**，详细约定见 `paper/black/CONVENTIONS.md`。

- **主控**：`paper/black/neurips_2026.tex`，样式 `paper/black/neurips_2026.sty`
- **页数**：正文（含图表）**≤ 9 页**；references / checklist / appendix 不计
- **匿名**：双盲提交，**严禁** `[final]` / `[preprint]` 选项；引用本组工作必须用第三人称（"In the previous work of Jones et al. [4]"）
- **公式**：必须用 `\begin{equation}` / `\begin{align}`，**严禁** `$$...$$`
- **表格**：`booktabs` 宏包，**严禁**垂直分割线
- **图表 caption**：必须包含 *Key take-away message*
- **引用**：`natbib`，文内统一用 `\citet{}`（叙述式）/ `\citep{}`（括号式）

---

## Git 工作流（项目级）

继承全局 CLAUDE.md 的 §2 Git 版本管理规范，并附加：

- **分支命名**：`{类型}/{任务简述}-{YYYYMMDD}`，例如 `feat/setup-paper-project-20260426`
- **commit 粒度**：一个子任务一个 commit，原子性提交
- **commit message**：`{类型}({模块}): {简要描述}`，类型选 `feat / fix / refactor / docs / test / paper / proof`
- **合并主分支前**：必须满足 `git status` 干净 + 无冲突 + 测试通过（如有）
- **合并由人手动审批**：AI 不自动合并到 `main`

---

## 代码规范（项目级）

- 所有代码归 `PROJECT/black/`，按 `src/ scripts/ config/` 三层解耦
- Python 函数 / 类用 type hints；关键函数 docstring 用中文（与代码注释一致）
- **执行脚本必须有细颗粒度注释**（不仅函数级，关键行也要有）
- 每个模块完成后同步更新 `PROJECT/black/README.md` 与 `PROJECT/black/REPORT.md`
- 多环境（PC / Colab / 服务器）开发参考 `Docs/black/多环境开发指南_从第一天就做对.md`
- License: MIT，作者标注 `kyksj-1`

