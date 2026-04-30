# MISSION · 当前阶段指令

> **即写即用即换**。持续性内容请去 `CLAUDE.md`；进度请去 `REPORT.md`；状态 / 决策日志请去 `MEMORY.md`。

---

## 当前状态（2026-04-30）

**服务器**：3 GPU 全满 — E2 BVAwareScore + Sharp IC Ours + Sharp IC Baseline 均在 tmux 运行中

**代码（本地）**：
- E1 Burgers: 完整闭环 (StandardScore / BVAwareScore / Baseline / IC-conditioning / time loss / 少步消融 / 传统 solver baseline)
- E2 Buckley-Leverett: solver + 数据 + StandardScore + Baseline 完成，BVAwareScore 服务器训练中
- E3 Euler Sod: solver + 数据生成器就绪
- E4 Shallow-Water: solver + 数据生成器就绪
- 所有 1D PDE flux 模块统一接口：`src/pdes/{pde}_solver.py`

**论文**：§5 Experiments 实写中（setup + E1 已写，E2/E3 待填）

**下一阶段**：Foundation Model — 一个 DiT 模型解决全部双曲 PDE

---

## 当前任务：Foundation Model 开发

详见 `CLAUDE.md §W5 Foundation Model 开发协议`

### 核心设计
- **Backbone**: DiT-1D (Diffusion Transformer)，替代 UNet
- **输入**: [noisy_u | IC | PDE_type_embedding] 3 channels
- **Patch embedding**: 自适应多分辨率
- **训练**: 混合 PDE 数据交替采样
- **规模**: tiny(single GPU) → small(3090) → base(H100) → large(H100×6)

### 待开发模块

- [ ] `src/models/dit_1d.py` — DiT-1D backbone
- [ ] `src/models/foundation_score.py` — FoundationScore wrapper
- [ ] `src/data/mixed_pde_dataset.py` — 混合 PDE 数据加载器
- [ ] `scripts/train_foundation.py` — 混合训练脚本
- [ ] `configs/foundation/` — 多规模配置
- [ ] `scripts/eval_foundation.py` — 跨 PDE 评估

### 服务器 tmux 会话（当前运行中）
- `e2_bvaware` (GPU1): E2 BVAwareScore 200ep
- `sharp_ours` (GPU2): Sharp IC BVAwareScore 500ep
- `sharp_base` (GPU0): Sharp IC StandardScore 500ep

---

### 启动时必读
- `CLAUDE.md §W5 Foundation Model 开发协议` — 架构 + 任务清单
- `REPORT.md` — 诚实进度
- `Docs/path_A_method_skeleton.md` — 论文框架
- 服务器连接: `ssh -p 227 liuyanzhi@202.121.181.105`
