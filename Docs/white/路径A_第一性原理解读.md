# 路径 A 第一性原理解读

> **写给谁看**：明白扩散模型是干嘛的、PDE 大致会写、但还没亲手写过扩散模型代码、也还没系统学过弱解 / 最优传输的物理系学生。
> **目标**：把 `Docs/idea_originality_analysis.md` §3 路径 A 的那一整段话**逐句拆开 + 把里面的 12 个黑话从零讲清**，让你看完后再翻 `path_A_method_skeleton.md` 不再卡。
> **作者口吻**：扩散模型领域的人（J. Ho 视角）+ 物理直觉优先。
> **日期**：2026-04-25

---

## 0. 30 秒先抓住路径 A 在干什么

一句话：

> **现有的扩散模型解 PDE，遇到"激波"就崩。我们用扩散模型自己内部的"激波结构"（Score Shocks 论文揭示的 Burgers 方程）反过来设计一个"懂激波"的扩散采样器，并且在数学上证明它能收敛到 PDE 的"正确弱解"（熵解）。**

如果你只能记住这一句，你就把住了整篇论文的脉。剩下的全是为这句话服务的：观察、诊断、方法、理论、实验。

---

## 1. 先把那段话**逐句翻译**成大白话

我把原文的 5 个步骤拆开，每一句给一个"大白话翻译 + 它在说什么数学对象"。

### 1.1 第 1 步 · 观察

> "主流 diffusion PDE solver（DiffusionPDE / FunDPS）在光滑 PDE 上已饱和，但**双曲型 / 尖锐解 PDE** 表现急剧下滑。"

**翻译**：现在用扩散模型解 PDE 的 SOTA 工作（DiffusionPDE 发在 NeurIPS 2024，FunDPS 发在 NeurIPS 2025），在"光滑解"的 PDE（比如低 Reynolds 数 Navier-Stokes、Darcy 流、热传导）上已经把精度刷到天花板了；但只要 PDE 的解出现**陡峭间断**（"shock / 激波"），它们就崩。

**对应数学对象**：
- "光滑 PDE" ≈ 椭圆型 / 抛物型 + 强黏性。
- "双曲型 PDE" ≈ 信息以有限速度沿"特征线"传播、容易在有限时间内出现间断的方程。Burgers、Euler、Buckley–Leverett、激波管这些。
- "尖锐解" = 解函数 $u(x,t)$ 在某个曲面上不连续，左极限 ≠ 右极限。

后面 §2.1 会从交通流的例子告诉你"shock 到底怎么自然出来的"。

### 1.2 第 2 步 · 诊断

> "用 Score Shocks (2604.07404) 的 Burgers 方程结构分析，指出标准 DDPM/EDM 的 score 会**在 shock 附近出现奇异**。"

**翻译**：2026 年的论文 *Score Shocks* 揭示了一件惊人的事——**扩散模型在反向去噪时所学的"得分函数 $s(x,\tau)$"，本身满足一个粘性 Burgers 方程**。Burgers 方程是 PDE 教科书里讲激波的"原型方程"。所以扩散模型自己内部就是个 Burgers 系统，会自己产生激波；而当我们要建模的 PDE 解里也有激波时，"score 的 shock"和"PDE 解的 shock"会狭路相逢，传统的 score 网络在这里学不准。

**对应数学对象**：
- "score" $s(x,\tau) = \nabla_x \log p_\tau(x)$，扩散模型的核心量，详见 §2.4。
- "DDPM" / "EDM"：扩散模型的两种主流实现（Ho et al. 2020、Karras et al. 2022），详见 §2.5。
- "奇异" = 这个量在 shock 处趋于无穷大或不连续。

§2.6 会专门讲 Score Shocks 论文那个"震惊"的等价关系。

### 1.3 第 3 步 · 方法

> "设计 shock-aware score parameterization——用熵解（entropy solution）的 viscosity 正则化思想，引入一个 **level-dependent viscosity schedule**，对应到一个**修改的反向 SDE / ODE**。"

**翻译**：我们要做的"方法创新"分三层：

1. **shock-aware score parameterization**：让神经网络里的 score 函数**主动把 tanh 形状的"激波层"作为内置结构**，而不是让网络从零去拟合 tanh。这样 shock 的形态由数学决定，网络只需要学"shock 在哪里、跳多大"。
2. **viscosity 正则化思想**（来自 PDE 数学家百年套路）：你不能直接解 inviscid（无黏性）双曲方程的 shock，因为方程在 shock 处没定义。但你可以加一个小小的扩散项 $\nu \Delta u$，把 shock"涂软"成一个陡峭但连续的过渡层；然后让 $\nu \to 0$，得到的极限就是物理上正确的"熵解"。
3. **level-dependent viscosity schedule**：扩散模型在不同噪声水平 $\tau$ 上有"不同强度的高斯模糊"。我们让这个模糊强度的衰减节奏**和 PDE 自己的物理黏性对齐**，使得"扩散模型的数值黏性"和"PDE 的物理黏性"同步退到 0。

**对应数学对象**：
- "反向 SDE / ODE" = 扩散模型从噪声生成数据时跑的那条随机/常微分方程，详见 §2.5。
- "viscosity / 黏性"详见 §2.3。

### 1.4 第 4 步 · 理论

> "证明（i）新方法在 BV 空间 / Wasserstein-1 距离下的收敛率；（ii）与经典 WENO/DG 方法在 Kruzhkov 熵解下的一致性。"

**翻译**：要在数学上证两件事——

- (i) 你这个新采样器跑出来的样本分布，距离"真实 PDE 解的分布"有多近？我们要在两个特别为 shock 设计的距离尺子（**BV 空间** / **Wasserstein-1 距离**）下给出收敛率（误差怎么随训练误差衰减）。
- (ii) 你跑出来的"采样解"是不是物理上正确的那个解？双曲 PDE 的弱解可能有无穷多个，但 **Kruzhkov 熵条件**会唯一挑出物理解（不会"反向产生信息"的那个）。我们要证明你的采样器吐出的解就是这个唯一的熵解，并且和教科书数值方法（**WENO / DG**）跑出来的一致。

**对应数学对象**：
- "BV 空间" = bounded-variation function space，详见 §2.7。
- "Wasserstein-1 距离" = 最优传输里的 $W_1$，详见 §2.7。
- "Kruzhkov 熵解" / "WENO" / "DG" 详见 §2.2、§2.3。

### 1.5 第 5 步 · 实验

> "经典 benchmark：Burgers、Buckley-Leverett、Euler（Sod 激波）、LeVeque 1D/2D；进阶：带 shock 的 compressible Navier-Stokes、磁流体 MHD；加分：plasma 的 Vlasov-Poisson 弱解（有分布不连续性）。"

**翻译**：实验从最经典的"激波教学方程"开始（Burgers、Sod 激波管），逐步爬到工业级（多介质、磁流体），最后用等离子体的弱解做加分项。**难度梯度**和你的 IDEA 里"高维 / 等离子体"完美衔接。

| 方程 | 难度 | 它是干啥的 | shock 长什么样 |
|---|---|---|---|
| Burgers | ★ | 最简单的非线性双曲方程 | 单个一维激波 |
| Buckley–Leverett | ★★ | 两相流（油水驱替） | shock + rarefaction 混合 |
| Euler / Sod | ★★★ | 一维空气动力学 | shock + 接触间断 + 稀疏波 |
| LeVeque 测试集 | ★★ | PDE 数值领域的标准 benchmark | 多种 |
| compressible NS | ★★★★ | 真正的可压流 | shock + boundary layer |
| MHD | ★★★★ | 磁流体（等离子体物理基础方程） | shock + 磁奇异 |
| Vlasov–Poisson | ★★★★★ | 等离子体相空间 PDE | filamentation 弱解 |

---

## 2. 把 12 个黑话从零讲清

按你看路径 A 那段话的"卡点"顺序讲。每节都是 **物理直觉 + 公式 + 在路径 A 里的角色** 三段式。

---

### 2.1 双曲型 PDE 与 shock：用堵车理解一切

#### 直觉 · 堵车的数学

想象一条直公路，车流密度 $\rho(x,t)$（单位长度上的车数）。每辆车的速度只取决于本地密度 $v=v(\rho)$（密度大开得慢），所以**通量** $f(\rho) = \rho v(\rho)$。守恒律告诉我们

$$\partial_t \rho + \partial_x f(\rho) = 0.$$

这是**标量守恒律**——双曲型 PDE 的最简形式。把 $f(\rho)=\rho^2/2$ 代进去就是 **Burgers 方程**：

$$\partial_t u + u\,\partial_x u = 0.$$

#### 直觉 · shock 是怎么自然出现的

Burgers 方程的"特征线"是 $\dot x = u$，也就是**信息以速度 $u$ 沿着 x 轴跑**。如果初始条件里左边的车跑得快（$u$ 大）、右边的车跑得慢（$u$ 小），那左边的特征线会撞上右边的——两条特征线相交意味着同一个 $(x,t)$ 处方程要求 $u$ 同时取两个值，矛盾。**这种"特征线相交"就是 shock 形成的瞬间**，对应物理上就是堵车前沿、音爆面、海啸前沿、超新星激波。

数学上，$u$ 在 shock 曲线 $x=x_s(t)$ 两侧取不同值 $u_L, u_R$，**经典意义下方程在这条线上不成立**（导数都没定义）。

#### 直觉 · 弱解 / 跳跃条件 / Rankine–Hugoniot

我们退一步：把方程乘上一个测试函数 $\varphi(x,t)$ 再积分，分部积分把导数移到 $\varphi$ 上。这样得到的方程**对不连续 $u$ 也有意义**——这个就是**弱解**。

弱解必须满足一个**跳跃关系**（Rankine–Hugoniot，简称 R–H）：shock 的速度等于通量跳跃除以解跳跃，

$$\dot x_s = \frac{f(u_L)-f(u_R)}{u_L-u_R}.$$

#### 直觉 · 但弱解不唯一！需要熵解

更糟的是，**满足弱解定义的解可能有无穷多个**——比如有的解从一个均匀状态"自发产生"两段不同状态（在物理上违反"信息不能凭空诞生"）。1970 年 Kruzhkov 写下的**熵条件**，本质就是要求"解只能让熵增、不能让熵减"，这才唯一挑出物理上正确的弱解。这个被挑出的解就叫**熵解（entropy solution）**。

> **路径 A 在哪用到这一节？**
>
> - 原文"双曲型 / 尖锐解 PDE 表现急剧下滑"——指的就是 Burgers / Euler / Buckley–Leverett 这一类。
> - 原文"Kruzhkov 熵解下的一致性"——指证明你跑出的扩散解就是 Kruzhkov 那一套挑出来的唯一物理解。
> - R–H 条件会出现在 path_A_method_skeleton.md 的 Theorem 4，是路径 A 的"实锤验证条件"。

---

### 2.2 经典数值方法 WENO / DG / Godunov：你不需要变专家，但要知道它们在论文里扮演谁

PDE 数学家用了 70 年，发展出一系列**保熵解**的数值方法：

- **Godunov 方法**：每一格的更新用"局部 Riemann 问题"的精确解。简单粗暴，一阶精度，**但保熵**。
- **WENO**（Weighted Essentially Non-Oscillatory）：高阶（5 阶常用），在 shock 附近自适应降阶来抑制振荡，是当前工业界做激波计算的主力。
- **DG**（Discontinuous Galerkin）：每个格内用多项式近似 $u$，格之间允许不连续，配合数值通量保持守恒。也保熵。

**在路径 A 里它们的角色**：

1. **生成训练数据**——你跑 WENO/DG 得到的高精度解就是扩散模型的"训练样本"。
2. **作为对比 baseline**——证明你的方法不输甚至好过 WENO（路径 A 的"加分项"）。
3. **作为理论一致性的标尺**——Theorem 4 要证你的扩散解满足和 WENO/DG 一样的 R–H + Lax 熵条件。

> 你不需要会写 WENO，理解它"是个高阶保熵的有限差分"就够了。

---

### 2.3 黏性方法 / 熵解 / viscosity 正则化：把 shock 涂软

#### 直觉

无黏 Burgers 会发展出 shock，**但加一点点扩散** $\nu \partial_{xx} u$（黏性）后变成

$$\partial_t u + u\,\partial_x u = \nu \partial_{xx} u,$$

这个方程的解永远光滑（抛物型方程的标准结果）。然后我们让 $\nu \to 0$，得到的**极限**就是无黏方程的**熵解**。这个套路叫**vanishing viscosity method**，是 PDE 数学家选出"物理上正确弱解"的最古典方式之一。

为什么是熵解？因为黏性方程满足"能量耗散"的物理图像，极限继承"熵不减"性质。这件事 Kruzhkov（1970）严格证明了。

#### 路径 A 借用了这套思想

扩散模型在反向采样时本身就有"高斯模糊在退去"的过程——这相当于**一个内置的、在时间上自动衰减的"数值黏性"**。路径 A 的关键洞察是：

> **如果让扩散模型的"黏性退化节奏"和 PDE 自己的"vanishing viscosity"对齐，那扩散模型在去噪到尾声时所学到的解，自动就是熵解。**

这就是路径 A 中"viscosity-matched schedule"的由来：

$$\sigma^2(\tau) = 2\nu_{\text{phys}}\,\tau.$$

> $\sigma(\tau)$ 是扩散模型在时刻 $\tau$ 处的噪声标准差，$\nu_{\text{phys}}$ 是目标 PDE 的物理黏性。这个 ansatz 把 score 层的 Burgers 和物理层的 Burgers **共享一个 viscous profile**。详见 path_A_method_skeleton §3.2.B。

---

### 2.4 score 到底是什么：从最大似然到去噪

#### 物理类比

设你想造一个能采样的概率密度 $p(x)$。你**不学 $p$ 本身**，而学它的"势能梯度"

$$s(x) := \nabla_x \log p(x).$$

在物理直觉里，$-\nabla \log p$ 是个"势能"的力场——如果你按 Langevin 动力学 $\dot x = s(x) + \sqrt{2}\,\dot W$ 跑下去，平稳分布就是 $p(x)$。所以**学 $s$ 就等价于会从 $p$ 采样**。

#### 为什么在扩散模型里要学不止一个 score

扩散模型把数据 $x_0 \sim p_{\text{data}}$ 加噪声变成 $x_\tau$，得到一族 noised distribution $p_\tau$，从 $p_0=p_{\text{data}}$ 到 $p_T \approx \mathcal N(0,I)$。每个 $\tau$ 上都有自己的 score $s_\tau(x) = \nabla_x \log p_\tau(x)$。

**反向去噪 = 沿 $\tau$ 倒着走，每一步用 $s_\tau$ 做"梯度上升回到高密度区"**。这就是 score-based diffusion 的 mental model。

#### 怎么训练 $s_\tau$：denoising score matching

一个奇迹般的等式（Vincent 2011）告诉我们

$$s_\tau(x_\tau) = -\frac{1}{\sigma(\tau)^2}\mathbb E[\,x_\tau - x_0 \mid x_\tau\,].$$

也就是说**学 score 等价于学"给定 $x_\tau$ 预测原始 $x_0$"**。这就是为什么扩散模型的损失长这样：

$$\mathcal L_{\text{DSM}} = \mathbb E_{\tau, x_0, \epsilon}\bigl\|D_\theta(x_0 + \sigma(\tau)\epsilon, \tau) - x_0\bigr\|^2,$$

其中 $D_\theta$ 是去噪网络，$\epsilon \sim \mathcal N(0,I)$。

> **路径 A 在哪用到这一节？**
>
> path_A_method_skeleton §3.2 给的"三种 score parameterization (A)(B)(C)"都是在选**怎么把神经网络挂到 $s_\tau$ 上**。其中 (C) "BV-aware parameterization"是核心创新：把 score 显式写成"光滑背景 + tanh 激波层"两个部分。这是因为下一节我们会看到，**$s_\tau$ 在 shock 附近的精确形态恰好就是 tanh**，硬把这个结构嵌进网络架构，就斩断了误差放大源。

---

### 2.5 反向 SDE / 反向 ODE 是什么

#### 前向：加噪声

最简单的"方差爆炸 SDE"（VE-SDE）是

$$dx = \sqrt{2\dot\sigma^2(\tau)}\,dW_\tau, \quad x_0 \sim p_{\text{data}}.$$

它把数据淹没成纯高斯。

#### 反向：去噪

Anderson 1982 的经典定理告诉我们：上面那条 SDE 对应的"反向时间 SDE"是

$$dx = -2\dot\sigma^2(\tau)\,s_\tau(x)\,d\tau + \sqrt{2\dot\sigma^2(\tau)}\,d\bar W_\tau.$$

这条**反向 SDE** 从 $\tau=T$ 处的纯噪声出发，沿着 $\tau$ 减小方向跑，跑到 $\tau=0$ 就生成一个数据样本。

#### 概率流 ODE

如果你嫌 SDE 太随机，Song et al. 2021 证明存在一个对应的**确定性 ODE**（probability-flow ODE）：

$$\frac{dx}{d\tau} = -\dot\sigma^2(\tau)\,s_\tau(x),$$

它和反向 SDE 在每个 $\tau$ 上的边缘分布**一模一样**——这意味着只要解这条 ODE 就能采样，且可以用高阶 ODE 求解器（Heun 法、DPM-Solver）少跑步数。**EDM**（Karras et al. 2022）和 path_A_method_skeleton 里用的就是这个。

#### DDPM vs EDM

| | DDPM | EDM |
|---|---|---|
| 时间参数 | 离散 0..T | 连续，统一参数化 |
| 采样器 | 反向 SDE | 概率流 ODE + Heun |
| 步数 | 1000 步典型 | 18 步即可 |
| 路径 A 选谁 | 不选 | **选 EDM**（path_A_method_skeleton §3.4） |

> **路径 A 在哪用到这一节？**
>
> 路径 A 的"修改的反向 SDE / ODE"——指的就是把上面那条标准反向 SDE 里的 $\sigma(\tau)$ 替换成 viscosity-matched schedule，把 $s_\tau(x)$ 换成 BV-aware parameterization (C)。改的就是这两个量。

---

### 2.6 Score Shocks 论文：扩散模型自己就是 Burgers 方程

这是路径 A 的**理论钥匙**，必须看懂。

#### 关键观察

把前向 SDE 的 Fokker–Planck 方程
$$\partial_\tau p_\tau = \frac{1}{2}\dot\sigma^2(\tau)\Delta p_\tau$$
两边求 $\nabla \log$，再用 Cole–Hopf 变换，**直接推出** score 满足

$$\boxed{\partial_\tau s + 2 s\cdot\nabla_x s = \Delta_x s.\quad (\star)}$$

把 $u := -2s$，这就是**带粘性的 Burgers 方程**！是不是震惊？扩散模型反向去噪所依赖的 score 场，**它在扩散时间方向上自己就是个 Burgers 流体**。

#### 推论：score 在 $\tau\to 0$ 处会发展出激波

既然是 Burgers，就会形成 shock。Sarkar 2026 证明了：

- 在数据分布的"模式之间"（两个高密度区中间的低密度走廊），score 在 $\tau \to 0$ 时会形成一个**陡峭的 tanh 形状的 layer**——这是 Burgers 经典的 viscous shock profile。
- 任何 score 估计误差，会被一个**指数因子 $\exp(\Lambda)$ 放大**（$\Lambda \approx \mathrm{SNR}/2$）。这就是为什么扩散模型在临数据端的精度特别难做高。

#### 路径 A 的杠杆

既然 score 在 shock 附近有**精确的 tanh 形态**，那就**别让神经网络从零去拟合 tanh**——直接把 tanh 写进网络架构（path_A_method_skeleton §3.2.C 的 BV-aware parameterization）：

$$s_\theta(u, \tau) = \nabla \phi^{\text{sm}}_\theta + \frac{\kappa_\theta}{2}\tanh\!\left(\frac{\phi^{\text{sh}}_\theta}{2}\right)\nabla \phi^{\text{sh}}_\theta.$$

物理意义：
- $\phi^{\text{sm}}$：光滑背景势能（远离 shock 的平滑梯度）
- $\phi^{\text{sh}}$：到 shock 的有符号距离（在 shock 处过零）
- $\kappa$：跳跃强度（受 R–H 约束）
- $\tanh$：把数学家给好的"激波 profile"硬植入

这个改动直接把 Theorem 6.3（Score Shocks）里那个 $\exp(\Lambda)$ 的放大常数**降到 $\mathcal O(1)$**，这是 path_A_method_skeleton Theorem 3 的核心收益。

---

### 2.7 BV 空间和 Wasserstein 距离：度量"shock 解"的正确尺子

为什么要发明新尺子？因为 $L^2$、$L^\infty$ 这些"光滑函数"的尺子在 shock 解上**不收敛**——错位一点点 shock 位置，$L^2$ 误差就跳大一截。

#### BV 空间（bounded variation）

定义：$f:[a,b]\to \mathbb R$ 的**全变差**

$$\mathrm{TV}(f) := \sup_{a=x_0<\cdots<x_N=b}\sum_{i=1}^N|f(x_i)-f(x_{i-1})|.$$

如果 $\mathrm{TV}(f)<\infty$，就说 $f \in BV$。

直觉：BV 函数 = "可以有间断，但'总跳跃量'有限"的函数。一个阶跃函数 $\mathbf 1_{x>0}$ 不在 $C^1$ 里，但**在 BV 里**，TV = 1。

为什么对 shock PDE 友好？Kruzhkov 1970 + Kuznetsov 1976 证明：标量守恒律的熵解是 $L^1\cap BV$ 的，且对初值在 $L^1$ 下满足"压缩性"（contraction）：
$$\|u(\cdot,t)-v(\cdot,t)\|_{L^1}\le \|u(\cdot,0)-v(\cdot,0)\|_{L^1}.$$

所以**在 $L^1+BV$ 框架下，熵解是稳定的**。这就是为什么 path_A_method_skeleton Theorem 3 选 $L^1/BV$ 做收敛尺子。

#### Wasserstein-1 距离 $W_1$

定义（最优传输形式）：
$$W_1(\mu,\nu) := \inf_{\pi \in \Pi(\mu,\nu)}\int |x-y|\,d\pi(x,y),$$
其中 $\Pi(\mu,\nu)$ 是边缘分别为 $\mu,\nu$ 的耦合。直觉是"把 $\mu$ 这堆土搬到 $\nu$ 那堆土需要的最少'土 × 距离'"。

为什么对 shock 友好？$W_1$ 对**质量的位置错位**罚款是**线性的**（错一格就错一格的费用），而 $L^2$ 是平方放大；所以 $W_1$ 不会被一点点 shock 位置抖动放大。

更妙的是 **Kantorovich–Rubinstein 对偶**：
$$W_1(\mu,\nu) = \sup_{\|f\|_{\text{Lip}}\le 1}\Bigl|\int f\,d\mu - \int f\,d\nu\Bigr|.$$

所以 $W_1$ 等于"在 1-Lipschitz 测试函数下能拉开多大的差"。这个对偶让你能用 Gronwall + Lipschitz 估计来证收敛——也是 path_A_method_skeleton Theorem 2/3 的关键工具。

#### 对应路径 A 第 4 步

所以"BV 空间 / Wasserstein-1 距离下的收敛率"就是：

> **找一个常数 $C$ 和一个指数 $\alpha \in (0,1]$，证明**
> $$W_1\bigl(\mathrm{Law}(\hat u),\,\mathrm{Law}(u^\star)\bigr)\le C\varepsilon^\alpha,$$
> **其中 $\varepsilon$ 是 score 训练误差，$u^\star$ 是 PDE 的 Kruzhkov 熵解。**

path_A_method_skeleton 里 Theorem 2 给 $\alpha=1$ 但带 $\exp(\Lambda T)$ 因子（不好），Theorem 3 用 BV-aware parameterization 把 $\exp(\Lambda T)$ 干掉、改成 $\alpha=1/2$（好）。这就是"主定理"。

---

## 3. 把 5 步逻辑链条**带数学**再走一遍

理解了 §2 之后，我们把 §1 那段话从头**用数学符号**讲一遍。这样你下次看 path_A_method_skeleton.md 就跑得顺。

### 3.1 第 1 步 · 观察（formal version）

设目标 PDE 是标量守恒律
$$\partial_t u + \partial_x f(u) = 0,\qquad u(\cdot,0)=u_0,$$
$f$ 凸，初值 $u_0$ 光滑。我们关心 $u$ 在物理时间 $T$ 处的分布 $\rho_T$（由初值分布 $\nu_0$ 推前）。

DiffusionPDE / FunDPS 的方案：训一个扩散模型 $s_\theta$ 学 $\rho_T$，反向采样得到 $\hat u \sim \hat\rho_T$。

**实证**：在 $f(u)=u^2/2$（Burgers）取 $\nu_{\text{phys}}=10^{-2}$（强黏性）下 $W_1(\hat\rho_T,\rho_T)$ 很小；但取 $\nu_{\text{phys}}=0$（无黏，shock 出现）则误差暴涨到原来的 5–10 倍。**这就是路径 A 的实验空白**。

### 3.2 第 2 步 · 诊断（formal version）

引用 Score Shocks 的核心等式 $(\star)$：score 满足

$$\partial_\tau s + 2s\nabla_x s = \Delta_x s.$$

进一步（Theorem 5.5）：在两个数据模式 $u_L, u_R$ 之间，**score 的 viscous shock profile** 是

$$s_\tau(x) \approx -\frac{u_L+u_R}{2\sigma^2(\tau)} + \frac{u_L-u_R}{2\sigma^2(\tau)}\tanh\!\left(\frac{(u_L-u_R)(x-x_s(\tau))}{4\sigma^2(\tau)}\right),$$

其中 $x_s(\tau)$ 是 score 层 shock 的位置。

**误差放大引理**（Theorem 6.3）：若 score 估计误差 $\|s_\theta-s\|_{L^2}\le \varepsilon$，则反向采样诱导的 KL 误差 $\le \varepsilon^2 \exp(\Lambda T_d)$，$\Lambda \approx \mathrm{SNR}/2$。

**结论**：score 在 shock 附近的几何（tanh）+ 反向放大（$\exp\Lambda$）=> **必须把 tanh 几何嵌入网络架构**才能干掉 $\exp\Lambda$。

### 3.3 第 3 步 · 方法（formal version）

三件武器：

1. **Viscosity-matched schedule**（路径 A 的"level-dependent viscosity schedule"）：

$$\sigma^2(\tau) = 2\nu_{\text{phys}}\tau.$$

2. **BV-aware score parameterization**：

$$s_\theta(u,\tau) = \nabla \phi^{\text{sm}}_\theta + \frac{\kappa_\theta}{2}\tanh\!\left(\frac{\phi^{\text{sh}}_\theta}{2}\right)\nabla \phi^{\text{sh}}_\theta.$$

3. **Loss family**：

$$\mathcal L = \mathcal L_{\text{DSM}} + \lambda_{\text{ent}}\,\mathrm R_{\text{ent}}(D_\theta) + \lambda_{\text{BV}}\,\mathrm{TV}(D_\theta) + \lambda_{\text{Burg}}\,\|\partial_\tau s_\theta + 2s_\theta\partial_u s_\theta - \partial_{uu}s_\theta\|^2,$$

各项分别强制：
- **熵正则**：训练时直接惩罚 Kruzhkov 熵不等式被违反的程度（保物理熵解）；
- **BV 正则**：控制去噪输出的全变差（保 $\hat u \in BV$，进入 Kruzhkov 框架）；
- **Burgers 一致性**：强迫 score 自己满足 $(\star)$（提升泛化）。

### 3.4 第 4 步 · 理论（formal version）

5 个定理（path_A_method_skeleton §4）按重要性：

| Thm | 内容 | 对应路径 A 哪一句 |
|---|---|---|
| 1 | Double-Burgers 耦合：score 层 + solution 层都满足 Burgers，且 shock set 几何对应 | 路径 A 的"Burgers structure"诊断 |
| 2 | $W_1$ 误差 $\le C\varepsilon\exp(\Lambda T)$（baseline parameterization） | 路径 A 第 4 步 (i)，但带可改进的常数 |
| 3 ⭐ | $W_1$ 误差 $\le C\varepsilon^{1/2}$（去除 $\exp\Lambda$，BV-aware parameterization） | **主定理** |
| 4 | $\sigma\to 0$ 极限下 R–H + Lax 熵条件成立 | 路径 A 第 4 步 (ii) |
| 5 | 反向 ODE 是 $W_2$ 上 JKO scheme 的神经离散 | 高阶解释 |

### 3.5 第 5 步 · 实验（formal version）

5 个 PDE 按难度梯度（path_A_method_skeleton §5）：E1 Burgers → E2 Buckley–Leverett → E3 Euler/Sod → E4 shallow-water → E5 Vlasov–Poisson（加分）。每个都用 WENO5/Godunov 生成 ground truth，对比 baseline 是 DiffusionPDE + FNO。

---

## 4. 这条路径对你（物理系学生）意味着什么

### 4.1 你已有的 / 还差的

| 模块 | 是否需要 | 你大概有 | 你需要补 |
|---|---|---|---|
| 偏微分方程基础 | 必须 | ✓ 应该有 | 弱解、Sobolev、BV、特征线 |
| 概率论 / 随机过程 | 必须 | ✓ 应该有 | 反向 SDE、Itô formula |
| 扩散模型 | 必须 | ⌀ 知道是啥 | DDPM 公式细节、EDM、score matching 推导 |
| 最优传输 | 必须 | ⌀ 不熟 | $W_p$ 定义、JKO scheme、Otto calculus |
| 双曲守恒律 | 必须 | ⌀ 不熟 | Kruzhkov 熵、Lax 熵、R–H、vanishing viscosity |
| 数值方法 | 推荐 | ⌀ 不熟 | Godunov、WENO（用就够，不用造） |
| 黎曼几何 | 加分 | ⌀ 不熟 | Otto–Villani 的 Wasserstein 几何 |

### 4.2 顺序学习路径（4 周补课）

| 周 | 学什么 | 推荐资源 |
|---|---|---|
| W1 | 扩散模型完整数学 | Yang Song 博客 "Generative Modeling by Estimating Gradients of the Data Distribution"（2021）+ Karras 2022 EDM paper |
| W2 | 双曲守恒律基础 | LeVeque 1992 *Numerical Methods for Conservation Laws* 第 3, 11, 12 章 |
| W3 | 最优传输 + JKO | Villani 2003 *Topics in Optimal Transportation* 前 3 章 + JKO 1998 原始论文 |
| W4 | 把 Score Shocks 论文精读 | arXiv:2604.07404，逐 Theorem 推 |

### 4.3 风险提示

按 path_A_method_skeleton §7：
- Theorem 3（主定理）证不出的概率"中"，冲击"高"——必须有备用计划（退化到 $\exp(\Lambda/2)$）；
- BV-aware parameterization 的 $\phi^{\text{sh}}$ 在 2D 上工程难度大——先 1D 跑通；
- 12 周时间紧——E1+E2 必做，E3-E5 增量。

---

## 5. 下一步可执行的 3 个动作

1. **看 path_A_method_skeleton.md**（你现在已经能看懂大概 70%）。把里面 Theorem 3 的"为什么 $\exp\Lambda$ 退化到 $\mathcal O(1)$"那段标黄，那是论文的命门。
2. **下载 + 精读 Score Shocks (arXiv:2604.07404)**，重点看 Section 4（Burgers 结构推导）和 Section 6（误差放大）。这是路径 A 的理论前提，绕不过去。
3. **跟我要 L1 讲义**——按 path_A_method_skeleton §6 的 W1 计划，下一份产物是 *L1 · 扩散模型与 Fokker-Planck 方程的等价性*（路径 A 的最底层基石）。读完它你就能从零推 $(\star)$。

---

## 附录 A · 一页速查表（黑话 → 大白话）

| 黑话 | 大白话 | 路径 A 中的角色 |
|---|---|---|
| 双曲型 PDE | 信息沿特征线传播、易出 shock 的方程 | 论文的目标 PDE 范围 |
| shock | 解的不连续面 | 主要难点 |
| 弱解 | 用测试函数积分意义下的解 | shock 时唯一可写的"解"概念 |
| 熵解 | 满足 Kruzhkov 熵条件的弱解 | 物理上正确的那个 |
| Rankine–Hugoniot | 跳跃速度公式 | Theorem 4 的验证条件 |
| viscosity 正则化 | 加 $\nu\Delta u$ 让 shock 涂软 | 路径 A 设计 schedule 的灵魂 |
| score | $\nabla\log p$ | 扩散模型的核心量 |
| DDPM / EDM | 扩散模型的两种实现 | 路径 A 选 EDM |
| 反向 SDE / ODE | 从噪声生成数据的微分方程 | 路径 A 修改的对象 |
| Score Shocks | 揭示 score 满足 Burgers 的论文 | 路径 A 的理论钥匙 |
| BV 空间 | 全变差有限的函数空间 | 收敛率的尺子 |
| Wasserstein-$p$ | 最优传输距离 | 收敛率的另一把尺子 |
| Kruzhkov 熵 | 唯一性的熵条件 | 一致性的判据 |
| WENO / DG | 高阶保熵数值方法 | ground truth + baseline |
| JKO scheme | 在 $W_2$ 上的"梯度流离散" | Theorem 5 的桥梁 |

---

> **如果看完仍有"卡点"，告诉我具体在哪一节卡，我把那一节再拆细到你彻底懂为止。**
