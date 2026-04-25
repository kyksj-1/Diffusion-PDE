# REPORT · 项目进度报告

> **阅读对象 · 人**（用户、合作者、导师；可直接给人看）。
> **AI 的状态 / 决策日志在 `MEMORY.md`，规则在 `CLAUDE.md`，当前指令在 `MISSION.md`。**
> **更新节奏**：与 MEMORY 同节奏（重大决策 / 里程碑 / 阶段切换）。

---

## 1 · 30 秒摘要

我们决定走**路径 A**：用 shock-aware diffusion 解 hyperbolic PDE，理论命门是把"扩散模型 score 自身就是个 Burgers 方程"（Score Shocks 论文）这一观察，转成一个对 Kruzhkov 熵解有 $\mathcal{O}(\varepsilon^{1/2})$ 收敛率保证的算法。项目代号 **EntroDiff**，目标 NeurIPS 2026 主会双盲投稿。

**当前周次**：W2（共 12 周）。**距离投稿截止还有 ~10 周可用**。

**整体完成度估计**：

| 维度 | 完成度 | 备注 |
|---|---|---|
| 决策 / 选题 | **100%** | 路径 A 锁定 |
| 基础设施 / 工作区 | **95%** | paper / PROJECT / 元数据三件套就位；`.gitignore` 根目录尚未建 |
| 理论证明 | **15%** | Theorem 3 已有 v2 草稿 + critique；Theorem 1, 2, 4, 5 0% |
| 论文写作 | **5%** | 9 个章节占位骨架，所有内容皆为 `\todo{}` |
| 代码实现 | **2%** | 包结构 / 类签名 / 配置 / 测试 stubs 就位；所有核心函数 `raise NotImplementedError` |
| 实验 | **0%** | 未生成任何数据；未跑任何 baseline |
| 综合 | **~12%** | 风险按计划可控，理论是 12 周成败决定项 |

**最大风险**（截至本报告）：

1. **R1 · Theorem 3 主定理证不出** — 用户已有 v2 草稿 + critique，正在迭代修订
2. **R5 · 12 周时间紧** — 已规划"E1+E2 必做，E3+加分"的最小可投稿集
3. **R8 · over-claim** — 本次报告即在响应这条风险，所有"完成"严格对应可见产物

---

## 2 · 已完成（详细）

### 2.1 决策与方法论

| 事项 | 状态 | 产物 |
|---|---|---|
| 投稿目标确认（NeurIPS 2026 双盲）| ✓ | `CLAUDE.md` |
| 论文方向（路径 A vs B vs C）| ✓ | `Docs/used/idea_originality_analysis.md` |
| 方法骨架（5 大定理 + 12 周时间表）| ✓ | `Docs/black/path_A_method_skeleton.md` |
| 角色 / 写作风格（Anima Anandkumar）| ✓ | `MEMORY.md §A` |
| 用户身份 / 痛点 / 期望（持续）| ✓ | `CLAUDE.md §用户身份` |

### 2.2 文档（教学 / 解读 / 讲义）

| 产物 | 路径 | 备注 |
|---|---|---|
| 第一性原理解读（讲给物理系学生）| `Docs/white/路径A_第一性原理解读.md` | 27.6 KB；用户已学完 |
| 原创性分析 | `Docs/used/idea_originality_analysis.md` | 用户已确认结论 |
| 方法骨架 | `Docs/black/path_A_method_skeleton.md` | 论文 / 代码 / 证明的唯一坐标系 |
| L1–L8 旧讲义（reference）| `Docs/black/lectures/L*.md` | 已迁位；用户决定不再新写讲义，保留作参考 |
| 多环境开发指南 | `Docs/black/多环境开发指南_从第一天就做对.md` | 用户先前提供 |

### 2.3 论文工作区（`paper/black/`）

| 产物 | 状态 |
|---|---|
| `neurips_2026.tex` 主控 | ✓ 双盲、natbib、booktabs、amsmath/amsthm、5 个 theorem 环境 |
| `neurips_2026.sty`（官方样式）| ✓ 拷贝自 `paper/2026_template/` |
| `checklist.tex` | ✓ 拷贝；待写作期填充 |
| `macros/notation.tex` | ✓ 与 `path_A_method_skeleton §3.1` 符号表对齐 |
| 8 个 sections 占位 | ✓ 全部 `\todo{}` 标注；intro / related / prelim / double-burgers / method / theory / exp / conclusion |
| 3 个 appendix 占位 | ✓ proofs / extra-experiments / impl-details |
| `references.bib` | ✓ 17 个 key 占位（DiffusionPDE / FunDPS / Score Shocks / FNO / EDM / 等）|
| `CONVENTIONS.md` | ✓ 排版强制 / 引用风格 / 占位标记 / 提交前 checklist |
| `README.md` | ✓ 工作区导航 + latexmk 命令 |
| 编译测试 | **未跑** — 待 W2 内试编 一次 |

### 2.4 代码工作区（`PROJECT/black/`）

| 产物 | 状态 |
|---|---|
| 三层解耦目录（`src/scripts/config/tests`）| ✓ |
| `pyproject.toml` + `requirements.txt` | ✓ 含 ruff/black/mypy/pytest 配置 |
| `.gitignore` | ✓ 排除 ckpt / wandb / venv / data |
| `README.md` + `REPORT.md` | ✓ |
| 8 个 module（pdes / models / losses / samplers / schedules / utils）| **占位** — 包结构 / 类签名 / type hints / docstring 就位；所有核心函数 `raise NotImplementedError` |
| 4 个 CLI 入口（train / sample / eval / data_gen）| **占位** — argparse 完成，主流程未实现 |
| 4 个 YAML 配置（default / e1 / e2 / e3）| ✓ |
| 测试 stubs（`test_pdes.py`, `test_samplers.py`）| ✓ pytest skip 标记，待 W5 启用 |
| **实际可运行的代码** | **0 行** |

### 2.5 元数据（项目根目录）

| 文件 | 状态 |
|---|---|
| `MISSION.md` | ✓ 已瘦身为"当前阶段指令" |
| `CLAUDE.md` | ✓ 已吸收 MISSION 持续性内容 + 12 周时间表 |
| `MEMORY.md` | ✓ §A–G 完整；含 AI 行动 hints |
| `REPORT.md`（本文件）| ✓ 首版 |
| `EXPERIENCE.md` | ⚪ 空文件，待"值得复用的模式"出现时填 |

### 2.6 用户独立产出（**未由 AI 触碰**）

| 产物 | 路径 | 备注 |
|---|---|---|
| Theorem 3 草稿 v2（符号统一修订版）| `Docs/proof/Theorem 3 draft.md` | 已就阶段 1-3 推导；阶段 4-6 待补 |
| Theorem 3 证明 critique（6 个符号问题 + 5 个论证漏洞）| `Docs/proof/Theorem 3 证明改进.md` | 修订路线图已成型 |

---

## 3 · 未完成（详细）

### 3.1 理论证明

| Theorem | 内容 | 当前状态 |
|---|---|---|
| **Theorem 1**（Double-Burgers coupling）| score-level + solution-level 两个 Burgers 在 shock set 上的几何耦合 | **0%** — 未动笔；需基于 Score Shocks Thm 4.3 + Liouville-on-characteristics |
| **Theorem 2**（Stability, baseline rate）| $W_1 \le C\varepsilon \exp(\Lambda T)$ | **0%** — 未动笔；用 Gronwall + Score Shocks Thm 6.3 + Kruzhkov $L^1$-contraction |
| **Theorem 3 ⭐**（Improved rate $\varepsilon^{1/2}$）| 论文主定理，命门 | **~30%** — 用户 v2 草稿 + critique 已成型；待按 critique 修订 + 补阶段 4-6 |
| **Theorem 4**（Shock-location admissibility）| R-H + Lax 熵条件 | **0%** — 未动笔；用 Score Shocks Thm 5.5 + 5.11 |
| **Theorem 5**（JKO correspondence）| 反向 ODE = $W_2$ JKO 离散 | **0%** — 未动笔；标准 JKO + PDE 约束 Lagrangian |

### 3.2 论文写作（`paper/black/sections/`）

每个章节都是 `\todo{...}` 占位，0 行实际段落。

| Section | 任务 | 完成度 |
|---|---|---|
| 01 Intro | 三段式 Gap / Insight / Contribution | 0% |
| 02 Related Work | 4 组（function-space diffusion / FM / PDE perspective / 数值）| 0% |
| 03 Preliminaries | VE-SDE / Kruzhkov / W_1 / BV | 0% |
| 04 Double-Burgers | Theorem 1 + 几何示意图 | 0% |
| 05 Method | viscosity-matched + BV-aware + loss family + sampler | 0% |
| 06 Theory | Theorem 2-5 + 证明 sketch | 0% |
| 07 Experiments | E1-E3 主结果 + 消融 | 0% |
| 08 Conclusion | 限制 + future work | 0% |
| A1 Proofs | 5 大定理完整证明 | 0%（Thm 3 部分有草稿）|
| A2 Extra Experiments | E4 / E5 留作 rebuttal | 0% |
| A3 Implementation Details | arch / hyperparams / compute | 0% |

### 3.3 代码实现（`PROJECT/black/src/entrodiff/`）

每个模块都是 `raise NotImplementedError` 的占位。

| 模块 | 关键 class / function | 状态 |
|---|---|---|
| `pdes/burgers.py` | `generate_burgers_dataset` | 占位 — W5 启用 |
| `pdes/buckley_leverett.py` | `generate_bl_dataset` | 占位 — W5 启用 |
| `pdes/euler_sod.py` | `generate_euler_sod_dataset` | 占位 — W6 启用 |
| `models/score_baseline.py` | `EDMDenoiser`, `BaselineScoreNet` | 占位 — W5 启用 |
| `models/score_bvaware.py` ⭐ | `BVAwareScoreNet` | 占位 — W5–6 启用（论文核心创新）|
| `losses/dsm.py` | `dsm_loss` | ✓ 已实装（10 行）|
| `losses/entropy_reg.py` | `kruzhkov_entropy_loss` | 占位 |
| `losses/bv_reg.py` | `tv_loss` | ✓ 已实装（10 行）|
| `losses/burgers_consistency.py` | `burgers_consistency_loss` | ✓ 已实装（5 行）|
| `samplers/reverse_ode.py` | `HeunSampler` | 占位 |
| `samplers/godunov_guidance.py` | `godunov_guidance` | 占位 |
| `schedules/viscosity_matched.py` | `ViscosityMatchedSchedule` | ✓ 已实装（10 行；σ=√(2ν τ)）|
| `utils/metrics.py` | `wasserstein_1`, `l1_error`, `shock_location_error` | 部分实装（`l1_error` ✓ 其余占位）|
| `utils/io.py` | `load_yaml`, `save_checkpoint`, `load_checkpoint` | ✓ 已实装（25 行）|

### 3.4 实验

| 实验 | 计划 | 状态 |
|---|---|---|
| E1 · Inviscid Burgers | shock 形成 + $W_1$ 标度律验证 Theorem 3 | 0% — 数据未生成 |
| E2 · Buckley–Leverett | 非凸通量 + R-H 验证 | 0% |
| E3 · 1D Euler / Sod | shock + contact + rarefaction | 0% |
| E4 · 2D Shallow-water（rebuttal）| hydraulic jump | 0% — 留 rebuttal |
| E5 · Vlasov-Poisson（rebuttal）| 弱解 / filamentation | 0% — 留 rebuttal |

### 3.5 工程基础设施剩余项

| 项 | 状态 |
|---|---|
| 仓库根 `.gitignore`（排除 `.obsidian/`、`copilot/` 等）| **未建** |
| `paper/black/neurips_2026.tex` 编译验证 | 未跑 latexmk |
| `pip install -e PROJECT/black` 可装性验证 | 未跑 |
| pre-commit hook（ruff / black / pytest）| 未配 |
| CI（GitHub Actions）| 未配 |

---

## 4 · 下一步建议（按优先级）

### P0 · 本周必做

1. **Theorem 3 修订**：把 `Docs/proof/Theorem 3 *.md` 迁到 `Docs/black/proofs/thm3.md`，按 critique 6 项修订符号 + 5 项漏洞补丁
2. **paper/black/ latexmk 编译**：确保现在的占位骨架能编出 PDF（即使所有内容都是 `\todo{}`），把"工程编译"从未知风险变成已验证

### P1 · 本周努力做

3. **`pdes/burgers.py` 实装**：Godunov + WENO5 ground truth 生成器（不超过 200 行 Python）
4. **`models/score_baseline.py` 实装**：1D U-Net + EDM 标准去噪头，作为 E1 baseline

### P2 · 下周（W3）

5. Theorem 1 + 2 证明定稿
6. `models/score_bvaware.py` 核心创新实装
7. E1 跑通（哪怕初版还很粗）

### 不要做的事

- ❌ 写新讲义（用户已决定跳过）
- ❌ 直接进 E5（plasma）— 那是 rebuttal 加分项
- ❌ 把 Theorem 3 推迟到所有实验之后 — 它是命门，必须 W4 末定稿

---

## 5 · 风险与阻塞（人话版）

| 风险 | 详情 | 应对 |
|---|---|---|
| **理论证不出** | Theorem 3 是论文卖点；如果指数因子 $\exp(\Lambda)$ 干不掉，论文价值大幅缩水 | 用户已主动迭代到 v2；保留"退而求次证 $\exp(\Lambda/2)$"的 fallback；最坏情况转投 ICLR 给更多时间 |
| **时间紧** | 12 周里有大约 10 周可用；3 个实验 + 5 个 theorem + 9 页正文 + 25 页 appendix | E1+E2 锁定必做，E3 努力做，E4/E5 留 rebuttal；理论章节做厚换实验数量 |
| **审稿人是 baseline 作者** | DiffusionPDE / FunDPS 作者大概率是 reviewer | 主实验直接用他们的公开代码 + 数据当 baseline，杜绝实验细节挑刺 |
| **AI 喊"完成"** | 之前 commit message 用了 "完成"、"task done" 字样导致 over-claim | 本次起：commit 用"做了什么"动词；进度对账 REPORT；MEMORY R8 监控 |

---

## 6 · 历史里程碑

| 日期 | 事件 |
|---|---|
| 2026-04-21 | 项目初始化（commit `2099801`），16 篇 baseline PDF 备齐 |
| 2026-04-25 | 完成路径 A 第一性原理解读 + 方法骨架；用户开始 Theorem 3 草稿 |
| **2026-04-26** | 路径 A 决策；paper / PROJECT 工作区基础设施搭建（5 commits 合并到 main）；MISSION/CLAUDE/MEMORY/REPORT 四件套体系建立 |
| 2026-04-26 晚 | MISSION 瘦身、CLAUDE 吸收持续性内容、新增 REPORT；任务范式从"讲义"切换到"撰写+实验" |
| W3-W12 | （未来）见 `CLAUDE.md §12 周时间表` |
