# L5 Score–Burgers 对应与双 Burgers 耦合（Theorem 1）

> **本讲定位**：五讲系列的收束。把 L1（扩散 ⇔ FP）、L2（$W_2$ 几何）、L3（JKO）、L4（熵解 / 粘性消失）这四条线索**汇成一条叙事**：扩散模型的 score 本身是一个 Burgers 速度场；目标双曲 PDE 也是（或结构相似于）Burgers；两个 Burgers 沿正交方向耦合，这就是 **EntroDiff 方法的理论土壤**。
> **先修**：L1–L4 全部；Score Shocks 论文至少浏览过 §4–§6。
> **直接输出**：路径 A Theorem 1（Double-Burgers Coupling）的完整陈述 + Theorem 3 的证明骨架。
> **长度**：约 5000 字。

---

## §0 本讲的结构

本讲分三块：

| 块 | 节 | 内容 |
|---|---|---|
| A | §1–§3 | **Score–Burgers correspondence**：Score Shocks 论文核心结果完整梳理 |
| B | §4–§5 | **Double-Burgers Coupling**：路径 A Theorem 1 的陈述与证明 sketch |
| C | §6–§7 | **从 Double Burgers 到 EntroDiff parameterization (C)**：Theorem 3 证明骨架 |

§8 给全五讲的一页地图。§9 给 L6/代码实现的 hand-off。

---

## A — Score–Burgers Correspondence

## §1 推导：从热方程到 Score 的 Burgers 方程

### 1.1 设定

VE-SDE 情形，L1 §2.6 我们已经把前向 FP 方程变成标准热方程（选累计扩散时间 $\tilde\tau = \sigma^2/2$）：
$$
\partial_{\tilde\tau} p = \Delta p, \qquad p(u, 0) = \rho(u). \tag{1.1}
$$
本讲全文使用 $\tilde\tau$ 时间（除非说明）。Score $s(u, \tilde\tau) = \nabla_u \log p(u, \tilde\tau)$。

### 1.2 一维 Score PDE（Score Shocks Theorem 4.1）

**命题 1.1**：$p > 0$ 光滑时，$s = \partial_u \log p = p_u/p$（$d = 1$）满足
$$
\boxed{\partial_{\tilde\tau} s = \partial_{uu} s + 2 s \, \partial_u s.} \tag{1.2}
$$

**完整推导**：
1. $s = p_u / p$，故 $p_u = s p$。
2. 微分 $p_u = s p$：
$$
p_{uu} = s_u p + s p_u = (s_u + s^2) p, \tag{1.3}
$$
$$
p_{uuu} = [s_u + s^2]_u p + (s_u + s^2) p_u = [s_{uu} + 2 s s_u + (s_u + s^2) s] p = (s_{uu} + 3 s s_u + s^3) p. \tag{1.4}
$$
3. 对 $s = p_u / p$ 求 $\tilde\tau$ 偏导：
$$
\partial_{\tilde\tau} s = \frac{p_{\tilde\tau u} p - p_u p_{\tilde\tau}}{p^2} = \frac{p_{\tilde\tau u}}{p} - s \frac{p_{\tilde\tau}}{p}. \tag{1.5}
$$
4. 用热方程 $p_{\tilde\tau} = p_{uu}$ 和 $p_{\tilde\tau u} = p_{uuu}$：
$$
\partial_{\tilde\tau} s = \frac{p_{uuu}}{p} - s \frac{p_{uu}}{p}.
$$
代入 (1.3) (1.4)：
$$
\partial_{\tilde\tau} s = (s_{uu} + 3 s s_u + s^3) - s(s_u + s^2) = s_{uu} + 2 s s_u.
$$
即 (1.2)。∎

**Remark 1.2**：(1.2) 不是近似，是**恒等式**。只要 $p$ 严格正，(1.2) 对任意 $\rho$ 都成立。

### 1.3 Cole–Hopf → 粘性 Burgers（Theorem 4.3）

**命题 1.3**：设 $w \coloneqq -2 s$。则 $w$ 满足
$$
\boxed{\partial_{\tilde\tau} w + w \partial_u w = \partial_{uu} w,} \tag{1.6}
$$
即**粘性 Burgers 方程**（单位粘性）。

**证明**：$s = -w/2$，$s_u = -w_u/2$，$s_{uu} = -w_{uu}/2$，$s_{\tilde\tau} = -w_{\tilde\tau}/2$。代入 (1.2)：
$$
-\frac{w_{\tilde\tau}}{2} = -\frac{w_{uu}}{2} + 2 \cdot \left(-\frac{w}{2}\right) \cdot \left(-\frac{w_u}{2}\right) = -\frac{w_{uu}}{2} + \frac{w w_u}{2}.
$$
乘以 $-2$：$w_{\tilde\tau} = w_{uu} - w w_u$，即 (1.6)。∎

**解读**：**$w = -2s$ 就是一个粘性 Burgers 的速度场**，粘性 $= 1$（因为我们用 $\tilde\tau$ 归一化）。这是 L1 §6 我们预告的结论。

### 1.4 Cole–Hopf 的来源

(1.6) 到热方程有一个经典变换（L4 没讲，这里补充）：设 $w = -2 \partial_u \log \varphi$，$\varphi > 0$。代入 (1.6) 验证 $\partial_{\tilde\tau} \varphi = \partial_{uu} \varphi$——即 $\varphi$ 满足热方程。

对比：我们有 $w = -2 s = -2 \partial_u \log p$，且 $p$ 满足热方程。所以 Score–Burgers 对应不过是 **Cole–Hopf 的一次直接应用**：热方程的 log-gradient 就是粘性 Burgers 速度。

## §2 多维推广：Vector Burgers

### 2.1 Vector Score PDE

**命题 2.1（Score Shocks §7.1）**：$d$-维 VE 扩散下，$s = \nabla_u \log p \in \mathbb R^d$ 满足
$$
\partial_{\tilde\tau} s_i = \Delta s_i + 2 (s \cdot \nabla) s_i + 2 (\nabla \cdot s) s_i, \quad i = 1, \ldots, d. \tag{2.1}
$$

**推导**：对 $s_i = \partial_i \log p = p_i / p$ 逐分量重复 §1.2 的代数（用 $\partial_j p = s_j p$）。细节略。

### 2.2 Vector Burgers + Curl Preservation

**命题 2.2（Score Shocks Theorem 7.5）**：$w \coloneqq -2s \in \mathbb R^d$ 满足
$$
\boxed{\partial_{\tilde\tau} w + (w \cdot \nabla) w = \Delta w,} \tag{2.2}
$$
且 **$w$ 无旋**：curl$(w) = \nabla \times w = 0$。

**说明**：由于 $w = -2 \nabla \log p$ 是梯度，$w$ 无旋是恒等式。Burgers 动力学 (2.2) **保持**这个无旋性——即使 $w_0$ 只是近似无旋（比如网络训练误差导致），演化下去仍保持接近无旋。

### 2.3 路径 A 的用处

curl-preservation 保证：即使 neural network 学的 $s_\theta$ 有小的 curl，(2.2) 的动力学不会放大这个 curl。**所以 $s_\theta$ 的 curl 是 network approximation error，不是 dynamics 本质问题**（这是 Score Shocks 对 Vuong et al. 2025 观察的一个重要澄清）。

---

## §3 Score Shocks 的五大结论（路径 A 会反复引用）

把论文 §5–§9 的核心结论压缩给你：

### (i) Speciation Threshold（何时 shock 形成）

**命题 3.1**：$\rho$ 是 $d$-维对称二元 Gaussian 混合 $\tfrac12 \mathcal N(\mu_1, \sigma_0^2 I) + \tfrac12 \mathcal N(\mu_2, \sigma_0^2 I)$，则 Score Burgers (2.2) 在 $\tilde\tau = \tilde\tau^\star \coloneqq \|\mu_1 - \mu_2\|^2/4 - \sigma_0^2$ 处形成第一个 shock（mode 分化时刻）。

一般（非 Gaussian）混合，$\tilde\tau^\star$ 由 between-class covariance 的最大特征值决定。

### (ii) Interfacial Profile（shock 附近 $w$ 的形状）

**命题 3.2（Proposition 5.4 of Score Shocks）**：对任意光滑二元分解 $p = p_1 + p_2$（$p_i > 0$），记 $\phi = \log(p_1/p_2)$，则在某"正则 mode 边界"近处：
$$
w(u, \tilde\tau) = \underbrace{w^{\mathrm{sm}}(u, \tilde\tau)}_{\text{光滑背景}} + \underbrace{\frac{\kappa(u, \tilde\tau)}{2} \tanh\!\left(\frac{\phi(u, \tilde\tau)}{2}\right) \nabla \phi(u, \tilde\tau)}_{\text{interfacial layer}} + o(1). \tag{3.1}
$$

**解读**：interfacial layer 的形状是 $\tanh$，宽度由 $|\nabla\phi|^{-1}$ 决定，强度（跳跃高度）由 $\kappa$ 决定。**这是一个精确形式，不是 ansatz**。

### (iii) Error Amplification（这条最关键）

**命题 3.3（Theorem 6.3 of Score Shocks）**：设 score 误差 $\|s_\theta - s\|_{L^2} \leq \varepsilon$。在 interfacial layer 附近（shock forming），从 $\tilde\tau = \tilde\tau_0$ 到 $\tilde\tau = \tilde\tau_f$ 的反向轨迹，
$$
\|\hat u(\tilde\tau_f) - u(\tilde\tau_f)\| \leq \varepsilon \exp(\Lambda(\tilde\tau_f - \tilde\tau_0)), \qquad \Lambda \approx \frac{\mathrm{SNR}}{2}. \tag{3.2}
$$

**严重性**：反向采样在 shock formation 时，score 误差被**指数放大**。若 $\mathrm{SNR} \sim 10$（典型值），$\Lambda \sim 5$，走 $T = 1$ 单位时间就是 $e^5 \approx 150$ 倍放大——小 $\varepsilon$ 被拉到 $\mathcal O(1)$。

**路径 A 正是要去除这个 $\exp(\Lambda T)$ 因子**。方法：把 (3.1) 的 tanh 结构**直接嵌入到 network architecture**（parameterization (C)）——网络不"学"tanh，tanh 是 built-in 的。见 §6。

### (iv) Curl Preservation（已在 §2 说）

### (v) VP-to-VE Reduction

**Theorem 8.5**：VP-SDE 可通过坐标变换 $u \to u/\alpha(\tilde\tau)$ 归约到 VE。所以路径 A 只用 VE 设定证明 Theorem 1–5，VP 情形是 corollary。

---

## B — Double-Burgers Coupling（Theorem 1）

## §4 Setup：两个时间方向

### 4.1 两个时间，两个 Burgers

| 时间 | 含义 | 方程 |
|---|---|---|
| $t$ | **物理时间** | 目标双曲 PDE：$\partial_t u + \partial_x f(u) = 0$ |
| $\tilde\tau$ | **扩散时间** | Score Burgers：$\partial_{\tilde\tau} w + w \partial_u w = \partial_{uu} w$, $w = -2s$ |

这是**两个正交的时间方向**。$t$ 上目标 PDE 生成数据；$\tilde\tau$ 上扩散模型从 noise 到 data。路径 A Theorem 1 揭示两者的几何耦合。

### 4.2 Data-generating distribution $\rho_t$

设初值分布 $\rho_0$（比如 Gaussian process，$\rho_0 \in \mathcal P_2(BV(\Omega))$）。物理 PDE 驱动 $\rho_0$ 在 $t$ 方向演化：$u_0 \sim \rho_0 \Rightarrow u(\cdot, t) \sim \rho_t$。

（严格说，$\rho_t$ 是 "$\rho_0$ 在 solution operator $S_t$ 下的推前"，即 $\rho_t = (S_t)_\# \rho_0$，$S_t$ 是 Kruzhkov 熵解半群。）

### 4.3 训练数据

路径 A 的**数据集** = $\{(u_0^{(i)}, u^{(i)}(\cdot, T))\}_{i=1}^N$（从 $\rho_0$ 采初值，跑到物理时间 $T$ 得到 solution）。扩散模型学 $\rho_T$。

（更精细地，学的是 joint $(u_0, u_T)$ 的分布，这对应 DiffusionPDE 的 joint embedding 思想。但 Theorem 1 陈述为了简洁只看 $\rho_T$。）

---

## §5 Theorem 1 — Double-Burgers Coupling

### 5.1 Statement（formal 版）

> **Theorem 1**（Double-Burgers Coupling）
>
> 设 $f \in C^2(\mathbb R)$ 凸通量，$u_0 \sim \rho_0$，$\rho_0 \in \mathcal P_2(L^\infty(\Omega) \cap BV(\Omega))$。设 $u(\cdot, t)$ 是 (1.1) 的 Kruzhkov 熵解，$\rho_t = (S_t)_\# \rho_0$。定义 $p_{\tilde\tau, t}(u) \coloneqq (\rho_t * G_{\tilde\tau})(u)$ 为扩散模型学的 noised density，score $s_{\tilde\tau, t}(u) = \nabla_u \log p_{\tilde\tau, t}(u)$，$w_{\tilde\tau, t} \coloneqq -2 s_{\tilde\tau, t}$。
>
> 则：
>
> **(A) Score Burgers**：在 $\tilde\tau > 0$ 所有点，$w_{\tilde\tau, t}$ 沿 $\tilde\tau$ 方向满足 vector Burgers
> $$
> \partial_{\tilde\tau} w + (w \cdot \nabla_u) w = \Delta_u w. \tag{5.1}
> $$
>
> **(B) Physical 结构**：在物理时间 $t$ 方向，$\rho_t$ 作为 $\mathcal P_2(L^\infty)$ 中的曲线满足**连续性方程**
> $$
> \partial_t \rho_t + \nabla_u \cdot (\rho_t \cdot V_t) = 0, \quad V_t(u)(x) = -\partial_x f(u(x)), \tag{5.2}
> $$
> （沿 PDE 特征线 + 粘性消失极限下的修正）。
>
> **(C) Shock 集合同址**：设 $\Sigma_{\mathrm{phys}}(t) \subset \Omega$ 是 $u(\cdot, t)$ 的物理 shock 集合（=跳跃集），$\Sigma_{\mathrm{score}}(\tilde\tau, t) \subset \mathbb R^{|\Omega|}$ 是 $w_{\tilde\tau, t}$ 的 interfacial layer 集合（§3(ii) 中 $|\nabla\phi| \gtrsim 1$ 的区域）。则
> $$
> \Sigma_{\mathrm{score}}(\tilde\tau, t) \big|_{\tilde\tau \to 0^+} \ \longleftrightarrow \ \Sigma_{\mathrm{phys}}(t) \tag{5.3}
> $$
> 在测度收敛意义下。

### 5.2 Proof Sketch

**(A) 推导**：$p_{\tilde\tau, t} = \rho_t * G_{\tilde\tau}$ 对固定 $t$ 沿 $\tilde\tau$ 满足热方程（Gaussian 核的性质）。然后直接套用 §1–§2 的 Score–Burgers 推导。∎

**(B) 推导**：$\rho_t = (S_t)_\# \rho_0$，$S_t$ 是熵解半群。Kruzhkov 1970 证明 $S_t$ 是 $L^1$ 上的连续半群，但要**在 $\rho_t \in \mathcal P_2$ 意义下写成 (5.2) 需要用粘性消失**。设 $\rho_t^\varepsilon = (S_t^\varepsilon)_\# \rho_0$，$S_t^\varepsilon$ 是粘性 PDE (L4 (5.1)) 的 semigroup。则 $\rho_t^\varepsilon$ 满足
$$
\partial_t \rho_t^\varepsilon + \nabla_u \cdot \big(\rho_t^\varepsilon V_t^\varepsilon\big) = \varepsilon \Delta_u \rho_t^\varepsilon + \mathrm{lower\ order}.
$$
取 $\varepsilon \to 0^+$ 并用 BV compactness（L4 §6）抽取子列，得 (5.2) 的弱形式。∎

**(C) 推导**：这是最微妙的一步。要用 §3(ii) 的 interfacial profile (3.1) + (B) 的 $\rho_t$ 的 BV 结构。关键：$\rho_t$ 的**支集奇异性** = 物理 shock 的位置和幅度由初值 $\rho_0$ 决定。对小 $\tilde\tau$，$p_{\tilde\tau, t}$ 的"mode boundary"就被物理 shock "刻"出来。具体化为 (5.3) 的测度收敛需要仔细论证，属于 Theorem 1 的主要数学工作量。

∎（完整证明留给论文附录，本讲只给骨架）

### 5.3 Theorem 1 的意义

**这是整篇论文的核心几何观察**：
- 没有 Theorem 1，EntroDiff 只是一个"加了熵正则的 DiffusionPDE"；
- 有了 Theorem 1，EntroDiff 的设计从 (C) parameterization 到 loss family 都有了**几何必然性**：两个 Burgers 的 shock 同址，所以必须把 tanh interfacial layer 嵌进 network，让它和物理 shock 对齐。

---

## C — From Theorem 1 to EntroDiff

## §6 EntroDiff Parameterization (C) 的设计原理

回到方法骨架 §3.2 的 (C)：
$$
s_\theta(u, \tilde\tau) = \nabla_u \phi^{\mathrm{sm}}_\theta(u, \tilde\tau) + \frac{\kappa_\theta(u, \tilde\tau)}{2} \tanh\!\left(\frac{\phi^{\mathrm{sh}}_\theta(u, \tilde\tau)}{2}\right) \nabla_u \phi^{\mathrm{sh}}_\theta(u, \tilde\tau). \tag{6.1}
$$

### 6.1 各组件的几何含义

| 组件 | Score Shocks (3.1) 对应 | 解读 |
|---|---|---|
| $\phi^{\mathrm{sm}}_\theta$ | $w^{\mathrm{sm}}/2$（的势函数） | 数据分布"光滑背景"的 log-density |
| $\phi^{\mathrm{sh}}_\theta$ | $\phi$ | signed log-ratio of modes（实际上是 signed distance to shock）|
| $\kappa_\theta$ | $\kappa$ | interfacial strength，由 Rankine–Hugoniot 决定 |

### 6.2 为什么这样能去除 $\exp(\Lambda)$ 放大？

**关键**：在 standard parameterization (A)（如 EDM 的 $D_\theta$），网络**从 scratch 学 tanh 结构**。学的过程中任何偏差（$L^2$ 意义下的 $\varepsilon$ 误差）都可能让 shock 附近的 score 形状错位，进而在 Score Burgers 动力学下被 $\exp(\Lambda)$ 放大。

**而 (C) 参数化直接把 tanh 结构"硬写入" architecture**：网络只需要学 $\phi^{\mathrm{sm}}, \phi^{\mathrm{sh}}, \kappa$ 三个**光滑**场。这些场在 shock 附近**不需要** sharp transition——sharpness 由外层的 $\tanh$ 提供。结果：网络误差不触发 $\exp(\Lambda)$ 放大。

### 6.3 训练

(6.1) 的每个组件都是一个神经网络子模块。训练时：
- $\phi^{\mathrm{sm}}$：用 residual MLP / U-Net，预测光滑 scalar；
- $\phi^{\mathrm{sh}}$：用同样架构，但在 loss 里加 "signed distance" 监督（用经典 PDE solver 生成的 ground-truth shock 位置作监督信号）；
- $\kappa$：轻量 MLP；

Loss：standard DSM on $s_\theta$ + optional BV regularizer + optional entropy regularizer。详见 W5-W6 代码阶段。

### 6.4 Remark：和 DiffusionPDE 的区别

DiffusionPDE 的 $D_\theta$ 是 vanilla U-Net；没有任何关于 shock 的 architectural prior。其 score 在 shock 附近**只能靠数据量堆**（观察到足够多带 shock 的样本才能 "emulate" tanh 形状）。**(C) 参数化直接把这个 prior 写死**，采样效率和泛化性质都应比 DiffusionPDE 好。

---

## §7 Theorem 3 证明骨架（Improved Rate）

回到方法骨架 §4 的 Theorem 3：在 parameterization (C) + loss $\mathcal L_3$ 下，
$$
W_1(\mathrm{Law}(\hat u), \mathrm{Law}(u^\star)) \leq C \varepsilon^{1/2}. \tag{7.1}
$$

**证明骨架（5 步）**：

**Step 1（界分拆）**：用 triangle inequality
$$
W_1(\mathrm{Law}(\hat u), \mathrm{Law}(u^\star)) \leq \underbrace{W_1(\mathrm{Law}(\hat u), \rho_T)}_{(\mathrm{i})} + \underbrace{W_1(\rho_T, \mathrm{Law}(u^\star))}_{(\mathrm{ii})}.
$$
(ii) = 0 若训练数据就是 $u^\star$ 样本；(i) 是采样误差。

**Step 2（采样误差 = score 误差传播）**：反向 SDE 产生的 $\hat u$ 和真实 $u \sim \rho_T$ 的差，由 score 误差 $\|s_\theta - s\|$ 决定。用 Girsanov / Chen–Chewi 技术，得
$$
W_1(\mathrm{Law}(\hat u), \rho_T) \leq \int_0^{T_d} \|s_\theta(\cdot, \tilde\tau) - s(\cdot, \tilde\tau)\|_{L^2(p_{\tilde\tau})} \, d\mu(\tilde\tau) \cdot \exp\!\bigg(\int_0^{T_d} \Lambda(\tilde\tau) d\tilde\tau\bigg).
$$
这就是 (i) 的 standard bound（Benton et al. 2024 类型）。

**Step 3（去除 $\exp$ 放大）**：在 parameterization (C) 下，关键事实是 $\|s_\theta - s\|$ 的 "$\Lambda$-weighted norm" 比普通 $L^2$ 小——因为 (C) 不让误差集中在 interfacial layer（层内 $\tanh$ profile 是 exact）。形式化为 Lemma：
$$
\int_0^{T_d} \Lambda(\tilde\tau) \|s_\theta - s\|_{L^2(p_{\tilde\tau, \mathrm{layer}})}^2 d\tilde\tau \leq C_1 \varepsilon^2, \tag{7.2}
$$
即 interfacial layer 上的 weighted error 由 total $L^2$ error $\varepsilon$ 控制。

**Step 4（BV 正则的效用）**：loss $\mathcal L_3$ 的 BV term $\lambda_{\mathrm{BV}} \mathrm{TV}(D_\theta)$ 保证 $\hat u \in BV$（或至少接近）。由 L4 §6 的 Helly 紧性，sampling 产出的 $\hat u$ 有极限子列；结合 (7.2) 的 weighted bound 得 $W_1$ 意义下 $\hat u \to u^\star$。

**Step 5（速率）**：把 (7.2) 和 (ii) 组合，最后速率是 $\mathcal O(\varepsilon^{1/2})$——由 Step 3 的 "$L^2 \to$ weighted $L^2$" 改进（平方根）给出。

∎（完整证明 ~ 10-15 页，论文附录给）

### 7.1 Remark：为什么是 $\varepsilon^{1/2}$ 而不是 $\varepsilon$？

最理想当然是 $\mathcal O(\varepsilon)$（线性）。$\varepsilon^{1/2}$ 来自 Step 3 的 $L^2 \to$ weighted 估计——这是由 Score Shocks Theorem 6.3 的误差放大**部分**保留（只在 layer 以外消失，layer 内被 (C) 抑制）。

如果能证 $\mathcal O(\varepsilon)$ 我们当然会追求。目前的证明路线**保守地**给 $\varepsilon^{1/2}$，写进论文也足够超越 DiffusionPDE / FunDPS 的 $\varepsilon \exp(\Lambda T)$（指数放大 vs 平方根退化，后者在 $\varepsilon \ll 1$ 时压倒性更好）。

---

## §8 五讲 Map（一页叙事）

把 L1–L5 做一个 totality 总结：

```
L1: 扩散模型 ⇔ Fokker–Planck
    (前向 Langevin SDE + 反向 Anderson + DSM + Tweedie)
            │
            ↓ "score 的本质"
L5 §1:  Score–Burgers Correspondence (1D)
    w = -2s 满足粘性 Burgers
            │
            ↓ "解分布的度量"
L2: 最优传输 & W_2 几何
    (Monge → Kantorovich → Brenier → W_2 → Otto calculus)
            │
            ↓ "FP = W_2-梯度流"
L3: JKO Scheme
    (proximal step in P_2; τ→0 极限恢复 FP)
            │
            ↓ "路径 A 的梯度流骨架"
Theorem 5: EntroDiff ⇔ constrained JKO
            │
            ║
            ↓ "目标 PDE 的解不光滑"
L4: 双曲 PDE 弱解理论
    (shock + Rankine–Hugoniot + Kruzhkov 熵 + BV + 粘性消失)
            │
            ↓ "shock 位置的几何"
L5 §2-§5: Double-Burgers Coupling (Theorem 1)
    Σ_phys ↔ Σ_score
            │
            ↓ "BV-aware score architecture"
L5 §6: EntroDiff parameterization (C)
    s_θ = ∇φ^sm + (κ/2)tanh(φ^sh/2)∇φ^sh
            │
            ↓ "主定理"
Theorem 3: W_1 ≤ O(ε^{1/2})  (去除 exp(Λ) 放大)
```

**论文的三大理论贡献**（intro 那句话）就是上面 bold 的三块：Theorem 1（结构）、parameterization (C)（算法）、Theorem 3（收敛率）。

---

## §9 Hand-off：讲义到代码的衔接

到此，5 讲的理论地基打完。下一步进入方法骨架的 W4 阶段（定理证明完整化）和 W5 阶段（代码）。

**论文需要补充的讲义外内容**（留作 issue）：
- Theorem 2 / Theorem 4 / Theorem 5 的完整证明（每个 5–10 页）；
- 数值 benchmark 的详细 setup（每个 1–2 页）；
- ablation 设计（3 个：parameterization A/B/C 对比、loss L₁/L₂/L₃/L₄ 对比、schedule 对比）；
- GPU 时间 / 参数 count / 训练时间表。

**代码需要的工程项**（留给 W5–W6）：
- EDM 代码库 fork（基础 diffusion framework）；
- BV-aware U-Net（分 $\phi^{\mathrm{sm}}, \phi^{\mathrm{sh}}, \kappa$ 三个 head）；
- Godunov 数值通量的 PyTorch 实现（for $\mathcal L_{\mathrm{PDE}}$）；
- Kruzhkov entropy residual 的 random-$k$ 采样实现。

---

## 附录 A：常见疑问

**Q1**：Theorem 1 (5.3) 的 "$\longleftrightarrow$" 在测度收敛意义下具体是什么？
A：最清晰的版本是：把 $\Sigma_{\mathrm{score}}$ 投影到 $\Omega$ 得 $\pi_\Omega(\Sigma_{\mathrm{score}}) \subset \Omega$；此集随 $\tilde\tau \to 0^+$ 在 Hausdorff 距离下收敛到 $\Sigma_{\mathrm{phys}}(t)$。细节论文 Theorem 1 证明给。

**Q2**：路径 A 的 VE 设定和 Score Shocks 完全一致？
A：是的。我们用 Score Shocks §8 的 VP-to-VE reduction 把 VP 归约到 VE；论文主定理全部在 VE 下陈述。

**Q3**：Theorem 3 证明 Step 2 的 "Girsanov / Chen–Chewi" 技术需要额外讲义吗？
A：不必单独开讲义。在论文附录直接写 3–4 页证明即可；需要的工具（Girsanov 定理，KL-chain rule）是 Itô calculus 标准部分。但 W4 周完整化这个证明时我会单独起一个文档 `Docs/proofs/thm3.md`。

**Q4**：parameterization (C) 的 $\phi^{\mathrm{sh}}$ 如何用 neural network 近似 "signed distance"？
A：两种选项：（i）直接回归到 ground-truth shock set 的 signed distance（训练时需预先跑 Godunov solver 标注 shock 位置——贵但准）；（ii）无监督：用 eikonal loss $\||\nabla \phi^{\mathrm{sh}}| - 1\|^2$ 驱动 $\phi^{\mathrm{sh}}$ 变成 signed distance。论文应试 (ii) 优先（更接近真实部署场景）。

**Q5**：五讲写完后，我是不是可以直接去读论文主要部分 + 开始打码？
A：是。五讲是理解整个 path A 的**必要条件**（而非充分）。读完 L1–L5 + 路径 A method skeleton，你已经可以 (a) 独立陈述 Theorem 1–5；(b) 理解 parameterization A/B/C 的几何动机；(c) 看懂 DiffusionPDE / FunDPS 代码不会云里雾里。剩下的是工程和证明细化——这是 W4 之后的事。
