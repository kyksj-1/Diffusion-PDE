# MEMORY · 项目活档案（给 AI 看）

> **阅读对象 · AI**。给人看的进度报告在 `REPORT.md`。

---

## A · 角色选择

当前角色：**Anima Anandkumar 教授**（Caltech / NVIDIA）。理由见 `CLAUDE.md`。

---

## B · 决策日志

### 2026-04-30 晚 · W5 Foundation Model 全栈闭环 + 服务器训练启动

- **角色切换**: Anima → Zongyi Li (DiT 代码工程主导)
- **大方向决策** (用户拍板):
  - 双轨并行: DiT-BVAware (主) + DiT-Plain (基线), UNet 路线保留作 toy validation
  - 论文用户写, 我做代码; DiT 是锦上添花, 不出结果论文也能交
  - DiT 实现复用 facebookresearch/DiT 改 1D
- **技术决策** (与 DeepSeek 初稿不同):
  - DiT 不替代 BVAware, 仅替换其 phi_sm 子网 → Theorem 3 论证完整保留
  - PDE 条件走 AdaLN 注入, 不走 channel concat (DiT 标准做法)
  - patch_size=4 (不是 8/16) 以保证 shock 定位精度
  - per-PDE Nx 不强制统一 (BL 数据线性插值会抹平 shock)
  - 训练脚本不破坏现有 train_*.py, 新增 train_foundation.py
- **兼容性铁律**: BVAwareScore 加 backbone='unet'|'dit' 开关, 默认 unet 行为 bit-wise 不变
- **预先存在的代码 bug 浮出水面**: BVAwareScore 输出 shape == 输入 shape (B, in_C, Nx), 与 StandardScore 的 (B, 1, Nx) 不一致. 走 sampler 的 cond 路径会因此在第二次 cat 失败. 不在 W5-C 范围内修复.
- **执行**: 6 个 W5 任务全部完成, 39/39 单元测试 (本地 + 服务器 1:1), 服务器 dit_bvaware × {burgers + BL} 混合训练 epoch 3 loss=0.108 (从 0.456 下降 2.6×)
- **服务器**: tmux entrodiff:foundation_small (window 3), GPU 0 (5GB / 61% util), 数据 burgers + bl + sharp 都在 output/data/

### 2026-04-30 早 · E2 闭环 + 少步消融系统化 + REPORT 大刷新

- E2 Buckley-Leverett 全栈完成: flux → solver → 数据 → 训练 → eval
- **少步消融核心发现**: BV-aware 10 步 (W₁=0.681) > Baseline 50 步 (0.706) → 论文级亮点
- BV-aware 500ep 过拟合 → 退回 200ep
- E2 上 Ours 比 Baseline 好 7.4% (W₁ 0.163 vs 0.176)
- 决定: 现有数字足够写论文 §5, 不再硬调参

### 2026-04-29 · 代码 MVP 跑通 + 服务器上线

- 本地 PC RTX 4060 完成 E1 数据+训练+eval 全闭环
- 服务器 3×RTX 3090 部署
- BVAwareScore 梯度真值化 + Godunov PDE guidance + 梯度裁剪
- Time loss 轻量版实现
- PDE guidance 对无条件采样无益, 正确用途是逆问题

### 2026-04-28 · 论文前三节精修 + 定理附录完整迁入 LaTeX

- §1/§2/§3 (§5 Method) / §4 (§6 Theory) 全实写
- A1 5 大定理 LaTeX 证明完整
- notation.tex 全部宏落地

---

## C · 状态快照

### C.1 当前阶段

- **周次**: W5 (12 周时间表)
- **本阶段主任务**: Foundation Model 训练完成 → 论文 §5 + §5.4 (Foundation transfer) 实写
- **下一里程碑**: foundation_small 训练完成 + eval → DiT-Plain baseline 训练 → 跨 PDE 表格

### C.2 已完成

- 路径 A 选定 + 项目基础设施
- 论文 §1–§4 + A1 附录 100% 实写
- E1 Burgers 全闭环 (数据/训练/eval/消融)
- E2 Buckley-Leverett StandardScore 闭环
- 少步消融系统化
- Time loss / sharp IC / coarse grid 脚本就绪
- 服务器 tmux 实验编排
- **W5 Foundation Model: 代码全栈 + 服务器训练启动**
  - DiT-1D backbone (10 测试 pass)
  - MixedPDEDataset (11 测试 pass, 配置驱动 N-PDE)
  - FoundationScore + BVAwareScore(backbone='dit') (18 测试 pass)
  - train_foundation.py + tiny/small/base/smoke 配置
  - eval_foundation.py 跨 PDE 表格 + 图
  - 服务器 dit_bvaware 训练运行中

### C.3 待做

- foundation_small 训练完成 (服务器, ~3-7 小时)
- DiT-Plain 基线训练 (相同 config 切 model.type=dit_plain)
- eval_foundation.py 出真实跨 PDE 表格
- 论文 §5.4 Transfer across conservation laws (用户写)
- 论文 §5 Experiments 主表填数 (用户写)
- 论文 §6 Conclusion (用户写)

---

## D · 风险簿

| ID | 描述 | 状态 |
|---|---|---|
| R3 | Baseline 作者审稿 | 已准备 |
| R5 | 实验时间紧 | 已缓解: E1+E2 闭环 + W5 foundation 启动 |
| R6 | "只是 Score Shocks 应用" | 少步优势 + E2 跨方程 + Foundation Model 跨 PDE 三重反驳 |
| **R7 (新)** | BVAware sampler+cond 路径 shape 不匹配 | 预先存在; eval 时绕过 (用 in_channels=1 + no cond); 真要修需协调 train_bvaware 现有 ckpt 兼容 |
| **R8 (新)** | DiT + AMP 与 BVAware 二阶导兼容性 | tiny/small 配置默认关 AMP; DiT-Plain 路线可试开 |

---

## E · 维护规则

重大决策/里程碑/风险变化时更新。进度数字去 REPORT.md。

---

> 若你正在读这份文件却不知接下来该做什么——读 `MISSION.md`。
