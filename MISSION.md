# MISSION · 当前阶段指令

> **即写即用即换**。持续性内容请去 `CLAUDE.md`；进度请去 `REPORT.md`；状态 / 决策日志请去 `MEMORY.md`。

---

## 当前状态（2026-04-29）

**论文**：§1–§4 全实写（含 5 大定理附录）；§5 (§7) Experiments 和 §6 (§8) Conclusion 仍是 `\todo` 占位。

**代码**：8 核心源文件全实写 + `generate_data.py` + `train_mvp.py` 均已跑通。E1 数据 246MB 已生成，训练 10 epoch 产出 2 个 checkpoint。**但无评估脚本 → 无指标/图表 → 论文 §5 填不了**。

**核心瓶颈**：缺 `scripts/eval_viz.py`（见 CLAUDE.md §W4 协议）。

---

## AI 任务清单

### 已完成
- [x] 论文 §1 Introduction / §2 Related Work / §3 (§5) Method / §4 (§6) Theory 全实写
- [x] 5 大定理 LaTeX 证明从 `Docs/proof/` 迁入 `A1_proofs.tex`
- [x] notation.tex 全部宏落地
- [x] 代码 MVP 跑通（数据生成 + 训练）
- [x] REPORT / MEMORY 进度大刷新（2026-04-29）

### 待完成（按优先级）

- [ ] **`scripts/eval_viz.py`**（最高优先）—— E1 Burgers 评估 + 可视化 + 指标输出
- [ ] **`scripts/train_baseline.py`** —— 纯 EDM baseline 训练（用于对比）
- [ ] **eval_viz 扩展** —— baseline vs ours 三栏对比图
- [ ] **BVAwareScore 梯度真值化**（`src/models/score_param.py`）
- [ ] **Sampler Godunov guidance 真梯度**（`src/diffusion/samplers.py`）
- [ ] §5 (§7) Experiments 实写（依赖 eval 产出数字）
- [ ] §6 (§8) Conclusion 实写
- [ ] 全文 `\todo{}` 清除 + 最终 polish

### 远期
- [ ] E1 消融实验（schedule / loss / parameterization）
- [ ] E2 Buckley–Leverett
- [ ] E3 Euler Sod

---

### 启动时必读
- `CLAUDE.md §W4 实验代码开发专项协议` — 详细开发指令
- `REPORT.md` — 诚实进度
- `MEMORY.md` — 决策日志
- `paper/black/sections/03_method.tex` — 论文方法章节（代码对齐依据）
