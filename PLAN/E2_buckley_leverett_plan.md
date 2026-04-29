# E2 Buckley–Leverett 开发计划

> **项目**: EntroDiff · **实验**: E2 · **日期**: 2026-04-29  
> **目标**: 在 1D Buckley–Leverett 方程上对比 EntroDiff (BVAwareScore + Godunov) vs EDM Baseline，验证非凸通量下 rarefaction+shock 混合波的物理一致性优势。

---

## 1. PDE 简介

Buckley–Leverett 方程是一个标量守恒律：

$$
\partial_t u + \partial_x f(u) = 0, \quad f(u) = \frac{u^2}{u^2 + (1-u)^2}
$$

其中 $u \in [0,1]$ 是饱和度（saturation），通量 $f(u)$ 具有 **S 形非凸** 结构：

- $f(0)=0$, $f(1)=1$
- $f'(u) \geq 0$ 在 $[0,1]$
- $f''(u)$ 变号（在 $u \approx 0.5$ 处有 inflection）
- 典型的 Riemann 问题产生 **shock + rarefaction 复合波**（compound wave）

**论文对齐**：E2 验证 Theorem 1 (double-Burgers coupling) 和 Theorem 4 (Rankine-Hugoniot admissibility) 在非凸通量下的推广。

## 2. 为什么我们的方法预期拉开差距

| 特征 | Baseline (中心差分 + StandardScore) | EntroDiff (Godunov + BVAwareScore) |
|---|---|---|
| **shock 处理** | 中心差分离散在 shock 处震荡（Gibbs 现象） | Godunov flux 间断处迎风，BVAwareScore tanh 层硬编码 shock 剖面 |
| **rarefaction 处理** | 非凸通量下，中心差分的数值粘性不足 → 非物理熵违反 | Godunov flux 单调且熵满足，Osher 公式精确处理 sonic point |
| **复合波 (shock+rarefaction)** | 两处都产生误差，互相干扰 | 分别精确处理，互不干扰 |

预期 W₁ 差距扩大 **15-20%**（vs E1 的 ~5%）。

## 3. 需要新增的模块

### 3.1 `src/pdes/bl_solver.py` — Buckley–Leverett Godunov 求解器

**非凸 Godunov flux（Osher 公式）**：对通量 $f(u) = u^2/(u^2+(1-u)^2)$，

$$F^{\mathrm{God}}(u_L, u_R) = 
\begin{cases}
\min_{u \in [u_L, u_R]} f(u) & u_L \leq u_R \\
\max_{u \in [u_R, u_L]} f(u) & u_L > u_R
\end{cases}$$

由于 $f$ 非凸，min/max 不能简单取端点值——需要在区间内搜索局部极值。$f'(u)=0$ 的解：

$$f'(u) = \frac{2u(1-u)}{(u^2+(1-u)^2)^2} = 0 \quad\Rightarrow\quad u=0 \text{ 或 } u=1$$

所以 $f(u)$ 在 $[0,1]$ 上单调增，Godunov flux 退化为简单的：

$$F^{\mathrm{God}}(u_L, u_R) = \begin{cases} f(u_L) & u_L < u_R \\ f(u_R) & u_L \geq u_R \end{cases}$$

**关键发现**：$f(u)$ 实际上是单调的！Godunov flux 退化为迎风格式。但 $f''(u)$ 变号意味着 wave speed 的排序可能非平凡——可能产生复合波。实际 Godunov 求解需要 Riemann 问题的精确解，但在标量情况下上述公式就是精确的。

**接口**：
```python
def bl_flux(u):           # f(u) = u²/(u²+(1-u)²)
def bl_godunov_flux(ul, ur):  # Godunov 数值通量
def bl_godunov_step(u, dt, dx):  # 一步 Godunov 推进
def solve_bl_1d(u0, nx, nt, dt, dx):  # 完整时间推进
```

### 3.2 `scripts/generate_bl_data.py` — 数据生成

- IC: 跳跃型初始条件 `u0 = uL if x < π else uR`（多种 (uL, uR) 组合）
- 每组合 500 样本，共 2000–5000 样本
- 标准参数: Nx=128, T=0.5, (uL,uR) ∈ {(0.8,0.2), (0.2,0.8), (0.6,0.1), (0.1,0.9), (0.9,0.3)}
- Output: `bl_1d_N5000_Nx128.npy`

### 3.3 `configs/experiment/e2_bl.yaml` — 实验配置

参考 `mvp_burgers.yaml`，专用超参：
- nu=1.0 (VE-SDE 单位粘度)
- lambda_bv=0.1, lambda_time=1.0
- epochs=200 (服务器) / 10 (本地 MVP 验证)
- data_file: "bl_1d_N5000_Nx128.npy"

### 3.4 scripts 复用

- `train_mvp.py` → 改 data_file + config 即可复用 ✓
- `eval_viz.py` → 改 data_file 即可复用 ✓
- `eval_step_ablation.py` → 直接复用 ✓

## 4. TDD 开发步骤

### Step 1: flux 单元测试 ← 先写测试
`tests/test_bl_flux.py`:
- test: f(0)=0, f(1)=1, f(0.5)=0.5
- test: 单调性 (u 递增 → f(u) 递增)
- test: Godunov flux 符号正确

### Step 2: solver 实现
`src/pdes/bl_solver.py`
- 实现 flux + Godunov 推进
- 对简单 Riemann 问题手动验证 shock speed

### Step 3: 数据生成 + 可视化
- 生成 (0.8,0.2) 的 Riemann 解
- 画出 u(x) 的时空演化 → 确认有 shock + rarefaction
- 与 WENO5 参考解对比

### Step 4: 训练 + eval
- 用 train_mvp.py 训 10 epoch MVP
- eval_viz 出对比图
- 对比 W₁：EntroDiff vs Baseline

## 5. 时间估计

| 步骤 | 工时 |
|---|---|
| flux 测试 | 15 min |
| solver 实现 | 30 min |
| 数据生成脚本 | 20 min |
| 数据生成运行 | ~1 min |
| 训练 MVP 测试 | 5 min (10 epoch) |
| eval 对比 | 2 min |
| **总计** | **~1.5 h** |

## 6. 风险

| 风险 | 应对 |
|---|---|
| $f(u)$ 单调导致 Godunov flux 过于简单，没有预期中的 rarefaction 优势 | 即使单调，$f''(u)$ 变号导致 compound wave 结构，中心差分仍可能产生非物理解。如 gap 仍小，尝试 **多组分 Buckley-Leverett** (有粘性项的变体) |
| BVAwareScore 在非 Gauss-like 分布上表现差 | Buckley-Leverett 的解分布在 [0,1] 内，不是纯高斯 → 验证是否需 `sigma_data` 调整 |
