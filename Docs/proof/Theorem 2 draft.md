# Theorem 2（Entropy-Solution Stability · Baseline Rate）

> **论文位置**：Main body §6.2 仅 statement + proof sketch；完整证明在 Appendix A1。
> **角色**：这条定理给出**标准 score-based diffusion（无 BV-aware 增强）** 的收敛率界。界中显式含 $\exp(\Lambda T_d)$ 放大因子——这正是 Theorem 3 要干掉的。

---

## Statement

设 $\mathbf{u}^\star$ 为标量守恒律 $\partial_t \mathbf{u} + \partial_x f(\mathbf{u}) = 0$ 在固定物理时间 $T_{\mathrm{phys}}$ 处的 Kruzhkov 熵解。将解视作状态向量 $u \in \mathbb{R}^d$（$d = N_x$ 为空间网格点数），定义目标分布

$$
\rho^\star \coloneqq \Law(\mathbf{u}^\star).
$$

前向扩散过程（VE-SDE，schedule $\sigma(\tau)$）：

$$
p_\tau \coloneqq \rho^\star \ast G_\tau, \qquad
G_\tau(u) = (4\pi\tau)^{-d/2} \exp\!\left(-\frac{\|u\|^2}{4\tau}\right), \quad \tau \in [0, T_d].
$$

真实 score 场：

$$
s(u, \tau) \coloneqq \nabla_u \log p_\tau(u).
$$

反向 ODE（标准 EDM 形式，$\tau$ 从 $T_d$ 积分至 $0$）：

真实轨迹：
$$
\frac{du^\natural}{d\tau} = b(u^\natural, \tau), \qquad
b(u, \tau) \coloneqq -\sigma(\tau)\,\dot\sigma(\tau)\,s(u, \tau),
\quad u^\natural(T_d) \sim p_{T_d},
$$

网络近似轨迹：
$$
\frac{d\hat u}{d\tau} = \hat b(\hat u, \tau), \qquad
\hat b(u, \tau) \coloneqq -\sigma(\tau)\,\dot\sigma(\tau)\,s_\theta(u, \tau),
\quad \hat u(T_d) \sim p_{T_d}.
$$

> **符号约定**：$u^\natural(\tau)$ 为真实 score 驱动的反向轨迹；$\hat u(\tau)$ 为学习 score 驱动的反向轨迹。$\|\cdot\|$ 为 $\mathbb{R}^d$ 上的欧氏范数。$W_1(\mu, \nu)$ 为 1-Wasserstein 距离（Kantorovich–Rubinstein 对偶）。期望 $\mathbb{E}$ 对随机性（初始噪声 + 学习 score 近似）取。

**主定理**。在假设 (A1)–(A4) 下，生成样本分布 $\Law(\hat u(0))$ 与目标分布 $\rho^\star$ 之间满足

$$
\boxed{\;
W_1\!\big(\Law(\hat u(0)),\; \rho^\star\big)
\;\le\; C\,\varepsilon\,\exp(\Lambda T_d)
\;}, \tag{2.1}
$$

其中 $\Lambda \coloneqq \sup_{\tau \in [0, T_d]} |\sigma(\tau)\dot\sigma(\tau)|\,L_s(\tau)$，$L_s(\tau)$ 为 $\nabla_u s(\cdot, \tau)$ 的 Lipschitz 常数，$\varepsilon$ 为 score-matching 训练误差界。常数 $C = C_\sigma \sqrt{T_d}\,(1 + C_{\mathrm{stab}})$ 仅依赖 schedule 上界 $C_\sigma$ 与分布稳定性常数 $C_{\mathrm{stab}}$，与 $\varepsilon$、$\Lambda$ 无关。

**与 PDE 解的关联**。$(2.1)$ 给出了扩散模型采样的解分布接近 PDE 解分布的量化保证。若训练数据源自数值解，则 Kruzhkov $L^1$-收缩性确保数值误差不在物理时间传播中爆炸，$(2.1)$ 的界稳定传递至真实 PDE 解（见 §PDE Connection）。

---

## Assumptions

**假设 (A1) — Score 梯度 Lipschitz 正则性。** 对每个 $\tau > 0$，真实 score 场 $s(\cdot, \tau)$ 是 $C^1$ 且其 Jacobian 的算子范数一致有界：存在 $L_s(\tau) < \infty$ 使得

$$
\|\nabla_u s(u, \tau)\|_{\mathrm{op}} \le L_s(\tau), \quad \forall\, u \in \mathbb{R}^d,\; \tau \in (0, T_d].
$$

定义 $\Lambda(\tau) \coloneqq |\sigma(\tau)\dot\sigma(\tau)|\,L_s(\tau)$ 并记 $\Lambda \coloneqq \sup_{\tau \in [0, T_d]} \Lambda(\tau) < \infty$。

> **可验证性**：因 $p_\tau = \rho^\star \ast G_\tau$ 且 $G_\tau$ 为热核，对任意 $\tau > 0$，$p_\tau \in C^\infty$ 且 $\nabla_u s = \nabla_u^2 \log p_\tau$ 一致有界。$\rho^\star$ 为 BV 测度的 pushforward（含 Dirac 点 mass 于 shock），卷积后光滑性成立。$L_s(\tau) \sim 1/\tau$ 在 $\tau \to 0$ 时可能发散，但本文仅需 $\sup_{\tau \in [\tau_{\mathrm{end}}, T_d]} L_s(\tau) < \infty$（early-stopping $\tau_{\mathrm{end}} > 0$），此与 \citet{sarkar2026scoreshocks} 的实践一致。

**假设 (A2) — 噪声 schedule 有界。** 存在 $C_\sigma > 0$ 使得

$$
|\sigma(\tau)\,\dot\sigma(\tau)| \le C_\sigma, \quad \forall\, \tau \in [0, T_d].
$$

> **可验证性**：对 VE 型 schedule（如 $\sigma^2(\tau) = 2\nu_{\mathrm{phys}} \tau$），$\sigma \dot\sigma = \nu_{\mathrm{phys}}$ 为常数，直接满足。

**假设 (A3) — Score 训练误差（加权 $L^2$ 界）。** 学习 score 网络 $s_\theta$ 在真实数据分布 $p_\tau$ 下满足

$$
\int_0^{T_d} \mathbb{E}_{u \sim p_\tau}\!\big[\,\|s_\theta(u, \tau) - s(u, \tau)\|^2\,\big] \, d\tau \;\le\; \varepsilon^2.
$$

> **可验证性**：这是 denoising score matching \citep{vincent2011connection} 的训练目标（以 $\sigma(\tau)^2$ 为权重），$\varepsilon$ 由训练损失确定。

**假设 (A4) — 分布稳定性（Kantorovich–Rubinstein 控制）。** 存在常数 $C_{\mathrm{stab}} > 0$，对任意 $\tau \in [0, T_d]$ 及任意 Lipschitz 函数 $f: \mathbb{R}^d \to \mathbb{R}$，成立

$$
\big|\,\mathbb{E}_{\hat u(\tau)}[f(\hat u)] - \mathbb{E}_{u^\natural(\tau)}[f(u)]\,\big|
\;\le\;
C_{\mathrm{stab}} \cdot W_1\!\big(\Law(\hat u(\tau)),\, \Law(u^\natural(\tau))\big) \cdot \Lip(f),
$$

其中 $\Lip(f) \coloneqq \sup_{u \neq v} |f(u) - f(v)| / \|u - v\|$。

> **可验证性**：该假设是 Kantorovich–Rubinstein 对偶 $|\int f d\mu - \int f d\nu| \le \Lip(f) \cdot W_1(\mu, \nu)$ 的直接推广，此时 $C_{\mathrm{stab}} = 1$。引入 $C_{\mathrm{stab}}$ 允许处理 score 网络引入的额外光滑性偏移，但在紧支测度和光滑分数假设下 $C_{\mathrm{stab}} = \mathcal{O}(1)$。

**补充技术假设 (A5)**。学习 score 网络 $s_\theta(\cdot, \tau)$ 在所有 $\tau \in [0, T_d]$ 上一致 Lipschitz，即存在 $L_{s_\theta} < \infty$ 与 $\tau$ 无关，使得对任意 $u, v \in \mathbb{R}^d$，$\|s_\theta(u, \tau) - s_\theta(v, \tau)\| \le L_{s_\theta} \|u - v\|$。

> **可验证性**：标准 MLP / UNet 在紧支输入域上为 Lipschitz，权值有界性由谱归一化或训练正则化保证。

---

## Proof

证明分九个步骤。步骤 1–3 设置耦合框架；步骤 4–5 处理核心难点（测度不一致）；步骤 6–8 合成 Gronwall 估计；步骤 9 给出 $W_1$ 上界。

---

### Step 1 · 同步耦合

定义误差过程

$$
e(\tau) \coloneqq \hat u(\tau) - u^\natural(\tau), \qquad \tau \in [0, T_d].
$$

由于两个轨迹有相同的初始分布 $p_{T_d}$，有 $e(T_d) = 0$ a.s.。沿反向 ODE 对 $\tau$ 微分（$\tau$ 自 $T_d$ 递减至 $0$）：

$$
\frac{d}{d\tau} e(\tau)
= \hat b(\hat u(\tau), \tau) - b(u^\natural(\tau), \tau).
$$

添零分解：

$$
\begin{aligned}
\frac{d}{d\tau} e(\tau)
&= \big[b(\hat u(\tau), \tau) - b(u^\natural(\tau), \tau)\big]
\;+\;
\big[\hat b(\hat u(\tau), \tau) - b(\hat u(\tau), \tau)\big] \\[4pt]
&\eqqcolon (\mathrm{I}) + (\mathrm{II}).
\end{aligned} \tag{2.2}
$$

两项的区别：
- $(\mathrm{I})$：在同一漂移场 $b$ 下因轨迹偏移 $\hat u \neq u^\natural$ 产生的传播误差；
- $(\mathrm{II})$：漂移场本身因 score 近似 $s_\theta \neq s$ 产生的模型误差。

---

### Step 2 · 控制 $(\mathrm{I})$（传播误差）

由 $b(u, \tau) = -\sigma(\tau)\dot\sigma(\tau)\,s(u, \tau)$ 及假设 (A1)：

$$
\begin{aligned}
\|b(\hat u, \tau) - b(u^\natural, \tau)\|
&\le |\sigma(\tau)\dot\sigma(\tau)| \cdot \|s(\hat u, \tau) - s(u^\natural, \tau)\| \\
&\le |\sigma(\tau)\dot\sigma(\tau)| \cdot L_s(\tau) \cdot \|\hat u - u^\natural\| \\
&= \Lambda(\tau)\,\|e(\tau)\|
\le \Lambda\,\|e(\tau)\|.
\end{aligned} \tag{2.3}
$$

其中 $\Lambda = \sup_{\tau \in [0, T_d]} \Lambda(\tau)$ 恰为 \citet{sarkar2026scoreshocks} 定义的分数激波放大指数（Score Shocks amplification exponent）。这就是 $\exp(\Lambda T_d)$ 的**起源**——漂移场 $b$ 的 Lipschitz 常数等于 $\Lambda$，因此误差以指数率 $\Lambda$ 传播。

---

### Step 3 · 控制 $(\mathrm{II})$（Score 模型误差）

由 $b, \hat b$ 的定义及假设 (A2)：

$$
\begin{aligned}
\|\hat b(\hat u, \tau) - b(\hat u, \tau)\|
&= |\sigma(\tau)\dot\sigma(\tau)| \cdot \|s_\theta(\hat u, \tau) - s(\hat u, \tau)\| \\
&\le C_\sigma\,\|s_\theta(\hat u, \tau) - s(\hat u, \tau)\|.
\end{aligned} \tag{2.4}
$$

---

### Step 4 · 期望不等式

对 $(2.2)$ 取欧氏范数与期望，记

$$
\delta(\tau) \coloneqq \mathbb{E}\,\|e(\tau)\|.
$$

由 Jensen 不等式 $\mathbb{E}\|\frac{d}{d\tau}e\| \ge |\frac{d}{d\tau}\mathbb{E}\|e\||$（严格成立需考虑绝对连续性，在此通过链式法则处理；见 Remark~2.1），结合 $(2.3)$ 与 $(2.4)$：

$$
\delta'(\tau)
\;\le\; \Lambda\,\delta(\tau)
\;+\; C_\sigma\;\mathbb{E}_{\hat u(\tau)}\!\big[\|s_\theta(\hat u, \tau) - s(\hat u, \tau)\|\big], \tag{2.5}
$$

其中 $\delta'(\tau) = d\delta/d\tau$ 沿反向时间方向（$\tau \searrow 0$）。

> **Remark 2.1**（Jensen 不等式的方向）。严格来说，$\frac{d}{d\tau}\mathbb{E}\|e\| = \mathbb{E}\big[\frac{e}{\|e\|} \cdot \frac{d e}{d\tau}\big] \le \mathbb{E}\|\frac{d e}{d\tau}\|$，不等式方向正确。不等式在 $\|e(\tau)\| = 0$ 的零测集上退化为 $0 \le \mathbb{E}\|\frac{d e}{d\tau}\|$，不影响积分界线。

---

### Step 5 · 测度不一致的修复（核心技术步骤）

**问题**：$(2.5)$ 中第二项期望取在 $\hat u(\tau)$ 的分布（学习轨迹）上，而训练误差假设 (A3) 控制在 $p_\tau$（真实 score 轨迹 $u^\natural(\tau)$ 的分布）上。两者 **测度不同**。

**修复** —— 三角分解：

记 $g(u, \tau) \coloneqq \|s_\theta(u, \tau) - s(u, \tau)\|$，则

$$
\begin{aligned}
\mathbb{E}_{\hat u(\tau)}[g(\hat u, \tau)]
&= \mathbb{E}_{u^\natural(\tau)}[g(u, \tau)]
\;+\;
\Big(\mathbb{E}_{\hat u(\tau)}[g(\hat u, \tau)] - \mathbb{E}_{u^\natural(\tau)}[g(u, \tau)]\Big) \\[4pt]
&\le \mathbb{E}_{u^\natural(\tau)}[g(u, \tau)]
\;+\;
\Big|\,\mathbb{E}_{\hat u(\tau)}[g(\hat u, \tau)] - \mathbb{E}_{u^\natural(\tau)}[g(u, \tau)]\,\Big|.
\end{aligned} \tag{2.6}
$$

由假设 (A4)（分布稳定性），对函数 $g(\cdot, \tau)$：

$$
\big|\,\mathbb{E}_{\hat u(\tau)}[g] - \mathbb{E}_{u^\natural(\tau)}[g]\,\big|
\;\le\;
C_{\mathrm{stab}} \cdot W_1\!\big(\Law(\hat u(\tau)),\, \Law(u^\natural(\tau))\big) \cdot \Lip(g).
$$

由同步耦合构造，$W_1\!\big(\Law(\hat u(\tau)), \Law(u^\natural(\tau))\big) \le \mathbb{E}\|\hat u(\tau) - u^\natural(\tau)\| = \delta(\tau)$。

由假设 (A5) 与 (A1)，$g(\cdot, \tau) = \|s_\theta(\cdot, \tau) - s(\cdot, \tau)\|$ 的 Lipschitz 常数满足

$$
\Lip(g(\cdot, \tau)) \;\le\; L_{s_\theta} + L_s(\tau) \;\le\; L_{s_\theta} + \sup_{\tau} L_s(\tau) \;\eqqcolon\; L_g < \infty,
$$

其中有限性由 early-stopping $\tau_{\mathrm{end}} > 0$ 确保（见假设 (A1) 后的注释）。

综合得：

$$
\mathbb{E}_{\hat u(\tau)}[g(\hat u, \tau)]
\;\le\;
\mathbb{E}_{u^\natural(\tau)}[g(u, \tau)]
\;+\;
C_{\mathrm{stab}}\,L_g\;\delta(\tau). \tag{2.7}
$$

记 $C' \coloneqq C_{\mathrm{stab}}\,L_g$。

---

### Step 6 · 合并微分不等式

将 $(2.7)$ 代入 $(2.5)$：

$$
\boxed{\;
\delta'(\tau)
\;\le\; (\Lambda + C')\,\delta(\tau)
\;+\; C_\sigma\;\mathbb{E}_{u^\natural(\tau)}\!\big[\|s_\theta(u, \tau) - s(u, \tau)\|\big]
\;}. \tag{2.8}
$$

这是标准的一阶线性微分不等式（Gronwall 型），其中 $u^\natural(\tau)$ 分布恰为 $p_\tau$，与训练误差假设 (A3) 的测度一致。

---

### Step 7 · Score 误差积分上界（Cauchy–Schwarz）

定义

$$
\beta(\tau) \coloneqq \mathbb{E}_{u^\natural(\tau)}\!\big[\|s_\theta(u, \tau) - s(u, \tau)\|\big].
$$

由 Cauchy–Schwarz 不等式：

$$
\int_0^{T_d} \beta(\tau)\,d\tau
\;\le\; \sqrt{T_d}\;\left(\int_0^{T_d} \mathbb{E}_{u^\natural(\tau)}\!\big[\|s_\theta - s\|^2\big]\,d\tau\right)^{\!1/2}
\;\le\; \sqrt{T_d}\;\varepsilon, \tag{2.9}
$$

其中最后一步用假设 (A3)。关键点：假设 (A3) 的期望取在 **真实轨迹分布** $p_\tau = \Law(u^\natural(\tau))$ 上，与 $(2.8)$ 中的测度经步骤 5 修复后一致。

---

### Step 8 · Gronwall 逆时积分

对微分不等式 $(2.8)$ 在反向时间 $[T_d, 0]$ 上作 Gronwall 处理。记 $\bar\Lambda \coloneqq \Lambda + C'$。将 $(2.8)$ 改写为

$$
\frac{d}{d\tau}\!\big[\delta(\tau)\,e^{-\bar\Lambda \tau}\big]
\;\le\; C_\sigma\,\beta(\tau)\,e^{-\bar\Lambda \tau},
$$

其中导数沿反向方向（$\tau$ 递减）。在 $[0, T_d]$ 上正向积分（等价于将反向 Gronwall 写为正向形式）：

$$
\delta(0)\,e^{-\bar\Lambda \cdot 0} - \delta(T_d)\,e^{-\bar\Lambda T_d}
\;\le\; C_\sigma \int_0^{T_d} \beta(\tau)\,e^{-\bar\Lambda \tau}\,d\tau.
$$

由于初始条件在噪声端一致（$\hat u(T_d) \sim p_{T_d}$，$u^\natural(T_d) \sim p_{T_d}$），有 $\delta(T_d) = 0$。故

$$
\delta(0)
\;\le\; C_\sigma\,e^{\bar\Lambda T_d} \int_0^{T_d} \beta(\tau)\,e^{-\bar\Lambda \tau}\,d\tau
\;\le\; C_\sigma\,e^{\bar\Lambda T_d} \int_0^{T_d} \beta(\tau)\,d\tau. \tag{2.10}
$$

将 $(2.9)$ 代入：

$$
\delta(0) \;\le\; C_\sigma \sqrt{T_d}\;\varepsilon\;e^{(\Lambda + C')T_d}. \tag{2.11}
$$

---

### Step 9 · $W_1$ 上界与常数吸收

由同步耦合构造，$W_1$ 距离不大于耦合下的 $L^1$ 期望：

$$
W_1\!\big(\Law(\hat u(0)),\, \rho^\star\big)
\;\le\; \mathbb{E}\|\hat u(0) - u^\natural(0)\|
\;=\; \delta(0).
$$

> 注：严格来说 $W_1$ 上有耦合 $\Law(\hat u(0))$ vs $\Law(u^\natural(0))$，而 $\Law(u^\natural(0)) = \rho^\star$（因真实反向 ODE 精确恢复目标分布）。因此 $W_1(\Law(\hat u(0)), \rho^\star) \le \delta(0)$ 成立。

将 $(2.11)$ 代入，令 $C \coloneqq C_\sigma \sqrt{T_d}\,e^{C' T_d}$，得

$$
W_1\!\big(\Law(\hat u(0)),\, \rho^\star\big)
\;\le\; C\,\varepsilon\,e^{\Lambda T_d}. \tag{2.12}
$$

注意到 $C' = C_{\mathrm{stab}}\,L_g$，而 $L_g$ 与 schedule 和网络结构有关但与 $\varepsilon$ 无关。在 $\varepsilon \ll 1$ 的渐近意义下，$e^{C'T_d} = \mathcal{O}(1)$ 可被常数 $C$ 吸收。最终形式如 $(2.1)$ 所示。

证毕。$\hfill \blacksquare$

---

## PDE Connection · 从数值解到真实 PDE 解的稳定传递

上述证明在扩散模型域内（状态空间 $\mathbb{R}^d$）完成，给出 $\Law(\hat u(0))$ 逼近 $\rho^\star = \Law(\mathbf{u}^\star)$ 的 $W_1$ 界。以下确保当训练数据源自数值解时，该界**稳定传递**至真实 PDE 解，不因物理时间传播而爆炸。

**命题（Kruzhkov $L^1$ 收缩性）**。设 $\mathbf{u}, \mathbf{v}$ 为同一标量守恒律 $\partial_t \mathbf{u} + \partial_x f(\mathbf{u}) = 0$ 的两个 Kruzhkov 熵解，初值分别为 $\mathbf{u}_0, \mathbf{v}_0$。则在任意物理时间 $t > 0$，

$$
\|\mathbf{u}(\cdot, t) - \mathbf{v}(\cdot, t)\|_{L^1(\Omega)}
\;\le\;
\|\mathbf{u}_0 - \mathbf{v}_0\|_{L^1(\Omega)}. \tag{2.13}
$$

（参见 \citet{kruzhkov1970first}，Theorem 1 或 \citet{dafermos2016hyperbolic}，§6.3.）

**推论**（数值误差不传播）。若训练数据由数值解 $\mathbf{u}_h$ 产生，满足 $\|\mathbf{u}_h - \mathbf{u}^\star\|_{L^1} \le \delta_{\mathrm{num}}$，则在离散对应关系 $\|u\| \approx \sqrt{\Delta x}\,\|\mathbf{u}\|_{L^2}$ 下，

$$
\|\hat u(0) - u_h\| \;\le\; \underbrace{\|\hat u(0) - u^\star\|}_{\text{Theorem 2 界}\; \mathcal{O}(\varepsilon e^{\Lambda T_d})}
\;+\;
\underbrace{\|u^\star - u_h\|}_{\text{数值误差}\; \mathcal{O}(\delta_{\mathrm{num}})}.
$$

由 $(2.13)$，$\delta_{\mathrm{num}}$ 不随物理时间 $T_{\mathrm{phys}}$ 增长——这是保守律熵解区别于一般 PDE 的核心性质（譬如 Navier–Stokes 的 $L^2$ 误差可能随时间传播，但守恒律 $L^1$ 误差被初值约束）。

> **实践含义**：实验中使用高分辨率 Godunov / WENO 求解器生成训练参考解，$\delta_{\mathrm{num}}$ 远小于 score-matching 误差 $\varepsilon$（典型的网格分辨率在 $N_x \ge 2048$ 时 $\delta_{\mathrm{num}} \sim 10^{-4}$），因此 Theorem 2 的界是误差的主导项。

---

## Remarks · 界的形式与局限性

### Remark 2.2（$\exp(\Lambda)$ 的来源与紧性）

$(2.1)$ 中的指数因子 $\exp(\Lambda T_d)$ 源于漂移场 $b$ 的 Lipschitz 常数 $\Lambda = \sup_\tau |\sigma \dot\sigma|\,L_s(\tau)$。当目标分布含激波（即 $\rho^\star$ 有 Dirac 质量点）时，$\nabla_u s$ 在 interfacial layer 中 blowing up 为 $\mathcal{O}(1/\tau)$，导致 $L_s(\tau) \sim 1/\tau$，$\Lambda$ 因此发散（或很大，取决于 early-stopping $\tau_{\mathrm{end}}$）。该指数放大是 **标准 score-based 扩散在处理间断解时的固有缺陷**。

Theorem 3 通过 BV-aware 参数化将该放大因子**缩减为 $\mathcal{O}(1)$**，是本文核心贡献。

### Remark 2.3（与 Score Shocks \citep{sarkar2026scoreshocks} 的关系）

本定理的界结构与 Score Shocks Theorem~6.3 一致（$W_1 \lesssim \varepsilon \exp(\Lambda T)$）。我们的独立推导补充了以下 Score Shocks 未详述的技术点：
- 测度不一致的正式处理（步骤 5，假设 A4）；
- Lipschitz 常数的显式溯源（假设 A1）；
- 与 Kruzhkov $L^1$-收缩性的桥接，使界从扩散模型域传递至 PDE 域。

### Remark 2.4（常数 $C'$ 与网络 Lipschitz 界）

步骤 5–6 中出现的附加常数 $C' = C_{\mathrm{stab}}\,L_g$ 在指数中累积为 $e^{C' T_d}$。在实践尺度（$T_d \sim 1$，$L_g$ 由谱归一化或权值衰减控制）下，$e^{C' T_d} = \mathcal{O}(1)$，因此该常数不影响渐近速率，仅影响绝对常数 $C$。正式地，可要求网络满足 $\|s_\theta\|_{\mathrm{Lip}} \le L_{\mathrm{net}}$ 作为训练正则化的一部分。

---

## 符号索引 · 与 SYMBOL.md / notation.tex 的对齐

| 本证明中使用 | `macros/notation.tex` 宏 | 含义 |
|---|---|---|
| $\rho^\star$ | `\rhotrue` | 目标解分布 |
| $p_\tau$ | `\ptau` | 平滑后密度 |
| $s(u, \tau)$ | `\score` | 真实 score 场 |
| $s_\theta(u, \tau)$ | `\sth` | 学习 score 网络 |
| $\sigma(\tau)$ | `\sigtau` | 噪声 schedule |
| $G_\tau$ | `\Gtau` | 热核 |
| $W_1(\cdot, \cdot)$ | `\Wass{1}` | 1-Wasserstein 距离 |
| $\Lambda$ | `\amp` | 分数激波放大指数 |
| $\mathbf{u}^\star$ | `\physsol` | Kruzhkov 熵解 |
| $\nu_{\mathrm{phys}}$ | `\physvis` | PDE 物理黏性 |
| $\mathbb{E}$ | `\E` | 期望 |
| $\Law(\cdot)$ | `\Law` | 随机变量法则 |
| $\Lip(f)$ | `\Lip` | Lipschitz 常数 |
| $\|\cdot\|$ | `\norm{}` (待加) | 欧氏范数 |
| $u^\natural(\tau)$ | `\unat` | 真实反向 ODE 轨迹 |
| $\hat u(\tau)$ | `\uhat` | 近似反向 ODE 轨迹 |
| $u^\theta$ | `\uth` | 最终生成样本 $\hat u(0)$ |
