# MISSION · 当前阶段指令

> **即写即用即换**。持续性内容请去 `CLAUDE.md`；进度请去 `REPORT.md`；状态 / 决策日志请去 `MEMORY.md`。

---

## 当前状态（2026-04-29 晚）

**实验**：E1 Burgers 完整闭环完成。服务器上 3 条训练线跑通：
- StandardScore Ours (0.4M, 50ep) | Baseline (0.4M, 50ep) | **BVAwareScore (7.7M, 200ep)**
- eval_viz 支持多模型 / 多步数 / 多 zeta_pde 对比
- PDE guidance 已实现但仅适用于条件生成 (无条件采样推往零解)

**发现**：BV-aware 少步数优势 (25 步 > Baseline 50 步) ⭐ 可作论文亮点

**论文**：§1–§4 全实写，§5 (§7) / §6 (§8) 仍 `\todo`

---

## AI 任务清单

### 已完成
- [x] 论文 §1–§4 全实写 + 5 大定理附录
- [x] BVAwareScore 梯度真值化 + train_bvaware 脚本
- [x] Sampler Godunov 真梯度 + 梯度裁剪防 NaN
- [x] eval_viz 多模型/多步数/PDE guidance 支持
- [x] 服务器 3 线训练跑通 + 综合 eval

### 待完成（按优先级）

- [ ] **时间信息 Loss** (轻量版) — dataset 加相邻帧 + loss 加 ‖ûₙ₊₁ - Godunov_step(uₙ)‖²（~30 行改动）
- [ ] **BVAwareScore 大模型重训** — dim=256, epochs=500, 加时间 loss
- [ ] **E2 Buckley–Leverett** (本地 PC) — 新 solver + 数据 + 训练 + eval
- [ ] §5 (§7) Experiments 实写 (等 W₁ 压到 <0.5 后填入)
- [ ] §6 (§8) Conclusion 实写
- [ ] 全文 `\todo{}` 清除

### 远期
- [ ] 重量版时间 loss (L_Burg: score 层面 Burgers 一致性)
- [ ] E3 Euler Sod
- [ ] E4/E5 (rebuttal)

---

### 启动时必读
- `CLAUDE.md §W4 实验发现与后续策略` — 少步数 / PDE guidance / E2 规划 / 时间 loss
- `REPORT.md` — 诚实进度
- `MEMORY.md` — 决策日志
- `Docs/path_A_method_skeleton.md` — 论文框架
