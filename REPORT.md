# REPORT · 项目进度报告

> **阅读对象 · 人**（用户、合作者、导师；可直接给人看）。
> **AI 的状态 / 决策日志在 `MEMORY.md`，规则在 `CLAUDE.md`，当前指令在 `MISSION.md`。**
> **更新节奏**：与 MEMORY 同节奏（重大决策 / 里程碑 / 阶段切换）。
> **上次更新**：2026-04-29

---

## 1 · 30 秒摘要

项目代号 **EntroDiff**，目标 NeurIPS 2026 主会双盲投稿。核心方法：利用扩散模型 score 场自身是 Burgers 方程这一恒等式（Score Shocks），设计 BV-aware score 参数化 + 熵正则 + 粘性匹配调度，对 Kruzhkov 熵解达到 $W_1 \le \mathcal{O}(\varepsilon^{1/2})$ 收敛率（去除 $\exp(\Lambda)$ 指数放大）。

**标题**：*EntroDiff: Taming Hyperbolic Shocks via Double-Burgers Coupling*

**当前状态**：论文主体完成；代码 MVP 已跑通（数据生成 + 10 epoch 训练产出 checkpoint）；**缺少评估 / 可视化脚本**，E1 实验尚未完整闭环。

**整体完成度估计**：

| 维度 | 完成度 | 备注 |
|---|---|---|
| 决策 / 选题 | **100%** | 路径 A 锁定，投稿目标 NeurIPS 2026 双盲不变 |
| 论文写作（正文） | **~82%** | §1–§4 全实写；§5 (§7 Experiments) 和 §6 (§8 Conclusion) 仍 `\todo` |
| 论文写作（附录） | **~85%** | A1 5 大定理证明全英文完成；A2/A3 占位 |
| 编译就绪 | **100%** | 所有宏包补齐，节号冲突修复，中文→英文翻译完成 |
| 代码实现 | **~40%** | **8 个源文件全实写**（UNet1D / StandardScore / BVAwareScore / losses / schedules / sampler / Godunov solver / dataset）；2 个工作脚本（generate_data.py / train_mvp.py）；**缺 eval 脚本** |
| 实验 | **~15%** | **E1 Burgers：数据 246MB 已生成，训练 10 epoch 产出 2 个 checkpoint**；无 eval 无指标无图表；E2/E3 未启动 |

**最近一次里程碑**（2026-04-29）:
- **代码 MVP 跑通**：数据生成（Burgers Godunov 1D, 5000 samples × 128 grids, 246MB）→ 10 epoch 训练（EDM denoiser + viscosity-matched schedule + L_DSM + λ_BV * TV）→ 产出 2 个 checkpoint（epoch 5/10, 各 ~7.7MB）
- **8 个核心源文件全部实写**（非 `raise NotImplementedError`）：`unet_1d.py` / `score_param.py` (Standard+BVaware) / `schedules.py` / `losses.py` (DSM+BV+Godunov flux) / `samplers.py` (Heun + Algorithm 1 骨架) / `burgers_1d_solver.py` / `burgers_dataset.py` / `env_manager.py`

**历史里程碑**（2026-04-28）:
- 论文从 6-section(原8节) 精简为 6-section 结构：`01_intro` / `02_related_work` / `03_method` / `04_theory` / `05_experiments` / `06_conclusion`
- `\input` 文件名同步更新；节内注释头部与内部 `§x.y` 引用全部对齐
- `proofs/thm3_proof.tex` 全文件从中文翻译为英文（定理陈述 + A0–A6 假设体系 + 四阶段证明 + 三份附录）
- 编译依赖补全：`algorithm` / `algpseudocode` / `stmaryrd`
- `\item[$...$]` 中括号嵌套冲突修复（2 处）
- 标题改为 `EntroDiff: Taming Hyperbolic Shocks via Double-Burgers Coupling`

---

## 2 · 已完成（详细）

### 2.1 决策与方法论

| 事项 | 状态 | 产物 |
|---|---|---|
| 投稿目标确认（NeurIPS 2026 双盲） | ✓ | `CLAUDE.md` |
| 方法骨架（5 大定理 + 12 周时间表） | ✓ | `Docs/black/path_A_method_skeleton.md` |
| 论文结构精简（8→6 节） | ✓ | 删除 03_preliminaries、04_double_burgers；合并入 §2、§4 |

### 2.2 论文正文 — 全英文散文（除 `\todo` 占位外）

| Section | 文件 | 完成度 | 说明 |
|---|---|---|---|
| §1 Introduction | `sections/01_intro.tex` | **100%** | 三段式 Gap / Insight / Contribution + (C1)(C2)(C3) 列表 |
| §2 Related Work + Background | `sections/02_related_work.tex` | **100%** | 4 组 related work + 3 段 Background（VE-SDE / 双曲 / W & BV） |
| §3 Methodology | `sections/03_method.tex` | **100%** | §3.1 Viscosity-matched schedule + §3.2 BV-aware parameterization + §3.3 Loss family (含 `tab:loss-family`) + §3.4 Sampler (含 Algorithm 1 + Godunov flux) |
| §4 Theory Analysis | `sections/04_theory.tex` | **100%** | §4.1 桥段 + 5 个 Theorem statement + 5 段 proof sketch（全散文，不超 15 行/段） |
| §5 Experiments | `sections/05_experiments.tex` | **~5%** | 8 处 `\todo` 占位 + 空 figure/table 壳子 |
| §6 Conclusion | `sections/06_conclusion.tex` | **~10%** | 3 处 `\todo` 占位；限制/future work 骨架已写 |

### 2.3 论文附录

| 附录 | 文件 | 完成度 | 说明 |
|---|---|---|---|
| A1 Proofs | `sections/A1_proofs.tex` + `proofs/thmN_proof.tex` (×5) | **100%** | Theorem 1–5 完整 LaTeX 证明，全部英文 |
| A2 Extra Experiments | `sections/A2_extra_experiments.tex` | 0% | E4/E5 留 rebuttal；3 处 `\todo` |
| A3 Implementation Details | `sections/A3_implementation_details.tex` | 0% | 架构/超参/计算；4 处 `\todo` |

**各定理证明详情**：

| Theorem | 文件 | 内容 | 语言 |
|---|---|---|---|
| Thm 1 (Double-Burgers coupling) | `proofs/thm1_proof.tex` | Part A Score Burgers + Part B Physical Transport + Part C Shock Co-location；Hausdorff 收敛 | EN ✓ |
| Thm 2 (Stability, baseline rate) | `proofs/thm2_proof.tex` | 9 步 Gronwall + (A1)–(A5) 假设体系 + 测度修复 + PDE 关联 | EN ✓ |
| **Thm 3** ⭐ (Improved rate $\varepsilon^{1/2}$) | `proofs/thm3_proof.tex` | A0–A6 假设体系 + Stage 1 函数空间分解 + Stage 2 单侧Lipschitz+Gronwall + Stage 3 Kruzhkov $L^1$收缩 + Stage 4 Wasserstein组装 + 附录 A/B/C | **EN ✓**（2026-04-28 全文翻译） |
| Thm 4 (Shock-location admissibility) | `proofs/thm4_proof.tex` | Part I 粘性匹配几何对应 + Part II 弱形式极限 + Part III Lax 熵条件 | EN ✓ |
| Thm 5 (JKO correspondence) | `proofs/thm5_proof.tex` | 6 步 JKO 推导（连续性方程→速度场→熵变分→PDE约束→自由能梯度→JKO离散） | EN ✓ |

### 2.4 编译基础设施

| 事项 | 状态 |
|---|---|
| `neurips_2026.tex` 主控 | ✓ `\input` 文件名全部与实际文件一致（01→06） |
| `neurips_2026.sty` | ✓ 官方模板 |
| `macros/notation.tex` | ✓ 全部宏落地，与 skeleton §3.1 对齐 |
| 缺失宏包 | ✓ `algorithm` / `algpseudocode` / `stmaryrd` 已补 |
| `\item[...]` 中括号冲突 | ✓ `proofs/thm3_proof.tex` 2 处已加花括号隔离 |
| `\llbracket` / `\rrbracket` | ✓ `stmaryrd` 提供 |
| 编译测试 | 待用户在 Overleaf 验证 |

### 2.5 代码工作区（`PROJECT/black/`）

| 模块 | 状态 | 关键函数 |
|---|---|---|
| `src/data/burgers_1d_solver.py` | ✓ Godunov 1D 有限体积求解器 | `burgers_godunov_1d()` |
| `src/data/burgers_dataset.py` | ✓ PyTorch Dataset（80/10/10 切分） | `BurgersDataset` |
| `src/models/unet_1d.py` | ✓ 轻量 1D U-Net（4 层下/上采样，~0.4M 参数） | `UNet1D` |
| `src/models/score_param.py` | ✓ StandardScore（EDM preconditioning）+ BVAwareScore（tanh 骨架，grad 暂用 proxy） | `StandardScore`, `BVAwareScore` |
| `src/diffusion/schedules.py` | ✓ BaselineSchedule + ViscosityMatchedSchedule（σ²=2ντ） | `ViscosityMatchedSchedule` |
| `src/diffusion/losses.py` | ✓ DSM loss + BV (TV) loss + Godunov flux + PDE residual | `get_dsm_loss`, `get_bv_loss`, `godunov_flux`, `pde_residual` |
| `src/diffusion/samplers.py` | ✓ Heun 二阶 ODE 采样器（含 Godunov PDE guidance proxy） | `entrodiff_heun_sampler` |
| `src/utils/env_manager.py` | ✓ 单例 env 管理器（自动 fallback） | `env` |
| `scripts/generate_data.py` | ✓ 跑通，生成 246MB `.npy` | — |
| `scripts/train_mvp.py` | ✓ 跑通，10 epoch ~7.7MB checkpoint | — |
| **scripts/eval_viz.py** | **缺** | — |

> **注**：REPORT 上一版（2026-04-28）误称所有核心函数 `raise NotImplementedError` —— 这是过时信息。实际上述全部实写并可运行。

### 2.6 元数据

| 文件 | 状态 |
|---|---|
| `MISSION.md` | ✓ |
| `CLAUDE.md` | ✓ 含 12 周时间表 |
| `MEMORY.md` | ✓ §A–G 完整 |
| `REPORT.md`（本文件） | ✓ 本次全面更新 |
| `paper/black/CONVENTIONS.md` | ✓ 本次同步修正（序号 01..08→01..06；proofs 后缀 .md→.tex） |

### 本轮产出摘要（2026-04-28 W3）

| 文件 | 状态 |
|---|---|
| `sections/01_intro.tex` | ✓ 精修（强化 GAP 诊断、符号统一） |
| `sections/02_related_work.tex` | ✓ 精修（VE-SDE 链补全、宏统一） |
| `sections/05_method.tex` | ✓ **完整实写**（4 子节 + Table 1 + Algorithm 1） |
| `sections/06_theory.tex` | ✓ proof sketch 全实写（5 段思想线 + 附录 ref） |
| `sections/A1_proofs.tex` | ✓ 5 定理完整 LaTeX 证明（5 子文件 + 主控） |
| `proofs/thm1_proof.tex` | ✓ 290 行 |
| `proofs/thm2_proof.tex` | ✓ 391 行 |
| `proofs/thm3_proof.tex` | ✓ 635 行（主定理，待用户 review） |
| `proofs/thm4_proof.tex` | ✓ 357 行 |
| `proofs/thm5_proof.tex` | ✓ 471 行 |
| `macros/notation.tex` | ✓ 11 个 `[planned]` 宏全部落地 |
| `SYMBOL.md` | ✓ 同步更新 |
| `PLAN/W3_sections_refine_plan.md` | ✓ 新计划 |
| `REPORT.md` / `MEMORY.md` | ✓ 全面刷新 |

---

---

## 3 · 未完成（详细）

### 3.1 论文写作：剩余 `\todo` 共 18 处

| 文件 | `\todo` 数量 | 内容 |
|---|---|---|
| `sections/05_experiments.tex` | 8 | Setup / E1 / E2 / E3 / Ablation 段落正文 + Figure caption + Table caption |
| `sections/06_conclusion.tex` | 3 | Conclusion 段，Limitations 段，Future work 段 |
| `sections/A2_extra_experiments.tex` | 3 | E4 / E5 / Extended ablations |
| `sections/A3_implementation_details.tex` | 4 | Architecture / Training / Sampling / Compute |

此外 abstract 仍为注释占位，需在 W10 实写。

### 3.2 references.bib

- 6 篇核心 PDF 已校验封面：huang2024diffusionpde / yao2025fundps / sarkar2026scoreshocks / albergo2025interpolants / bhola2025fmo / armegioiu2026chaotic
- 其余 key 仍 TODO（提交前用 arXiv API 批量填充）

### 3.3 代码实现

**已完成（8 模块 + 2 脚本）**，详见 §2.5。已知缺口：

| 缺口 | 详情 |
|---|---|
| `scripts/eval_viz.py` | **缺** —— 无法加载 checkpoint 跑采样 + 出对比图 |
| `BVAwareScore` 梯度实现 | 当前用 proxy 加法代替 `torch.autograd.grad` 的真梯度；需补 `create_graph=True` 版本 |
| `entrodiff_heun_sampler` PDE guidance | 当前用 `pde_residual` 直接作方向 proxy（非严格 `∇_u L_PDE`）；需补 autograd 真梯度版 |
| 测试 stubs | 0 个 pytest 测试 |
| Ablation 脚本 | **缺** —— 无法跑 schedule / loss / param 消融实验 |
| E2/E3 数据和训练 | 未启动 |

### 3.4 实验

| 实验 | 数据 | 训练 | 评估 | 图表 |
|---|---|---|---|---|
| **E1 · Inviscid Burgers** | ✓ 246MB, 5000 samples, Nx=128 | ✓ 10 epoch, 2 ckpt | **缺** | **缺** |
| E2 · Buckley–Leverett | 0% | 0% | 0% | 0% |
| E3 · 1D Euler / Sod | 0% | 0% | 0% | 0% |
| E4/E5 (rebuttal) | 0% | 0% | 0% | 0% |

> **当前真实位置**：E1 数据就绪 + 模型训练完毕，但**没有评估脚本** → 无法获取 `W_1` / `L¹` / shock-location error 等指标，**还不能声称"E1 实验完成"**。

### 3.5 工程基础设施

| 项 | 状态 |
|---|---|
| 仓库根 `.gitignore` | 未建 |
| `pip install -e PROJECT/black` 可装性 | 未验证 |
| pre-commit / CI | 未配 |
| 全文 `grep \todo` 清零 | 18 处待清除 |
| checklist.tex 回答 | 全部 `\answerTODO` |

---

## 4 · 下一步建议（按优先级）

1. **写 `scripts/eval_viz.py`**（最高优先级）：加载 epoch 10 checkpoint → 对 test split 采样 → 出 shock 对比图 + 算 `W_1` / `L¹` → 把第一张 Burgers shock 对比图放进论文
2. **§5 (§7) Experiments 实写**：等 eval 跑出数字后，把 `\todo` 占位替换为真实 Setup 描述 + E1 结果 + Figure 2 caption
3. **§6 (§8) Conclusion 实写**：conclusion + limitations + future work
4. **Overleaf 编译验证**：上传到 Overleaf，验证无错误
5. **BVAwareScore 梯度真值化**：替换 proxy 为 `torch.autograd.grad(create_graph=True)`
6. **references.bib 补全**：填充所有 `\citep` 引用的 bib entries
7. **消融实验**（E1 闭环后）：schedule 消融 / loss term 消融 / parameterization 消融
8. **E2 Buckley–Leverett**：下一 PDE

> **当前瓶颈**：没有 eval 脚本 → 没有指标 → 论文 §5 不能写真实数字 → 全文 `\todo` 无法清零

---

## 5 · 风险与阻塞

| 风险 | 详情 | 应对 |
|---|---|---|
| **实验时间紧** | §3/§4 理论写完后，实验仍是 0% | E1+E2 锁定必做；E3 努力做；理论章节做厚换实验数量 |
| **审稿人是 baseline 作者** | DiffusionPDE / FunDPS 作者大概率审稿 | 主实验直接用他们的公开代码 + 数据当 baseline |
| **references.bib 缺条目** | 正文引用了但 bib 无 entry 会导致编译警告 | 提交前一次性批量填充 |
| **未验证编译** | 本地无 LaTeX 环境，依赖 Overleaf | 尽快上传验证 |

---

## 6 · 历史里程碑

| 日期 | 事件 |
|---|---|
| 2026-04-21 | 项目初始化，16 篇 baseline PDF 备齐 |
| 2026-04-25 | 完成路径 A 第一性原理解读 + 方法骨架 |
| **2026-04-26** | 路径 A 决策；paper / PROJECT 工作区基础设施搭建；MISSION/CLAUDE/MEMORY/REPORT 四件套建立 |
| 2026-04-26 晚 | 首次进入论文实写：§1/§2 实写；删除 03/04 独立 section；references.bib 校验 6 篇 |
| **2026-04-28 (W3)** | §3 Method 完整实写（Algorithm 1 + Godunov flux）；§4 Theory 5 段 proof sketch 实写；A1 5 大定理 LaTeX 迁入；notation.tex 11 个宏落地 |
| **2026-04-28 (会后)** | 论文结构精简（8→6 section）；`\input` 文件名修复；thm3_proof.tex 全文中译英；编译依赖补全；标题改为 `EntroDiff: Taming Hyperbolic Shocks via Double-Burgers Coupling`；REPORT 全面更新 |
| **2026-04-29 (W4)** | **代码 MVP 首次跑通**：8 源文件全实写 → 数据生成 (246MB) → 10 epoch 训练 (2 ckpt)；REPORT/MEMORY 进度刷新（纠正 2%→40% 的过时信息）

---

## 7 · 规则修正记录（本次 REPORT 更新同步）

| 旧规则 | 新规则 | 原因 |
|---|---|---|
| CONVENTIONS.md "序号 01..08" | "01..06" | 正文已精简为 6 节 |
| CONVENTIONS.md "proofs/\<thmN\>.md" | "proofs/thmN_proof.tex" | 实际已为 LaTeX 文件 |
| REPORT §7.2 "proof sketch ≤ 12 行" | "proof sketch 只写思想线，不写技术细节" | 行数限制过于机械；实际从 4–15 行不等均可，关键是读者读完能拿到陈述+杠杆+位置三件事 |

