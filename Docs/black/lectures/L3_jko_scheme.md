# L3 JKO Scheme：Fokker–Planck 作为 Wasserstein 梯度流的时间离散

> **本讲定位**：在 L2 的几何框架（$\mathcal P_2$ Riemannian 结构、$W_2$ 梯度流）基础上，给出"把 FP 方程写成时间离散最小化问题"的 JKO 构造。这是路径 A Theorem 5 的直接母题，也是未来我们把扩散模型和 Wasserstein 梯度流对齐的技术支架。
> **先修**：L2（$W_2$ 距离、Otto calculus、相对熵作为泛函）。
> **后续依赖**：L5、路径 A Theorem 5。
> **长度**：约 4500 字。

---

## §0 本讲目标

L2 最后一幕我们看到一个惊人的事实：FP 方程 $\partial_t \mu = \Delta \mu + \nabla \cdot (\mu \nabla V)$ 就是**相对熵 $\mathcal H[\cdot | \nu]$（$\nu \propto e^{-V}$）在 $W_2$ 空间的梯度流** (L2 §7.4)。但这是一个**连续时间**的陈述。

本讲要回答三个问题：

1. 能不能把这个连续时间梯度流"时间离散"，写成一个 $W_2$ 空间的**迭代最小化算法**？（能，这就是 JKO scheme，§2–§4）
2. 这个算法的极限（时间步长 $\tau \to 0$）真的恢复 FP 方程吗？（是，JKO 1998 主定理，§5）
3. 这个算法和**扩散模型的反向采样一步**有什么关系？（非常深的关系，§7——这是路径 A Theorem 5 的源头）

读完本讲，你应该能在纸上默写 JKO 的变分问题（§2.1）、写出它的欧拉–拉格朗日方程（§4）、并能讲清楚"一步扩散反向采样 ≈ 一步 JKO" 的直觉。

---

## §1 提醒：欧氏空间的 Proximal 算子

先用有限维回忆一下。给定光滑函数 $F: \mathbb R^N \to \mathbb R$，梯度流 $\dot x(t) = -\nabla F(x(t))$。

**Backward Euler 离散**：给定时间步长 $\tau > 0$，从 $x_k$ 产生 $x_{k+1}$
$$
x_{k+1} = x_k - \tau \nabla F(x_{k+1}). \tag{1.1}
$$

**Proximal form**（Moreau 1962）：(1.1) 等价于
$$
\boxed{x_{k+1} = \arg\min_{y \in \mathbb R^N} \left\{ F(y) + \tfrac{1}{2\tau} \|y - x_k\|^2 \right\}.} \tag{1.2}
$$

**等价性验证**：(1.2) 的最优性条件 $\nabla F(y) + \tfrac{1}{\tau}(y - x_k) = 0$ 即 $y = x_k - \tau \nabla F(y)$，对应 (1.1)。

**JKO 的主意（一句话）**：把 (1.2) 里的 $\mathbb R^N$ 换成 $\mathcal P_2(\mathbb R^N)$，把 $F$ 换成泛函 $\mathcal F$，把 $\|\cdot\|$ 换成 $W_2$。

---

## §2 JKO Scheme

### 2.1 定义

**定义 2.1（Jordan–Kinderlehrer–Otto 1998）**：给定泛函 $\mathcal F: \mathcal P_2(\mathbb R^N) \to \mathbb R \cup \{+\infty\}$，时间步长 $\tau > 0$ 和初始分布 $\mu_0 \in \mathcal P_2$，定义迭代
$$
\boxed{\mu_{k+1}^\tau \in \arg\min_{\mu \in \mathcal P_2} \left\{ \mathcal F[\mu] + \frac{1}{2\tau} W_2^2(\mu, \mu_k^\tau) \right\}, \quad k = 0, 1, 2, \ldots} \tag{2.1}
$$

**解读**：
- 第一项 $\mathcal F[\mu]$ "拉"着解往 $\mathcal F$ 的最小点走（能量下降）；
- 第二项 $\frac{1}{2\tau} W_2^2$ "拴"着解不要跑太远（proximal 约束）；
- $\tau$ 控制两者平衡：$\tau \to 0$ 则完全拴住（不动），$\tau \to \infty$ 则直接跳到 $\mathcal F$ 的最小点。

### 2.2 离散轨道

给定 $\tau$，JKO 产生一串测度 $\mu_0^\tau, \mu_1^\tau, \mu_2^\tau, \ldots$。构造**分段常数插值**
$$
\mu^\tau(t) \coloneqq \mu_k^\tau \quad \text{若 } t \in [k\tau, (k+1)\tau).
$$
我们的问题是：当 $\tau \to 0$，$\mu^\tau(t)$ 是否收敛到 FP 方程的解？答案是"是"（§5）。

---

## §3 存在性

**命题 3.1**：若 $\mathcal F$ 下半连续（在 $W_2$ 拓扑下）、下有界、且次水平集 $\{\mathcal F \leq c\}$ 相对紧，则对任意 $\mu_k^\tau \in \mathcal P_2$，(2.1) 的最小值被取到。

**证明思路**：直接用 Weierstrass 形式的存在性证明。子水平集紧 + 下半连续保证取得最小值。

具体到 $\mathcal F = \mathcal H[\cdot | \nu]$（相对熵），这些条件在 $V$ 有合适增长下成立。我们不深究，只记住：**JKO 最小化是 well-defined 的**。

---

## §4 JKO 的最优性条件

这里是 L3 的技术核心。我们要从最小化 (2.1) 推出一个**PDE**。

### 4.1 变分法设置

设 $\mu^\star \coloneqq \mu_{k+1}^\tau$ 是 (2.1) 的最小值。对任意"容许扰动"$\nu$（我们会在后面具体指定），有
$$
\mathcal F[\mu^\star] + \frac{1}{2\tau} W_2^2(\mu^\star, \mu_k^\tau) \leq \mathcal F[\nu] + \frac{1}{2\tau} W_2^2(\nu, \mu_k^\tau).
$$

### 4.2 用向量场扰动

令 $\xi \in C_c^\infty(\mathbb R^N; \mathbb R^N)$ 是紧支撑光滑向量场，$\varepsilon > 0$ 小。定义扰动测度
$$
\nu_\varepsilon \coloneqq (\mathrm{id} + \varepsilon \xi)_\# \mu^\star.
$$
（即把 $\mu^\star$ 里每粒质量沿 $\xi$ 方向平移 $\varepsilon$）

**$\mathcal F$ 的变分**：
$$
\mathcal F[\nu_\varepsilon] = \mathcal F[\mu^\star] + \varepsilon \int \nabla \frac{\delta \mathcal F}{\delta \mu^\star}(x) \cdot \xi(x) \, d\mu^\star(x) + o(\varepsilon). \tag{4.1}
$$

（这是 L2 (7.1) 的反推：Otto calculus 下 $\mathcal F$ 沿速度场 $\xi$ 的方向导数。）

**$W_2^2$ 的变分**：设 $\pi^\star$ 是 $(\mu^\star, \mu_k^\tau)$ 的最优 coupling。则
$$
W_2^2(\nu_\varepsilon, \mu_k^\tau) = W_2^2(\mu^\star, \mu_k^\tau) + 2 \varepsilon \int (x - y) \cdot \xi(x) \, d\pi^\star(x, y) + o(\varepsilon). \tag{4.2}
$$

### 4.3 一阶条件

将 (4.1)(4.2) 代入最小性不等式，除以 $\varepsilon$，取 $\varepsilon \to 0^+$，得
$$
\int \nabla \frac{\delta \mathcal F}{\delta \mu^\star}(x) \cdot \xi(x) \, d\mu^\star(x) + \frac{1}{\tau} \int (x - y) \cdot \xi(x) \, d\pi^\star(x, y) = 0. \tag{4.3}
$$

（取 $\xi$ 再取 $-\xi$ 即是等式。）

### 4.4 解读：用 Brenier map

由 L2 §3.2（Brenier 定理），当 $\mu^\star$ 关于 Lebesgue 绝对连续时，最优 coupling 是某凸函数 $\psi$ 的梯度图
$$
\pi^\star = (\mathrm{id}, \nabla \psi)_\# \mu^\star, \quad \nabla \psi : \mu^\star \to \mu_k^\tau.
$$

代入 (4.3)：
$$
\int \left[ \nabla \frac{\delta \mathcal F}{\delta \mu^\star}(x) + \frac{1}{\tau}(x - \nabla \psi(x)) \right] \cdot \xi(x) \, d\mu^\star(x) = 0.
$$
$\xi$ 任取，故括号为零 $\mu^\star$-几乎处处：
$$
\boxed{x - \nabla \psi(x) = -\tau \nabla \frac{\delta \mathcal F}{\delta \mu^\star}(x), \quad \text{in } L^2(\mu^\star).} \tag{4.4}
$$

即：**从 $\mu^\star$ 到 $\mu_k^\tau$ 的 Brenier 逆映射（$\mathrm{id} - \nabla \psi$）就是 $-\tau \nabla \delta \mathcal F / \delta \mu^\star$**。

### 4.5 翻译：backward Euler in $W_2$

(4.4) 等价于
$$
\mu_k^\tau = (\mathrm{id} - \tau \nabla \delta \mathcal F / \delta \mu^\star)_\# \mu^\star + \text{curvature correction}.
$$
近似一阶版本：
$$
\mu^\star \approx (\mathrm{id} + \tau \nabla \delta \mathcal F / \delta \mu_k^\tau)^{-1}_\# \mu_k^\tau.
$$

**直观**：$\mu^\star$ 由 $\mu_k^\tau$ 沿速度场 $-\nabla \delta \mathcal F / \delta \mu^\star$ 往前移动 $\tau$ 时间得到——这正是在 $\mathcal P_2$ 上做 **backward Euler** 求解梯度流 (L2 (7.2))。

---

## §5 极限 $\tau \to 0$：恢复 Fokker–Planck

**定理 5.1（JKO 1998 主定理，情形 $\mathcal F = \mathcal H[\cdot | \nu]$）**：设 $\nu = e^{-V}$，$V \in C^2$ 下有界，初始 $\mu_0 \in \mathcal P_2$。则 JKO 迭代的分段常数插值 $\mu^\tau(t)$ 在 $\tau \to 0$ 下 **narrow convergence**（弱*收敛）到连续函数 $[0,\infty) \ni t \mapsto \mu_t \in \mathcal P_2$，$\mu_t$ 以弱意义满足 FP 方程
$$
\partial_t \mu_t = \Delta \mu_t + \nabla \cdot (\mu_t \nabla V). \tag{5.1}
$$

**证明思路**（4 步）：

**Step 1（能量估计）**：对 (2.1) 取 $\mu = \mu_k^\tau$ 作试验：
$$
\mathcal F[\mu_{k+1}^\tau] + \frac{1}{2\tau} W_2^2(\mu_{k+1}^\tau, \mu_k^\tau) \leq \mathcal F[\mu_k^\tau].
$$
累加 $k$：
$$
\frac{1}{2\tau}\sum_k W_2^2(\mu_{k+1}^\tau, \mu_k^\tau) \leq \mathcal F[\mu_0] - \inf \mathcal F < \infty.
$$

**Step 2（弱紧性）**：上面的能量估计给出 $\mu^\tau$ 的 $\tau$-Hölder 半连续性
$$
W_2(\mu^\tau(s), \mu^\tau(t)) \leq C \sqrt{|t - s| + \tau}.
$$
由 Arzelà–Ascoli 型定理（弱拓扑版），可抽子列 $\mu^{\tau_n} \to \mu$ narrow。

**Step 3（确认极限满足弱 FP）**：用 (4.4) 和 $\mathcal F = \mathcal H[\cdot | \nu]$ 的第一变分 $\delta \mathcal F / \delta \mu = \log \mu + V + 1$（已在 L2 §7.4 算过），对测试函数 $\phi \in C_c^\infty$：
$$
\int \phi \, d(\mu_{k+1}^\tau - \mu_k^\tau) = \tau \int \nabla \phi \cdot \nabla (\log \mu + V) \, d\mu + o(\tau).
$$
累加 + Passing to the limit + 分部积分即得弱 FP (5.1)。

**Step 4（唯一性 + 子列收敛 → 全收敛）**：弱 FP 的解在合适函数空间中唯一，故整族 $\mu^\tau$ 收敛到同一个极限。

∎（技术细节跳过）

### 5.2 意义

定理 5.1 是 20 世纪数学分析的一个里程碑：
- **新视角**：FP 方程从"密度的抛物 PDE"变成"$W_2$ 空间的梯度流"；
- **新工具**：原来只能用线性 PDE 理论研究 FP，现在可以用最优传输 / 测度论 / 变分方法；
- **新推广**：所有具有"能量 + 约束"结构的 PDE（多孔介质方程、Cahn–Hilliard、某些 Euler 方程）都可以在这个框架下研究。

---

## §6 JKO 的其它例子（扩宽视野）

不同 $\mathcal F$ 给出不同的 PDE（全部是 $W_2$-梯度流）：

| $\mathcal F[\mu]$ | PDE（$\partial_t \mu = -\nabla_{W_2} \mathcal F$） |
|---|---|
| $\int V \, d\mu$ | Transport: $\partial_t \mu + \nabla \cdot(\mu (-\nabla V)) = 0$ |
| $\mathcal H[\mu | \nu]$ | FP: $\partial_t \mu = \Delta \mu + \nabla \cdot(\mu \nabla V)$ |
| $\int \mu^m / (m-1) \, dx$ ($m > 1$) | Porous medium: $\partial_t \mu = \Delta (\mu^m)$ |
| $\int \mu \log \mu \, dx - \tfrac12\iint W(x-y) d\mu(x)d\mu(y)$ | McKean–Vlasov |

**要点**：$W_2$-梯度流视角下，**扩散现象**（Laplacian）统一为"相对熵 / 熵 / 内能"这类凸泛函的 $W_2$-梯度。

---

## §7 JKO 与扩散模型的联系（路径 A Theorem 5 的前奏）

这是全讲最重要的一节。我们要把扩散模型的反向采样和 JKO proximal 步**并排比较**。

### 7.1 扩散模型的反向采样（一步）

从 L1 §3.3，扩散模型的 probability flow ODE 是
$$
\frac{du}{d\tau} = -\tfrac12 g^2(\tau) s(u, \tau) \quad (\text{VE, } f=0). \tag{7.1}
$$
对 density $p_\tau$ 本身的一步反向演化（用连续性方程重写 + L1 §3.3 的代数变形）：
$$
\partial_\tau p_\tau = \nabla \cdot \left( p_\tau \cdot \tfrac12 g^2(\tau) s \right) = \nabla \cdot \left( p_\tau \cdot \tfrac12 g^2 \nabla \log p_\tau \right). \tag{7.2}
$$

注意 $\tau$ 是从大到小跑（反向时间），所以 (7.2) 实际 $\tau \mapsto -\tau$ 后是 $\partial_{-\tau} p = -\nabla \cdot(p \tfrac{g^2}{2} \nabla \log p)$。

**另一边看**：负熵 $\mathcal E[\mu] \coloneqq -\mathcal H[\mu | \mathrm{Leb}] = \int \mu \log \mu \, dx$ 的第一变分是 $\log \mu + 1$，其梯度 $\nabla \log \mu = s$。所以
$$
\partial_t \mu_t = -\nabla_{W_2} \mathcal E = \nabla \cdot(\mu \nabla (\log \mu)) = \Delta \mu.
$$
对应**纯热方程**。反向看就是
$$
\partial_{-t} \mu = -\Delta \mu,
$$
这是热方程的**倒放**——反扩散，并非梯度流（它是"anti-gradient flow"）。

**关键观察**：扩散模型的反向采样**不是**任何固定泛函的 $W_2$-梯度流。它是**反方向 + 时间依赖 schedule** 的 descent。直接对应 Theorem 5 里要对比的对象。

### 7.2 用 JKO 语言改写扩散反向一步

设反向时间步长 $\Delta \tau$，schedule $\sigma(\tau)$。反向一步把 $\mu_\tau \to \mu_{\tau - \Delta \tau}$。

**命题 7.1（形式版）**：反向一步可写为
$$
\mu_{\tau - \Delta \tau} \approx \arg\min_\nu \left\{ \mathcal F_\tau[\nu] + \frac{1}{2 \Delta \tau} W_2^2(\nu, \mu_\tau) \right\},
$$
其中 $\mathcal F_\tau[\nu] = -\tfrac{g^2(\tau) \Delta \tau}{2} \mathcal H[\nu | \mathrm{Leb}] + \mathrm{higher order}$。

这是**带时间依赖系数的 JKO**。它告诉我们：**反向采样每一步就是 $\mathcal P_2$ 上一个 proximal 步——但 proximal 的对象是负熵，系数由 schedule 决定**。

### 7.3 路径 A Theorem 5 的声明

把上面的"形式 JKO"写成严格的渐近等价，并加上**我们的 PDE constraint**：路径 A 里我们让扩散模型学的不是 $\rho$（普通数据分布），而是 $\rho_t$（**目标 PDE 解的分布**）。我们希望反向采样的每一步在 $\Delta \tau \to 0$ 极限下恢复
$$
\partial_t \mu_t = -\nabla_{W_2} \left[ \mathcal H[\mu_t | \rho^\star] + \int \lambda \cdot L(u) \, d\mu_t \right],
$$
其中 $L$ 是目标 PDE 的微分算子，$\lambda$ 是 Lagrange multiplier，$\rho^\star$ 是目标解的分布。

**这就是 Theorem 5 的大致内容**。证明要用 §4 的一阶条件 + 扩散模型 score 网络的收敛 + JKO 1998 极限定理。

---

## §8 实际计算：Deep Kinetic JKO

Mercado et al.（arXiv:2603.23901, 2026 年 3 月）把 JKO scheme 做成一个数值方法：**用神经网络参数化 $\mu_k$ 的 Brenier map，直接求解 (2.1)**。

### 8.1 算法骨架

1. 参数化 $\mu_{k+1} = T_\theta{}_\# \mu_k$，$T_\theta = \nabla \psi_\theta$，$\psi_\theta$ 是某凸神经网络（ICNN, input-convex NN）。
2. 损失函数：
   $$
   \mathcal L(\theta) = \mathcal F[T_\theta{}_\# \mu_k] + \frac{1}{2\tau} \mathbb E_{x \sim \mu_k} \|T_\theta(x) - x\|^2.
   $$
3. 用 SGD 训练 $\theta$，得 $\mu_{k+1}$。

### 8.2 和路径 A 的关系

Mercado 等人的工作是**纯 JKO-based**：每一步都是一次 neural optimization，没有用扩散模型的 score matching 机制。

**路径 A 的策略不同**：我们用 **predeterministic 的扩散 schedule**（由 score matching 预训练得到 score）+ **entropy-aware guidance**；Theorem 5 是在**渐近意义下**证明这两者等价，而**不是真的把 JKO 作为算法实现**。

Mercado 的工作可以作为 Theorem 5 的实验验证 baseline：把我们的方法应用于他们的 Vlasov–Fokker–Planck 数据集，看 $W_2$ 误差和 Mercado 的 neural JKO 比较如何。

---

## §9 小结 + L4 预告

**L3 一句话**：JKO scheme = $W_2$ 空间的 proximal（"backward Euler"），其 $\tau \to 0$ 极限恢复 $W_2$-梯度流。具体到相对熵 $\mathcal H[\cdot|\nu]$，JKO 恢复 FP 方程。扩散模型的反向采样**形式上**是 JKO，**严格意义**上是带时间依赖系数的 proximal 流——这一联系是路径 A Theorem 5 的核心。

**到此为止的 L1–L3 帮我们建立了"光滑 PDE + $W_2$ 几何"的框架**。但**路径 A 的核心是双曲 PDE**——那里解不是光滑函数，而是**带 shock 的 BV 函数**。FP / $W_2$ 梯度流这套工具对 shock 并不直接适用。

L4 要做的事：
1. 讲清双曲 PDE 为什么必然出现 shock（特征线交汇）；
2. 弱解（weak solution）的定义及其问题（非唯一）；
3. Kruzhkov 熵条件：怎么挑出"物理的"唯一解；
4. BV 空间：shock 解所在的函数空间；
5. 粘性消失法：如何从粘性 PDE 极限得到熵解——这是路径 A viscosity-matched schedule 的数学原型。

---

## 附录 A：几个常见疑问

**Q1**：JKO 和 Kingma–Welling 的 VI 算法、或 Wasserstein GAN 的训练有什么关系？
A：**概念层有关系**（都是 $W_2$ 距离 / Kantorovich 对偶），**目标不同**。JKO 是 PDE 数值算法（目标：近似一个 FP 解）；WGAN 是生成模型训练（目标：最小化 $W_1$ 到数据分布）。Theorem 5 不涉及 WGAN/VI。

**Q2**：(4.1) 里 $\nabla \frac{\delta \mathcal F}{\delta \mu^\star}$ 要求 $\mu^\star$ 是什么光滑度？
A：技术上需要 $\mu^\star$ 绝对连续 + $\delta \mathcal F / \delta \mu$ 可微。对相对熵，这要求 $\mu^\star$ 的密度 $> 0$ 且 $\nabla \log \mu^\star \in L^2$。JKO 1998 证明了从任意 $\mu_0 \in \mathcal P_2$ 出发，$\mu_k^\tau$（$k \geq 1$）立刻变得光滑（正则化效应）。

**Q3**：为什么 JKO 的"时间步长"一般叫 $\tau$，而不是 $\Delta t$？
A：传统。我们这里在 FP 方程的时间上用 $t$，JKO proximal 步用 $\tau$。**注意不要和扩散模型的 $\tau$ 混淆**——两者在 L5 / Theorem 5 中确实会区分，这时会用 $\tau_{\mathrm{diff}}$ 和 $\tau_{\mathrm{JKO}}$。

**Q4**：Benamou–Brenier (L2 §6) 和 JKO 是一回事吗？
A：**不是**。Benamou–Brenier 给出 $W_2^2$ 的**动力学表述**（"最小动能"）。JKO 给出**FP = $W_2$-梯度流的时间离散**。两者互补：BB 描述$W_2$ 几何，JKO 描述怎么在这个几何上做 backward Euler。路径 A Theorem 5 证明里两者都要用。

**Q5**：如果 $\mathcal F$ 不凸，JKO 还 work 吗？
A：存在性仍成立（命题 3.1），但极限 PDE 可能不唯一或有 blow-up。路径 A 里 $\mathcal F$ 是相对熵 + 线性 PDE constraint，凸性良好，不是问题。
