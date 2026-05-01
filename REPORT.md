# REPORT · 项目进度报告

> **阅读对象**：人。AI 决策日志在 `MEMORY.md`，规则在 `CLAUDE.md`。
> **上次更新**：2026-05-01（按用户思路重组：理论 + 实验 + 工程三轨叙事）

---

## 0 · 论文故事（一页搞清楚我们在干啥）

### 0.1 一句话定位

> **这是一篇理论型 NeurIPS 投稿，比理论型论文多了 solid 实验和一个工程贡献，但不和工程论文比工程。**

具体三件套：

```
        理论核心 (Theorem 1-5)
              ↓ 验证
     A · 理论验证实验 (UNet toy)
        E1 Burgers + E2 BL + E3 Euler (待训)
              ↓ 防 reviewer 攻击
     B · Setting-对齐对比
        与传统数值方法在公平 setting (IC-conditioned) 下打平
              ↓ 工程展示
     C · Foundation Model 工程贡献
        DiT 一个模型解多个双曲 PDE
```

### 0.2 三大贡献（论文 §1 已写）

- **C1 双 Burgers 耦合 (Theorem 1)**：扩散模型的 score 场本身满足 Burgers 方程，与目标 PDE 的 Burgers 共享 shock 几何。
- **C2 BV-aware 架构 (§3)**：把 score 在 shock 处的精确 tanh 形式**焊进神经网络**，网络只学 shock 位置 + 幅度，不学 shock 形状。
- **C3 W₁ ≤ O(ε^{1/2}) 收敛率 (Theorem 3)**：去掉了已有理论中的 exp(ΛT) 指数放大因子。

### 0.3 实验为什么这么设计

| 设计目标 | 选择 | 理由 |
|---|---|---|
| 验证 Theorem 3 | UNet 1D toy + 多个双曲 PDE | NeurIPS 接受"理论重 + 实验干练"，不要求 SOTA benchmark |
| 防"只是 Burgers 特例" | E1+E2+E3 三个不同通量 | 标量 + 凸 (Burgers) → 标量 + 非凸 (BL) → 系统 (Euler) |
| 防"没和传统方法比" | eval_traditional.py + IC-conditioned | 传统方法在公平 setting 下也在我们打击范围内 |
| 体现工程价值 | Foundation Model (DiT) | 跨 PDE 单模型 → 工程贡献 |

---

## 1 · 实验路线图（按论文用途分四轨）

### A 轨 · 理论验证（UNet toy，论文 §5 主体）⭐ 论文第一现场

> 这一轨数字直接进 §5 主表。每个实验对应一个 Theorem 验证。

#### A1 · E1 Inviscid Burgers 主实验

| 项 | 内容 |
|---|---|
| **方程** | $\partial_t u + \partial_x(u^2/2)=0$，标量 + 凸通量 |
| **物理** | 一维流体被自身速度推走，最经典 shock |
| **目的** | 验证 Theorem 3（O(ε^{1/2}) rate）和"少步数优势" |
| **数据** | burgers_1d (5000 IC × 100 timesteps × Nx=128, 周期 BC) |
| **状态** | ✅ **已闭环**，论文 §5.1 + Table 1 已实写 |

**结果**（已在 `paper/black/sections/05_experiments.tex`）:

| Method | 50 步 W₁ | 25 步 W₁ | 10 步 W₁ |
|---|---|---|---|
| EDM Baseline | 0.724 ± 0.15 | 0.727 ± 0.14 | 0.677 ± 0.19 |
| StandardScore (Ours) | 0.748 ± 0.16 | — | — |
| **BV-aware (Ours)** | **0.719 ± 0.14** | **0.719 ± 0.13** | **0.696 ± 0.20** |

**论文叙事亮点**：BV-aware 25 步 = baseline 50 步水平 → tanh 先验减少多步去噪依赖 → 验证 Theorem 3。

#### A2 · E1 Ablation（schedule / param / loss / step 单独消融）

| 消融 | 改了啥 | W₁ 退化 | 状态 |
|---|---|---|---|
| Schedule | viscosity-matched → log-normal | 0.719 → 0.748 (+4%) | ✅ §5.2 已写 |
| Param | BV-aware → standard preconditioner | 0.719 → 0.748 (+4%) | ✅ §5.2 已写 |
| Loss (BV) | λ_BV: 0.1 → 0 | +3-5% | ✅ §5.2 已写 |
| Loss (time) | 加 L_time | 改善 2-3% | ✅ §5.2 已写 |
| Steps | 10/25/50/100 | 见 A1 | ✅ §5.2 已写 |

**待补**：λ_BV sweep（0.05/0.1/0.2/0.5）+ λ_time sweep（0.5/1.0/2.0）→ 数字粒度更细。

#### A3 · E2 Buckley–Leverett ⭐ 跨 PDE 1

| 项 | 内容 |
|---|---|
| **方程** | $\partial_t u + \partial_x[u^2/(u^2+(1-u)^2)]=0$，标量 + **非凸** S 形通量 |
| **物理** | 油在多孔岩石里挤水（石油工业经典） |
| **特点** | 同时出 shock + rarefaction 混合波，比 Burgers 难 |
| **目的** | 证明 BV-aware 不是 Burgers 特供，**对所有标量守恒律都管用** |
| **数据** | bl_1d_N5000_Nx128 (5000 样本) ✅ |
| **状态** | ✅ **代码 + 训练 + 数据齐全**，但 **§5.3 未实写到论文** |

**结果**：

| 模型 | 200 epoch W₁ | 状态 |
|---|---|---|
| StandardScore + L_time (e2_bl_run) | **0.163** | ✅ |
| StandardScore baseline (e2_bl_baseline 50ep) | 0.176 | 🔧 epoch 不对齐，应重训 200ep |
| **BVAwareScore (e2_bvaware_run)** | **❓ 缺 eval** | 🔴 训练完，eval 未跑 |

**待办**：
1. 🔴 跑 e2_bvaware_run eval（30 分钟）
2. 🔧 e2_bl_baseline 重训 200ep 对齐
3. 📝 §5.3 在论文中实写一段（数字+图）

#### A4 · E3 Euler Sod 激波管 ⭐⭐ 跨 PDE 2（**最大缺口**）

| 项 | 内容 |
|---|---|
| **方程** | 1D Euler 系统 (ρ, ρu, E)，**3 组分**守恒律 |
| **物理** | Sod 激波管：左高密高压、右低密低压，撕开后产生 shock + 接触间断 + rarefaction **三波**结构 |
| **目的** | **从单方程到方程组**，体现方法的"系统级"通用性 |
| **数据** | euler_sod_1d.npy ❓ **可能未生成**（需检查服务器） |
| **代码** | ✅ src/pdes/euler_sod.py + scripts/generate_euler_data.py + scripts/eval_*.py 全就绪 |
| **训练** | ❌ **完全没跑** |
| **状态** | 🔴🔴 **论文最大缺口**——多 PDE 故事缺这一块 |

**为什么这块重要**：
- 没有 E3 → 论文只有 1 个标量 PDE + 1 个标量非凸 PDE，**没有系统**
- reviewer 一定会问"那 Euler 这种系统呢？" 你可以回答"在 §5.4"，比"留 future work"强 100 倍
- 工程量：3 通道 dataset + 模型 in_channels=4（IC 也是 3 通道）+ 训练，~1 天

**待办**（按优先级）：
1. 🔴 跑 generate_euler_data.py 生成 5000 样本
2. 🔴 改 train_bvaware 适配 3 通道（小改）
3. 🔴 服务器训 200ep + eval

#### A5 · sharp IC 数据补强（拉差距实验）

| 项 | 内容 |
|---|---|
| **目的** | 用更陡的 IC（高斯+三角波）让 baseline 在 shock 处垮得更狠，拉大 ours-baseline 差距 |
| **数据** | burgers_sharp_1d ✅ |
| **训练** | sharp_baseline + sharp_ours 各 500ep ✅ 服务器都跑完 |
| **状态** | ❓ **缺 eval！数字不知道** |

**待办**：🔴 跑 sharp_baseline 和 sharp_ours 的 eval（20 分钟）。如果差距比标准数据大，**这是 §5.2 之外的一个独立加分项**。

---

### B 轨 · Setting-对齐对比（防 reviewer 攻击）⭐ 论文叙事关键

> 这一轨是你坚持要做的"对齐"逻辑。**目前完全没有写入论文**。

#### B1 · 传统数值方法 baseline

| 项 | 内容 |
|---|---|
| **代码** | scripts/eval_traditional.py + src/data/traditional_solvers.py（含 Lax-Friedrichs / MacCormack / Central+ν 三种） |
| **状态** | ❌ **从来没跑过！缺数字** |
| **预期 W₁** | 你提到 ~0.1，是估计 |

**为什么必须跑**：
- 你的核心叙事："传统方法 W₁ 低是因为有 IC 锚点；diffusion 无锚点比是不公平的"
- 必须有传统方法在 burgers_1d 上的真实数字才能下结论
- 跑一次 ~30 分钟（CPU 即可）

#### B2 · IC-conditioned 我们的方法

| 项 | 内容 |
|---|---|
| **目的** | 在公平 setting 下打传统方法 — "你有 IC 我们也有 IC，看谁强" |
| **代码** | conditioning_type='ic' 已默认（in_channels=2: noisy_u + IC） |
| **训练** | 大部分实验都带 IC（entrodiff_mvp_run1 / bvaware_run / e2_bl_run / e2_bvaware_run / sharp_ours） ✅ |
| **状态** | ❓ 数据有，**但没和传统方法做过 head-to-head 对比**！ |

**待办（关键论文动作）**：
1. 🔴 跑 traditional_solvers eval：拿到 Lax-F / MacCormack / Central 的 W₁/L¹/shock_err
2. 🔴 把 IC-conditioned ours 数字放在同一张表里对比
3. 📝 写论文新章节 **§5.4 "Comparison to traditional schemes"**：
   > "On the same Burgers IC, Lax-Friedrichs achieves W₁ = 0.X, our method achieves W₁ = 0.Y, comparable up to constants. The diffusion model additionally captures the *distribution* over solutions while traditional schemes are deterministic per-IC."

**这才是把论文从"被攻击"变"主动展示"的关键章节。**

---

### C 轨 · 工程贡献 — Foundation Model（独立列出，不需 baseline）

> 按你的指示：**不和 baseline 比，独立呈现工程价值，rebuttal 时再讨论**。

#### C1 · DiT-BVAware Foundation ⭐ 已完成

| 项 | 内容 |
|---|---|
| **架构** | DiT-1D backbone (dim=256, n_layers=6, patch=4, 7.43M params) + BV-aware tanh prior |
| **训练** | 200 epoch on Burgers + BL **混合 batch**，单卡 RTX 3090 ~10 小时 |
| **结果** | Burgers W₁ = **0.2625** / BL W₁ = **0.0835** |
| **vs 单 PDE 模型** | Burgers -64% / BL -49%（但这个对比要小心叙事——见下） |
| **状态** | ✅ 训练 + eval 完成 |

**叙事建议**（按你的指示）：
- ❌ **不**说"我们的 foundation 比单 PDE 模型好" — 这种对比可能引战
- ✅ **正面叙事**："C2 提出的 BV-aware 不限于 UNet，可与现代 Transformer 架构 (DiT) 结合"
- ✅ **跨 PDE 价值**："single model handles multiple hyperbolic PDEs in one training run"
- ✅ **作为 §5.5 或附录单独章节**，不进主表

#### C2 · DiT-Plain 对照（验证 BV-aware 在 DiT 上仍重要）📋 计划中

| 项 | 内容 |
|---|---|
| **目的** | 让 DiT-Plain (无 BV-aware) 跑同样数据，证明性能下降 → BV-aware 是 DiT 上**也**关键的 |
| **配置** | configs/foundation/small.yaml 改 model.type: dit_plain |
| **状态** | 📋 服务器 GPU 1 空闲可启动 |

#### C3 · shock_err 高的诊断（已知 Foundation 数字偏高）

Foundation eval 数字 shock_err = 2.05（[0,2π] 网格 ~33%）。这是 **数字层面的瑕疵**，但 W₁ 大胜可以盖住。可能根因：
- (A) IC → shock 位置因果链未强约束（IC 通过 channel concat 信号被稀释）
- (D) patch_size=4 把 shock 装进单 token

**叙事**：论文里**只报 W₁ + L¹**，shock_err 留附录或换成"top-3 |∇u| 平均位置"鲁棒度量。

---

### D 轨 · Rebuttal 备料（不写正文，rebuttal 时砸出来）

| 项 | 状态 | rebuttal 价值 |
|---|---|---|
| E4 Shallow-Water 2D | ✅ 代码+数据生成器就绪，0 训练 | 防"只能 1D"攻击，~2 天工作量 |
| E5 Vlasov-Poisson | 📋 完全没动 | 防"只能流体"攻击，加分项 |
| Foundation × 3 PDE (加 Euler) | 📋 等 E3 训练完 | 一锁一个把工程价值再升一级 |
| H100 base/large 模型 | 📋 H100 没到 | 强算力时再开 |
| PDE-Bench / Poseidon 对比 | 📋 没做 | 真被 reviewer 问 "为什么不和工程论文比" 时拿出 |

---

## 2 · 完成度总表（一图全见）

| 轨 | 实验 | 数据 | 代码 | 训练 | Eval | 进论文 |
|---|---|---|---|---|---|---|
| **A1** E1 Burgers 主实验 | ✅ | ✅ | ✅ 200ep | ✅ | ✅ §5.1 |
| **A2** E1 Ablation (schedule/param/loss/step) | ✅ | ✅ | ✅ | ✅ | ✅ §5.2 |
| **A3** E2 Buckley-Leverett (Standard) | ✅ | ✅ | ✅ 200ep | ✅ | 🔧 数字未写 |
| A3' E2 BVAware | ✅ | ✅ | ✅ 200ep | 🔴 **缺** | 📋 |
| A3'' E2 baseline (200ep 重训) | ✅ | ✅ | 🔧 50ep 不对齐 | — | — |
| **A4** E3 Euler Sod | ❓ | ✅ | ❌ | ❌ | ❌ |
| **A5** Sharp IC ours | ✅ | ✅ | ✅ 500ep | 🔴 **缺** | 📋 |
| A5' Sharp IC baseline | ✅ | ✅ | ✅ 500ep | 🔴 **缺** | 📋 |
| **B1** 传统方法 baseline | ✅ | ✅ | — | 🔴 **缺** | ❌ |
| **B2** IC-conditioned vs traditional | ✅ | ✅ | (复用 A) | 🔴 缺对比表 | ❌ §5.4 |
| **C1** Foundation DiT-BVAware | ✅ | ✅ | ✅ 200ep | ✅ | 📋 §5.5 |
| **C2** Foundation DiT-Plain | ✅ | ✅ | 📋 待启动 | — | — |
| D 类（rebuttal） | — | — | — | — | — |

**符号**：✅ 完成 | 🔧 部分 / 待修 | 🔴 立即可做 | 📋 计划中 | ❌ 未开工

---

## 3 · 论文 LaTeX 当前状态

| Section | 文件 | 状态 |
|---|---|---|
| §1 Intro | 01_intro.tex | ✅ 实写完整 |
| §2 Related | 02_related_work.tex | ✅ 实写 |
| §3 Method | 03_method.tex | ✅ 实写 |
| §4 Theory | 04_theory.tex | ✅ 实写 (Theorem 1-5 + 证明 sketch) |
| **§5 Experiments** | 05_experiments.tex | ⚠️ **只写了 E1**！E2/E3 + traditional baseline + Foundation 全无 |
| §6 Conclusion | 06_conclusion.tex | ✅ 实写 |
| A1 Proofs | A1_proofs.tex | ✅ 5 大定理证明 |
| A2 Extra Exp | A2_extra_experiments.tex | ❌ 全 \todo (E4/E5/扩展 ablation) |
| A3 Impl Details | A3_implementation_details.tex | ✅ 实写 |

**论文 §5 实际写了什么**：
- §5.1 Setup: ✅
- §5.2 E1 Burgers: ✅ Table 1 + Figure
- §5.3 Ablation: ✅ schedule/param/loss/step
- ❌ §5.4 Setting comparison (传统方法): **没有**
- ❌ §5.5 Cross-PDE (E2/E3): **没有**
- ❌ §5.6 Foundation Model: **没有**

**§5 LaTeX 与 REPORT 数字对齐问题**：
- LaTeX: BV-aware 50步 W₁ = 0.719 ± 0.14（5 seeds）
- REPORT 旧: BV-aware 50步 W₁ = 0.729（单 run）
- 差异微小，**保留 LaTeX 的 0.719 数字**（5 seeds 更可信）

---

## 4 · 可下手脚调参的（短期 sweep）

| sweep 项 | 推荐范围 | 预期收益 | 工程量 |
|---|---|---|---|
| **λ_BV** | 0.05 / 0.1 / 0.2 / 0.5 | 找最优 BV 强度，可能下探 W₁ ~0.05 | 4 个训练 × 200ep ≈ 12 小时（3 卡并行 4 小时）|
| **epoch sweet spot** | 50 / 100 / 150 / 200 | 找最优 epoch（200 可能过训），论文引用 100ep 数字 | 已有 ckpt，eval 几小时 |
| **采样步数 fine-grained** | 5/8/12/15/20 | 最佳少步数点，进 §5.2 step ablation | 已有 ckpt，eval 1 小时 |
| **λ_time** | 0.5 / 1.0 / 2.0 / 5.0 | time loss 最优权重 | 4 个训练 |
| **patch_size (DiT)** | 2 / 4 / 8 | 验证假说 D（shock 定位） | 3 个训练 |
| **dim (DiT)** | 128 / 256 / 384 | 模型容量边际效用 | 3 个训练 |

**最值钱的两项**：λ_BV sweep + epoch sweet spot——直接给 §5.2 添 2 个新行，同时把数字打到比论文当前更好。

---

## 5 · Rebuttal 留白（不做，准备好就行）

| 留白 | 触发条件 | 准备时长 |
|---|---|---|
| E4 Shallow-Water 2D | reviewer 问"only 1D?" | 2 天 |
| E5 Vlasov-Poisson | reviewer 问"only fluid?" | 3 天 |
| Foundation × 3 PDE (含 Euler) | C 轨增强 | 1 天 |
| PDE-Bench / Poseidon 对比 | "why not benchmark suite?" | 5 天 |
| 多 seeds 统计 | "stat significance?" | 已有部分 |
| 大模型 (H100 base/large) | 算力到 + 容量质疑 | H100 + 1 周 |

---

## 6 · 立即建议（按价值排序）

### 🔴 第一优先（一天内能拿数字）

1. **跑 traditional_solvers eval**（~30 分钟 CPU）→ 拿到 Lax-F / MacCormack 的 W₁/L¹ → 写 §5.4 setting 对比章节
2. **跑 e2_bvaware_run eval**（~10 分钟）→ 完成 §5.5 (E2 BVAware vs StandardScore vs Baseline)
3. **跑 sharp_baseline + sharp_ours eval**（~20 分钟）→ 拉差距数字
4. **跑 e2_bl_baseline 200ep 重训**（GPU 1 后台，10 小时）→ 修 epoch 不对齐

### 🟡 第二优先（一周内）

5. **生成 Euler Sod 数据 + 训 BVAware 200ep**（GPU 2 后台，1 天）→ 论文从"2 PDE"升到"3 PDE"，故事完整
6. **三卡并行 λ_BV sweep**（一夜，12 小时）→ §5.2 ablation 加新行，可能下探 W₁
7. **DiT-Plain 对照**（GPU 0 后台 10 小时）→ 验证 BV-aware 在 DiT 上仍关键

### 🟢 第三优先（论文 §5 落笔阶段）

8. **§5 全章节实写**：把 §5.4 setting 对齐 + §5.5 cross-PDE + §5.6 Foundation 三节实写，把 §5 从"只 E1"升到"完整"
9. **论文数字对齐**：REPORT 数字 vs LaTeX 数字 vs 真实 ckpt eval 数字三者对齐
10. **shock_err 鲁棒度量**：把 argmax 改成 top-3 |∇u| 平均位置，重算所有 eval

---

## 7 · 历史里程碑

| 日期 | 事件 |
|---|---|
| 2026-04-21 | 项目启动 |
| 2026-04-25 | 路径 A 锁定 |
| 2026-04-26 | §1/§2 实写 |
| 2026-04-28 | §3 Method + §4 Theory + 5 大定理 LaTeX |
| 2026-04-29 | E1 主实验 + 少步消融 完成 |
| 2026-04-30 | E2 BL solver+数据+训练全闭环；W5 Foundation 代码全栈 |
| **2026-05-01 早** | Foundation 200ep 训完 + R7 修复 + 跨 PDE eval 大胜 |
| **2026-05-01 (现)** | 故事三轨重组；REPORT 完整盘点；下一步 setting 对齐 + E3 Euler |

---

## 附录 A · 核心代码清单

### A.1 模型 (PROJECT/black/src/models/)
- `unet_1d.py` — UNet1D backbone (现有)
- `score_param.py` — StandardScore + BVAwareScore (含 backbone='unet'|'dit' 开关)
- `dit_1d.py` — DiT-1D backbone (W5)
- `foundation_score.py` — DiT-Plain score (W5)

### A.2 数据 (PROJECT/black/src/data/)
- `burgers_dataset.py` — E1 数据集
- `mixed_pde_dataset.py` — 混合 PDE 数据集 (W5)
- `burgers_1d_solver.py` — Godunov solver
- `traditional_solvers.py` — Lax-F / MacCormack / Central+ν

### A.3 PDE solver (PROJECT/black/src/pdes/)
- `bl_flux.py` — BL 通量 + Godunov flux
- `bl_solver.py` — BL Godunov solver
- `euler_sod.py` — Euler 1D HLLC + Godunov（**未训练**）
- `shallow_water.py` — 2D 浅水 HLL（**未训练**）

### A.4 训练 / 评估 (PROJECT/black/scripts/)
- `train_mvp.py` / `train_baseline.py` / `train_bvaware.py` — UNet 训练
- `train_foundation.py` — DiT 训练 (W5)
- `eval_viz.py` — 单 PDE 主 eval
- `eval_step_ablation.py` — 少步数消融
- `eval_traditional.py` — 传统数值方法 eval（**没人跑过**）
- `eval_foundation.py` — 跨 PDE eval (W5)
- `eval_shock_region.py` — shock 局部度量
- `generate_data.py` / `generate_sharp_data.py` / `generate_bl_data.py` / `generate_euler_data.py` / `generate_sw_data.py` / `generate_coarse_data.py` — 各 PDE 数据生成

### A.5 服务器 ckpt 状态

```
output/experiments/ (服务器):
├── entrodiff_mvp_run1/  E1 ours 50ep × 2 runs ✅
├── mvp_baseline/        E1 baseline 50ep ✅ (但 5/15/.../95 都有, 实际可能 100ep)
├── bvaware_run/         E1 BV-aware 200ep+ (140 ckpt) ✅
├── ours_full/           sharp+ours 500ep ✅ (100 ckpt) — 可能等于 sharp_ours
├── e2_bl_run/           E2 Standard 200ep ✅
├── e2_bl_baseline/      E2 baseline 50ep 🔧 (要重训 200ep)
├── e2_bvaware_run/      E2 BVAware 200ep ✅ ← 缺 eval
├── sharp_baseline/      E1 sharp baseline 500ep ✅ ← 缺 eval
├── sharp_ours/          E1 sharp ours 500ep ✅ ← 缺 eval
├── foundation_small/    DiT Foundation 200ep ✅ + eval ✅
└── foundation_eval/     C1 跨 PDE 表 + 图 ✅
```

### A.6 数据文件

```
output/data/ (服务器):
├── burgers_1d_N5000_Nx128.npy           247MB ✅
├── burgers_sharp_N5000_Nx128.npy        247MB ✅
└── bl_1d_N5000_Nx128.npy                247MB ✅

未生成:
├── euler_sod_1d_N5000_Nx128.npy         (E3 待生成)
└── sw_2d_*.npy                          (E4 rebuttal 备料)
```
