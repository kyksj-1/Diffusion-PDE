# W5 Foundation Model 工程方案（Sub-Agent 开工指南）

> **角色**：Zongyi Li · Caltech/NVIDIA
> **日期**：2026-04-30
> **目的**：DiT-1D backbone 集成进 EntroDiff 主管线，支持双轨实验（DiT-Plain 基线 + DiT-BVAware 主线），同时保留现有 UNet 全部产出。
> **读者**：进入各 worktree 的 sub-agent；他们看不到主会话上下文，本文档是唯一权威。

---

## 0. 设计哲学（不可违反）

### 0.1 兼容性铁律

**任何新增 score model 必须满足现有接口契约**：

```python
# 统一签名（现有 StandardScore / BVAwareScore 均遵循）
D_x = model(x_input, sigma, pde_id=None)
# x_input: (B, C_in, Nx)   — channel-concat 输入: [noisy_u | IC | (可选其他)]
# sigma:   (B,)             — EDM 标量噪声水平
# pde_id:  (B,) long 或 None — 新增可选参数；None 时退化为单 PDE 行为
# D_x:     (B, 1, Nx)        — Tweedie 反演输出
```

**绝不允许**：
- 修改 `src/diffusion/samplers.py` / `src/diffusion/losses.py` 现有签名（只允许新增参数且默认 None）
- 修改 `src/models/unet_1d.py`
- 修改 `src/data/burgers_dataset.py`
- 修改 `scripts/train_mvp.py / train_baseline.py / train_bvaware.py`

**允许**：
- 在现有 `score_param.py` 的 `BVAwareScore.__init__` 加 **可选** kwarg `backbone="unet"|"dit"`，默认 `"unet"` 保持现有行为
- 新增文件
- 在 loss/sampler 加 **可选** `pde_id=None` kwarg（默认 None → 退化为现行单 PDE Burgers 行为）

### 0.2 可配置性铁律

**绝不硬编码 PDE 列表**。所有 PDE 配置走 YAML：

```yaml
pdes:                                   # 列表元素数量 = num_pde_types
  - name: "burgers"
    data_file: "burgers_1d_N5000_Nx128.npy"
    flux_type: "burgers"                # 用于 L_time 的 godunov_flux 派遣
  - name: "buckley_leverett"
    data_file: "bl_1d_N5000_Nx128.npy"
    flux_type: "buckley_leverett"
  # 新增 PDE 只需追加一项 → dataset / model / loss 自动适配
```

PDE 数量 / 名称 / flux 全部从 YAML 读，代码里**不能出现** `["burgers", "buckley_leverett"]` 这样的字面量。

### 0.3 多环境铁律

- **PC RTX 4060 (8GB)**：tiny 配置 + AMP + grad accumulation 模拟大 batch
- **服务器 RTX 3090 (24GB)×3**：small/base 配置，tmux session
- **路径**：一律 `env.data_dir / env.output_dir`，禁止绝对路径
- **Windows**：`num_workers=0`；**Linux**：`num_workers=4`

---

## 1. 现有接口快速参照

### 1.1 数据接口

```python
# 现有 BurgersDataset 签名（不动）
ds = BurgersDataset(data_path, mode='train'|'val'|'test', conditioning_type='none'|'ic')
batch = ds[i]   # tensor (N_time, N_x)
cond = ds.get_conditioning(batch)   # (B, 1, Nx) 首帧，或 None
x_target = batch[:, -1, :].unsqueeze(1)   # (B, 1, Nx) 末帧作为去噪目标
```

### 1.2 Loss 接口

```python
# src/diffusion/losses.py 现有
get_dsm_loss(model, x, sigma, conditioning=None, ic=None)
get_bv_loss(model, x, sigma, conditioning=None, ic=None)
get_godunov_time_loss(model, x_prev, x_target, sigma, dt, dx, conditioning=None, ic=None)
godunov_flux(ul, ur)  # 仅 Burgers flux f=u^2/2
pde_residual(u, dx)   # 仅 Burgers
```

**改造点**：W5-D 阶段需在 `losses.py` **新增** `flux_type` 派遣（不删原函数），路由到 BL flux（`src/pdes/bl_flux.py` 已有）。

### 1.3 Sampler 接口

```python
entrodiff_heun_sampler(
    model, shape, sigma_min, sigma_max, tau_max, nu,
    num_steps=50, device, zeta_obs=0.0, zeta_pde=0.0,
    conditioning=None, ic=None,
)
```

### 1.4 Schedule

```python
ViscosityMatchedSchedule(nu, tau_max)   # σ²=2νt
BaselineSchedule(p_mean=-1.2, p_std=1.2)   # EDM log-normal
```

### 1.5 Env 接口

```python
from src.utils.env_manager import env, PROJECT_ROOT
env.data_dir, env.output_dir, env.default_device, env.num_workers
env._config["hardware"]["max_batch_size"]
```

---

## 2. 模块设计规范

### 2.1 W5-A · `src/models/dit_1d.py`

**职责**：1D 版 DiT backbone，参考 facebookresearch/DiT 改 PatchEmbed2D → 1D。

**类清单**：

```python
class PatchEmbed1D(nn.Module):
    """(B, C_in, Nx) → (B, N_patch, D)
    用 Conv1d(C_in, D, kernel=patch, stride=patch) 实现。
    """
    def __init__(self, in_channels: int, embed_dim: int, patch_size: int): ...

class TimestepEmbedder(nn.Module):
    """连续 sigma → D 维 embedding。复用 SinusoidalPositionEmbeddings + MLP。"""

class PDEEmbedder(nn.Module):
    """(B,) long pde_id → D 维 embedding。
    nn.Embedding(n_pde_types, D) + MLP 投影。
    pde_id=None 时输出 0 (单 PDE 退化)。
    """
    def __init__(self, n_pde_types: int, embed_dim: int): ...

class DiTBlock(nn.Module):
    """AdaLN-Zero block (DiT 标准):
        x = x + gate1 * MSA(LN(x) * (1+scale1) + shift1)
        x = x + gate2 * MLP(LN(x) * (1+scale2) + shift2)
    cond = time_emb + pde_emb (加和注入 AdaLN, 不进通道)
    """
    def __init__(self, dim: int, n_heads: int, mlp_ratio: float = 4.0, dropout: float = 0.0): ...

class FinalLayer(nn.Module):
    """AdaLN + Linear → patch 还原"""
    def __init__(self, dim: int, patch_size: int, out_channels: int): ...

class DiT1D(nn.Module):
    """主类。
    Args:
        in_channels: int   # 通常 2 (noisy_u + IC)；如有其他 channel cond 也走这里
        out_channels: int  # 通常 1
        Nx: int            # 必须能整除 patch_size
        dim: int           # token 维度
        n_layers: int
        n_heads: int
        patch_size: int    # 推荐 4
        n_pde_types: int   # >= 1；=1 时 PDEEmbedder 退化为常量 0
        dropout: float
    Forward:
        x: (B, in_channels, Nx)
        sigma: (B,) — 标量噪声水平 (raw σ；内部做 c_noise = log σ / 4)
        pde_id: (B,) long 或 None
    Returns:
        (B, out_channels, Nx)
    """
```

**位置编码**：1D 正余弦 positional embedding（不要 2D），可学习 / 不可学习均可（推荐固定 sin/cos 起步）。

**初始化**：DiTBlock 的 AdaLN-Zero（最后一个 Linear 输出全零，gate 初始化 0）— 严格按官方 DiT 做法。

**单元测试**（必须自带）：

```python
# tests/test_dit_1d.py
def test_shape():
    m = DiT1D(in_channels=2, out_channels=1, Nx=128, dim=256, n_layers=4, n_heads=4, patch_size=4, n_pde_types=2)
    x = torch.randn(8, 2, 128)
    sigma = torch.rand(8)
    pde = torch.randint(0, 2, (8,))
    y = m(x, sigma, pde_id=pde)
    assert y.shape == (8, 1, 128)

def test_pde_id_none():
    """pde_id=None 时也必须正常前向 (单 PDE 退化)"""
    m = DiT1D(..., n_pde_types=1)
    y = m(x, sigma, pde_id=None)
    assert y.shape == (8, 1, 128)

def test_grad_flow():
    """梯度必须传到 patch_embed / dit_blocks / final"""
    y.sum().backward()
    assert all(p.grad is not None for p in m.parameters() if p.requires_grad)
```

---

### 2.2 W5-B · `src/data/mixed_pde_dataset.py`

**职责**：从 YAML 配置驱动，混合 N 个 PDE 数据集，每个 sample 带 pde_id。

```python
class MixedPDEDataset(Dataset):
    """
    Args:
        pdes_config: List[Dict] —— 来自 YAML pdes 字段
            示例: [{"name": "burgers", "data_file": "...", "flux_type": "burgers"},
                   {"name": "buckley_leverett", ...}]
        data_dir: Path
        mode: 'train'|'val'|'test'
        conditioning_type: 'none'|'ic'

    每个 PDE 独立 80/10/10 划分，混合时按 sample 数加权 (or uniform，配置项)。

    __getitem__ 返回:
        {
            "trajectory": (N_time, Nx),         # 完整轨迹
            "ic": (1, Nx),                       # 首帧
            "x_target": (1, Nx),                 # 末帧 (训练目标)
            "pde_id": int,                       # 0..n-1 索引到 pdes_config
            "pde_name": str,                     # 便于 debug
        }

    扩展性: 新 PDE 只需在 YAML 加项，无代码改动。
    """

    @staticmethod
    def collate_fn(batch_list):
        """处理不同 PDE Nx 不一致的情况 (本期 Burgers/BL 都 Nx=128, 暂时简单 stack;
        但接口预留: 若未来不同 Nx, 按 pde_id 分桶 → 每桶单独 forward)."""
```

**关键设计**：必须返回 `pde_id`（即使当前都是 Nx=128 同形状）；这样 W5-D 训练脚本可以把 pde_id 喂给 loss 去派遣 flux。

---

### 2.3 W5-C · DiT 双轨 Score

#### 2.3.1 `src/models/foundation_score.py` (DiT-Plain)

```python
class FoundationScore(nn.Module):
    """
    DiT-Plain: EDM precondition + DiT1D backbone, 直接输出 D_x。
    与 StandardScore 唯一区别: backbone 从 UNet1D → DiT1D, 且支持 pde_id。

    Args:
        in_channels: int = 2          # noisy_u + IC (默认 IC-conditioning)
        Nx: int = 128
        dit_kwargs: Dict              # 透传给 DiT1D (dim/n_layers/n_heads/patch_size/n_pde_types/dropout)
        sigma_data: float = 0.5

    Forward:
        x:      (B, in_channels, Nx)  — channel-concat 输入
        sigma:  (B,)
        pde_id: (B,) long 或 None
    Returns:
        D_x: (B, 1, Nx)

    EDM precondition (与 StandardScore 一致):
        c_skip = σ_d² / (σ² + σ_d²)
        c_out  = σ·σ_d / sqrt(σ² + σ_d²)
        c_in   = 1 / sqrt(σ_d² + σ²)
        c_noise= log σ / 4
        D_x = c_skip * x[:, :1] + c_out * F_θ(c_in * x, c_noise, pde_id)
    """
```

#### 2.3.2 修改 `src/models/score_param.py` 的 `BVAwareScore`

**添加可选 kwarg，默认行为不变**：

```python
class BVAwareScore(nn.Module):
    def __init__(self,
                 in_channels: int = 1,
                 dim: int = 64,
                 return_denoiser: bool = True,
                 backbone: str = "unet",        # 新增: "unet" | "dit"
                 dit_kwargs: dict | None = None, # 新增: 当 backbone="dit" 时透传
                 n_pde_types: int = 1,           # 新增: ≥2 启用 PDE 条件
                ):
        ...
        if backbone == "unet":
            self.phi_sm_net = UNet1D(in_channels, 1, dim)   # 现有行为
        elif backbone == "dit":
            self.phi_sm_net = DiT1D(in_channels=in_channels, out_channels=1,
                                    Nx=dit_kwargs["Nx"], n_pde_types=n_pde_types,
                                    **{k:v for k,v in dit_kwargs.items() if k != "Nx"})
        # phi_sh_net / kappa_net 保持小 conv stack 不变 (它们是局部预测)
        self.backbone = backbone

    def forward(self, x, sigma, pde_id=None):  # 新增可选 pde_id
        ...
        if self.backbone == "dit":
            phi_sm = self.phi_sm_net(x, sigma, pde_id=pde_id)  # DiT 需要 raw sigma
        else:
            phi_sm = self.phi_sm_net(x, sigma.log() / 4.0)     # UNet 现有行为
```

**关键**：`backbone="unet"` 默认值保证 `train_bvaware.py / train_mvp.py` **不动一行**仍能跑。

---

### 2.4 W5-D · 训练脚本 + 配置

#### 2.4.1 `scripts/train_foundation.py`

**结构（与 `train_bvaware.py` 同款，但混合 PDE）**：

```
1. 读 YAML 配置 (pdes 列表 + model + train + loss)
2. 构建 MixedPDEDataset → DataLoader
3. 根据 model.type 实例化:
   - "dit_plain"   → FoundationScore(...)
   - "dit_bvaware" → BVAwareScore(backbone="dit", ...)
4. 训练循环:
   for batch:
     pde_ids = batch["pde_id"]
     x_target = batch["x_target"]
     ic       = batch["ic"]
     loss_dsm = get_dsm_loss(model, x_target, sigmas, conditioning=ic, pde_id=pde_ids)
     loss_bv  = get_bv_loss(...)
     loss_time = get_godunov_time_loss(..., flux_dispatch=pde_flux_table[pde_ids])
     loss = λ_dsm·dsm + λ_bv·bv + λ_time·time
     loss.backward()
5. AMP + grad accumulation 支持 (AMP 与 BVAwareScore 的 autograd.grad create_graph=True 可能冲突,
   需要测试: 用 GradScaler + create_graph 兼容性。如果不兼容, BVAware 路径降级 fp32)
```

**Loss 改造**：在 `losses.py` 中**新增**（不删原函数）：

```python
def get_dsm_loss(model, x, sigma, conditioning=None, ic=None, pde_id=None):
    # 仅在 model 接受 pde_id 时透传; 否则忽略 (通过 try/except 或 inspect)
    ...
```

或者更干净：新增 `losses_pde_aware.py` 文件，但**优先**就地扩展（添加 kwarg + 默认 None），保持现有调用兼容。

**Flux 派遣**：在 `losses.py` 添加 `godunov_flux_dispatch(ul, ur, flux_type: str)`，路由到 burgers 或 BL。

#### 2.4.2 `configs/foundation/{tiny,small,base}.yaml`

```yaml
# tiny.yaml — RTX 4060 / Colab T4 可跑
experiment:
  name: "foundation_tiny"
  epochs: 100
  learning_rate: 2.0e-4
  batch_size: 32
  grad_accum_steps: 2
  use_amp: true             # base/small AMP; tiny 关
  nu: 1.0
  tau_max: 1.0

model:
  type: "dit_bvaware"       # "dit_plain" | "dit_bvaware"
  in_channels: 2            # noisy_u + IC (常数, 由 dataset conditioning_type 决定)
  Nx: 128
  dit:
    dim: 256
    n_layers: 6
    n_heads: 4
    patch_size: 4
    dropout: 0.1

loss:
  lambda_dsm: 1.0
  lambda_bv: 0.1
  lambda_time: 0.5

data:
  conditioning_type: "ic"
  pdes:
    - name: "burgers"
      data_file: "burgers_1d_N5000_Nx128.npy"
      flux_type: "burgers"
      weight: 1.0
    - name: "buckley_leverett"
      data_file: "bl_1d_N5000_Nx128.npy"
      flux_type: "buckley_leverett"
      weight: 1.0
  mix_strategy: "uniform"   # "uniform" | "weighted_by_size"

# small.yaml: dim=512, n_layers=8, n_heads=8, batch=64, no grad_accum
# base.yaml:  dim=768, n_layers=12, n_heads=12, batch=128 (服务器多卡可用)
```

---

### 2.5 W5-E · `scripts/eval_foundation.py`

**职责**：

1. 加载 ckpt + 重建模型（从 ckpt 同目录 cfg 自动推断）
2. 对配置中**每个** PDE：
   - 加载 test split → ground truth
   - sampler 生成 N 个样本 (PDE-id 显式传入)
   - 计算 W₁、L¹ rel err、shock-loc err
3. 生成对比表（行=PDE，列=指标）+ 三栏图（gt / DiT-Plain / DiT-BVAware）→ `Output/black/foundation/<run>/`

**接口与现有 `eval_viz.py` 风格一致**，但循环 PDE。

---

### 2.6 W5-F · 服务器部署 + tmux

**步骤**：

1. SSH 测试连通：`ssh -p 227 liuyanzhi@202.121.181.105`（端口 227）
2. 同步代码：`git push origin feat/foundation-model-20260430`，服务器 `git pull`
3. 检查环境：`tmux ls`（确认现有 3 个 session 名），`nvidia-smi`（确认空闲 GPU id）
4. 启动 tmux session（命名 `foundation_small`）：
   ```bash
   tmux new -s foundation_small
   conda activate /home/liuyanzhi/miniconda3/envs/ljz_env/
   cd /home/liuyanzhi/ljz/EntroDiffCode
   CUDA_VISIBLE_DEVICES=<空闲 id> python PROJECT/black/scripts/train_foundation.py \
       --config PROJECT/black/configs/foundation/small.yaml
   # Ctrl+b d 脱离
   ```
5. 服务器版 `env_config.yaml` 单独维护（不 commit），num_workers=4

---

## 3. Worktree 与 Git 规范

### 3.1 分支命名

| Worktree | 分支 |
|---|---|
| A | `feat/dit-1d-backbone-20260430` |
| B | `feat/mixed-pde-dataset-20260430` |
| C | `feat/dit-scores-20260501` |
| D | `feat/train-foundation-20260501` |
| E | `feat/eval-foundation-20260501` |

### 3.2 Commit 粒度

每个文件一次 commit；`{类型}({模块}): {简要}`，如 `feat(models): DiT-1D backbone with PDE embedding + AdaLN`。

### 3.3 合并顺序

A → B → C → D → E（按依赖链）。每条线 sub-agent 完成后由主 AI（你）跑 merge dry-run 再合 main。

---

## 4. 风险点（Sub-Agent 必读）

1. **BVAwareScore + DiT + AMP 三件套**：BVAware 内部 `autograd.grad(create_graph=True)`，AMP 的 GradScaler 对二阶梯度有限制。tiny 配置先关 AMP 验证；small/base 上单独测 AMP-BVAware 兼容性，不行就降级 fp32。
2. **patch_size=4 整除约束**：Nx 必须能被 patch 整除。Burgers/BL 都 128 OK。新加 PDE 时 README 提示用户。
3. **PDE flux 派遣的 batch 内异质**：一个 batch 里同时有 burgers 和 BL 样本 → `get_godunov_time_loss` 必须按 pde_id 分组计算 flux。简化方案：batch 内分 mask，分组 forward Godunov，结果 concat。
4. **DiT 对 1D shock 的 attention 失败模式**：如果 patch_size=4 仍把 shock 切到两个 patch，attention head 可能学不到。备选：positional encoding 用更高分辨率（Nx 维 sinusoidal）；先观察首批结果。
5. **服务器 conda env 缺包**：DiT 不需要新依赖（只用 torch.nn），但 mixed_pde_dataset 用 PyYAML 和 numpy 都已在。

---

## 5. 验收标准

- [ ] 所有现有脚本（train_mvp, train_baseline, train_bvaware, eval_viz）跑通，输出与改动前 bit-wise 一致（通过 `diff` 验证 ckpt loss 曲线）
- [ ] DiT1D 单元测试通过（shape / pde_id=None / grad）
- [ ] MixedPDEDataset 在 N=2 PDE 上跑通；新增第 3 个 PDE 仅改 YAML
- [ ] FoundationScore 与 BVAwareScore(backbone="dit") 在 tiny 配置下 forward+backward 不爆显存（4060 8GB）
- [ ] train_foundation.py 在 PC 上 5 epoch 收敛 (loss 下降)
- [ ] eval_foundation.py 输出表格 + 3 PDE figure（即使数字不漂亮也要先有）
- [ ] 服务器 tmux session 跑通 small 配置至少 1 epoch
