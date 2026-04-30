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
- 注释只能增加，不能减少！！！详细的颗粒度，把关键行的目的都要点出来！

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
prompt	>	MISSION.md  >  CLAUDE.md  >  MEMORY.md  >  ~/.claude/CLAUDE.md (全局)
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

---

## 注意事项补充清单（**给下次会话的 AI 用**）

> **2026-04-26 晚定**。

### 不要做的事（别忘）

- ❌ 本地编译 LaTeX（用户用 Overleaf；CLAUDE.md §LaTeX 编译工作流）
- ❌ 写新讲义
- ❌ 自动合并 main
- ❌ 随意发明新 loss / schedule / 架构，未在论文 §3 (§5) 中描述的一律不写

### 建议做的事

- ✅ 任何任务遇到大不确定，**停下问用户**（CLAUDE.md "90% 把握再行动"），使用askquestion功能
- ✅ 用 sub-agent + worktree 并行修订各阶段
- ✅ 完成后跑 merge dry-run，等用户审批
- ✅ 同步刷新 REPORT.md + MEMORY.md（二者强制更新）

---

## W4 实验代码开发专项协议 (给代码 AI 的指令)

> **当前阶段核心目标**: E1 Burgers 实验完整闭环——从 "数据+训练 done" 推进到 **"出图+出表+填论文 §5"**。
>
> **现状**（2026-04-29）请读 `REPORT.md` → 简版如下：
> - ✅ 8 核心源文件全实写（UNet1D / StandardScore / BVAwareScore / schedule / loss / sampler / solver / dataset）
> - ✅ `generate_data.py` 跑通（Burgers 1D, 5000 samples, Nx=128, ~246MB）
> - ✅ `train_mvp.py` 跑通（10 epoch, 2 ckpt at epoch 5/10, ~7.7MB each）
> - ❌ **无 eval 脚本** → 无指标 / 无图表 / 论文 §5 `\todo` 填不了
> - ❌ **无 pure EDM baseline 训练** → 无法出 "EDM vs Ours" 对比图
> - ❌ **BVAwareScore 梯度 proxy**（真 autograd 未接）
> - ❌ **Godunov PDE guidance proxy**（直接残差而非 ∇L_PDE）

### 1. 角色设定
- **扮演角色**：Zongyi Li（李宗沂，Caltech / NVIDIA，FNO 核心一作）。
- **扮演理由**：拥有 AI4PDE 领域最顶级的工程落地能力（参考 `neuraloperator` 库），编码风格严谨、数学推导扎实，能够在保障工业级代码规范的同时完美复刻前沿数学方程。

### 2. 第一阶段（本 session · 必须完成）—— E1 Burgers 出图闭环

#### 2.1 `scripts/eval_viz.py` — 评估 + 可视化（**最高优先**）
直接新建文件，不要改已有代码。

**功能要求**：
1. 加载 epoch 10 checkpoint（`output_dir / mvp_run / entrodiff_mvp_ep10.pt`）
2. 构建 `StandardScore` 模型 + `ViscosityMatchedSchedule(nu=0.01)`
3. 从 `BurgersDataset(test)` 取 test split 的 ground truth
4. 用 `entrodiff_heun_sampler`（已有）跑反向采样生成解
5. 计算三个指标：**W₁**、**L¹ relative error**、**shock-location error**（shock 位置 = max |grad| 的 x 坐标）
6. 出图并存 `Output/black/experiments/mvp_run/`：
   - `e1_shock_comparison.png` — 上：ground truth 线 + 生成线；下：逐点误差
7. 打印指标摘要到 stdout

#### 2.2 `scripts/train_baseline.py` — 纯 EDM baseline 训练
**目的**：必须有一个不使用 viscosity-matched schedule 和 BV loss 的纯 EDM 对比线。

**实现方式**：
- 从 `train_mvp.py` 拷贝框架
- 将 `ViscosityMatchedSchedule` 换为 `BaselineSchedule`（EDM 标准 log-normal sigma 采样）
- 将 loss 改为仅 `L_DSM`（删掉 `lambda_bv * L_BV`），保持其他超参对齐（epochs=10, lr=2e-4, batch_size=64）
- 保存 checkpoint 到 `output_dir / mvp_baseline /`

#### 2.3 eval_viz 扩展——baseline vs ours 对比图
在 eval_viz.py 中同时加载 baseline ckpt 和 ours ckpt，出三栏对比图：
- 左：ground truth（test split 某条曲线）
- 中：EDM baseline 生成
- 右：EntroDiff 生成
→ 保存 `e1_baseline_vs_ours.png`

### 3. 第二阶段（可本 session 或下一 session）——梯度真值化

#### 3.1 BVAwareScore 真梯度
文件 `src/models/score_param.py:55–82`，当前是用 `phi_sm + (kappa/2)*tanh*phi_sh` 的 proxy 加法。
**正确实现**：
```python
x.requires_grad_(True)
phi_sm = self.phi_sm_net(x, sigma.log()/4.0)
phi_sh = self.phi_sh_net(x)
kappa  = self.kappa_net(x) + 1e-4
tanh_factor = torch.tanh(phi_sh / (2 * sigma**2 + 1e-6))

# 真梯度：必须 create_graph=True，因为 loss 会对 s_theta 再求导
grad_phi_sm = torch.autograd.grad(phi_sm.sum(), x, create_graph=True)[0]
grad_phi_sh = torch.autograd.grad(phi_sh.sum(), x, create_graph=True)[0]
s_theta = grad_phi_sm + (kappa / 2.0) * tanh_factor * grad_phi_sh
```

#### 3.2 Sampler Godunov guidance 真梯度
文件 `src/diffusion/samplers.py:38–46`，当前用 `pde_residual(u_tau, dx)` 直接作方向 proxy。
**正确实现**：
```python
loss_pde = pde_residual(u_tau, dx).pow(2).mean()
grad_u = torch.autograd.grad(loss_pde, u_tau)[0]
# 用 grad_u 替代 l_pde_t 作为 guidance direction
```

### 4. 第三阶段（远期）——消融实验 + E2/E3
- 消融脚本：schedule 消融 / loss term 消融 / parameterization 消融（等 E1 完全闭环后）
- E2 Buckley–Leverett：新 solver + 数据生成 + 训练
- E3 Euler Sod：三组分系统

### 5. 环境与硬件约束
- **PC 端 RTX 4060**（算力/显存有限），所有代码必须在 <8GB 显存下运行
- **Windows**：`num_workers=0` 避免 multiprocessing 报错
- **配置解耦**：`configs/env_config.yaml`（不 commit），绝对路径绝不写死

### 6. 论文对齐规则（强制）
- **所有 Loss / schedule 代码注释必须引用论文公式编号**（如 `Eq. 3.2`、`Algorithm 1 line 5`）
- `train_mvp.py` 已对齐的注释标准保持不降
- 不要随意发明新 loss / 新 schedule 未经论文背书
- 任何架构改动先读 `paper/black/sections/03_method.tex` 确认是否已在论文中描述

### 7. 代码规范（继续）
- **注释只增不删**，新注释用中文
- 函数/类用 type hints
- 执行脚本有细颗粒度注释（行级，不仅函数级）
- Commit 原子化：一个子任务一个 commit，message 用 `feat(scripts): ...` 格式
- 分支命名：`feat/eval-viz-YYYYMMDD` 等

---

## W4 实验发现与后续策略 (2026-04-29 更新)

### 关键实验发现

**1. 少步数优势** ⭐ 可作论文亮点
- BV-aware 在 25 Heun 步下 W₁=0.719, 优于 baseline 50 步的 0.734
- **少步数 + BVAwareScore = 超过半数步数 Baseline** — 证明建筑先验减少了对多步去噪的依赖
- 机制: tanh(φ_sh/2σ²) 硬编码了 interfacial profile, 网络无需多步迭代来"学习" shock 形状

**2. PDE guidance 状态**
- Godunov 真梯度已实现, 梯度裁剪修复了 NaN
- 但无条件采样时 PDE guidance 推往 u≡0 (trivial solution), 对 W₁ 无益
- 正确用途: 条件生成 / 逆问题 (给定观测点, PDE guidance 保证解的物理一致性)

**3. BVAwareScore vs StandardScore**
- BVAwareScore (7.7M, dim=128, 200ep) 比 StandardScore (0.4M, 50ep) 的 W₁ 仅改善 ~3%
- 主因: 模型仍未学透 Burgers 分布 → 下一步需 (a)更大模型 (b)时间信息 (c)更多数据

### E2 Buckley–Leverett 规划 (本地开发)
- 目标: 非凸通量 f(u)=u²/(u²+(1-u)²), 产生 shock + rarefaction 混合波
- Baseline 中央差分在 rarefaction 处表现更差 — 预期拉开差距
- 需要: 新 Godunov solver, 新 dataset, 新 config
- 工程量: 中等 (~200 行新代码 + 1 天训练)
- 在本地 PC 进行, 不占用服务器

### 时间信息 Loss 路线图
- **轻量版** (推荐): dataset 返回 (u(tₙ), u(tₙ₊₁)), loss += ‖ûₙ₊₁ - Godunov_step(uₙ)‖²
  - 改动量: ~30 行 (dataset + loss)
  - 不改变模型架构
- **重量版**: L_Burg = ‖∂τ s + 2s·∇u s - Δu s‖²
  - 需要 score 的 Hessian, 工程量大的数据重构
  - 留 Phase 3

### 论文写作状态
- ✅ E1 实验完整闭环 (数据 → 训练 → eval → 出图)
- ✅ E2 Buckley-Leverett solver+数据+StandardScore 训练完成
- ✅ E3 Euler Sod + E4 Shallow-Water solver+数据 代码就绪
- ❌ §5 Experiments 实写中 (setup+E1 已写, E2/E3 待填入)
- ❌ §6 Conclusion 仍 todo

---

## W5 Foundation Model 开发协议 (给代码 AI 的指令)

> **当前阶段核心目标**: 构建跨 PDE 的 Foundation Model — 一个模型解决 Burgers / Buckley-Leverett / Euler Sod / Shallow-Water 等多类双曲 PDE，使用 DiT backbone + PDE embedding + mixed-batch 训练。

### 1. 角色设定
- **扮演角色**：Zongyi Li（李宗沂，Caltech / NVIDIA，FNO/DiT 架构设计）
- **扮演理由**：AI4PDE 工程落地第一人；DiT 架构设计经验 + 多 PDE 训练范式

### 2. Foundation Model 架构设计

#### 2.1 DiT-1D Backbone（替代 UNet）
```
Input: [noisy_u (1) | IC (1) | PDE_type (1)] → 3 channels
  ↓ Patch Embedding: Nx=256 → 32 patches × 8, linear project → D=512
  ↓
× N_layers DiT Block:
  AdaLN( time_emb | PDE_emb ) → Self-Attention → AdaLN → MLP
  ↓
Unpatchify → denoised_u (1 channel)
```

**组件**：
- **PDE Token**: 可学习 embedding `(n_pde_types, D)`，类似 ViT class token
- **AdaLN**: time embedding + PDE embedding 联合调控 scale/shift
- **Patch Size**: 可配置 (PC=16, 服务器=8, H100=4)

#### 2.2 多规模配置 (PC → H100)

| 规模 | dim | layers | heads | patch | 参数量 | 目标硬件 |
|---|---|---|---|---|---|---|
| `tiny` | 256 | 6 | 4 | 16 | ~5M | 单卡 RTX 4060 (PC) |
| `small` | 512 | 8 | 8 | 8 | ~30M | RTX 3090×1 |
| `base` | 768 | 12 | 12 | 8 | ~100M | H100×1 |
| `large` | 1024 | 24 | 16 | 4 | ~400M | H100×4-6 |

**所有规模共享同一代码**，仅通过 YAML 切换。config 示例：
```yaml
model:
  type: "dit"
  scale: "small"  # tiny | small | base | large
  dim: 512
  n_layers: 8
  n_heads: 8
  patch_size: 8
  dropout: 0.1
```

#### 2.3 混合 PDE 训练
- 数据加载器轮流采样 Burgers / BL / Euler 的 batch
- PDE type token 按 sample 注入
- Loss = L_DSM + λ_BV·L_BV + λ_time·L_time（复用现有 loss）
- 统一 pad 所有 PDE 到相同 Nx（如 256）

### 3. 开发任务清单（按优先级）

- [ ] `src/models/dit_1d.py` — DiT-1D backbone (PatchEmbed + DiTBlock + AdaLN + Unpatch)
- [ ] `src/models/foundation_score.py` — FoundationScore wrapper (替代 StandardScore/BVAwareScore, 输出 D_x)
- [ ] `src/data/mixed_pde_dataset.py` — 混合 PDE 数据加载器 (交替采样 + PDE type 标记)
- [ ] `scripts/train_foundation.py` — 混合训练脚本 (支持 grad accumulation, mixed precision)
- [ ] `configs/foundation/` — 多规模配置 (tiny/small/base/large)
- [ ] `scripts/eval_foundation.py` — 跨 PDE 评估脚本
- [ ] 微调接口: `--finetune` + `freeze_backbone` 支持零样本适配新 PDE

### 4. 服务器部署计划
- 当前服务器 (3×RTX 3090): 跑 `small` 规模混合训练
- H100 到货后: 跑 `base/large` 规模, batch_size=256
- tmux 管理: 每个实验独立 tmux session

### 5. 论文对齐
- Foundation model 对应论文 §5.4 "Transfer across conservation laws"
- DiT 架构选择在 §3.2 中解释为 "modern diffusion backbone replacing UNet"
- 跨 PDE 泛化能力作为 Claim 2 的实证


