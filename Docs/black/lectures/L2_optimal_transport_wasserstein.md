# L2 最优传输与 Wasserstein 几何

> **本讲定位**：把视角从"概率密度 $p_\tau$ 作为 $\mathbb R^N$ 上的函数"切换到"概率测度 $\mu$ 作为 $\mathcal P_2$ 空间中的点"。后者是 L3（JKO scheme）与路径 A Theorem 5 的数学土壤。
> **先修**：L1（密度、FP 方程、连续性方程）；本科高年级的测度论和凸分析基本直觉。
> **后续依赖**：L3、L5；路径 A Theorem 2、3、5。
> **长度**：约 4500 字。

---

## §0 为什么需要换视角

L1 里我们把数据分布 $\rho$ 和 $p_\tau$ 都当作 $\mathbb R^N$ 上的函数。这视角下 FP 方程是一个关于**密度**的 PDE。

但在路径 A 里，我们要证的定理（Theorem 2、3、5）都不是在 density 层面做的，而是在**测度之间的距离**（特别是 Wasserstein 距离 $W_1, W_2$）层面做的。原因：

- 双曲 PDE 的**解是不连续的**（带 shock），在 $\mathbb R^N$ 上不是光滑函数，$L^2$ 距离可能不稳定（比如一个单位跳跃 + 小平移，$L^2$ 距离是 $\mathcal O(1)$）；
- Wasserstein 距离对"平移"敏感但对函数正则性不敏感——这正是我们处理 shock 想要的度量。

所以**本讲的唯一目标**是：把 Wasserstein 距离 $W_p$、Wasserstein 空间 $\mathcal P_p$、以及 $W_2$ 空间上的"梯度流"这三件事讲到你能独立使用的程度。

---

## §1 Monge 问题（1781）

### 1.1 物理叙述

想象你是一位工程师。在 $\mathbb R^N$ 上有两堆土：

- 一堆初始分布由测度 $\mu$ 描述（比如一个山坡）；
- 一堆目标分布由测度 $\nu$ 描述（比如一块平地）。

你要搬运 $\mu$ 使其变成 $\nu$。"搬运计划"用一个映射 $T: \mathbb R^N \to \mathbb R^N$ 描述：在位置 $x$ 处的那粒土被送到 $T(x)$。

**要求**：搬完以后，分布必须是 $\nu$，即
$$
T_\# \mu = \nu, \qquad \text{即 } \nu(B) = \mu(T^{-1}(B)) \text{ 对所有可测 } B. \tag{1.1}
$$
读作"$\mu$ 在 $T$ 下的推前（pushforward）等于 $\nu$"。

**代价**：搬运 $\mu$-单位质量从 $x$ 到 $T(x)$ 的代价是 $c(x, T(x))$（通常 $c = \|x - y\|^p$，$p \geq 1$）。总代价
$$
\mathcal C_{\mathrm{Monge}}(T) = \int c(x, T(x)) \, d\mu(x).
$$

### 1.2 Monge 问题

$$
\boxed{\inf_T \int c(x, T(x)) \, d\mu(x) \quad \text{s.t.} \quad T_\# \mu = \nu.} \tag{M}
$$

### 1.3 Monge 问题的困难

(M) 的存在性没有保证。典型反例：$\mu = \delta_0$（原点处单点质量），$\nu = \tfrac12 \delta_1 + \tfrac12 \delta_{-1}$。任何映射 $T$ 只能把单点送到单点，不可能得到两点质量的 $\nu$——故 (M) 不可行。

**问题根源**：Monge 强制每粒土只能去一个地方。真实世界允许"一粒土劈成两半"。Kantorovich 的松弛正是修复这一点。

---

## §2 Kantorovich 松弛（1942）

### 2.1 Coupling（耦合）

**定义 2.1**：$\mu \in \mathcal P(\mathbb R^N)$，$\nu \in \mathcal P(\mathbb R^M)$。它们的 **coupling** 是 $\mathbb R^N \times \mathbb R^M$ 上的联合测度 $\pi$，其两个 marginal 分别是 $\mu, \nu$：
$$
(\mathrm{pr}_1)_\# \pi = \mu, \quad (\mathrm{pr}_2)_\# \pi = \nu.
$$
所有这样的 $\pi$ 组成集合 $\Pi(\mu, \nu)$。

物理解读：$\pi(A \times B)$ 是"从 $A$ 运到 $B$ 的质量"。一粒土现在可以被劈开送往多个目的地。

### 2.2 Kantorovich 问题

$$
\boxed{W_c(\mu, \nu) = \inf_{\pi \in \Pi(\mu, \nu)} \int c(x, y) \, d\pi(x, y).} \tag{K}
$$

### 2.3 Monge → Kantorovich

每个 Monge map $T$ 对应一个 Kantorovich coupling $\pi_T = (\mathrm{id}, T)_\# \mu$（集中在图像 $\{(x, T(x))\}$ 上）。所以 $(M) \geq (K)$——Kantorovich 是**松弛**，永远不劣于 Monge。

对上面的反例（$\mu = \delta_0$，$\nu = \tfrac12 \delta_1 + \tfrac12 \delta_{-1}$），(K) 的最优解是 $\pi = \tfrac12 \delta_{(0,1)} + \tfrac12 \delta_{(0,-1)}$——把原点处的质量一半送到 $1$、一半送到 $-1$。存在、有限，完美解决。

### 2.4 存在性（相比 Monge 的优势）

**命题 2.2**：若 $c$ 连续下半有界，$\mu, \nu$ 在 $\mathbb R^N$ 上，则 (K) 的最小值在 $\Pi(\mu, \nu)$ 中被取到。

证明基于 $\Pi(\mu, \nu)$ 在弱拓扑下的紧性 + 积分的下半连续性。工具性，跳过细节。

---

## §3 Kantorovich 对偶与 Brenier 定理

### 3.1 对偶问题

线性规划有对偶。Kantorovich 问题的对偶是：

$$
\sup_{\varphi, \psi} \left\{ \int \varphi \, d\mu + \int \psi \, d\nu \ :\ \varphi(x) + \psi(y) \leq c(x, y) \right\}. \tag{K*}
$$

**物理解读**：$\varphi(x)$ 是"收购价"（土商在 $x$ 点付给你的钱），$\psi(y)$ 是"销售价"（你在 $y$ 卖出土收到的钱）。约束 $\varphi + \psi \leq c$ 是"差价不超过自己搬运的代价"，否则你自己搬更赚。(K\*) 问：土商定价能让你做生意（不超过代价）的最大总利润。这等于 Kantorovich 搬运代价（强对偶）。

**定理 3.1（Kantorovich 对偶）**：在温和条件下，(K) = (K\*)。

### 3.2 二次代价 $c(x, y) = \tfrac12 \|x-y\|^2$：Brenier 定理

这个代价在 $W_2$ 距离中出现，也是路径 A 最关心的。此时对偶问题可以进一步化简。

**定理 3.2（Brenier 1991）**：设 $\mu, \nu \in \mathcal P_2(\mathbb R^N)$（即有二阶矩），$\mu$ 对 Lebesgue 测度绝对连续。则：
(i) 存在凸函数 $\psi: \mathbb R^N \to \mathbb R$，使得 $T = \nabla \psi$ 是唯一的最优 Monge map，$T_\# \mu = \nu$；
(ii) 唯一最优 coupling 是 $\pi = (\mathrm{id}, \nabla \psi)_\# \mu$（集中在 $\nabla \psi$ 的图像）。
(iii) Monge 与 Kantorovich 最优值相等。

**解读**：在二次代价下，**最优 transport map 永远是一个凸函数的梯度**。这和我们熟悉的"最速下降 = 梯度"有相通的几何精神。

**对路径 A 的用处**：后面 L3 的 JKO scheme 每一步都是求一个 $W_2$ 距离下的 proximal（"离上一步最近 + 使目标泛函减小"），Brenier 定理告诉我们 proximal 的解总是一个凸函数的梯度。这是把 $W_2$-gradient flow 变成可计算对象的关键。

### 3.3 一维的特殊公式

1D 情况特别简单：最优 coupling 是 **按分位数对齐**。即设 $F_\mu, F_\nu$ 是 $\mu, \nu$ 的 CDF，$F_\mu^{-1}, F_\nu^{-1}$ 是逆 CDF，则
$$
W_p^p(\mu, \nu) = \int_0^1 |F_\mu^{-1}(q) - F_\nu^{-1}(q)|^p \, dq. \tag{3.1}
$$

**对路径 A 的用处**：我们的 benchmark E1/E2 都是 1D 标量守恒律，评估误差用 $W_1$ 就用 (3.1) 直接算，不需要训练任何东西。

---

## §4 Wasserstein 距离

### 4.1 定义

**定义 4.1**：设 $p \geq 1$，$\mu, \nu \in \mathcal P_p(\mathbb R^N)$（即 $\int \|x\|^p d\mu < \infty$）。
$$
\boxed{W_p(\mu, \nu) \coloneqq \left( \inf_{\pi \in \Pi(\mu, \nu)} \int \|x-y\|^p \, d\pi(x,y) \right)^{1/p}.} \tag{4.1}
$$

### 4.2 基本性质

- $W_p$ 是 $\mathcal P_p(\mathbb R^N)$ 上的一个**度量**（满足距离公理）。
- $W_p$ **度量化弱收敛 + $p$-阶矩收敛**：$W_p(\mu_n, \mu) \to 0$ $\Leftrightarrow$ $\mu_n \rightharpoonup \mu$ 且 $\int \|x\|^p d\mu_n \to \int \|x\|^p d\mu$。
- **与 $L^p$ 距离的区别**：$L^p$ 距离只比较"**在同一个点上**的密度差"；$W_p$ 允许"**搬动**"。经典例子：$\mu = \delta_0, \nu_\varepsilon = \delta_\varepsilon$。$L^p$ 距离（弱对偶意义下）是 $\mathcal O(1)$（两个 delta 支持不相交），$W_p$ 距离是 $\varepsilon$。Wasserstein 对平移敏感、对"锐度"不敏感。

**为什么路径 A 用 $W_1$**：双曲 PDE 带 shock，shock 位置若被反向采样搞错 $\varepsilon$，$L^1$ 距离会感受到 $\mathcal O(1)$ 的误差（沿跳跃），但 $W_1$ 只感受到 $\mathcal O(\varepsilon)$。所以 $W_1$ 对 shock 位置误差是**自然的**度量。

### 4.3 Gaussian 显式公式（L3/L5 要用）

**命题 4.2**：若 $\mu = \mathcal N(m_1, \Sigma_1), \nu = \mathcal N(m_2, \Sigma_2)$，则
$$
W_2^2(\mu, \nu) = \|m_1 - m_2\|^2 + \mathrm{tr}\!\left(\Sigma_1 + \Sigma_2 - 2(\Sigma_1^{1/2}\Sigma_2 \Sigma_1^{1/2})^{1/2}\right). \tag{4.2}
$$

**各向同性 + 同协方差**（最常用）：若 $\Sigma_1 = \Sigma_2 = \sigma^2 I$，第二项为零，$W_2 = \|m_1 - m_2\|$。这会在路径 A Theorem 2 证明中用到（"扩散模型前向 Gaussian 核在 $W_2$ 下简单"）。

### 4.4 $W_2$ vs 其他距离

| 距离 | 定义/含义 | 对平移敏感 | 对函数正则性敏感 |
|---|---|---|---|
| TV | $\sup_A |\mu(A) - \nu(A)|$ | **不敏感**（只要支持不重合就饱和到 1） | 不敏感 |
| KL | $\int \log \frac{d\mu}{d\nu} d\mu$ | 不敏感（支撑不同直接无穷） | 非常敏感 |
| $L^2$ | $\int (p-q)^2 dx$ | 不敏感 | 非常敏感 |
| $W_1$ | Kantorovich–Rubinstein | **敏感**（$\varepsilon$ 平移得 $\varepsilon$） | 不敏感 |
| $W_2$ | (4.1), $p=2$ | 敏感 | 不敏感 |

### 4.5 Kantorovich–Rubinstein 公式（$W_1$ 的另一面）

**命题 4.3**：$W_1(\mu, \nu) = \sup_{\|\varphi\|_{\mathrm{Lip}} \leq 1} \int \varphi \, d(\mu - \nu)$。

这是 (K\*) 在 $c = \|x-y\|$ 特例下的化简。对偶"测试函数"取到 Lipschitz 1 的全体——这给 $W_1$ 一个**operational** 解读：*最强的 1-Lipschitz 测试**能**区分 $\mu, \nu$ 到多大程度*。

在路径 A 证明 Theorem 2 时，这是主要的操控工具之一。

---

## §5 Wasserstein 空间的几何

$\mathcal P_2(\mathbb R^N)$ 配以 $W_2$ 距离形成一个度量空间。但它不只是度量空间——它**具有 Riemannian 流形的"形状"**（虽然是无限维）。

### 5.1 测地线

**命题 5.1（$W_2$ 测地线）**：给定 $\mu_0, \mu_1 \in \mathcal P_2$ 和 Brenier 最优 map $T = \nabla \psi$（$T_\# \mu_0 = \mu_1$），定义**常速度插值**
$$
\mu_t \coloneqq [(1 - t) \mathrm{id} + t T]_\# \mu_0, \quad t \in [0, 1]. \tag{5.1}
$$
则 $\mu_t$ 是 $W_2$ 测地线，且 $W_2(\mu_s, \mu_t) = |s-t| W_2(\mu_0, \mu_1)$。

**物理解读**：测地线是"所有质点沿直线匀速从 $x$ 走到 $T(x)$"。这回归到**粒子流**的物理图像。

### 5.2 切空间（非正式介绍）

在 Riemannian 流形上，切空间是速度向量。$\mathcal P_2$ 的切空间是一个函数空间。

**非正式**：设 $t \mapsto \mu_t$ 是 $\mathcal P_2$ 中的一条曲线。它满足一个连续性方程
$$
\partial_t \mu_t + \nabla \cdot (\mu_t v_t) = 0, \tag{5.2}
$$
其中 $v_t(x)$ 是一个向量场（"质量速度"）。

**定义 5.2**：$\mathcal P_2$ 在 $\mu$ 点的切空间
$$
T_\mu \mathcal P_2 = \overline{\{ \nabla \varphi : \varphi \in C_c^\infty(\mathbb R^N) \}}^{L^2(\mu)}.
$$
即由梯度向量场生成、在 $L^2(\mu)$ 下闭包。

**Remark**：Otto（2001）首次把 $\mathcal P_2$ 这套几何写得严格化。这个几何叫 **Otto calculus**。路径 A Theorem 5 的"JKO 对应"就是 Otto calculus 框架下的一个陈述。

---

## §6 Benamou–Brenier 动力学公式

Wasserstein 距离定义 (4.1) 是"静态"（用 coupling）。Benamou–Brenier 给出一个等价的"动态"形式。

**定理 6.1（Benamou–Brenier 2000）**：
$$
\boxed{W_2^2(\mu_0, \mu_1) = \inf_{(\mu_t, v_t)} \left\{ \int_0^1 \int \|v_t(x)\|^2 \, d\mu_t(x) \, dt \ :\ \partial_t \mu_t + \nabla \cdot (\mu_t v_t) = 0, \ \mu_{t=0} = \mu_0, \ \mu_{t=1} = \mu_1 \right\}.} \tag{6.1}
$$

**解读**：$W_2^2$ = "最小动能"。$\mu_0 \to \mu_1$ 的所有满足连续性方程的搬运路径中，最省动能的那条就是 $W_2$ 测地线，动能值就是 $W_2^2$。

**对路径 A 的连接**：扩散模型的 probability flow ODE (L1 §3.3) 本质就是一个连续性方程 (5.2)，速度场是 $v_\tau = f - \tfrac12 g^2 s$。我们可以把整个反向采样过程视作 $\mathcal P_2$ 空间中的一条动力学曲线，而 Benamou–Brenier 告诉我们这条曲线的"动能"是什么。L3 会把这一点更精确化。

---

## §7 Wasserstein 梯度流（为 L3 铺路）

### 7.1 目标：在 $\mathcal P_2$ 上定义梯度流

类比：在欧氏空间 $\mathbb R^N$ 上，梯度流是 $\dot x = -\nabla F(x)$。

在 $\mathcal P_2$ 上，我们要找：给定泛函 $\mathcal F: \mathcal P_2 \to \mathbb R$，曲线 $t \mapsto \mu_t$ 是"$\mathcal F$ 的 $W_2$ 梯度流"是什么意思？

### 7.2 形式化：第一变分 $\delta \mathcal F / \delta \mu$

设 $\mathcal F[\mu] = \int F(\mu(x)) \, dx$（密度的泛函）或 $\mathcal F[\mu] = \int V(x) d\mu(x)$ 等。其**第一变分**是一个函数 $\delta \mathcal F / \delta \mu: \mathbb R^N \to \mathbb R$，定义满足
$$
\frac{d}{d\varepsilon}\bigg|_{\varepsilon = 0} \mathcal F[\mu + \varepsilon \chi] = \int \frac{\delta \mathcal F}{\delta \mu}(x) \chi(x) \, dx
$$
对所有满足 $\int \chi = 0$ 的扰动 $\chi$ 成立。

**例子**：
- **相对熵** $\mathcal H[\mu | \nu] = \int \log\frac{d\mu}{d\nu} d\mu$，则 $\frac{\delta \mathcal H}{\delta \mu} = \log\frac{d\mu}{d\nu} + 1$。
- **势能** $\mathcal V[\mu] = \int V d\mu$，则 $\frac{\delta \mathcal V}{\delta \mu} = V$。
- **内能** $\mathcal U[\mu] = \int U(\mu(x)) dx$（$U$ 凸函数），则 $\frac{\delta \mathcal U}{\delta \mu} = U'(\mu)$。

### 7.3 Wasserstein 梯度与梯度流

**Otto calculus 的关键事实**：$\mathcal F$ 在 $\mu$ 点的 $W_2$-梯度是
$$
\nabla_{W_2} \mathcal F[\mu] = -\nabla \cdot \left( \mu \nabla \frac{\delta \mathcal F}{\delta \mu} \right). \tag{7.1}
$$
（在切空间 $T_\mu \mathcal P_2$ 里的向量）

$W_2$ 梯度流
$$
\boxed{\partial_t \mu_t = -\nabla_{W_2} \mathcal F[\mu_t] = \nabla \cdot \left( \mu_t \nabla \frac{\delta \mathcal F}{\delta \mu_t} \right).} \tag{7.2}
$$

这正是一个**连续性方程**（速度 $v_t = -\nabla \delta \mathcal F / \delta \mu_t$）。

### 7.4 标志性例子：FP 方程 = 相对熵的 $W_2$-梯度流

设势能 $V: \mathbb R^N \to \mathbb R$，目标测度 $\nu \propto e^{-V}$。泛函取
$$
\mathcal F[\mu] = \mathcal H[\mu | \nu] = \int \log \frac{d\mu}{d\nu} \, d\mu.
$$

计算 $\delta \mathcal F / \delta \mu = \log \mu - \log \nu + 1 = \log \mu + V + \mathrm{const}$，代入 (7.2)：
$$
\partial_t \mu = \nabla \cdot (\mu \nabla (\log \mu + V)) = \nabla \cdot (\nabla \mu + \mu \nabla V) = \Delta \mu + \nabla \cdot (\mu \nabla V). \tag{7.3}
$$

**这正是势 $V$ 下的 Fokker–Planck 方程**！

> **核心事实（JKO 1998）**：Fokker–Planck 方程就是**相对熵 $\mathcal H[\cdot | \nu]$ 在 $W_2$ 空间的梯度流**。

这是 L3 的出发点，也是路径 A Theorem 5 的结构母题。

---

## §8 物理直觉总表

| 欧氏空间 $\mathbb R^N$ | Wasserstein 空间 $\mathcal P_2$ |
|---|---|
| 点 $x$ | 测度 $\mu$ |
| 直线段 $(1-t)x_0 + t x_1$ | 插值 $[(1-t)\mathrm{id} + tT]_\# \mu_0$ |
| 距离 $\|x_0 - x_1\|$ | $W_2(\mu_0, \mu_1)$ |
| 速度向量 $\dot x \in \mathbb R^N$ | 速度场 $v_t$（满足连续性方程） |
| 函数 $F: \mathbb R^N \to \mathbb R$ | 泛函 $\mathcal F: \mathcal P_2 \to \mathbb R$ |
| 梯度 $\nabla F(x)$ | $-\nabla \cdot(\mu \nabla \delta \mathcal F / \delta \mu)$ |
| 梯度流 $\dot x = -\nabla F$ | $\partial_t \mu = \nabla \cdot(\mu \nabla \delta \mathcal F / \delta \mu)$ |
| $x_{k+1} = \arg\min \{F(y) + \tfrac{1}{2\tau}\|y-x_k\|^2\}$ | $\mu_{k+1} = \arg\min \{\mathcal F[\nu] + \tfrac{1}{2\tau}W_2^2(\nu, \mu_k)\}$ |

最后一行就是 **JKO scheme**，L3 详细展开。

---

## §9 小结与 L3 预告

**L2 一句话总结**：
- $W_2$ 距离 = 最优运土代价 = 最小动能搬运；
- $\mathcal P_2$ 配 $W_2$ 是一个（无限维）Riemannian 流形，切空间由梯度向量场构成；
- FP 方程 = 相对熵在 $W_2$ 上的梯度流（Otto / JKO 的核心观察）。

**L3 要做的事**：
1. 把 (7.2) 的连续时间梯度流**时间离散化**：proximal 步 $\mu_{k+1} = \arg\min_{\nu} \{\mathcal F[\nu] + \tfrac{1}{2\tau}W_2^2(\nu, \mu_k)\}$，这就是 **JKO scheme**。
2. 证明 JKO 的 $\tau \to 0$ 极限恢复 FP 方程（JKO 1998 主定理）。
3. 把这个"离散 JKO 步"和扩散模型的**反向采样一步**对比——它们的相似之处就是路径 A Theorem 5 的技术核心。
4. 为什么这对路径 A 重要：**如果扩散模型反向采样的每一步就是一个 JKO proximal 步，那扩散模型本身就是"相对熵 $W_2$-梯度流的神经网络离散"——这把我们的方法从"经验有效"抬升到"Wasserstein 梯度流"的数学传统里**。

---

## 附录 A：几个常见疑问

**Q1**：$W_p$ 怎么读？
A："p-Wasserstein distance"（以 Leonid Kantorovich 的俄文 KaHTOPOBИЧ 音译同源的 Vasserstein 命名，现在约定俗成写作 Wasserstein）。

**Q2**：为什么 $W_2$ 比 $W_1$ 更"Riemannian"？
A：$W_2$ 对应 Hilbert-like 的 Riemannian 结构（Otto calculus）；$W_1$ 只对应一个度量结构（没有 inner product）。但我们路径 A 最终定理用 $W_1$ 作收敛度量（对 shock 最自然），而 JKO 内部用 $W_2$（Otto 结构可用）——这是有意的分工。

**Q3**：Brenier 定理在 1D 什么样？
A：1D 的最优 $T$ 是**单调递增**函数（因为凸函数的导数单调）。这和 "按分位数对齐"一致。

**Q4**：(7.1) 右边的"$-\nabla \cdot$"里的负号怎么来的？
A：$T_\mu \mathcal P_2$ 是梯度向量场的空间；其 inner product $\langle \nabla \varphi, \nabla \psi \rangle_\mu = \int \nabla \varphi \cdot \nabla \psi \, d\mu$。在这个 inner product 下，求 $\mathcal F$ 的 Riesz 表示即得到 (7.1) 的负 divergence 形式（分部积分一次）。

**Q5**：L1 里扩散模型的 probability flow ODE 是不是某种 $W_2$-梯度流？
A：**是**，但不是相对熵的。而是一个**时间依赖**泛函的梯度流（因为扩散时间 $\tau$ 本身出现在 $\mathcal F$ 里）。我们在 L3 后半 + 路径 A Theorem 5 证明时会严格化这一点。
