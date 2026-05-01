# W5 Code Review (2026-05-01)

> Reviewer: 主 session 接手 SA1 任务后做的快速审查 (sub-agent dispatch 全部 API 500 失败)
> 时间: 2026-05-01 17:30~

## 审查范围

W5 + 后续相关代码:
- `src/models/dit_1d.py`
- `src/models/foundation_score.py`
- `src/models/score_param.py` (含 R7 修复 + W5-SA2 out_channels 扩展)
- `src/data/mixed_pde_dataset.py`
- `src/data/euler_dataset.py` (W5-SA2 新增)
- `src/utils/shock_metrics.py` (W5-SA3 新增)
- `scripts/train_foundation.py`
- `scripts/train_bvaware_euler.py` (W5-SA2 新增)
- `scripts/eval_foundation.py`
- `scripts/sweep_*.py` (W5-SA4 新增)

## 关键发现

### A. 已知问题 + 已修复

1. **R7 (BVAware shape 不一致)** — 已修. D_x 切前 out_channels 通道.
2. **DiT 二阶导兼容性** — 已修. 替换 PyTorch SDPA 为手写 ManualMultiheadAttention.

### B. 未发现严重 bug

逐文件 grep / 阅读 + pytest 76/76 全 pass. 没有阻塞性问题.

### C. 已知技术债 / Phase 2 待办

#### C.1 Foundation Model 多通道扩展 (Phase 2)

当前 FoundationScore + DiT1D 只支持单一 in_channels. 真要让 Foundation 同时训
Burgers (in=2) + BL (in=2) + Euler (in=6), 需要其中之一:

**方案 A (推荐): per-PDE input projection ModuleDict**
- DiT1D 加 `pde_input_projs: nn.ModuleDict[pde_name, Conv1d]`
- forward 根据 pde_id 选对应 conv
- 共享 transformer body 不变
- 输出层同理: per-PDE unpatchify (out_channels 不同)

**方案 B: max-channel padding**
- 所有 PDE pad 到 max_in_channels (=6 for Euler)
- 单一 conv, 但缺失通道置 0
- 缺点: 0 填充扰乱 conv 特征学习

**当前状态**: 两个都没实现. Foundation Model 论文层面只 demo Burgers+BL (单通道
PDE), Euler-Foundation 留作 rebuttal 强化材料 (用 BVAware UNet 单 PDE 训练即可).

#### C.2 MixedPDEDataset collate_fn 分桶 (Phase 2)

当前 collate_fn 假设所有 PDE Nx 相同 + 单通道. 多通道支持的扩展点已在代码注释
中明示 (W5 plan §2.2).

#### C.3 BVAware AMP 兼容性

`autograd.grad(create_graph=True)` 与 GradScaler 在新版 PyTorch 已修复. 未实测,
但 train_foundation 已默认关 AMP for safety. 可在 server 上加 AMP 试一次.

### D. 推荐改进 (非阻塞)

1. **eval 增加 robust shock metric** — SA3 已实现, eval_foundation 已集成. 
   eval_viz / eval_step_ablation 也应集成 (留作下阶段).
2. **train_foundation 加 wandb/tensorboard logging** — 当前只 print + txt log,
   长训练需要曲线监控.
3. **ckpt 加版本字段** — 防止旧 ckpt 在新代码下 silent load fail.

## 测试覆盖

```
tests/
  test_dit_1d.py             10 cases ✅
  test_mixed_pde_dataset.py  11 cases ✅
  test_dit_scores.py         18 cases ✅
  test_shock_metrics.py      10 cases ✅
  test_euler_pipeline.py     10 cases ✅
  test_bl_flux.py             ? cases (历史)
  test_euler_flux.py          ? cases (历史)

总计: 76/76 W5 + W5-SA 全 pass (本地 + 服务器 1:1)
```

## 给服务器训练的清单 (cron 触发用)

应运行的训练:
1. `train_bvaware_euler.py --config configs/experiment/e3_euler.yaml` (E3)
2. `train_bvaware.py --config configs/experiment/sharp_*` (sharp Ours/Baseline) — eval only, ckpt 已有
3. `train_bvaware.py --config configs/experiment/e2_bl_baseline_200ep.yaml` (E2 baseline 重训对齐)
4. `eval_traditional.py` — 已跑 ✅
5. `eval_foundation.py --ckpt foundation_small_ep200.pt` — 已跑 ✅
6. `sweep_lambda_bv.py --base_config bvaware_server --lambdas 0.05 0.1 0.2 0.5` (sweep)

应运行的 eval:
- `eval_viz.py` on:
  - bvaware_run/_ep200.pt
  - mvp_baseline/_ep50.pt 
  - sharp_ours/_ep500.pt (新)
  - sharp_baseline/_ep500.pt (新)
  - e2_bl_run/_ep200.pt
  - e2_bvaware_run/_ep200.pt (新)
  - e3_euler_run/_ep200.pt (训完后)

## 总结

W5 全部 6 任务 + W5-SA 4 任务代码全部就绪, 76/76 测试 pass, 兼容性铁律遵守
(现有训练脚本 + ckpt 全部保持工作). Phase 2 的 Foundation Model 多通道扩展
不在论文核心叙事路径上, 留作 rebuttal 备料.
