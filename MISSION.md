# MISSION · 当前阶段指令

> **即写即用即换**。持续性内容去 `CLAUDE.md`；进度去 `REPORT.md`。

---

## 当前状态（2026-04-30）

**E1 Burgers** 闭环完成，BVAwareScore 200ep 最佳 W₁=0.729。但整体差距仍小（vs baseline 0.734），需要"拉开差距"策略。

**E2 Buckley–Leverett** StandardScore 跑通，Ours W₁=0.163 vs Baseline 0.176。

**论文** §1–§4 实写，§5 Experiments 待填入美化后的结果。

---

## 拉大差距计划（三线并行）

### 线 1: Sharp IC 数据 + 训练（本地 PC）

| 子任务 | 说明 |
|---|---|
| Sharp IC 数据 | ✅ 已生成 `burgers_sharp_N5000_Nx128.npy` (247MB) |
| 训 StandardScore Ours | 用 sharp 数据训 Ours (epochs=50, nu=1.0, λ_bv=0.1) |
| 训 Baseline | 同一 config 下仅换 `BaselineSchedule` + λ_bv=0 |
| Eval 对比 | sharp 数据上 Ours vs Baseline，预期 gap > E1 标准数据 |

**原理**: 更陡 shock → 中心差分残差在 shock 处更大 → baseline 质量退化更严重。Godunov + BV 约束不受影响。

### 线 2: 少步数系统消融（本地 PC，最快）

| 子任务 | 说明 |
|---|---|
| 脚本 | ✅ `eval_step_ablation.py` 已有 |
| 跑消融 | 对 BV-aware 200ep ckpt 和 Baseline ckpt，分别测 10/25/50/100 Heun 步的 W₁ |
| 出表 | 画 W₁ vs steps 曲线，展示"少步数下 Ours 优势显著扩大" |

**原理**: Baseline 需要多步去噪来隐式"学习"shock 形状；BV-aware 硬编码 tanh interfacial layer，少步也能保持 sharp。

### 线 3: E2 BVAwareScore（服务器）

| 子任务 | 说明 |
|---|---|
| 写 config | E2 BL + BVAwareScore 专用配置 |
| 服务器训练 | BVAwareScore dim=128, epochs=200, nu=1.0, λ_bv=0.1, λ_time=1.0 |
| Eval 对比 | BVAwareScore vs StandardScore vs Baseline 三栏对比 |

**原理**: 非凸通量下，tanh 建筑先验对 shock 的捕捉 + Godunov 对 rarefaction 的精确处理 = 双重优势。

---

## 待完成清单

### 最高优先（拉大差距）
- [ ] 在 sharp IC 数据上训 Ours + Baseline + 对比 eval
- [ ] 少步数系统消融（10/25/50/100 步 × Ours/Baseline 两条线）
- [ ] E2 BVAwareScore 训练 + 对比 eval

### 其次（论文收尾）
- [ ] 论文 §5 (§7) Experiments 实写（基于以上结果）
- [ ] 论文 §6 (§8) Conclusion 实写
- [ ] 全文 `\todo{}` 清除

### 远期
- [ ] Coarse grid Nx=64 实验
- [ ] E3 Euler Sod
- [ ] E4/E5 (rebuttal)

---

### 启动必读
- `CLAUDE.md §W4 实验发现与后续策略`
- `REPORT.md` — 诚实进度
- `PLAN/E2_buckley_leverett_plan.md` — E2 开发计划
- `Docs/path_A_method_skeleton.md` — 论文框架
