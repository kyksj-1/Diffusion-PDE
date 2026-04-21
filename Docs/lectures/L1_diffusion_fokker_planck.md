# L1 扩散模型与 Fokker-Planck 方程的等价性

> **本讲定位**：把"扩散模型"这个机器学习术语彻底翻译回物理系学生熟悉的 SDE/FP 框架。
> **先修**：朗之万方程、布朗运动、Fokker-Planck 方程、Itô 公式（最基础版本即可）。
> **后续依赖**：L2（最优传输）、L3（JKO）、L5（Score–Burgers）均承袭本讲的符号与公式。
> **长度**：约 4500 字。

---

## §0 本讲的目标

"Diffusion Model（扩散模型）"是机器学习社区最近几年的流行词。但对物理系学生来说，这个名字恰恰指向**你从大二统计物理就已经熟悉的那套数学**：布朗运动、Langevin 方程、Fokker–Planck 方程。本讲要做的事只有一件：

> *把"扩散模型"这个黑箱拆开，让你看到它不过是 FP 方程在机器学习话术下的一次重新包装。*

读完本讲，你应该能**用自己的话**给出下表的对应关系：

| 机器学习术语 | 物理/数学对应物 |
|---|---|
| "前向过程 (forward process)" | 把数据扩散到 Gaussian 的 Langevin SDE |
| $p_\tau(u)$，"noised density" | FP 方程在时间 $\tau$ 的解 |
| "score function" $s(u, \tau)$ | 对数密度梯度 $\nabla_u \log p_\tau(u)$ |
| "反向采样 (reverse sampling)" | 时间反演后的 Langevin SDE |
| "denoising score matching" | 回归问题，学经验密度的对数梯度 |
| "Tweedie's formula" | 给定噪声样本求原样本条件期望 |

路径 A 所有定理都建立在这张表之上。本讲把它一条一条过清楚。

---

## §1 设定与符号约定（全书通用）

| 符号 | 含义 |
|---|---|
| $u \in \mathbb{R}^N$ | 我们关心的向量（可视为 PDE 解在网格上的离散化，或更一般的数据点） |
| $\rho(u)$ | 数据分布（target，未知 but 有采样） |
| $\tau \in [0, T_d]$ | **扩散时间**（注意：与物理时间 $t$ 区分；$t$ 在 L4/L5 引入） |
| $p_\tau(u)$ | $u$ 在扩散时间 $\tau$ 的边际密度 |
| $s(u, \tau) \coloneqq \nabla_u \log p_\tau(u)$ | score function |
| $s_\theta(u, \tau)$ | 神经网络对 $s$ 的近似 |
| $W_\tau$ | 标准 $N$-维 Wiener 过程（Brown 运动） |
| $\sigma(\tau), g(\tau), \beta(\tau)$ | 噪声水平 / 扩散系数 / VP schedule |

**约定**：全文使用 Itô 积分。$\nabla = \nabla_u$，$\Delta = \nabla \cdot \nabla$（在 $u$ 空间）。

---

## §2 前向过程：把数据变成噪声

扩散模型的第一步：**把数据分布 $\rho$ 渐变为一个已知简单分布（通常是 Gaussian）**。这通过一个 SDE 实现。业内两种主流选择：

### 2.1 VE-SDE（Variance-Exploding）

$$
\boxed{dU_\tau = g(\tau) \, dW_\tau, \qquad U_0 \sim \rho.} \tag{2.1}
$$

这是**没有漂移的 Langevin 方程**，纯扩散。物理图像：一粒子在势能为零、温度由 $g(\tau)$ 决定的环境中做布朗运动。

### 2.2 VP-SDE（Variance-Preserving）

$$
dU_\tau = -\tfrac12 \beta(\tau) U_\tau \, d\tau + \sqrt{\beta(\tau)} \, dW_\tau. \tag{2.2}
$$

这是 **Ornstein–Uhlenbeck 过程**：漂移项把 $U$ 往原点拉，扩散项把它推散。达到平稳态 $\mathcal N(0, I)$。

### 2.3 命题（SDE ⇒ FP）

**命题 2.1（Kramers 方程）**：设 SDE $dU = f(U, \tau) \, d\tau + g(\tau) \, dW$，则边际密度 $p_\tau(u)$ 满足
$$
\partial_\tau p_\tau = -\nabla \cdot (f p_\tau) + \tfrac{g^2}{2} \Delta p_\tau. \tag{2.3}
$$

**证明梗概**（物理学生熟悉版）：取任意紧支撑测试函数 $\phi(u)$。Itô 公式：
$$
d\phi(U_\tau) = \big(f \cdot \nabla \phi + \tfrac{g^2}{2} \Delta \phi\big) d\tau + g \nabla \phi \cdot dW.
$$
两边对 $U \sim p_\tau$ 取期望（Wiener 项均值 $0$），得 $\frac{d}{d\tau}\mathbb E[\phi] = \mathbb E[f \cdot \nabla \phi + \tfrac{g^2}{2}\Delta \phi]$。把左边写成 $\int \phi \partial_\tau p_\tau \, du$，右边对 $p_\tau$ 做两次分部积分，比较被积函数即得 (2.3)。∎

### 2.4 两个例子的 FP

- **VE**：$f=0$，故 $\partial_\tau p_\tau = \tfrac{g^2}{2} \Delta p_\tau$。**这正是热方程**（扩散系数 $g^2/2$）。
- **VP**：$\partial_\tau p_\tau = \tfrac{\beta}{2} \nabla \cdot(u p_\tau) + \tfrac{\beta}{2} \Delta p_\tau$。OU 过程的标准 FP。

### 2.5 闭式解（因为 FP 是线性的）

对 VE，热方程的解是 Gaussian 核卷积：
$$
p_\tau(u) = (\rho \ast G_{\sigma^2(\tau)})(u), \quad \sigma^2(\tau) = \int_0^\tau g^2(s) \, ds, \tag{2.4}
$$
其中 $G_{\sigma^2}$ 是协方差 $\sigma^2 I$ 的 Gaussian 密度。等价地，**给定 $u_0 \sim \rho$，$U_\tau | u_0 \sim \mathcal N(u_0, \sigma^2(\tau) I)$**。

对 VP，记 $\alpha(\tau) \coloneqq \exp\!\big(-\tfrac12 \int_0^\tau \beta\big)$，则 $U_\tau | u_0 \sim \mathcal N(\alpha u_0, (1-\alpha^2) I)$。

**一句话总结**：前向过程就是 *把 $\rho$ 和 Gaussian 核卷积*，越往后噪声越强，最终接近纯 Gaussian。

### 2.6 Remark：时间重参数化（之后会多次用）

对 VE 设定，定义**累计扩散时间** $\tilde\tau \coloneqq \sigma^2(\tau)/2$，则 $d\tilde\tau = (g^2/2) d\tau$，热方程 (2.3) 变成
$$
\partial_{\tilde\tau} p = \Delta p, \qquad p(u, 0) = \rho(u). \tag{2.5}
$$
单位扩散系数的标准热方程。Score Shocks（见 L5）的所有推导都在这套 $\tilde\tau$-时间下进行。

---

## §3 反向过程：从噪声回到数据

采样（即"生成"）等价于**把 SDE 反过来跑**：从 $p_{T_d} \approx \mathcal N(0, \sigma^2 I)$ 出发，倒推回 $\rho$。

问题：已知 SDE 正向的 $f, g$，反向 SDE 长什么样？

### 3.1 命题（Anderson 1982 反向 SDE）

**命题 3.1**：前向 SDE $dU = f \, d\tau + g \, dW$ 的时间反演 $\tilde U_\tau \coloneqq U_{T_d - \tau}$ 满足
$$
\boxed{dU_\tau = \big[f(U_\tau, \tau) - g^2(\tau) \, s(U_\tau, \tau)\big] \, d\tau + g(\tau) \, d\bar W_\tau,} \tag{3.1}
$$
其中 $d\bar W$ 是反向时间的 Wiener 过程，$s(u, \tau) = \nabla \log p_\tau(u)$。公式读法：**反向过程的漂移 = 正向漂移 − $g^2 \cdot$ score**。

**证明路线**（直觉版）：严谨证明用反向 Markov filtration，Anderson 给出完整版本。物理直觉非常漂亮：

- $\nabla \log p_\tau(u)$ 指向**密度更高的方向**（想想 $\log$ 的梯度：从低概率走到高概率）。
- 正向过程 (2.1) 不断把 $u$ "稀释"到 Gaussian。
- 反向过程要恢复 data，就必须**往密度高处漂**——这个漂移的精确大小正是 $-g^2 s$。

### 3.2 推论（反向 FP 方程 = 正向 FP，倒着跑）

把 (3.1) 代入命题 2.1 得反向 FP。你会发现它和正向 FP 只差一个 $\tau \to -\tau$——这是必要的一致性。

### 3.3 Probability Flow ODE（概率流 ODE）

有一个更惊人的观察：反向 SDE (3.1) 有一个**确定性孪生**。

**命题 3.2（Song et al. 2021）**：下面的 ODE
$$
\boxed{\frac{du}{d\tau} = f(u, \tau) - \tfrac12 g^2(\tau) \, s(u, \tau),} \tag{3.2}
$$
使得其解的 marginal density 与反向 SDE (3.1) 在每个 $\tau$ 都相同。

**证明梗概**：把 FP 方程 (2.3) 改写为连续性方程
$$
\partial_\tau p_\tau + \nabla \cdot (v_\tau p_\tau) = 0, \qquad v_\tau(u) = f(u,\tau) - \tfrac12 g^2(\tau) s(u,\tau).
$$
这只是代数变形（$\tfrac{g^2}{2}\Delta p = \tfrac{g^2}{2} \nabla \cdot (\nabla p) = \tfrac{g^2}{2}\nabla \cdot(p \, \nabla \log p) = \tfrac{g^2}{2}\nabla \cdot(p \, s)$）。既然 $p_\tau$ 满足一个 continuity equation，那沿速度场 $v_\tau$ 运动一批粒子，就能复现相同的 $p_\tau$。∎

**注意系数**：SDE 里是 $g^2$，ODE 里是 $g^2/2$。**这个因子 2 不是印刷错误**，它来自把 Laplacian 分成"朝密度梯度漂移 + 额外扩散"两部分。

**实用后果**：ODE 比 SDE 快（可以用确定性积分器如 Heun 二阶），也更稳。EDM（Karras et al. 2022）默认就用 ODE 采样。

---

## §4 Score Matching：怎么学到 score？

前三节已经把问题归到一点：**反向过程里唯一的"未知"是 score $s(u, \tau) = \nabla \log p_\tau(u)$**。想要采样，必须学到它。

### 4.1 原始 score matching（Hyvärinen 2005）

目标（理想中）：
$$
\min_\theta J_{\mathrm{SM}}(\theta) = \mathbb E_{u \sim p_\tau} \|s_\theta(u, \tau) - s(u, \tau)\|^2. \tag{4.1}
$$

问题：$s$ 我们不知道。Hyvärinen 的聪明观察是：**用分部积分可以把 (4.1) 改写成一个不显式依赖 $s$ 的等价目标**。

**命题 4.1（Hyvärinen）**：在光滑正则条件下，
$$
J_{\mathrm{SM}}(\theta) = \mathbb E_{u \sim p_\tau} \big[ \|s_\theta\|^2 + 2 \,\mathrm{tr}(\nabla_u s_\theta) \big] + \mathrm{const}.
$$

**推导思路**：$\mathbb E[s_\theta \cdot s] = \int s_\theta \cdot \nabla p_\tau$，分部积分得 $-\int p_\tau \nabla \cdot s_\theta = -\mathbb E[\mathrm{tr}(\nabla s_\theta)]$。

**实际问题**：$\mathrm{tr}(\nabla s_\theta)$ 在 $N$ 维需要 $\mathcal O(N)$ 次反向传播，高维不可行（$N \sim 10^4$）。

### 4.2 Denoising Score Matching（Vincent 2011）

这是真正被用的版本。核心技巧：**既然前向过程给出条件分布 $p(u_\tau | u_0)$ 是 Gaussian，就用条件 score 代替 marginal score**。

**命题 4.2（Vincent 2011 等价性）**：以下两目标差一个常数：
$$
\min_\theta J_{\mathrm{DSM}}(\theta) = \mathbb E_{\tau, u_0 \sim \rho, \varepsilon \sim \mathcal N(0, I)} \left\| s_\theta(u_0 + \sigma(\tau) \varepsilon, \tau) + \frac{\varepsilon}{\sigma(\tau)} \right\|^2. \tag{4.2}
$$

**推导**：条件分布 $u_\tau | u_0 \sim \mathcal N(u_0, \sigma^2 I)$，所以条件 score
$$
\nabla_u \log p(u_\tau | u_0) = -\frac{u_\tau - u_0}{\sigma^2} = -\frac{\varepsilon}{\sigma}. \tag{4.3}
$$
一个关键代数恒等式（可自行验证）：
$$
\mathbb E \| s_\theta - \nabla \log p_\tau \|^2 = \mathbb E \| s_\theta - \nabla \log p(u_\tau | u_0) \|^2 + \mathrm{const}.
$$
即 marginal SM 目标和 conditional SM 目标差一个与 $\theta$ 无关的常数。

**含义**：
1. 训练时只需采 $(u_0, \varepsilon)$，不需要 $s$ 的真值。
2. 目标 (4.2) 等价于**一个回归问题**：给噪声样本 $u_\tau$，预测"往哪个方向走能减少噪声"。"Denoising"的名字由此而来。
3. 这是所有现代扩散模型的训练目标（DDPM、EDM、VE、VP 都是这个损失的变体）。

### 4.3 Tweedie's Formula（下一讲要大量用）

**命题 4.3（Tweedie）**：在 VE 设定下，
$$
\boxed{\mathbb E[u_0 | u_\tau] = u_\tau + \sigma^2(\tau) \, s(u_\tau, \tau).} \tag{4.4}
$$

**证明**：从 (4.3)，$\varepsilon = (u_\tau - u_0)/\sigma$，故 $u_0 = u_\tau - \sigma \varepsilon = u_\tau + \sigma^2 \cdot (-\varepsilon/\sigma)$。而 $-\varepsilon/\sigma$ 的条件期望就是 $\nabla_u \log p_\tau(u_\tau)$（用分层期望，推导和 4.2 类似）。∎

**含义**：Tweedie 公式把 score 给出**显式含义**——它是"从噪声样本到 clean 样本"的线性修正。FunDPS 的整个理论贡献就是把 (4.4) 从有限维拓展到 Banach 空间。这个公式在路径 A 的 Theorem 2、Theorem 3 证明中反复出现。

### 4.4 工程实现：EDM 的参数化

EDM（Karras et al. 2022）把 $s_\theta$ 进一步参数化为去噪器 $D_\theta$：
$$
s_\theta(u, \tau) = \frac{D_\theta(u, \tau) - u}{\sigma^2(\tau)}, \tag{4.5}
$$
即 $D_\theta \approx \mathbb E[u_0 | u_\tau]$（由 Tweedie）。这让训练稳定性更好（不用网络预测一个方差尺度不均的向量）。

**路径 A 的 parameterization (A)** 就是用 (4.5) 作为 baseline，后面 (B)、(C) 是对它的结构化增强。

---

## §5 物理直觉总表（建议打印贴在墙上）

| 机器学习说法 | 物理/数学对应 | 公式 |
|---|---|---|
| Forward process | 零势能 Langevin SDE | $dU = g \, dW$ |
| VP Forward | Ornstein–Uhlenbeck 过程 | $dU = -\tfrac12 \beta U d\tau + \sqrt{\beta} dW$ |
| Noised density | 热方程的解 | $\partial_\tau p = \tfrac{g^2}{2}\Delta p$ |
| Score | 对数密度梯度 | $s = \nabla \log p_\tau$ |
| Reverse SDE | 时间反演 Langevin | $dU = (f - g^2 s)d\tau + g d\bar W$ |
| Probability flow ODE | 连续性方程的速度场 | $\dot u = f - \tfrac12 g^2 s$ |
| Tweedie 公式 | Gaussian 混合下条件均值 | $\mathbb E[u_0|u_\tau] = u_\tau + \sigma^2 s$ |
| Denoising score matching | 条件 score 的 MSE 回归 | $\min \|s_\theta + \varepsilon/\sigma\|^2$ |

---

## §6 与 Score Shocks 的连接（给 L5 埋伏笔）

我们在 (2.5) 已经把 VE 情况的前向 FP 写成标准热方程 $\partial_{\tilde\tau} p = \Delta p$。对 score $s = \nabla \log p = \nabla p / p$ 直接求 $\tilde\tau$ 导数：
$$
\partial_{\tilde\tau} s = \frac{\partial_{\tilde\tau} (\nabla p)}{p} - \frac{\nabla p}{p^2} \partial_{\tilde\tau} p = \frac{\nabla(\Delta p)}{p} - s \Delta p / p \cdot \ldots \quad (\text{代数，细节 L5})
$$

整理后得到 (1D 标量情形)
$$
\partial_{\tilde\tau} s = \partial_{uu} s + 2 s \, \partial_u s. \tag{6.1}
$$

**关键变换**：令 $w = -2s$，则 (6.1) 变为
$$
\partial_{\tilde\tau} w + w \, \partial_u w = \partial_{uu} w. \tag{6.2}
$$

**这是粘性 Burgers 方程**。换句话说：**扩散模型的 score 场本身就是一个 Burgers 速度场**。

这不是一个类比，是**恒等式**。这就是 Score Shocks 的 Theorem 4.3，也是路径 A 整个论文的理论钥匙。

L5 会详细展开这条等式及其推论：
- 在 $\tilde\tau \to 0$（逼近 data）时 $w = -2s$ 会形成 shock；
- shock 位置对应数据分布的 mode boundary；
- 我们的论文把这个 shock 和物理 PDE（如 Burgers、Euler）的 shock 耦合起来，得到 *double-Burgers* 结构。

---

## §7 小结与下一讲预告

**L1 一句话总结**：扩散模型的前向过程是一个 Langevin SDE（对应 FP 方程 $\partial_\tau p = -\nabla \cdot (fp) + \tfrac{g^2}{2}\Delta p$）；反向采样需要 score $s = \nabla \log p_\tau$；denoising score matching 用条件 score 把学 $s$ 变成一个回归任务。

**三件事要牢牢记住**：
1. 反向 SDE (3.1)：$dU = (f - g^2 s) d\tau + g d\bar W$；Probability flow ODE (3.2)：$\dot u = f - \tfrac12 g^2 s$。
2. Tweedie 公式 (4.4)：$\mathbb E[u_0 | u_\tau] = u_\tau + \sigma^2 s$。
3. Score 自己满足 Burgers 方程 (6.2)（Score–Burgers correspondence）。

**L2 预告**：到目前为止我们看的都是"密度视角"（$p_\tau$ 作为 $\mathbb R^N$ 上的函数）。L2 会换一个截然不同的视角——**把 $p_\tau$ 看作 $\mathcal P_2(\mathbb R^N)$（$L^2$-Wasserstein 概率空间）中的一个点**。我们会看到，在这个视角下 FP 方程具有一个惊人的结构：**它是相对熵在 $W_2$ 空间的梯度流**。这是 L3 的 JKO scheme 和路径 A 的 Theorem 5 的基础。

---

## 附录 A：常见疑问

**Q1**：为什么叫 "score"？  
A：Fisher 的"score function"在参数估计里是 $\nabla_\theta \log p_\theta(x)$（对参数求导）。这里是 $\nabla_x \log p(x)$（对变量求导）——虽然借用了同一个词，但逻辑位置不同。机器学习界约定俗成，你就把它当成 log-density gradient 的代名词即可。

**Q2**：DDPM（Ho et al. 2020）的推导看起来完全不是 SDE，是离散 Markov 链？  
A：Song et al. 2021 证明 DDPM 是 VP-SDE 的 Euler-Maruyama 离散化；它们在 $\Delta \tau \to 0$ 极限下等价。EDM 是 VE 的连续版。VP 和 VE 又被 Score Shocks §8 的坐标变换归约为同一个数学对象。所以现代讲扩散模型，直接讲 SDE 版即可，DDPM/DDIM/VP/VE/EDM 都是它的时间离散或参数化选择。

**Q3**：Score matching 和 MLE 什么关系？  
A：Score matching 是 MLE 的一个替代，适用于 unnormalized density（不需要算归一化常数）。在正则条件下，score matching 一致性（Hyvärinen）得到的估计量也是 consistent 的。但这一对比不影响我们的讨论——扩散模型用 DSM 就是因为它简单且 scale 得起来。

**Q4**：为什么不直接学 $\log p_\tau$ 而要学 score $\nabla \log p_\tau$？  
A：反向 SDE 的漂移只用到 $\nabla \log p$ 而不用 $\log p$ 本身。学 $\log p$ 还要处理归一化常数，没必要。
