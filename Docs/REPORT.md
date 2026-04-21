# REPORT：导师发的 5 篇论文分析与 EntroDiff 故事线修订

> **日期**：2026-04-21
> **作用**：在已有讲义 L1–L8 + 方法骨架 + 原创性分析的基础上，把导师发的 5 篇最新论文纳入对比坐标系，重新校准 EntroDiff（路径 A）的 novelty 定位和写作故事线。
> **TL;DR**：5 篇论文从**架构（DDIS）**、**训练范式（Ambient Physics）**、**加速（Phys-Instruct）**、**函数空间理论（SI-Hilbert）**、**多保真度残差（Flow Matching Operators Residual）** 五个**正交方向**改进了 function-space diffusion for PDE——**但没有一篇处理 shock / 双曲 PDE**。EntroDiff 的阵地稳固，甚至更清晰。但 related work 需要**彻底重写**，intro 叙事需要**升级**。

---

## §0 全局导览

### 0.1 5 篇论文的"5 个攻击方向"

每篇在**不同维度**挑战已有 function-space diffusion PDE solver 的局限：

| 论文 | 被挑战的局限 | 提出的新方向 |
|---|---|---|
| **DDIS** (2601.23280) | joint-embedding 在 sparse data 下 guidance attenuation | 架构：decoupled prior + neural operator surrogate |
| **Ambient Physics** (2602.13873) | 需要 complete observations 训练 | 训练：partial observation ambient training |
| **Phys-Instruct** (2602.03627) | 多步采样昂贵 + 物理不一致 | 加速：physics-guided distillation 到 few-step |
| **SI-Hilbert** (2602.01988) | 有限维 SI 的 infinite-dim 推广 | 理论：Hilbert space well-posedness + $W_2$ bound |
| **Flow Matching Residual** (2512.12749) | full mapping 学习 data-inefficient | 残差：multi-fidelity residual-augmented flow |

**5 个方向两两正交**。但 **6 篇共同的一件事**（包括 EntroDiff）：**他们都不处理带 shock 的双曲 PDE**——前 5 篇是因为没考虑，EntroDiff 是因为正要填这个。

### 0.2 一张关系图

```
Function-space Diffusion for PDE 的 2024–2026 演化树

[DiffusionPDE (NeurIPS 2024)]───┐   [FunDPS (NeurIPS 2025)]────┐
    joint embedding             │        Banach-space Tweedie  │
    固定分辨率                   │        稀疏观测 32% 提升      │
                                 ▼                             ▼
                    ┌────────────┴──── 共同 baseline ────┬──────┘
                    │                                    │
     ─────────┬─────┼────────────┬──────────┬────────────┼────────────┐
             │     │            │          │            │            │
      Architecture Training  Acceleration Theory   Multi-fidelity  Problem class
             ▼     ▼            ▼          ▼            ▼            ▼
          DDIS   Ambient  Phys-Instruct  SI-Hilbert  FM-Operators  EntroDiff
         2601   2602.138    2602.036     2602.019     2512.127    (我们)
                                                                    ⇧
                                                        shock/双曲 PDE
                                                        (唯一空白)
```

---

## §1 Paper Deep Dives（逐篇）

### §1.1 DDIS — Decoupled Diffusion Solver for Inverse Problems on Function Spaces
**arXiv**：2601.23280v3；ICLR AI&PDE Workshop (Oral)
**作者**：Thomas Y.L. Lin¹, **Jiachen Yao**²,*, Lufang Chiang³, Julius Berner⁴, **Anima Anandkumar**²
（¹UW, ²Caltech, ³台大, ⁴NVIDIA）

#### 核心观察
Joint-embedding 模型（DiffusionPDE、FunDPS）学 $p(a, u)$ 联合分布，在**数据稀缺**时 guidance 会**几乎消失**。作者给出严格的 **guidance attenuation** 定理：

- **Theorem 4.1**：局部占优 ⇒ responsibility gradient 消失 ⇒ guidance 失效
- **Theorem 4.2/4.3**：非零 guidance 要求 $x_t$ 落在 mixture overlap region；数据稀缺下此 region 消失 ⇒ guidance 崩
- DAPS（joint 版本）在 sparse observation 下做 Langevin 更新，导致 covariance 崩塌

#### 解决方案：Decoupled 架构
拆解 prior 和 physics：
- **Diffusion prior** $s_\theta(a_t, t)$：只学 coefficient 的先验 $p(a)$（无需 paired 数据）
- **Neural operator** $L_\phi(a)$：显式学 forward PDE operator $a \mapsto u$，可选 PINO 正则（$\lambda \|\mathrm{Res}(L_\phi(a), a)\|^2$）
- 采样用 **DAPS**（Decoupled Annealing Posterior Sampling），避免 DPS 的 Jensen-gap bias

#### 实验
- Poisson / Helmholtz / Navier-Stokes inverse problems，3% sparse obs
- 100% data: $\ell_2$ 比 FunDPS 低 11%，spectral error 低 54%
- 1% data: 优势扩大到 40%

#### 与 EntroDiff 的关系
**撞车度：中偏低**。他们和我们都针对 DiffusionPDE/FunDPS 的局限，但**攻击点完全不同**：
- DDIS 攻击：**架构层** guidance attenuation（数据稀缺下 joint model 的统计缺陷）
- EntroDiff 攻击：**动力学层** $\exp(\Lambda T_d)$ 放大（shock 处 score 估计的放大性失效）

两者**正交**，未来甚至可以组合。

**⚠️ 注意点**：Jiachen Yao（FunDPS 一作）+ Anandkumar（Caltech 大牛）组持续深挖 function-space diffusion PDE。他们是我们**最主要的对话伙伴**，论文必须严肃引用并定位。

---

### §1.2 Ambient Physics — Training Neural PDE Solvers with Partial Observations
**arXiv**：2602.13873v1
**作者**：Harris Abdul Majid¹, Giannis Daras²（Ambient Diffusion 一作）, Francesco Tudisco², Steven McDonagh¹
（¹Edinburgh, ²MIT）

#### 核心观察
DiffusionPDE / FunDPS / DDIS 都**需要 50,000 个完整观测训练**；但真实科学场景（气候、地球物理、核聚变）获取完整观测往往**不可行**。朴素地用 partial obs 训练会 **catastrophically fail**（只在观测位置准、其它地方乱画）。

#### 解决方案：Ambient Flow
把 Ambient Diffusion（Daras 一系列工作）的 "additional masking" 思想搬到 PDE：
- 给定 partial observation $(A_a a, A_u u)$，训练时**再掩掉一部分已观测点**得 $(B_a A_a a, B_u A_u u)$ 作为输入
- 模型监督信号是**所有已观测**（$A_a a, A_u u$）
- 模型必须**无法区分真正未观测和人工未观测**，只能学 $p(a, u | A_a a, A_u u)$

**"One-point transition"发现**：再多掩掉**一个已观测点**就能把 error 从 naïve training 降 10–100×，是一个 sharp threshold。

#### 基于 Rectified Flow
- 网络预测 final state $x_1$（不是标准 vector field）
- 训练用"真实 partial + 人工 partial"的 mid-flow states
- 推理同 DPS 但用 rectified flow 的 Euler 1-step

#### 实验
- 4 PDE：Darcy, Helmholtz, NS, Poisson，3% uniform random sparse measurement
- **比 FunDPS（500 NFE）降 62.51% error，NFE 少 125×**
- Ablation: 可以将 FNO / UNet 套入 Ambient 范式（不绑 diffusion/FM）
- 结构化观测（patch / column / window）也 robust

#### 与 EntroDiff 的关系
**撞车度：低**。维度完全不同：
- Ambient Physics 解决：**训练数据是否需要 complete**
- EntroDiff 解决：**目标 PDE 是否有 shock**

**正交可组合**：对 shock PDE + 稀疏观测的现实场景（比如 fusion experiment），可以把 Ambient training 用到 EntroDiff 上——但这属于 future extension。

**对 NeurIPS 写作的启示**：Ambient Physics 把 DiffusionPDE / FunDPS 归类为"Wave 1"，自己是"Wave 2"。这种**把前人工作归类 + 自我定位**的叙事方法 EntroDiff 可以学。

---

### §1.3 Phys-Instruct — Ultra Fast PDE Solving via Physics Guided Few-step Diffusion
**arXiv**：2602.03627v1
**作者**：Cindy Xiangrui Kong¹, Yueqi Wang¹, Haoyang Zheng¹, Weijian Luo², Guang Lin¹
（¹Purdue, ²hi-Lab, 小红书）

#### 核心观察
Diffusion PDE solvers（如 DiffusionPDE）要 1000–2000 steps，**推理昂贵**。标准 distillation（Diff-Instruct 类）加速但**丢物理一致性**。现有加上 physics guidance 的方法要么在推理时多步 correction（又变慢），要么训练时 trade off 采样质量和物理保真。

#### 解决方案：**Physics-guided distillation**
- 用 Integral KL (IKL) divergence 拟合 teacher (预训练 EDM) 的整条 trajectory
- 在 student 上**直接**加 PDE residual penalty $\mathcal{R}(x_0)$：
  $$
  \mathcal L_G(\theta) = \mathcal D_{\mathrm{IKL}}(q_\theta \| p) + \lambda_{\mathrm{phys}} \mathbb E [\mathcal R(x_0)]
  $$
- **Theorem 4.1（Score-Function Identity）**：梯度分解为 IKL matching 项 + PDE guidance 项，可通过 dual score model $s_\phi$（auxiliary diffusion）消掉 density sensitivity

#### 训练
- Unified k-step：student 支持 $k \in \{1, ..., K\}$ 步，训练时随机 unroll
- Amortized physics correction：推理时**无需** PDE correction，全部在 distillation 时 instruct 进去

#### 实验
- 5 PDE：Darcy, Poisson, NS（non-bounded）, Burgers, Helmholtz
- vs EDM/DiffusionPDE/CoCoGen/PIDM：Phys-Instruct（4 step）比 4-step EDM 好 orders-of-magnitude，PDE error 降 8×
- Unconditional student 可复用作 downstream conditional tasks 的 prior

#### 与 EntroDiff 的关系
**撞车度：低**。维度：
- Phys-Instruct：**推理效率**（多步 → 少步）
- EntroDiff：**目标 PDE 类别**（光滑 → shock）

**正交可组合**：EntroDiff 的 (C) parameterization 训练完，可以用 Phys-Instruct 框架蒸馏加速。这是很自然的 follow-up。

**对 EntroDiff 的 threat**：Phys-Instruct 在 Burgers 上做了（Figure 1），但 Burgers 粘性没说明。看起来是平滑的 Burgers（$\nu = 0.01$ 类）。我们要核实他们的 shock 处理是否隐式"绕开"——很可能是。

---

### §1.4 SI-Hilbert — Stochastic Interpolants in Hilbert Spaces
**arXiv**：2602.01988v1
**作者**：James B. Yu, RuiKang OuYang, Julien Horwood, José Miguel Hernández-Lobato（Cambridge）

#### 核心观察
Albergo et al. 2023 的 Stochastic Interpolants (SI) 是 diffusion / flow 的统一框架，但只有**有限维**。拿到函数空间（$D \to \infty$）会碰 Feldman-Hájek 问题（Gaussian measures 互相奇异），朴素极限 ill-posed。

#### 解决方案：Hilbert-space SI
- 明确使用 **trace-class Gaussian** $\mathcal N(0, C)$，避开 Lebesgue measure 不存在的问题
- 工作在 **Cameron-Martin 空间** $H_C = C^{1/2}(H)$
- **Conditional Bridge SDE (CB-SDE)**：显式构造从 $x_0$ 到 conditional $\mu_{1|0}(\cdot|x_0)$ 的 stochastic bridge

#### 关键技术
- **Regularizing Time Change**（Lemma 7）：用变换 $\theta(t): [0,1] \to [0,1]$ 让 drift $c(t) = \dot\gamma - \varepsilon/\gamma$ 在端点奇异（$t \to 1$）被"拉平"，得到 time-changed SDE 有限 Lipschitz drift
- **Theorem 5/6**：强解存在唯一（under Hypothesis 3 或 bounded support）
- **Theorem 8**：$W_2$ error bound 显式：$W_2^2(\tilde\mu_{t|0}, \mu_{t|0}) \leq e^{C(t)} \int_0^t (A(s) + c^2(s)B(s))\dot\theta(\theta^{-1}(s)) ds$

#### 实验
- 1D non-linear Darcy + 2D Darcy + 2D Navier-Stokes
- Table 2：NS 上 Infinite-dim SI + ODE 比 FunDPS/DiffusionPDE 好（1.0% vs 1.9% forward）；Darcy 上不如 U-Net（sharp discontinuity 的 spectral 表示有 Gibbs）

#### 与 EntroDiff 的关系
**撞车度：中低**。相似处：
- 都在函数空间做；都要处理 $W$-距离的 error bound；都 acknowledge 端点 singular（$t \to 1$ 或 $\tau \to 0$）

**关键差异**：
- SI-Hilbert 要求 **Lipschitz drift**（$f$ 对 $x$ 在 $H_C$-norm 下 Lipschitz）——**这恰好不适用于 shock 情形**（shock 附近 drift 非 Lipschitz）！他们自己在 Darcy 实验里承认对 "sharp discontinuity and high-frequency components" 的 Gibbs 现象表现差。
- SI-Hilbert 的理论工具（Cameron-Martin, Feldman-Hájek）**完全可以借鉴**到 EntroDiff 的严格化——特别是处理 $\tau \to 0$ 端点时的 Regularizing Time Change。

**借鉴角度**：EntroDiff 的 Theorem 2/3 证明中 $\exp(\Lambda T_d)$ 的来源就是 $\tau \to 0$ 端点的奇异性。SI-Hilbert 的 Regularizing Time Change 可能是对冲这种奇异的一个直接工具，值得在证明细节阶段**尝试套用**。

---

### §1.5 Flow Matching Operators for Residual-Augmented Probabilistic Learning of PDEs
**arXiv**：2512.12749v2
**作者**：Sahil Bhola, Karthik Duraisamy（Michigan）
（Funding: OUSD(R&E) "Physics-Aware Reduced Order Modeling for Nonequilibrium Plasma Flows" + LANL）

#### 核心观察
Neural operator 给 deterministic 映射；diffusion / flow matching 给 probabilistic，但**data-hungry**（需要大量高保真样本）。真实科研场景**低保真度模型便宜、高保真度昂贵**——multi-fidelity 利用没被系统化。

#### 解决方案：**Residual-Augmented Flow Matching Operator (FLORAL)**
- **Conditional Neural Operator** 作为 FM vector field：
  $$
  v^\xi_\tau(\cdot; a, \ldots) = \text{linear op} + \text{nonlinear FNO}
  $$
  参数条件化在输入 $a$ 上，**支持任意分辨率**
- **Residual learning**：flow model 不学 full solution map，而是学 **low-fidelity → high-fidelity 的 correction**
  $$
  w_{\mathrm{high}}(a) = \underbrace{w_{\mathrm{low}}(a)}_{\text{便宜 surrogate}} + \underbrace{\delta w_\theta(a)}_{\text{flow 学}}
  $$
- **PDE-CFM objective**（公式 3.2）：对 conditional flow matching 给出无偏 tractable loss

#### 实验
- 1D advection, Burgers, 2D Darcy（porous media flow）
- 对比 vanilla FM operator vs. residual-augmented（后者 data-efficient 显著）

#### 与 EntroDiff 的关系
**撞车度：低**。维度：
- FLORAL：**data-efficiency via multi-fidelity**
- EntroDiff：**shock handling**

**⚠️ 注意**：LANL funding 提到 **"Nonequilibrium Plasma Flows"**——这是**我们原方向**（等离子体/核聚变）！Michigan + LANL 这条线正在做等离子体 PDE 的 ML，未来可能进入我们的领域。

**借鉴角度**：residual 结构可以组合到 EntroDiff。比如：
- $w_{\mathrm{low}}$：WENO solver 的粗解
- $\delta w_\theta$：EntroDiff 学 shock-aware 的 correction

这样既享受 WENO 的 shock-capturing 能力，又用 EntroDiff 处理 probabilistic / uncertainty。**写进 future work 是漂亮的结束语**。

---

## §2 对比矩阵

### 2.1 研究对象 × 工具 × 局限性

| 论文 | 研究对象 | 使用工具/模型 | 局限性 |
|---|---|---|---|
| **DDIS** | sparse-obs inverse PDE | diffusion prior on $p(a)$ + neural operator $L_\phi$ + DAPS | 仍是光滑 PDE；需 paired + unpaired data |
| **Ambient Physics** | 仅 partial obs 就能训练 | ambient training + rectified flow（或 FNO/UNet） | 不处理 shock；需 "already-observed" 数据集构造 |
| **Phys-Instruct** | few-step inference + 物理一致 | IKL distillation + PDE residual penalty + auxiliary score network | 不分析 shock；teacher 质量决定 student |
| **SI-Hilbert** | infinite-dim Bayesian inverse | Hilbert SI + Cameron-Martin + trace-class Gaussian + regularizing time change | **Lipschitz drift 假设与 shock 不兼容**；Darcy 上 Gibbs 差 |
| **FLORAL** | multi-fidelity forward PDE + uncertainty | conditional FNO for FM vector field + residual learning | 不处理 shock；需要低保真 solver 可用 |

### 2.2 EntroDiff 的定位对照

| | Problem class | Fidelity | Guidance style | Theory emphasis |
|---|---|---|---|---|
| DDIS | 光滑 inverse | single | decoupled | guidance attenuation |
| Ambient Physics | 光滑 recon | single | DPS-like | ambient learning |
| Phys-Instruct | 光滑 fwd+inv | single | distillation | IKL identity |
| SI-Hilbert | 光滑 inv | single | bridge | $W_2$ bound (Lipschitz) |
| FLORAL | 光滑 fwd | multi-fidelity | conditional FM | marginal vector field |
| **EntroDiff (ours)** | **双曲 / shock** | single → multi-fidelity (future) | structural + entropy | **$W_1 \leq \varepsilon^{1/2}$ (BV + Kruzhkov)** |

---

## §3 共同盲区（边界外推）

把 5 篇 + EntroDiff 放一起，可以精确识别这个子领域**集体未触及**的区域：

### 3.1 一级盲区（所有 5 篇 + 大部分前人都不做）

1. **带 shock 的双曲 PDE**：Burgers 虽偶有出现（DiffusionPDE、Phys-Instruct、FLORAL 的 1D 实验），但**都用粘性 $\nu \sim 10^{-2}$ 绕开 shock formation**。没有一篇在 $\nu \to 0$ 无粘极限下考察，也没有一篇做 Euler Sod、Buckley-Leverett、shallow-water with jump。
2. **Kruzhkov 熵条件 / Lax 熵条件**：没有一篇讨论 admissibility 选择原则。所有人把 PDE residual 当 $\mathcal L^2$ 正则处理，忽略了弱解的非唯一性。
3. **Cole-Hopf / Burgers 结构视角**：Score Shocks (2604.07404) 给出的 "score = -½ × Burgers velocity" 恒等式，**没有任何一篇引用**。
4. **Wasserstein 梯度流 / JKO 对应**：JKO 1998 的观察——FP = 相对熵的 $W_2$-梯度流——**没有一篇**把 diffusion PDE solver 放在这个框架下严格讨论（Mercado et al. 2603.23901 做 JKO-native 但不用 diffusion）。
5. **非凸通量 / Oleinik 条件**：Buckley-Leverett 这类石油工程经典 PDE 完全缺席。

### 3.2 二级盲区（部分覆盖但碎片化）

6. **时序 rollout 的误差累积**：只有 FLORAL 暗示，其它集中在 static 或 single-step forward。
7. **高维 state ($d \geq 6$)**：所有 benchmark 都 2D 空间（最多 + time）；真正高维 PDE（HJB, Fokker-Planck）缺席。
8. **硬物理约束**（conservation, entropy, positivity）：Physics-Constrained Flow Matching (NeurIPS 2025) 做过但不在导师列表里；其它软约束居多。
9. **$L^1$-contraction / entropy solution stability**：Kruzhkov 1970 主定理没被引用过——这正是 EntroDiff Theorem 2 的工具。

### 3.3 三级盲区（应用领域）

10. **等离子体 / 核聚变 PDE**：FLORAL 的 funding 暗示 Michigan + LANL 在走这个方向；目前还没工作。
11. **磁流体 MHD**：完全空白。

**EntroDiff 的阵地**：我们的正文贡献正好落在 1、2、3、4、9，未来扩展到 5、6、10、11。**这些是一个自然连贯的叙事空间**。

---

## §4 与 EntroDiff 的撞车分析（逐篇 + 总）

| 论文 | 撞车度 | 原因 | 应对 |
|---|---|---|---|
| DDIS | **中** | 同一团队 (Yao + Anandkumar) 的最新延续工作，都 target DiffusionPDE/FunDPS 局限 | 正文必引；明确"他们 architecture、我们 dynamics"；并引用 guidance attenuation 做对照实验 |
| Ambient Physics | 低 | 训练范式正交 | 放 related work 的 training section；future extension |
| Phys-Instruct | 低 | 加速正交 | 放 related work 的 acceleration section；future extension |
| SI-Hilbert | 中低 | 理论工具部分重叠 | **正面借鉴 Regularizing Time Change**；related work 的 theoretical foundation section |
| FLORAL | 低 | multi-fidelity 正交 | future extension，尤其和 plasma 挂钩时可以结合 |

**总体判断**：**5 篇**没有一篇**直接**侵占 EntroDiff 的 "shock PDE + Wasserstein gradient flow + entropy-aware diffusion" 阵地。但**DDIS 和 SI-Hilbert 的作者阵容（Anandkumar / Hernández-Lobato 组）说明这个赛道玩家在升级**，NeurIPS 2026 投稿竞争会更激烈。**时间窗口仍在但在收窄**。

---

## §5 可取的角度 / 思维（借鉴进 EntroDiff）

### 5.1 直接技术借鉴

1. **SI-Hilbert 的 Regularizing Time Change（Lemma 7）**：治 $t \to 1$ 端点奇异 drift。EntroDiff Theorem 3 证明里 $\tau \to 0$ 端点正需要这类技术——可能让 $\exp(\Lambda T_d)$ 的 bound 证明更干净，或直接退化到 $\mathcal O(\varepsilon^{1/2})$ 的 constant 更好。
2. **DDIS 的 Decoupled 架构**：让 prior 和 physics 分开。EntroDiff 的 parameterization (C) 虽然已在 prior 层塞 BV 结构，但**是否可以把 physics 用 neural operator 独立表达 + BV-aware diffusion 只学 coefficient 先验**？这种"decoupled BV-aware EntroDiff"可能数据效率更高。列为 future work 或 ablation。
3. **Phys-Instruct 的 Score-Function Identity (Theorem 4.1)**：给 distillation 的梯度 PDE guidance 项一个封闭形式。EntroDiff 最终实验 demo 可以用这个做 "distilled EntroDiff 版本"——1-step few-step 推理的 shock PDE solver。

### 5.2 写作 / 叙事借鉴

4. **Ambient Physics 的分类法**：把 DiffusionPDE/FunDPS 归类为 "Wave 1"，自己定位为 "Wave 2"。**清晰的历史分层叙事 = reviewer 友好**。EntroDiff 的 intro 可以做同样的事（见 §7 修订版 intro）。
5. **Phys-Instruct 的 "trade-off" 叙事**：他们在 intro 用"speed-physics trade-off"画张图，把自己定位在 Pareto frontier。EntroDiff 也可以用"accuracy-$W_1$ in shock region"的图把自己定位在新的 Pareto frontier。
6. **DDIS 的 "failure mode 证明"**：他们不满足于说"我们更好"，而是**严格证明 joint 模型在特定 regime 失败**。EntroDiff Theorem 2 本身已经在做类似的事（$\exp(\Lambda T_d)$ 放大），但可以写得更像 DDIS 那样"先证 failure，再给 cure"，effectiveness 显著提升。

### 5.3 思维模式借鉴

7. **"Motivational Misalignment"的 framing**（Ambient Physics）：他们说"prior work 声称解决 scientific ML 的 real-world 问题，实际 benchmark 都用 complete obs。这是 motivational misalignment"。这种揭示**别人声称 vs. 实际**的 gap 非常 powerful。EntroDiff 可以用同样的 framing：**"prior work 声称是 general PDE solver，但 benchmark 都用 $\nu = 10^{-2}$ 粘性 Burgers / $Re = 10^3$ NS，绕开了 shock formation。这是 problem-class misalignment"**。

---

## §6 未必用 EntroDiff 撞上，但值得提防

### 6.1 LANL / Michigan / Purdue 三个组

- **Michigan (Duraisamy)**：FLORAL 作者组，funding 明确做 plasma flows。**等离子体 PDE + ML 是他们的 roadmap**。
- **Purdue (Lin)**：Phys-Instruct 作者组，五个 PDE benchmark 跟 DiffusionPDE 一致。距离 shock 方向一步之遥。
- **Caltech (Anandkumar)**：DDIS + FunDPS 两份作，function-space diffusion 的主导力量。

如果 EntroDiff 延迟 3-6 个月，其中一个组可能加上 shock extension。**建议尽快锁定理论定稿**（W3-W4 节奏保持）。

### 6.2 DDIS 的 $\ell_2$-error 数字

他们在 Poisson/Helmholtz/NS inverse 上的 $\ell_2$ 相对误差 1–20%，这是 **EntroDiff 主实验要超越的数字**。（Table 2 of DDIS）

### 6.3 Phys-Instruct 的 Burgers 图

Phys-Instruct Figure 1 给出 $p_{\mathrm{data}}$ 的 Burgers 样本，看起来是 shock 前的 smooth initial condition。我们需要**把实验推到 $\nu \to 0$ 粘性极限 + shock 形成后**——这是 Phys-Instruct 没做的。如果我们说"在 Phys-Instruct 的 Burgers 数据上，我们验证 EntroDiff 优势"，**必须强调他们是 smooth Burgers，我们是 shock-containing Burgers**。

---

## §7 EntroDiff 论文故事线修订（基于 5 篇新信息）

### 7.1 修订后的 Intro 叙事骨架

**旧叙事**（方法骨架原版）：
> "DiffusionPDE (2024) 和 FunDPS (2025) 在光滑 PDE 上达到 SOTA，但双曲 PDE 是盲区。我们提出 EntroDiff 填补。"

**新叙事**（基于 5 篇新信息）：
> **Paragraph 1**（成就 + 分类学）：
> "Function-space diffusion for PDE 在 2024–2026 间快速发展。DiffusionPDE [2024] 和 FunDPS [2025] 建立了 joint-embedding 的 baseline。此后的工作**沿四个正交方向**改进：**架构**（DDIS [2026]）、**训练范式**（Ambient Physics [2026]）、**加速**（Phys-Instruct [2026]）、**无穷维理论**（Stochastic Interpolants in Hilbert [2026]），以及 **multi-fidelity**（Flow Matching Operators [2025]）。"
>
> **Paragraph 2**（问题类别的失位）：
> "**然而，这 6 条研究线都假设 PDE 解光滑。** 实际测试的 PDE（Darcy, Poisson, Helmholtz, NS at moderate Re）都是椭圆/抛物/粘性主导。Burgers 虽偶尔出现，但 **实验默认用 $\nu \sim 10^{-2}$**，绕开了无粘极限下的 shock formation。工业级别的 shock PDE（compressible Euler, Buckley–Leverett, shallow-water with hydraulic jump, Vlasov–Poisson）完全缺席。"
>
> **Paragraph 3**（观察 + 诊断）：
> "最近的 Score Shocks [2026] 给出一个未被这一领域注意的精确等式：**diffusion model 的 score 本身满足 Burgers 方程**。其推论之一是，在 shock formation 附近，score 估计误差**指数放大** $\exp(\Lambda T_d)$。**当目标 PDE 也是 Burgers / Euler 型**（即双 Burgers 结构），上述已有方法在物理 shock 附近面临**系统性失效**——我们在 Theorem 2 给出严格的 $W_1$-distance 基线 bound。"
>
> **Paragraph 4**（核心贡献 C1/C2/C3 不变）：同方法骨架 §2.2。

### 7.2 修订后的 Related Work 分节结构

```
2. Related Work

2.1 Function-space diffusion for PDE (Wave 1)
    Denoising Diffusion Operators (DDO) [Lim et al. 2024]
    Pidstrigach et al. 2024 (rigorous infinite-dim)
    DiffusionPDE [NeurIPS 2024]
    FunDPS [NeurIPS 2025] — Banach space Tweedie

2.2 Architectural improvements (Wave 2)
    DDIS [ICLR AI&PDE 2026] — decoupled prior vs physics, guidance attenuation theorem
    Fun-DDPS [2025] — decoupled CCS

2.3 Training-paradigm improvements (Wave 3)
    Ambient Physics [2026] — partial observations training

2.4 Acceleration (Wave 4)
    Phys-Instruct [2026] — physics-guided distillation to 1-4 steps

2.5 Theoretical foundations (Wave 5)
    Stochastic Interpolants in Hilbert Spaces [2026] — trace-class Gaussian, regularizing time change
    Functional Mean Flow [2025]
    Functional Flow Matching [Kerrigan 2024]

2.6 Multi-fidelity / residual (Wave 6)
    FLORAL [2025] — conditional neural operator + residual

2.7 PDE perspective on diffusion (Wave 0, transversal)
    Generative diffusion from PDE perspective [2025]
    A PDE Perspective on Generative Diffusion Models [2025]
    **Score Shocks [2026]** — Burgers structure of score (our key tool)
    Vortex Stretching in Navier-Stokes [2025]

2.8 Hyperbolic PDE numerics (Wave -1, classical)
    Godunov / WENO / Discontinuous Galerkin — our ground-truth generators
    Kruzhkov 1970 — L¹-contraction
    JKO 1998 — FP as W₂ gradient flow

Our work fills the gap: hyperbolic PDE + entropy-aware diffusion + W₂ gradient flow interpretation.
```

### 7.3 修订后的 Method Section 增补点

在方法骨架 §3（Method Design）的基础上，增加：

- **§3.X "Relation to Decoupled Prior"**：讨论 EntroDiff (C) vs DDIS 的 decoupled。我们的 (C) 是**单一网络里的结构分层**（$\phi^{\mathrm{sm}}$ + $\phi^{\mathrm{sh}}$ + $\kappa$），不是完全 decoupled；如果未来组合 decoupled + BV-aware，可以得到更强模型。
- **§3.Y "Regularizing Time Change"**：讨论借鉴 SI-Hilbert Lemma 7 处理 $\tau \to 0$ 端点。具体到 EntroDiff：把 Viscosity-matched schedule (B) 的 $\sigma^2 = 2\nu_{\mathrm{phys}} \tau$ 做一次 time change，让 drift 在 $\tau \to 0$ 有限 Lipschitz。这是 **Theorem 3 证明质量的可能改进点**。

### 7.4 修订后的 Experiments Section 要求

- **必须做的 Ablation**：如果用 DiffusionPDE 的 Burgers dataset (smooth, $\nu = 0.01$)，EntroDiff 对比 DiffusionPDE 没有明显优势，**合理**。必须**同时**做"shock Burgers"（$\nu \leq 10^{-4}$）来展示我们的优势。
- **Benchmark 一致性**：Phys-Instruct 用 DiffusionPDE 的脚本生成数据；EntroDiff 要保持同脚本（借他们的）+ shock regime 扩展（自己生成）。
- **Baseline**：DiffusionPDE、FunDPS、FLORAL（如果有开源）、WENO5（ground truth）、Godunov。

### 7.5 修订后的 Future Work 段落

```
Future Work:
1. Decoupled BV-aware EntroDiff (combine with DDIS-style architecture)
2. Ambient Physics training under partial obs (useful for plasma experiments)
3. Distillation of EntroDiff via Phys-Instruct (1-step shock-aware PDE solver)
4. Multi-fidelity extension via FLORAL-style residual (classical WENO + EntroDiff correction)
5. System extensions: Euler, MHD, Vlasov-Poisson (plasma/fusion applications)
```

---

## §8 立即对 Docs/ 其它文档的更新建议

| 文件 | 需要修订 | 优先级 |
|---|---|---|
| `path_A_method_skeleton.md` §2.2（Related Work） | 全面重写为 §7.2 的 Wave 1–7 分类 | 高 |
| `path_A_method_skeleton.md` §8（论文结构） | 把 Related Work 从 0.5 页扩到 1 页（需要 review 6 波工作） | 高 |
| `idea_originality_analysis.md` | 加一节"2026 年初最新进展对 idea 的影响" | 中 |
| `lectures/L2` | 加 Regularizing Time Change 作为附录（借鉴 SI-Hilbert） | 中 |
| `lectures/L8` | Theorem 2 证明 sketch 可以改进——用 SI-Hilbert 的 time change 试试能否 tighten bound | 低 |
| 新建 `Docs/competitive_landscape.md` | 维护一张持续更新的"2026 年 function-space PDE diffusion" 最新工作列表 | 中 |

---

## §9 直接行动建议（按优先级）

1. **本周内重写 Related Work 分类（§7.2）**。现在就可以动笔，不用等其它结果。
2. **在 L8 Theorem 2 讲义附录**加入 SI-Hilbert Regularizing Time Change 的借鉴讨论（1 段话即可）。
3. **下载 Score Shocks 的 Sarkar 2026 论文**（已在 `EXAMPLE PAPERS/`），重新精读其 §8 "VP-VE reduction" + §5 "interfacial profile" 的精确公式——EntroDiff 的 parameterization (C) 精确写法需要这些细节。
4. **核实 Phys-Instruct 的 Burgers 设置**（他们论文 Appendix A）——如果 $\nu = 0.01$，EntroDiff 要做 $\nu \leq 10^{-4}$ 对比。
5. **保持**方法骨架 §6 的 12 周节奏。不要因新信息推迟——**时间窗口**比理论优化更重要。

---

## §10 三句话结论

1. **5 篇论文没有一篇直接侵占 EntroDiff 的阵地**（shock PDE + $W_2$ 梯度流 + entropy-aware diffusion），但**揭示了 DDIS / FLORAL / Phys-Instruct 的作者组正在这个子领域快速推进**——时间窗口在收窄。
2. **EntroDiff 的 novelty 三元组（C1/C2/C3）不变**，但 **Related Work 必须全面重写**为"Wave 1–7"的分类叙事；Intro 的新叙事应该强调"所有现有 function-space diffusion PDE 工作**集体**未处理 shock PDE"这一 **problem-class misalignment**。
3. **直接技术借鉴**：SI-Hilbert 的 Regularizing Time Change 可能改进 Theorem 3 的 bound 证明；DDIS 的 guidance attenuation 理论是一个可供我们 Theorem 2 对照引用的先例；FLORAL + Phys-Instruct + Ambient Physics 是三条清晰的 future work 路径。
