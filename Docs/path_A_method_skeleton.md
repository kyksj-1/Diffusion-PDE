# Path A Method Skeleton: Entropy-Aware Diffusion for Hyperbolic PDEs

> **项目代号**：**EntroDiff**（暂定）—— Entropy-Aware Diffusion for Hyperbolic PDE Solving
> **投稿目标**：NeurIPS 2026（Main Conference，理论重度）
> **文档目的**：给出论文的**骨架 + 理论路线图 + 实验计划 + 风险对策**，为后续讲义 / 公式推导 / 代码实现奠定统一坐标系
> **日期**：2026-04-21

---

## 0. 导航

| 节 | 内容 |
|---|---|
| 1 | 问题陈述与动机（NeurIPS intro 的三段式） |
| 2 | 核心 idea：**双 Burgers 结构**及其可利用性 |
| 3 | 方法设计：3 个 score parameterization + 4 个 loss 组合 |
| 4 | 理论路线图：5 个核心定理与证明思路 |
| 5 | 实验 benchmark：5 个 PDE，难度梯度 |
| 6 | 12 周时间表 |
| 7 | 风险与对策 |
| 8 | 论文结构（section by section） |

---

## 1. 问题陈述与动机

### 1.1 Gap（现状问题）

设 $L$ 是一个偏微分算子，我们关心初值问题
$$
\partial_t u + L(u) = 0, \quad u(\cdot, 0) = u_0, \quad x \in \Omega \subset \mathbb{R}^d, \ t \in [0, T],
$$
其中 $L$ 属于**双曲型（hyperbolic）** 一类（典型例子：Burgers、Euler、Buckley–Leverett、shallow-water、MHD、Vlasov–Poisson）。这类方程的数学特征是：
- 初值任意光滑，有限时间内仍可能发展出**不连续结构**（shock、contact discontinuity、rarefaction wave）；
- 解通常在经典意义下不存在，必须在 **weak solution + Kruzhkov 熵条件** 意义下才唯一定义。

已有的扩散类 PDE solver（DiffusionPDE [Huang et al. 2024]、FunDPS [Yao et al. 2025]）在**椭圆 / 抛物型 PDE**（Darcy、Poisson、Helmholtz）及**黏性主导的 Navier–Stokes**（$Re \sim 10^3$）上取得 SOTA。但：

1. **实验侧**：DiffusionPDE 在 Burgers 实验中取 $\nu = 0.01$，绕开了 inviscid limit 中的 shock；FunDPS 的五个 benchmark 中**没有一个是双曲型**。
2. **理论侧**：两者的 PDE residual guidance 均假设 $\mathcal{L}_{\mathrm{PDE}}$ 可用有限差分无缝计算，但**shock 附近的 FD 导数没有定义**。
3. **guarantee 侧**：现有收敛理论（如 Chen et al. 2023、Benton et al. 2024）给出的是 $L^2$ / TV / $W_2$ 距离下对**光滑数据分布**的界，**未涵盖含 shock 的情形**。

### 1.2 Observation（理论杠杆）

近期工作 Score Shocks [Sarkar 2026, arXiv:2604.07404] 给出一个意外但精确的等式：**VE-SDE 扩散模型的 score 场 $s(x,\tau) = \nabla_x \log p_\tau(x)$ 严格满足粘性 Burgers 方程**
$$
\partial_\tau u + u \cdot \nabla u = \Delta u, \quad u \coloneqq -2s. \tag{$\star$}
$$

这把一条被主流忽视的等式摆到了桌面：

> *扩散模型的 score field 本身就是一个 Burgers 速度场，它在 $\tau \to 0$（数据端）会发展出 shock；而在此时附近，score 估计误差被指数因子 $\exp(\Lambda)$, $\Lambda \approx \mathrm{SNR}/2$ 放大。*

### 1.3 Question（论文核心问题）

> **当目标 PDE 本身也是 Burgers 型（或更一般的双曲型）时，扩散模型就面临一个"双 Burgers 结构"：score 层面的 Burgers ($\star$) 和 solution 层面的目标 PDE 的 Burgers。能否利用这种结构，设计出在 $W_1$ 距离下对 Kruzhkov 熵解有收敛率保证的扩散采样器？**

---

## 2. 核心 Idea：双 Burgers 结构

### 2.1 Double-Burgers Picture

设目标 PDE 解分布在物理时间 $t$ 下的 density 为 $\rho_t(u)$（$u$ 是函数值的样本），我们让扩散模型学 $\rho_t$（对任意固定 $t$）。记扩散时间为 $\tau$（与物理时间 $t$ 正交）。

- **物理层**（solution level，$t$ 方向）：$u(\cdot, t)$ 由 hyperbolic PDE 驱动，在 $t$ 方向形成 shock。
- **Score 层**（diffusion level，$\tau$ 方向）：$-2s_\tau(u)$ 在 $\tau$ 方向由 ($\star$) 驱动，在 $\tau \to 0$ 形成 shock。

两条"Burgers"方向**正交**，但它们的 shock set $\Sigma_{\mathrm{phys}}(t) \subset \Omega$ 与 $\Sigma_{\mathrm{score}}(\tau) \subset \mathbb{R}^{N_{\mathrm{grid}}}$ 存在**几何对应**：物理 shock 位置一旦出现，就决定了解分布 $\rho_t$ 的模态分界，从而**成为 score 层 interfacial layer 的定位**。

### 2.2 Three Novelty Claims（论文三大原创贡献，intro 一句话版）

1. **Claim 1（结构观察）**：物理 PDE shock 与 diffusion score shock 同址，构成一个耦合的"双 Burgers"系统。
2. **Claim 2（算法设计）**：据此设计 **entropy-aware noise schedule + BV-aware score parameterization**，使得反向采样在 Wasserstein 距离下一致于 Kruzhkov 熵解。**实验验证**（2026-04-29）：BV-aware 参数化在 **25 Heun 步**下达到 StandardScore 基线 **50 步**的 W₁ 水平——建筑先验（硬编码 tanh interfacial profile）减少了网络对多步迭代的依赖，是少步数去噪的工程优势。
3. **Claim 3（理论保证）**：证明所提采样器在 $W_1$ 距离下对带 shock 的 1D 标量守恒律和 1D Euler 方程，具有**去除 $\exp(\Lambda)$ 放大因子**的 $\mathcal{O}(\varepsilon^{1/2})$ 收敛率（$\varepsilon$ 为 score $L^2$ 训练误差）。

---

## 3. 方法设计

### 3.1 Notation（全文统一；后续讲义承袭）

| 符号 | 含义 |
|---|---|
| $u \in \mathbb{R}^N$ | 网格离散化的 PDE 解（$N = N_x$ 或 $N_x N_t$，根据 setup） |
| $\rho(u)$ | 解的数据分布，$u \sim \rho$ |
| $\tau \in [0, T_d]$ | 扩散时间，$T_d$ 为最大噪声水平 |
| $p_\tau(u) = (\rho \ast G_\tau)(u)$ | 扩散时间 $\tau$ 处的 noised density，$G_\tau$ 是热核 |
| $s_\tau(u) = \nabla_u \log p_\tau(u)$ | score |
| $s_\theta(u, \tau)$ | 神经网络近似 |
| $\sigma(\tau), g(\tau)$ | 噪声水平函数、扩散系数 |
| $\nu_{\mathrm{phys}}$ | 目标 PDE 的物理黏性 |
| $W_p(\mu, \nu)$ | $p$-Wasserstein 距离 |
| $\mathrm{TV}(f)$ | 全变差（total variation） |

### 3.2 Three Score Parameterizations

记 score network 为 $s_\theta(u, \tau)$。

#### (A) Standard EDM baseline
$$
s_\theta(u, \tau) = \frac{D_\theta(u, \tau) - u}{\sigma(\tau)^2},
$$
其中 $D_\theta$ 是 EDM 的去噪器（Karras et al. 2022）。**这是我们的 baseline，不是 novelty**。

#### (B) Viscosity-matched schedule
让扩散方程的"数值黏性" $\sigma(\tau)^2$ 与目标 PDE 的物理黏性 $\nu_{\mathrm{phys}}$ 对齐：
$$
\sigma^2(\tau) = 2 \nu_{\mathrm{phys}} \, \tau, \quad \tau \in [0, T_d].
$$
**动机**：根据 ($\star$)，扩散的 effective viscosity 恰好是 $g(\tau)^2/2$。如果与 $\nu_{\mathrm{phys}}$ 一致，则 score 层的 Burgers 和物理层的 Burgers **共享 viscous profile**，在 $\tau \to 0$ 极限下 interfacial width 和 PDE shock width 同阶衰减。

#### (C) BV-aware score parameterization ⭐（核心 novelty）
把 score 显式分解为 *smooth background* + *interfacial tanh layer*：
$$
s_\theta(u, \tau) = \underbrace{\nabla \phi^{\mathrm{sm}}_\theta(u, \tau)}_{\text{背景梯度}} + \frac{\kappa_\theta(u, \tau)}{2} \tanh\!\left(\frac{\phi^{\mathrm{sh}}_\theta(u, \tau)}{2}\right) \nabla \phi^{\mathrm{sh}}_\theta(u, \tau).
$$

- $\phi^{\mathrm{sm}}_\theta$：光滑背景势能，预期 Lipschitz；
- $\phi^{\mathrm{sh}}_\theta$：signed distance to shock set，在 shock 处过零；
- $\kappa_\theta$：局部"跳跃强度"，由 Rankine–Hugoniot 条件决定。

**动机**：Score Shocks Proposition 5.4 证明了 VE 扩散在 interfacial layer 附近 score 的 exact 形式就是 $\frac{1}{2}\tanh(\phi/2) \nabla\phi$。我们**把这个精确结构嵌入 network architecture**，使网络不用"学习" tanh 结构，而是在数据驱动下只学 $\phi^{\mathrm{sm}}, \phi^{\mathrm{sh}}, \kappa$。这直接斩断了 Theorem 6.3（Score Shocks）中 $\exp(\Lambda)$ 的误差放大源。

### 3.3 Loss Family

记 $\mathcal{L}_{\mathrm{DSM}}$ 为标准 denoising score matching 损失。

| Loss | 形式 | 目的 |
|---|---|---|
| $\mathcal{L}_0 = \mathcal{L}_{\mathrm{DSM}}$ | 标准 | baseline |
| $\mathcal{L}_1 = \mathcal{L}_{\mathrm{DSM}} + \lambda_{\mathrm{PDE}} \|L(D_\theta)\|_{L^2}^2$ | + PDE residual | 类似 DiffusionPDE，但仅用于对比 |
| $\mathcal{L}_2 = \mathcal{L}_0 + \lambda_{\mathrm{ent}} \mathrm{R}_{\mathrm{ent}}(D_\theta)$ | + Kruzhkov 熵正则 | 核心创新 1（训练层注入熵条件） |
| $\mathcal{L}_3 = \mathcal{L}_0 + \lambda_{\mathrm{BV}} \mathrm{TV}(D_\theta)$ | + BV 先验 | 核心创新 2（控制 TV，保证 entropy solution 一致性） |
| $\mathcal{L}_4 = \mathcal{L}_0 + \lambda_{\mathrm{Burg}} \|\partial_\tau s_\theta + 2 s_\theta \partial_u s_\theta - \partial_{uu} s_\theta\|^2$ | + Burgers 一致性 | 核心创新 3（强制 score 满足 ($\star$)） |

其中 Kruzhkov 熵正则
$$
\mathrm{R}_{\mathrm{ent}}(u) = \mathbb{E}_{k} \left[ \max\{0, \partial_t |u - k| + \partial_x (\mathrm{sgn}(u - k)(f(u) - f(k)))\} \right],
$$
$f$ 是目标 PDE 的通量函数，$k$ 取遍常数。

### 3.4 Reverse-time Sampler

采用概率流 ODE + Heun 二阶积分（EDM 标准）：
$$
\frac{du}{d\tau} = -\sigma(\tau)\dot\sigma(\tau) s_\theta(u, \tau).
$$
在此上加 DPS-style guidance：
$$
\nabla_u \log p_\tau(u | y_{\mathrm{obs}}) \approx s_\theta(u, \tau) - \zeta_{\mathrm{obs}} \nabla_u \mathcal{L}_{\mathrm{obs}}(u) - \zeta_{\mathrm{PDE}} \nabla_u \mathcal{L}_{\mathrm{PDE}}(u),
$$
但 $\mathcal{L}_{\mathrm{PDE}}$ 改为**Godunov 形式的熵一致通量差分**（不是 DiffusionPDE 的直接中心差分）。

### 3.5 Foundation Model: DiT Backbone ⭐（W5 新增）

> **2026-04-30 更新**：UNet → DiT (Diffusion Transformer) 架构升维。与 UNet 的本质区别：
> - Self-attention 天然捕捉 shock 处的全局信息（卷积感受野受限）
> - AdaLN 注入 PDE type embedding，同一模型处理多类双曲 PDE
> - Patch embedding 自适应多分辨率，无需 padding 损耗

**架构**：
```
Input: [noisy_u (1) | IC (1) | PDE_token (1)] → 3 channels
  ↓ Patch Embedding → D-dimensional tokens
  ↓
× N_layers DiT Block:
  AdaLN(time_emb, PDE_emb) → Self-Attention → AdaLN → MLP
  ↓
Unpatchify → denoised_u
```

**多规模配置**（PC 单卡 → H100×6）：
| 规模 | dim | layers | heads | 参数量 | 硬件 |
|---|---|---|---|---|---|
| tiny | 256 | 6 | 4 | ~5M | RTX 4060 (PC) |
| small | 512 | 8 | 8 | ~30M | RTX 3090×1 |
| base | 768 | 12 | 12 | ~100M | H100×1 |
| large | 1024 | 24 | 16 | ~400M | H100×4-6 |

**混合 PDE 训练**：Burgers / Buckley–Leverett / Euler Sod 交替采样，PDE type token 按 sample 区分。Loss 复用现有 L_DSM + L_BV + L_time。零样本+微调接口支持适配新 PDE。

**论文定位**：§5.4 "Transfer across conservation laws" — 证明建筑先验不是 Burgers 特供，而是整个双曲 PDE 类的共性结构。

---

## 4. 理论路线图：5 个核心定理

### Theorem 1（Double-Burgers Coupling）

> **Setting**：设 $\rho_t$ 是目标 1D 标量守恒律 $\partial_t u + \partial_x f(u) = 0$ 在物理时间 $t$ 处的数据分布（由初值分布在 PDE 流下推前），$p_{\tau, t}(u) = \rho_t \ast G_\tau(u)$。
>
> **Claim**：$s_{\tau, t} = \nabla_u \log p_{\tau, t}$ 满足耦合系统
> $$
> \partial_\tau s_{\tau, t} = \Delta_u s_{\tau, t} + 2 s_{\tau, t} \cdot \nabla_u s_{\tau, t}, \qquad \partial_t \rho_t + \partial_x(f(u) \rho_t) = 0 \ (\text{on characteristics}).
> $$
>
> **Proof sketch**：$\tau$ 方向直接引用 Score Shocks Theorem 4.3；$t$ 方向是 Liouville 方程在 characteristics 上的写法（PDE solution 推前的数据分布满足连续性方程）。关键在于两个方向的兼容性：物理 shock 集合 $\Sigma_{\mathrm{phys}}(t)$ 成为 $\rho_t$ 的支集奇异性，进而决定 $s_{\tau,t}$ 的 interfacial layer 位置。

### Theorem 2（Entropy-Solution Stability）

> 设 score 训练误差 $\mathbb{E}_\tau \|s_\theta - s\|^2 \leq \varepsilon^2$。令 $\hat u$ 为 $\mathcal{L}_0$ 训练下 reverse sampler 产出的样本，$u^\star$ 为目标 PDE 的 Kruzhkov 熵解。则
> $$
> W_1(\mathrm{Law}(\hat u), \mathrm{Law}(u^\star)) \leq C_1 \varepsilon \exp(\Lambda T),
> $$
> 其中 $\Lambda = \sup_\tau \mathrm{SNR}(\tau)/2$ 是 Score Shocks 的放大指数。
>
> **Proof sketch**：Gronwall + Score Shocks Theorem 6.3 的误差放大引理 + 熵解在 $W_1$ 下的 $L^1$-contraction 性质（Kruzhkov 1970）。

### Theorem 3（Improved Rate with BV-aware Parameterization）

> 在 parameterization (C) + 损失 $\mathcal{L}_3$ 下，在足够正则性假设下：
> $$
> W_1(\mathrm{Law}(\hat u), \mathrm{Law}(u^\star)) \leq C_2 \varepsilon^{1/2},
> $$
> 即去除了 $\exp(\Lambda T)$ 的指数放大。
>
> **Proof sketch**：关键在于 parameterization (C) 使 $s_\theta$ 的 interfacial profile 不再由神经网络自由拟合，而是**继承**了 Score Shocks Proposition 5.4 的精确 tanh 形式，导致 Gronwall 常数从 $\Lambda$ 退化到 $\mathcal O(1)$。BV 正则 $\lambda_{\mathrm{BV}} \mathrm{TV}(D_\theta)$ 控制 $\hat u$ 的全变差，从而 Kruzhkov 熵解在 $L^1$-compact 集内闭。

### Theorem 4（Shock Location Consistency）

> 在 $\sigma(\tau) \to 0$ 极限下（推断的最后一步），所提采样器生成的解在 shock 位置 $x_s(t)$ 处满足 Rankine–Hugoniot 条件
> $$
> \dot x_s(t) = \frac{f(u_L) - f(u_R)}{u_L - u_R}
> $$
> 且 Lax 熵条件 $f'(u_L) \geq \dot x_s \geq f'(u_R)$ 几乎处处成立。
>
> **Proof sketch**：Score Shocks Theorem 5.11（speciation time）给出 score 层 shock 形成的精确时间；我们证明在 viscosity-matched schedule (B) 下，此时间对应的物理时间恰好是 PDE 的 shock 形成时间。Rankine–Hugoniot 从跳跃量的 score 层对应（Theorem 5.5）平移而来。

### Theorem 5（JKO Correspondence）

> 带粘性匹配 schedule (B) + 损失 $\mathcal{L}_4$ 的反向 ODE，在时间离散 $\Delta\tau \to 0$ 极限下，每一步对应
> $$
> \rho^{n+1} = \arg\min_{\rho \in \mathcal P_2} \left\{ \mathcal F(\rho) + \frac{1}{2\Delta\tau} W_2^2(\rho, \rho^n) \right\},
> $$
> 其中 $\mathcal F(\rho) = \mathrm{Ent}(\rho | \rho^\star) + \langle \text{PDE constraint} \rangle$，$\rho^\star$ 是目标 PDE 解的分布。
>
> **Proof sketch**：Jordan–Kinderlehrer–Otto 1998 的经典结果给出 Fokker–Planck 在 $W_2$ 上的梯度流结构；加上 PDE constraint 作为约束项，在 Lagrangian 框架下恢复。这个定理的价值在于**把我们的方法论从"灵感启发"落实为"Wasserstein 梯度流的神经离散"**。

### 难度标定

| Theorem | 难度 | 风险 |
|---|---|---|
| 1 | 中（组合已有结果） | 低 |
| 2 | 中（标准稳定性分析） | 低 |
| 3 | **高**（需要仔细处理 parameterization 的函数类，以及 $\Lambda$ 到 $\mathcal{O}(1)$ 的退化论证） | 中，**但这是论文主定理** |
| 4 | 中高 | 中 |
| 5 | 中（JKO 已有，关键是 constraint 处理） | 低 |

---

## 5. 实验 Benchmark

> **原则**：实验为理论服务。5 个 benchmark 按难度分层，先确保前 2 个有结果，后面做到哪算哪。
>
> **E1 当前状态（2026-04-29）**：数据 + StandardScore + BVAwareScore + Baseline 全部跑通。BV-aware 在少步数下有优势（25 步优于 baseline 50 步），但整体 W₁ 仍偏高（~0.7-0.8）。下一步：加时间信息 loss + 更大模型。

| # | PDE | 维度 | 难点 | 对比 Baseline | 关键指标 | 状态 |
|---|---|---|---|---|---|---|
| E1 | Inviscid Burgers $\partial_t u + \partial_x(u^2/2) = 0$ | 1D | 有限时间 shock | EDM Baseline、FNO | $W_1$, $L^1$, shock-location err | ✅ 闭环，待精进 |
| E2 | Buckley–Leverett $\partial_t u + \partial_x(u^2/(u^2+(1-u)^2)) = 0$ | 1D | 非凸通量，rarefaction + shock 混合 | EDM Baseline、WENO5 | $W_1$, $L^1$, TV | 📋 计划中 (本地 PC) |
| E3 | 1D Euler（Sod 激波管） | 1D（3 components） | 3 种波系：shock + contact + rarefaction | 同上 | $W_1$ per component | 远期 |
| E4 | 2D Shallow-Water | 2D | Hydraulic jump | FNO、U-Net-diffusion | $W_2$, jump err | 远期 |
| E5 (stretch) | 1D Vlasov–Poisson（冷束流不稳定性） | 1D$\times$1D | 弱解、filamentation | Deep Kinetic JKO（[2603.23901]） | 相空间 $W_2$ | 远期 |

**E2 策略分析**：Buckley-Leverett 的非凸通量 $f(u)=u^2/(u^2+(1-u)^2)$ 产生 shock + rarefaction 混合波。Baseline 的中心差分离散在 rarefaction 波中会产生非物理震荡（而 Godunov flux 天然处理），这是 EntroDiff 预期拉开差距的场景。工程量估计：新 Godunov solver ~100 行 + 数据生成 ~50 行 + 训练 eval 复刻 E1 模式。在本地 PC（RTX 4060）进行，不占用服务器。

**数据生成**：
- E1/E2/E3：Godunov + WENO5 作为 ground truth
- E4：HLLC Riemann solver
- E5：particle-in-cell

---

## 6. 12 周时间表

| 周 | 阶段 | 任务 | 产出 |
|---|---|---|---|
| W1 | 理论基石 | L1 + L2 讲义（FP & OT） | `Docs/lectures/L1.md`, `L2.md` |
| W2 | 理论基石 | L3 + L4 讲义（JKO & 熵解） | L3.md, L4.md |
| W3 | 理论基石 | L5 讲义（Score–Burgers） + Theorem 1 formal proof | L5.md, `Docs/thm1.md` |
| W4 | 理论突破 | Theorem 2 + Theorem 3 证明 | `Docs/thm2.md`, `thm3.md` |
| W5 | 代码基建 | 复现 EDM + DiffusionPDE baseline | `code/baseline/` |
| W6 | 代码主体 | 实现 parameterization (C) + $\mathcal{L}_3$ | `code/entrodiff/` |
| W7 | 实验 E1 | Inviscid Burgers 完整跑通 | `results/E1/` |
| W8 | 实验 E2 + Theorem 4 | Buckley-Leverett + Rankine-Hugoniot 验证 | `results/E2/`, `thm4.md` |
| W9 | 实验 E3 + Theorem 5 | Euler Sod + JKO 对应证明 | `results/E3/`, `thm5.md` |
| W10 | 写作 | Intro + Method + Theory 章节初稿 | `paper/v1.tex` |
| W11 | 实验 E4 | Shallow-water（时间宽裕才做） | `results/E4/` |
| W12 | 冲刺 | 消融 + 写作 + 投稿 | 最终 `paper/final.pdf` |

---

## 7. 风险与对策

| 风险 | 概率 | 冲击 | 对策 |
|---|---|---|---|
| Theorem 3 证不出（$\exp(\Lambda) \to \mathcal{O}(1)$ 难度估计不足） | 中 | **高**（主定理） | 备用：退而求其次证 $\exp(\Lambda/2)$，仍对 baseline 有改进 |
| BV-aware parameterization 工程难 implement | 中 | 中 | 先 1D 版本，2D 用 mesh-based $\phi$ 代替 signed distance |
| DiffusionPDE 作者是 reviewer 挑实验 | 高 | 中 | 主实验直接用他们公开数据 + 代码作 baseline，避免对方对实验细节挑刺 |
| Score Shocks 的 VP-VE equivalence 假设在实际模型中不严格成立 | 低 | 中 | 论文声明只在 VE 设定下证明，VP 留作 future work |
| 12 周时间紧，你说"实验未必能跑出来" | 中 | 高 | E1 + E2 必做（最小工作量），E3-E5 增量；理论章节做厚，实验章节做准 |
| Reviewer 认为"只是 Score Shocks 的应用" | 中 | 中 | 在 intro 强调 Theorem 1 的耦合结构、Theorem 3 的收敛率改进、Theorem 5 的 JKO 桥梁——这三者 Score Shocks 都没有 |

---

## 8. 论文结构（NeurIPS 格式，9 页正文）

```
1. Introduction (1 页)
   - Gap: 双曲 PDE 是现有扩散 solver 的盲区
   - Observation: Score Shocks 揭示 score 本身是 Burgers
   - Contribution: (C1) Double-Burgers coupling (C2) BV-aware architecture (C3) 收敛率 W_1 ≤ O(ε^{1/2})

2. Related Work (0.5 页)
   - Function-space diffusion: DDO, FunDPS
   - Diffusion PDE solver: DiffusionPDE, FlowDAS, CFO
   - PDE perspective of diffusion: Score Shocks, Generative diffusion from PDE perspective
   - Hyperbolic PDE 经典数值: Godunov, WENO, DG (仅作为 ground truth)

3. Preliminaries (0.5 页)
   - VE-SDE, score matching, Tweedie
   - Hyperbolic PDE, Kruzhkov entropy solution, BV space
   - Wasserstein distance, JKO scheme

4. Double-Burgers Structure (1.5 页)
   - Theorem 1
   - 耦合系统的几何图示

5. Method: EntroDiff (2 页)
   - BV-aware parameterization (C)
   - Loss family, entropy regularization, BV regularization
   - Reverse sampler with Godunov-form PDE guidance

6. Theory (2 页) ⭐ 论文的理论核心
   - Theorem 2, 3 (main), 4, 5
   - 各自 1 段证明 sketch, 附录给完整证明

7. Experiments (1 页)
   - E1-E3 主结果
   - E4 (如有)
   - 消融：parameterization, loss, schedule

8. Conclusion & Limitations (0.5 页)
```

**附录目标**：25+ 页，Theorem 2-5 的完整证明 + 额外实验消融。

---

## 9. 立即下一步

> 骨架确定。进入论文写作阶段
>
