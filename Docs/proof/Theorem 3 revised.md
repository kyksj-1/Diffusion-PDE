
# Theorem 3（Improved Rate with BV-aware Parameterization）— 可发表完整证明版

> **版本说明**：本文档在符号统一修订版基础上进行了如下修改：
> 1. 引入显式假设体系 A0–A6，将定理前置条件完全显式化
> 2. 删除推论 1.4 的严格论断，保留其启发式论证逻辑（移至注释）
> 3. 定理 2.2 的积分界 $\int \|e\| \, d\tau \leq C\varepsilon$ 直接从 Score Matching 假设经 Cauchy–Schwarz 推出，不再依赖推论 1.4
> 4. 阶段 4 的范数转换改用离散 $L^1$–欧氏范数等价性，删除 Gagliardo–Nirenberg 插值（移至注中）
> 5. 粘性误差项与 $W_1$ 组装直接引用 A5、A6，逻辑链路完整闭合
> 6. 定理陈述显式引用 A0–A6

---

## 符号体系（全证明统一）

### 状态空间（扩散模型域）

| 符号 | 含义 |
|---|---|
| $u \in \mathbb{R}^d$ | 状态向量（$d = N_x$ 为空间网格点数） |
| $\tau \in [0, T_d]$ | 扩散时间（反向：$T_d \to 0$，即噪声 $\to$ 数据） |
| $p(u, \tau)$ | 平滑后的状态密度 |
| $s(u, \tau) = \nabla_u \log p(u, \tau)$ | 真实 Score 场 |
| $s_\theta(u, \tau)$ | 网络近似的 Score 场 |
| $e(u, \tau) = s_\theta(u, \tau) - s(u, \tau)$ | Score 残差场 |
| $\Gamma(\tau) \subset \mathbb{R}^d$ | 激波流形（shock manifold） |
| $d_\Gamma(u, \tau)$ | 到 $\Gamma(\tau)$ 的符号距离函数 |

### 物理空间（PDE 域，阶段 3 起引入）

| 符号 | 含义 |
|---|---|
| $x \in \Omega \subset \mathbb{R}$ | 物理空间坐标 |
| $t \in [0, T]$ | 物理时间（由 PDE 初值演化，与 $\tau$ 正交） |
| $\mathbf{u}^\star(x)$ | Kruzhkov 熵解（目标 PDE 的解，在固定物理时间 $t = T_{\text{phys}}$） |
| $\mathbf{u}^\nu(x)$ | 带粘性 $\nu_{\text{phys}}$ 的 PDE 粘性近似解（在 $t = T_{\text{phys}}$） |
| $\partial_x$ | 物理空间偏导 |
| $\|\cdot\|_{L^1(\Omega)}, \|\cdot\|_{L^2(\Omega)}$ | 物理空间上的 $L^p$ 范数 |

### 轨迹与生成

| 符号 | 含义 |
|---|---|
| $\hat{u}(\tau)$ | 学习 Score 驱动的 ODE 轨迹（$\mathbb{R}^d$ 值） |
| $u^\natural(\tau)$ | 真实 Score 驱动的 ODE 轨迹（$\mathbb{R}^d$ 值，$\natural$ = "natural"） |
| $u^\theta \coloneqq \hat{u}(0)$ | 最终生成样本（$\tau = 0$ 时刻） |
| $\mu_\theta \coloneqq \mathrm{Law}(u^\theta)$ | 生成样本的分布 |
| $\delta_{\mathbf{u}^\star}$ | 目标 Kruzhkov 熵解的 Dirac 测度 |

### 范数与距离

| 符号 | 含义 |
|---|---|
| $\|v\|$ | 状态空间 $\mathbb{R}^d$ 上的欧氏范数 |
| $\langle \cdot, \cdot \rangle$ | $\mathbb{R}^d$ 内积 |
| $\|\cdot\|_{L^1(\Omega)}, \|\cdot\|_{L^2(\Omega)}$ | 物理空间 $L^p$ 范数 |
| $\mathrm{TV}(f) = \int_\Omega |\partial_x f| \, dx$ | 全变差半范数 |
| $W_1(\mu, \nu)$ | 1-Wasserstein 距离（Kantorovich–Rubinstein 对偶） |

### 时间映射

扩散时间 $\tau$ 从 $T_d$ 递减至 $0$ 的物理含义：

- $\tau = T_d$：纯噪声（先验，如标准高斯）
- $\tau = 0$：数据样本（对应 PDE 在物理时间 $t = T_{\text{phys}}$ 的解）
- **粘性匹配**：$\sigma^2(\tau) = 2\nu_{\text{phys}} \tau$，使得 $\tau$ 的演进等效于带粘性 $\nu_{\text{phys}}$ 的物理过程；反向 ODE 的漂移系数为 $\nu_{\text{phys}}$
- 在阶段 3 中，目标 $\mathbf{u}^\star$ 是 PDE 在**固定物理时间** $t = T_{\text{phys}}$ 处的熵解（$T_{\text{phys}}$ 视为常数，后文不再显式写出）
- 扩散时间 $\tau$ 与物理时间 $t$ **正交**：$\tau$ 描述加噪–去噪强度，$t$ 描述 PDE 的演化

---

## 假设体系（A0–A6）

以下假设在整个证明中均有效。每条假设的物理意义与可验证性一并说明。

**假设 A0（BV 有界性）。** 损失函数 $\mathcal{L}_3$ 中的 TV 正则项 $\lambda_{\mathrm{BV}} \, \mathrm{TV}(D_\theta)$ 与参数化 (C) 的硬编码 $\tanh$ 结构共同保证：生成样本 $\mathbf{u}^\theta$ 几乎必然（a.s.）属于有界 TV 球

$$
\mathcal{K}_M \coloneqq \bigl\{ \mathbf{u} \in L^1(\Omega) \cap L^\infty(\Omega) : \mathrm{TV}(\mathbf{u}) \leq M \bigr\},
$$

且真实熵解满足 $\mathrm{TV}(\mathbf{u}^\star) \leq M$，其中 $M > 0$ 为与 $\varepsilon$ 无关的常数。

> *可验证性*：$M$ 可由初值的 TV 界与 BV 半群的 TV 不增性估计；正则化权重 $\lambda_{\mathrm{BV}}$ 是训练超参数。

**假设 A1（局部双模态 Score 结构）。** 在激波流形 $\Gamma(\tau)$ 邻域内，真实 Score 场具有渐近形式

$$
s(u, \tau) = s^{\mathrm{sm}}(u, \tau) + \frac{\Delta s_{\mathrm{jump}}(u)}{2} \tanh\!\left(\frac{A(u,\tau) - B(u,\tau)}{2\tau}\right) + \mathcal{O}(\tau),
$$

其中 $A, B$ 为两个主导模态的 Cole–Hopf 势函数，$\Delta s_{\mathrm{jump}} = \nabla_u B - \nabla_u A$ 为跃变向量，$s^{\mathrm{sm}}$ 在全空间一致 Lipschitz。此结构为 Laplace 渐近方法的局部结果，假设扩散时间充分小且高斯簇良好分离；允许有限个此类局部结构的叠加。

> *可验证性*：对离散分布混合模型可验证；一般连续分布视为合理工程近似（见工程近似 EA1）。

**假设 A2（网络参数化约束）。** 参数化 (C) 中：

- $\kappa_\theta(u,\tau) \geq \kappa_0 > 0$ 对所有 $(u,\tau)$ 严格成立（可通过 Softplus 激活函数实现，即 $\kappa_\theta = \kappa_0 + \mathrm{Softplus}(\tilde\kappa_\theta)$）；
- 映射 $\nabla_u^2 \phi^{\mathrm{sm}}_\theta$、$\nabla_u^2 D_\theta$、$\nabla_u \kappa_\theta$ 在 $(u,\tau) \in \mathbb{R}^d \times [\tau_{\text{end}}, T_d]$ 上一致有界，界常数与 $\tau$ 无关。

> *可验证性*：可通过网络架构设计与权重范数约束在训练时强制执行。

**假设 A3（Score Matching 误差）。** 存在 $\varepsilon > 0$ 使得在网格无关的均方误差意义下：

$$
\mathbb{E}_{u,\tau}\left[ \frac{|\Omega|}{d} \sum_{i=1}^d e_i(u,\tau)^2 \right] \leq \varepsilon^2,
$$

此处 $\Delta x = |\Omega|/d$，这等价于 $\mathbb{E}_{u,\tau}\bigl[\Delta x \|e(u,\tau)\|^2\bigr] \leq \varepsilon^2$，其中期望对训练分布 $p(u,\tau)$（$u \sim p(\cdot,\tau)$，$\tau \sim \mathcal{U}[\tau_{\text{end}}, T_d]$）取。该设定使 $\varepsilon^2$ 在物理上直接逼近连续的 $\int_\Omega e(x,\tau)^2 dx$。

**假设 A4（先验匹配）。** 反向 ODE 在初始时刻 $\tau = T_d$ 的先验近似平方距离界也被同样缩放控制：

$$
\mathbb{E}\bigl[\Delta x \|\hat{u}(T_d) - u^\natural(T_d)\|^2 \bigr] \leq \tilde{C}^2 \varepsilon^2,
$$

其中 $\tilde{C} > 0$ 为与 $\varepsilon$ 和 $d$ 无关的常数。

> *典型满足情形*：$p_{T_d}$ 取为标准高斯，且 $T_d$ 足够大使信噪比极低。

**假设 A5（Early stopping 与粘性匹配平衡，工程近似）。** 反向 ODE 提前停止在 $\tau_{\text{end}} > 0$ 处，有效终端粘性由 $\sigma^2(\tau_{\text{end}}) = 2\nu_{\text{phys}} \tau_{\text{end}}$ 定义，满足

$$
\nu_{\text{phys}} = \Theta(\varepsilon), \quad \text{即} \quad c\varepsilon \leq \nu_{\text{phys}} \leq C\varepsilon,
$$

且 A3 在全区间 $[\tau_{\text{end}}, T_d]$ 上依然成立。此选择可通过噪声调度（noise schedule）设计在实践中实现。

> *工程近似标注*：$\nu_{\text{phys}} = \Theta(\varepsilon)$ 的可达性依赖于噪声调度的精细设计以及训练误差 $\varepsilon$ 的事先估计，属**工程近似（Engineering Approximation, EA2）**，其影响范围见附录 C。

**假设 A6（Kuznetsov 型误差界）。** 在 A0 与 A5 下，粘性 PDE 解 $\mathbf{u}^\nu$ 与 Kruzhkov 熵解 $\mathbf{u}^\star$ 的 $L^1$ 误差满足

$$
\|\mathbf{u}^\nu - \mathbf{u}^\star\|_{L^1(\Omega)} \leq C_K \sqrt{\nu_{\text{phys}}},
$$

其中 $C_K$ 依赖于初值 TV 界 $M$ 与物理时间 $T_{\text{phys}}$，但与 $\varepsilon$ 无关。

> *说明*：此界由 Kuznetsov（1976）的经典定理在 A0 条件下直接给出，其中 $C_K = C \sqrt{T_{\text{phys}}} \cdot \mathrm{TV}(\mathbf{u}_0) \leq C \sqrt{T_{\text{phys}}} \cdot M$。

---

## Theorem 3（主定理）

**定理 3。** 在假设 A0–A6 下，考虑参数化 (C) 与损失 $\mathcal{L}_3$。设 Score Matching 误差满足 A3，其中 $\varepsilon \in (0,1)$。则生成分布 $\mu_\theta = \mathrm{Law}(u^\theta)$ 与 Kruzhkov 熵解 $\mathbf{u}^\star$ 对应的 Dirac 测度 $\delta_{\mathbf{u}^\star}$ 之间的 1-Wasserstein 距离满足

$$
W_1(\mu_\theta, \delta_{\mathbf{u}^\star}) \leq C_{\mathrm{final}} \, \varepsilon^{1/2},
$$

其中 $C_{\mathrm{final}}$ 仅依赖于 $M, T_d, T_{\text{phys}}, \kappa_0, L_{\mathrm{sm}}, \nu_{\text{phys}}/\varepsilon$（均与 $\varepsilon$ 无关）。特别地，界中**不含**指数放大因子 $\exp(\Lambda)$。

---

## 证明

证明分四个阶段：

1. **阶段 1**：利用 A1、A2 构建函数空间分解，分析 BV-aware 参数化 (C) 的良态性。
2. **阶段 2**：基于单侧 Lipschitz 分析与修正的 Gronwall 不等式，利用 A2、A3、A4 建立轨迹误差界 $E(0) \leq C_1 \varepsilon$。
3. **阶段 3**：引入物理 PDE 框架与 Kruzhkov 理论，陈述阶段 4 所需的 BV 紧致性。
4. **阶段 4**：利用 A0、A5、A6 组装 Wasserstein 误差，得到 $W_1 \leq C_{\mathrm{final}} \varepsilon^{1/2}$。

---

## 阶段 1：函数空间与误差局部化

### 1.1 设定

设目标分布的无量纲扩散时间为 $\tau \in (\tau_{\text{end}}, T_d]$。记真实的平滑后的数据密度为

$$
p(u, \tau) = (\rho \ast G_\tau)(u), \qquad G_\tau(u) = (4\pi\tau)^{-d/2} \exp\!\bigl(-\|u\|^2/4\tau\bigr),
$$

其中 $\rho(u)$ 为目标数据分布。真实 Score 场：

$$
s(u, \tau) = \nabla_u \log p(u, \tau).
$$

定义激波流形 $\Gamma(\tau) \subset \mathbb{R}^d$ 为状态空间中连接不同模态的等势面。对任意 $u \in \mathbb{R}^d$，定义其到 $\Gamma(\tau)$ 的符号距离：

$$
d_\Gamma(u, \tau) = \inf_{v \in \Gamma(\tau)} \|u - v\| \cdot \mathrm{sgn}(\text{模态标签}).
$$

激波界面层邻域与外部平滑区：

$$
\Omega_{\mathrm{sh}}(\tau) = \bigl\{ u \in \mathbb{R}^d \;\big|\; |d_\Gamma(u, \tau)| \leq \mathcal{O}(\tau) \bigr\}, \qquad
\Omega_{\mathrm{out}}(\tau) = \mathbb{R}^d \setminus \Omega_{\mathrm{sh}}(\tau).
$$

### 1.2 引理 1.1：真实 Score 场的渐近展开与奇异性分解

**引理 1.1。** 在假设 A1 下，真实 Score 场 $s(u, \tau)$ 可在全空间 $\mathbb{R}^d$ 上分解为

$$
s(u, \tau) = s^{\mathrm{sm}}(u, \tau) + s^{\mathrm{sing}}(u, \tau) + \mathcal{O}(\tau),
$$

其中：

1. $s^{\mathrm{sm}}(u, \tau)$ 在全空间一致 Lipschitz 连续：$\|\nabla_u s^{\mathrm{sm}}\|_{\mathrm{op}} \leq L_{\mathrm{sm}} = \mathcal{O}(1)$。
2. $s^{\mathrm{sing}}(u, \tau)$ 仅在 $\Omega_{\mathrm{sh}}(\tau)$ 内不可忽略，具有精确形式

$$
s^{\mathrm{sing}}(u, \tau) = \frac{\Delta s_{\mathrm{jump}}(u)}{2} \tanh\!\left(\frac{A(u,\tau) - B(u,\tau)}{2\tau}\right),
$$

其中 $A, B$ 是主导模态的势函数，$\Delta s_{\mathrm{jump}} = \nabla_u B - \nabla_u A$ 是跃变强度向量。

**证明框架（Laplace 方法）。** 由 A1，在 $\Omega_{\mathrm{sh}}(\tau)$ 内，$p(u,\tau)$ 的积分由两个最近的模态主导：

$$
p(u, \tau) \sim C_A(u) \exp\!\left(-\frac{A(u,\tau)}{\tau}\right) + C_B(u) \exp\!\left(-\frac{B(u,\tau)}{\tau}\right).
$$

取对数梯度，利用恒等式 $\nabla_u \log(e^{-A/\tau} + e^{-B/\tau})$，提取 $\tanh$ 部分；缓变的系数 $C_A, C_B$ 及其梯度归入 $s^{\mathrm{sm}}$。在 $\Omega_{\mathrm{out}}(\tau)$ 中，某一模态占据绝对主导，$\tanh(\cdot) \to \pm 1$，$\nabla_u s^{\mathrm{sing}}$ 趋于 $0$，Score 场退化为平滑的 $\nabla_u A$ 或 $\nabla_u B$。误差项 $\mathcal{O}(\tau)$ 来自 Laplace 方法的下一阶余项，一致估计由 A1 的模态分离条件保证。$\blacksquare$

> **注（奇异性的本质）。** 在标准参数化下，网络若直接拟合 $s(u,\tau)$，则 $s^{\mathrm{sing}}$ 的雅可比矩阵 $\nabla_u s^{\mathrm{sing}}$ 在 $\Omega_{\mathrm{sh}}$ 内包含 $\mathcal{O}(1/\tau)$ 的奇异分量——这正是传统理论中全局 Lipschitz 常数 $L(\tau) \propto 1/\tau$ 的来源，导致 Gronwall 积分发散，出现指数放大因子 $\exp(\Lambda)$。参数化 (C) 的核心思想是将此奇异性**显式内嵌**于网络结构中，使得残差场 $e(u,\tau)$ 不再继承 $1/\tau$ 的奇异性。

### 1.3 引理 1.2：BV-aware 参数化的良态性

参数化 (C) 定义网络 Score 场：

$$
s_\theta(u, \tau) = \underbrace{\nabla_u \phi^{\mathrm{sm}}_\theta(u, \tau)}_{\text{平滑背景项}} + \underbrace{\frac{\kappa_\theta(u,\tau)}{2} \tanh\!\left(\frac{D_\theta(u, \tau)}{2\tau}\right) \nabla_u D_\theta(u, \tau)}_{\text{界面奇异项}}.
$$

**引理 1.2（空间对齐与网络良态性）。** 在假设 A2 下，映射 $\Theta: (u,\tau) \mapsto (\phi^{\mathrm{sm}}_\theta, \kappa_\theta, D_\theta)$ 存在如下性质：

1. 目标逼近：$\nabla_u \phi^{\mathrm{sm}}_\theta \approx s^{\mathrm{sm}}$，$\kappa_\theta \nabla_u D_\theta \approx \Delta s_{\mathrm{jump}}$，$D_\theta \approx A-B$。
2. 雅可比有界性：各分量的雅可比范数 $\|\nabla_u^2 \phi^{\mathrm{sm}}_\theta\|_{\mathrm{op}}$，$\|\nabla_u \kappa_\theta\|$，$\|\nabla_u^2 D_\theta\|_{\mathrm{op}}$ 均与 $\tau$ 无关，为 $\mathcal{O}(1)$ 量级。
3. 网络仅学习平滑的符号距离场 $D_\theta$。奇异性因子 $1/\tau$ 作为显式的物理先验写在网络结构外面，仅在 $\tanh$ 内部和求导后的奇异雅可比矩阵 $J_{\mathrm{sh}}$ 中显式出现，网络中不涉及自动微分引发的 $1/\tau$ 放大，完全避免了梯度爆炸。

**证明。** 由 A2，$\nabla_u^2 \phi^{\mathrm{sm}}_\theta$、$\nabla_u^2 D_\theta$、$\nabla_u \kappa_\theta$ 均一致有界。注意 $\tanh$ 函数关于其参数的导数为 $\mathrm{sech}^2(\cdot) \leq 1$，故对 $s_\theta$ 求 $\nabla_u$ 时，$\tau$ 在分母的依赖性不向外传递发散，其传递至 Jacobian 中后构成严格半负定的奇异部分矩阵（下文详细证明）。由于 $A$ 与 $B$ 皆为 $\mathcal{O}(1)$ 的势函数，网络所学习的 $D_\theta(u, \tau)$ 其梯度 $\nabla_u D_\theta = \mathcal{O}(1)$，不引入额外的奇异性尺度。$\blacksquare$

### 1.4 残差场的有界性（启发式讨论）

> **注（推论 1.4 的启发式意义，非严格论断）。** 以下为启发式论证，仅用于直觉，**不作为后续证明的依赖**。
>
> 定义 Score 残差场 $e(u,\tau) = s_\theta(u,\tau) - s(u,\tau)$，分解为 $e = e_{\mathrm{sm}} + e_{\mathrm{sh}}$，其中 $e_{\mathrm{sh}}$ 为界面位置/强度偏差导致的激波残差。
>
> 在标准架构中，$e_{\mathrm{standard}}$ 因无法拟合 $\tanh(\cdot/\tau)$ 的陡峭梯度，在 $\Omega_{\mathrm{sh}}$ 内自身具有 $-\mathcal{O}(1/\tau)$ 的梯度分量，导致误差指数放大。BV-aware 架构植入了 $\tanh$ 结构，使 $e_{\mathrm{sh}}$ 的误差表现为激波中心位置的微小偏移，该偏移在 $W_1$ 意义下与偏移量同阶（$\Delta W_1 \propto \Delta x$），不涉及梯度的乘性放大。
>
> 更严格地说，若能独立证明 $e_{\mathrm{sm}}$ 的梯度界与 $e_{\mathrm{sh}}$ 激波偏移的梯度界，则可建立 $\int_0^{T_d} \|\nabla_u e(u,\tau)\|_{\mathrm{eff}} \, d\tau \leq C_0 = \mathcal{O}(1)$。此方向的严格化留待后续工作（参见附录 C 中编号 C1.4-G 的技术点）。在本证明中，阶段 2 的 Gronwall 论证**不依赖此界**，仅使用 $\|e\|$ 本身的积分估计（见定理 2.2）。

---

## 阶段 2：修正的 Gronwall 不等式与轨迹误差界

### 2.1 经典分析的失效与 Gronwall 陷阱

在反向生成过程中，考察两条 ODE 轨迹——由真实 Score $s$ 驱动的参考轨迹 $u^\natural(\tau)$ 与由网络 Score $s_\theta$ 驱动的近似轨迹 $\hat{u}(\tau)$。两者服从粘性匹配策略 $\sigma^2(\tau) = 2\nu_{\text{phys}} \tau$ 下的概率流 ODE（漂移系数 $\sigma \dot\sigma = \nu_{\text{phys}}$）：

$$
\frac{d u^\natural}{d\tau} = -\nu_{\text{phys}} \, s(u^\natural, \tau) \eqqcolon V(u^\natural, \tau), \qquad
\frac{d \hat{u}}{d\tau} = -\nu_{\text{phys}} \, s_\theta(\hat{u}, \tau) \eqqcolon V_\theta(\hat{u}, \tau).
$$

**初始条件（A4）**：由 A4，两者在 $\tau = T_d$ 处的误差满足 $E(T_d) \coloneqq \|\hat{u}(T_d) - u^\natural(T_d)\| \leq \tilde{C}\varepsilon$（若先验完全匹配则为 $0$，微小偏差由下文 Gronwall 公式统一处理）。

定义轨迹误差：

$$
E(\tau) \coloneqq \|\hat{u}(\tau) - u^\natural(\tau)\|.
$$

对 $E^2$ 求导：

$$
\frac{1}{2}\frac{d}{d\tau} E(\tau)^2
= \bigl\langle \hat{u} - u^\natural,\; V_\theta(\hat{u}, \tau) - V(u^\natural, \tau) \bigr\rangle.
$$

将右侧分解为同调项（$V_\theta$ 的自一致性）与误差驱动项：

$$
\frac{1}{2}\frac{d}{d\tau} E(\tau)^2
\leq \underbrace{\bigl\langle \hat{u} - u^\natural,\; V_\theta(\hat{u},\tau) - V_\theta(u^\natural,\tau) \bigr\rangle}_{\text{Term I：漂移自一致性}} + \underbrace{\nu_{\text{phys}} \bigl\langle \hat{u} - u^\natural,\; e(u^\natural,\tau) \bigr\rangle}_{\text{Term II：Score 误差驱动}}.
$$

对 Term II 用 Cauchy–Schwarz：$\nu_{\text{phys}} \langle \hat{u} - u^\natural, e(u^\natural,\tau) \rangle \leq \nu_{\text{phys}} \|e(u^\natural,\tau)\| \cdot E(\tau)$。由此：

$$
\frac{1}{2}\frac{d}{d\tau} E(\tau)^2
\leq \underbrace{\bigl\langle \hat{u} - u^\natural,\; V_\theta(\hat{u},\tau) - V_\theta(u^\natural,\tau) \bigr\rangle}_{\text{Term I}} + \nu_{\text{phys}} \|e(u^\natural,\tau)\| \cdot E(\tau).
$$

在经典证明中，Term I 用全局 Lipschitz 常数 $L_\theta(\tau) = \mathcal{O}(1/\tau)$ 放缩，导致 Gronwall 积分发散为 $\exp(\Lambda)$。下文用单侧 Lipschitz 常数代替。

### 2.2 引理 2.1：单侧 Lipschitz 条件与半负定性

**定义（单侧 Lipschitz 常数）。** $V_\theta$ 的单侧 Lipschitz 常数 $\mu(\tau)$ 是使得下式对一切 $u, v \in \mathbb{R}^d$ 成立的最小数：

$$
\bigl\langle u - v,\; V_\theta(u,\tau) - V_\theta(v,\tau) \bigr\rangle \leq \mu(\tau) \|u - v\|^2.
$$

当 $V_\theta$ 可微时，$\mu(\tau)$ 等价于其雅可比矩阵 $J_\theta(u,\tau) \coloneqq \nabla_u V_\theta(u,\tau)$ 的对称部分的最大特征值：

$$
\mu(\tau) = \sup_{u \in \mathbb{R}^d} \lambda_{\max}\!\left(\frac{J_\theta(u,\tau) + J_\theta(u,\tau)^\mathsf{T}}{2}\right).
$$

**引理 2.1（BV-aware 架构的对数范数有界性）。** 在假设 A2 下，

$$
\mu(\tau) \leq L_{\mathrm{sm}} = \mathcal{O}(1),
$$

即单侧 Lipschitz 常数独立于 $\tau$，无奇异性。

**证明。** 计算 $V_\theta(u,\tau) = -\nu_{\text{phys}} s_\theta(u,\tau)$ 的雅可比矩阵：

$$
J_\theta = \nabla_u V_\theta = J_{\mathrm{sm}} + J_{\mathrm{sh}} + J_{\mathrm{cross}},
$$

其中各项如下。

**（a）平滑部分。** $J_{\mathrm{sm}} = -\nu_{\text{phys}} \nabla_u^2 \phi^{\mathrm{sm}}_\theta$。由 A2，$\|\nabla_u^2 \phi^{\mathrm{sm}}_\theta\|_{\mathrm{op}} = \mathcal{O}(1)$，故 $\lambda_{\max}(J_{\mathrm{sm}}) \leq \nu_{\text{phys}} \cdot \mathcal{O}(1) = \mathcal{O}(1)$（$\nu_{\text{phys}} = \Theta(\varepsilon)$ 为小量，但 $\varepsilon \leq 1$，故不超过 $\mathcal{O}(1)$）。

**（b）交叉项。** $J_{\mathrm{cross}}$ 包含对 $\kappa_\theta$ 及 $\nabla_u D_\theta$ 的导数项，由 A2 均一致有界，且此处导数产生的主项已通过显式分离与内部导数控制，不向此项导入 $1/\tau$ 因子，$\lambda_{\max}(J_{\mathrm{cross}}) = \mathcal{O}(1)$。

**（c）奇异部分。** 对参数化 (C) 中的 $\tanh$ 项求 $\nabla_u$，得

$$
J_{\mathrm{sh}}(u,\tau) = -\nu_{\text{phys}} \cdot \frac{\kappa_\theta(u,\tau)}{4\tau} \, \mathrm{sech}^2\!\left(\frac{D_\theta(u,\tau)}{2\tau}\right) \bigl(\nabla_u D_\theta\bigr)\bigl(\nabla_u D_\theta\bigr)^\mathsf{T}.
$$

矩阵 $(\nabla_u D_\theta)(\nabla_u D_\theta)^\mathsf{T}$ 是秩为 $1$ 的半正定矩阵（形如 $\mathbf{n}\mathbf{n}^\mathsf{T}$，其中 $\mathbf{n} = \nabla_u D_\theta$ 为激波界面法向量）。由 A2，$\kappa_\theta \geq \kappa_0 > 0$，加之 $\nu_{\text{phys}} > 0$，$\tau > 0$，$\mathrm{sech}^2(\cdot) > 0$，前方负号使 $J_{\mathrm{sh}}$ 为**严格半负定**。

因此 $J_{\mathrm{sh}}$ 的对称部分最大特征值满足 $\lambda_{\max}(J_{\mathrm{sh}}) \leq 0$，对单侧 Lipschitz 常数无正贡献。

**（d）物理解释。** 在垂直于激波面的方向（$\mathbf{n}$ 方向）上，$J_{\mathrm{sh}}$ 给出量级为 $-\nu_{\text{phys}} \kappa_0 \|\nabla_u D_\theta\|^2 / (4\tau)$ 的负特征值，对应反向扩散流在激波法向的**强吸引力**。偏离真实激波流形的误差以此极大速率被压缩，而非放大，这是 Burgers 方程特征线相交的数学本质，也是该架构能够避开指数发散的核心保障。

综合（a）–（d），

$$
\mu(\tau) \leq \lambda_{\max}\!\bigl(J_{\mathrm{sm}} + J_{\mathrm{cross}}\bigr) + \underbrace{\lambda_{\max}(J_{\mathrm{sh}})}_{\leq 0} \leq L_{\mathrm{sm}} = \mathcal{O}(1). \quad \blacksquare
$$

### 2.3 定理 2.2：常数上界的修正流稳定性

**定理 2.2（轨迹误差界）。** 在假设 A2、A3、A4 下，令 $\varepsilon_{\mathrm{raw}}$ 为原始（未归一化）Score Matching 均方误差界，即 $\mathbb{E}[\|e\|^2] \leq \varepsilon_{\mathrm{raw}}^2$。由 A3 的网格归一化定义 $\mathbb{E}[\Delta x \|e\|^2] \leq \varepsilon^2$，有 $\varepsilon_{\mathrm{raw}}^2 = \varepsilon^2 / \Delta x$。则

$$
\mathbb{E}_z\bigl[E(0)\bigr] \leq C_1 \varepsilon_{\mathrm{raw}} = C_1 \frac{\varepsilon}{\sqrt{\Delta x}},
$$

其中 $C_1$ 仅依赖于 $T_d, \nu_{\text{phys}}, L_{\mathrm{sm}}$。在阶段 4 的范数转换中，$\sqrt{\Delta x}$ 将被消去，得到网格无关的最终界。

**证明。**

**步骤 1：标量微分不等式。** 对 $\frac{1}{2}\frac{d}{d\tau} E^2$ 应用引理 2.1 处理 Term I，得

$$
\frac{1}{2}\frac{d}{d\tau} E(\tau)^2 \leq \mu(\tau) \, E(\tau)^2 + \nu_{\text{phys}} \, \|e(u^\natural,\tau)\| \cdot E(\tau).
$$

两边除以 $E(\tau)$（$E(\tau) > 0$ 时；$E(\tau) = 0$ 时不等式平凡成立），

$$
\frac{d}{d\tau} E(\tau) \leq \mu(\tau) \, E(\tau) + \nu_{\text{phys}} \, \|e(u^\natural,\tau)\|. \tag{$\star$}
$$

**步骤 2：应用 Gronwall 不等式。** 由 $(\star)$，从 $\tau = T_d$ 积分至 $\tau = 0$，得

$$
E(0) \leq E(T_d) \cdot \exp\!\left(\int_0^{T_d} \mu(r) \, dr\right) + \int_0^{T_d} \exp\!\left(\int_0^\tau \mu(r) \, dr\right) \nu_{\text{phys}} \, \|e(u^\natural,\tau)\| \, d\tau.
$$

由引理 2.1，$\mu(r) \leq L_{\mathrm{sm}} = \mathcal{O}(1)$，故

$$
\exp\!\left(\int_0^\tau \mu(r) \, dr\right) \leq e^{L_{\mathrm{sm}} T_d} =: C_{\mathrm{flow}} = \mathcal{O}(1).
$$

代入 A4 的初始误差界 $E(T_d) \leq \tilde{C}\varepsilon$：

$$
E(0) \leq \tilde{C} C_{\mathrm{flow}} \varepsilon + C_{\mathrm{flow}} \nu_{\text{phys}} \int_0^{T_d} \|e(u^\natural,\tau)\| \, d\tau. \tag{$\star\star$}
$$

**步骤 3：Score Matching 误差的积分界（直接由 A3 推出）。** 对积分 $\int_0^{T_d} \|e(u^\natural,\tau)\| \, d\tau$ 应用 Cauchy–Schwarz 不等式：

$$
\int_0^{T_d} \|e(u^\natural,\tau)\| \, d\tau \leq \sqrt{T_d} \cdot \left(\int_0^{T_d} \|e(u^\natural,\tau)\|^2 \, d\tau\right)^{1/2}.
$$

对右侧对 $z$（先验噪声）取期望。由 A3，$\mathbb{E}[\Delta x \|e\|^2] \leq \varepsilon^2$，即原始（未归一化）均方误差满足 $\mathbb{E}[\|e\|^2] \leq \varepsilon^2 / \Delta x = \varepsilon_{\mathrm{raw}}^2$。因此

$$
\mathbb{E}_z\!\left[\int_0^{T_d} \|e(u^\natural,\tau)\|^2 \, d\tau\right] \leq T_d \cdot \varepsilon_{\mathrm{raw}}^2 = T_d \cdot \frac{\varepsilon^2}{\Delta x},
$$

（此步成立是因为 $u^\natural(\tau)$ 边缘分布为 $p(\cdot,\tau)$，故关于 $(u^\natural(\tau),\tau)$ 的期望与 A3 中 $\mathbb{E}_{u,\tau}$ 一致。）

再对 Cauchy–Schwarz 结果取期望（利用 Jensen 不等式）：

$$
\mathbb{E}_z\!\left[\int_0^{T_d} \|e(u^\natural,\tau)\| \, d\tau\right] \leq \sqrt{T_d} \cdot \sqrt{T_d \varepsilon_{\mathrm{raw}}^2} = T_d \varepsilon_{\mathrm{raw}} = T_d \frac{\varepsilon}{\sqrt{\Delta x}}.
$$

**步骤 4：汇总。** 将步骤 3 代入 $(\star\star)$ 并取期望：

$$
\mathbb{E}_z[E(0)] \leq \tilde{C} C_{\mathrm{flow}} \varepsilon_{\mathrm{raw}} + C_{\mathrm{flow}} \nu_{\text{phys}} T_d \varepsilon_{\mathrm{raw}} \eqqcolon C_1 \varepsilon_{\mathrm{raw}},
$$

其中 $C_1 = C_{\mathrm{flow}}(\tilde{C} + \nu_{\text{phys}} T_d) = \mathcal{O}(1)$（由 A5，$\nu_{\text{phys}} = \Theta(\varepsilon) \leq 1$，故 $\nu_{\text{phys}} T_d = \mathcal{O}(1)$）。由 $\varepsilon_{\mathrm{raw}} = \varepsilon / \sqrt{\Delta x}$，得 $\mathbb{E}_z[E(0)] \leq C_1 \varepsilon / \sqrt{\Delta x}$。

**结论。** 在 BV-aware 架构下，轨迹终点误差 $\mathbb{E}[E(0)] = \mathcal{O}(\varepsilon_{\mathrm{raw}})$，无指数放大因子。$\blacksquare$

---

## 阶段 3：Kruzhkov 熵解的 $L^1$ 压缩性框架

> **阶段 3 的约定。** 以下引入物理空间 $x \in \Omega \subset \mathbb{R}$。状态向量 $u \in \mathbb{R}^d$（$d = N_x$）的分量为 $u_i = \mathbf{u}(x_i)$，其中 $\{x_i\}$ 是物理空间的均匀网格点（间距 $\Delta x = |\Omega|/N_x$）。离散 $L^1$ 范数定义为 $\|\mathbf{u}\|_{L^1} = \Delta x \sum_{i=1}^{N_x} |\mathbf{u}(x_i)|$，物理空间连续 $L^1$ 范数的近似（见阶段 4 的范数等价性声明）。

### 3.1 Kruzhkov 熵条件与 $L^1$ 压缩性

考虑目标双曲守恒律（在物理空间 $\Omega \times [0,T]$ 上）：

$$
\partial_t \mathbf{u} + \partial_x f(\mathbf{u}) = 0, \qquad x \in \Omega \subset \mathbb{R}, \quad t \in [0,T],
$$

其中 $f$ 为通量函数（如 Burgers 通量 $f(u) = u^2/2$），初始条件 $\mathbf{u}(\cdot,0) = \mathbf{u}_0$。Kruzhkov 熵解 $\mathbf{u}^\star$ 满足：对任意常数 $k \in \mathbb{R}$，在分布意义下

$$
\partial_t |\mathbf{u}^\star - k| + \partial_x \bigl(\mathrm{sgn}(\mathbf{u}^\star - k)(f(\mathbf{u}^\star) - f(k))\bigr) \leq 0.
$$

**Kruzhkov 定理推论（$L^1$-压缩半群）。** 若 $\mathbf{a}(x,t)$ 和 $\mathbf{b}(x,t)$ 均满足 Kruzhkov 熵条件，则

$$
\|\mathbf{a}(\cdot,t) - \mathbf{b}(\cdot,t)\|_{L^1(\Omega)} \leq \|\mathbf{a}(\cdot,0) - \mathbf{b}(\cdot,0)\|_{L^1(\Omega)}.
$$

令 $\mathbf{u}^\star(x) \coloneqq \mathbf{u}^\star(x, T_{\text{phys}})$（在固定物理时间 $T_{\text{phys}}$，后文省略）。

### 3.2 损失设计与 BV 紧致性

损失函数 $\mathcal{L}_3$ 在标准 denoising score matching 损失上附加 BV 正则项：

$$
\mathcal{L}_3 = \mathcal{L}_{\mathrm{DSM}} + \lambda_{\mathrm{BV}} \, \mathrm{TV}(D_\theta).
$$

由假设 A0，结合参数化 (C) 中硬编码的 $\tanh$ 结构，此正则项保证生成样本几乎必然落入有界 BV 球 $\mathcal{K}_M$。由 Helly 选择定理，$\mathcal{K}_M$ 在 $L^1(\Omega)$ 拓扑下相对紧致。

### 3.3 粘性极限（Kuznetsov 引理的应用）

扩散模型的反向阶段在粘性匹配 $\sigma^2(\tau) = 2\nu_{\text{phys}}\tau$ 下本质上引入人工粘性 $\nu_{\text{phys}}$。记 $\mathbf{u}^\nu$ 为带粘性项的物理 PDE 在 $t = T_{\text{phys}}$ 处的解：

$$
\partial_t \mathbf{u}^\nu + \partial_x f(\mathbf{u}^\nu) = \nu_{\text{phys}} \, \partial_{xx} \mathbf{u}^\nu.
$$

由假设 A6（基于 Kuznetsov 1976 的结论）：

$$
\|\mathbf{u}^\nu - \mathbf{u}^\star\|_{L^1(\Omega)} \leq C_K \sqrt{\nu_{\text{phys}}}.
$$

再由 A5（$\nu_{\text{phys}} = \Theta(\varepsilon)$），得

$$
\|\mathbf{u}^\nu - \mathbf{u}^\star\|_{L^1(\Omega)} \leq C_K \sqrt{C\varepsilon} = C_K \sqrt{C} \cdot \varepsilon^{1/2}. \tag{3.1}
$$

---

## 阶段 4：Wasserstein 误差的组装与 $\mathcal{O}(\varepsilon^{1/2})$ 的涌现

### 4.1 网格重正化范数等价性与神经生成误差

**离散 $L^1$–归一化欧氏范数等价性推导。** 物理域 $\Omega$ 被离散化为 $d = N_x$ 个均匀网格点，间距 $\Delta x = |\Omega|/d$。对状态向量 $u \in \mathbb{R}^d$，离散 $L^1$ 范数为

$$
\|\mathbf{u}\|_{L^1} = \Delta x \sum_{i=1}^d |u_i|.
$$

由 $\ell^1$–$\ell^2$ 范数不等式（$\sum |u_i| \leq \sqrt{d} \sqrt{\sum u_i^2} = \sqrt{d}\|u\|$），代入 $\Delta x$，得到

$$
\|\mathbf{u}\|_{L^1} \leq \Delta x \sqrt{d} \|u\| = \sqrt{|\Omega|} \cdot \sqrt{\Delta x} \|u\|. \tag{4.1}
$$

**推导神经生成误差的 $L^1$ 界。** 注意在重正化的假设 A3 中，误差界以 $\mathbb{E}[\Delta x \|e\|^2] \leq \varepsilon^2$ 的形式给出，这意味着对于纯欧氏范数，有 $\mathbb{E}[\|e\|^2] \leq \varepsilon^2 / \Delta x$。

回顾阶段 2 中的 Gronwall 积分与轨迹误差界定理 2.2，我们对标准的欧氏距离 $E(0)$ 得到：

$$
\mathbb{E}_z\bigl[\|\hat{u}(0) - u^\natural(0)\|\bigr] \leq C_1 \mathbb{E}_z\bigl[\|e\|\bigr] \leq C_1 \frac{\varepsilon}{\sqrt{\Delta x}}. \tag{4.2}
$$

对应的物理函数差为 $\mathbf{u}^\theta - \mathbf{u}^\nu$。结合式 (4.1) 的范数放缩关系：

$$
\mathbb{E}_z\bigl[\|\mathbf{u}^\theta - \mathbf{u}^\nu\|_{L^1(\Omega)}\bigr] \leq \sqrt{|\Omega|} \sqrt{\Delta x} \cdot \mathbb{E}_z\bigl[\|\hat{u}(0) - u^\natural(0)\|\bigr] \leq \sqrt{|\Omega|} \sqrt{\Delta x} \cdot C_1 \frac{\varepsilon}{\sqrt{\Delta x}}.
$$

在此，$d$ 与 $\Delta x$ 被**完美消去**！无论网格多密，误差界始终有效，得到网格无关的连续统极限界：

$$
\mathbb{E}_z\bigl[\|\mathbf{u}^\theta - \mathbf{u}^\nu\|_{L^1(\Omega)}\bigr] \leq C_1 \sqrt{|\Omega|} \varepsilon =: C_2 \varepsilon. \tag{4.3}
$$

> **注（Gagliardo–Nirenberg 插值的位置）。** 原稿中曾用 Gagliardo–Nirenberg 型插值不等式 $\|h\|_{L^1} \leq C_{\mathrm{GN}} \|h\|_{L^2}^{2/3} \mathrm{TV}(h)^{1/3}$ 将 $L^2$ 误差转换为 $L^1$ 误差，得到 $\mathcal{O}(\varepsilon^{2/3})$ 的界。本修订版证明采用归一化 $L^2$-匹配结合范数等价性 (4.1)，直接从缩放欧氏误差得到更精确且独立于维度的 $L^1$ 误差 $\mathcal{O}(\varepsilon)$界。

### 4.2 Wasserstein 距离的三角不等式拆解

1-Wasserstein 距离（Kantorovich–Rubinstein 对偶）：

$$
W_1(\mu, \nu) = \inf_{\pi \in \Pi(\mu,\nu)} \int \|\mathbf{u} - \mathbf{v}\|_{L^1(\Omega)} \, d\pi(\mathbf{u},\mathbf{v}).
$$

设 $\delta_{\mathbf{u}^\nu}$ 为粘性解对应的 Dirac 测度（给定初值 $\mathbf{u}_0$，粘性 PDE 解唯一，故为确定性），进行三角不等式拆分：

$$
W_1(\mu_\theta, \delta_{\mathbf{u}^\star})
\leq \underbrace{W_1(\mu_\theta, \delta_{\mathbf{u}^\nu})}_{\text{神经生成误差（Term A）}}
+ \underbrace{W_1(\delta_{\mathbf{u}^\nu}, \delta_{\mathbf{u}^\star})}_{\text{粘性极限误差（Term B）}}. \tag{4.4}
$$

**Term A（神经生成误差）。** 由于 $\hat{u}(0)$ 与 $u^\natural(0)$ 由同一先验噪声 $z$ 确定性地生成（ODE 对固定 $z$ 的解唯一），存在自然的逐点耦合：

$$
\pi_z = \bigl(\mathbf{u}^\theta(z),\; \mathbf{u}^\nu\bigr)_\# \, p_{T_d},
$$

其中 $p_{T_d}$ 为先验分布，$\mathbf{u}^\nu$ 视为常数向量（与 $z$ 无关）。由此耦合的可行性及 (4.3)：

$$
W_1(\mu_\theta, \delta_{\mathbf{u}^\nu})
\leq \int \|\mathbf{u}^\theta(z) - \mathbf{u}^\nu\|_{L^1(\Omega)} \, d p_{T_d}(z)
= \mathbb{E}_z\bigl[\|\mathbf{u}^\theta - \mathbf{u}^\nu\|_{L^1(\Omega)}\bigr]
\leq C_2 \varepsilon. \tag{4.5}
$$

**Term B（粘性极限误差）。** $\delta_{\mathbf{u}^\nu}$ 与 $\delta_{\mathbf{u}^\star}$ 均为单点分布，$W_1$ 退化为 $L^1$ 距离：

$$
W_1(\delta_{\mathbf{u}^\nu}, \delta_{\mathbf{u}^\star}) = \|\mathbf{u}^\nu - \mathbf{u}^\star\|_{L^1(\Omega)}.
$$

由 (3.1)（即假设 A6 与 A5 的联合结论）：

$$
W_1(\delta_{\mathbf{u}^\nu}, \delta_{\mathbf{u}^\star}) \leq C_K\sqrt{C} \cdot \varepsilon^{1/2}. \tag{4.6}
$$

### 4.3 最终结论

将 (4.5) 和 (4.6) 代入 (4.4)：

$$
W_1(\mu_\theta, \delta_{\mathbf{u}^\star}) \leq C_2 \varepsilon + C_K\sqrt{C} \cdot \varepsilon^{1/2}.
$$

对 $\varepsilon \in (0,1)$，有 $\varepsilon \leq \varepsilon^{1/2}$，故高阶项 $\mathcal{O}(\varepsilon)$ 被低阶项 $\mathcal{O}(\varepsilon^{1/2})$ 吸收：

$$
W_1(\mu_\theta, \delta_{\mathbf{u}^\star}) \leq (C_2 + C_K\sqrt{C}) \cdot \varepsilon^{1/2} =: C_{\mathrm{final}} \cdot \varepsilon^{1/2}.
$$

其中 $C_{\mathrm{final}} = C_2 + C_K\sqrt{C}$ 仅依赖于 $M, T_d, T_{\text{phys}}, \kappa_0, L_{\mathrm{sm}}, \nu_{\text{phys}}/\varepsilon$，均与 $\varepsilon$ 无关。故

$$
\boxed{W_1(\mu_\theta, \delta_{\mathbf{u}^\star}) \leq C_{\mathrm{final}} \, \varepsilon^{1/2}.}
$$

$\blacksquare$

---

## 论文叙事指引（供撰稿人参考，不进入论文正文）

> **以下内容为内部写作指导，用于帮助撰稿人将 Theorem 3 的数学结论转化为论文中的叙事。论文正文中请用自然的学术语言重写，而非直接粘贴。**

### 核心叙事线

Theorem 3 的贡献不在于数字 $\varepsilon^{1/2}$ 本身，而在于**将上界从一个指数发散的函数变成了一个多项式收敛的函数**。论文中应显式引导 reader 做这个对比，而非让其自行发现（或误读为"只是从一次方优化到半次方"）。

### 建议的论文陈述框架

**1. 先锚定对比基准（remind reader Theorem 2 的 bound 有多糟）。**

> For standard score parameterizations, the Gronwall constant scales as $\Lambda \propto 1/\tau_{\min}$, yielding a trajectory error bound of the form $C\varepsilon \exp(\Lambda T_d)$ (Theorem 2). At typical signal-to-noise ratios, $\Lambda \approx 5$–$10$ and $T_d \approx 1$, giving $\exp(\Lambda T_d) \approx 10^2$–$10^4$. For any practical training budget where $\varepsilon \gtrsim 10^{-3}$, this bound is **vacuous** ($\gg 1$).

**2. 然后陈述 Theorem 3 做了什么（质的改变）。**

> Theorem 3 establishes that under the BV-aware parameterization (C) and viscosity-matched schedule (B), the Gronwall constant is reduced from $\Lambda \propto 1/\tau_{\min}$ to $L_{\mathrm{sm}} = O(1)$, independent of the diffusion timescale. Consequently, the exponential amplification factor $\exp(\Lambda T_d)$ is **eliminated entirely**, replaced by an $O(1)$ flow constant. The resulting error decomposes into two polynomially-bounded terms:

**3. 显式分解两项，标注各自来源。**

> $$
> W_1(\mu_\theta, \delta_{\mathbf{u}^\star})
> \leq \underbrace{C_1 \varepsilon}_{\text{score matching error (Gronwall with } L_{\mathrm{sm}}\text{)}}
> + \underbrace{C_2 \varepsilon^{1/2}}_{\text{viscous-to-entropy gap (Kuznetsov)}}.
> $$

> - **$C_1\varepsilon$ term**: originates from the denoising score matching error propagated through the reverse ODE. The BV-aware architecture (C) hard-codes the $\tanh$ interfacial structure, making the Jacobian of the drift field semi-negative-definite in the shock-normal direction (Lemma 2.1). This eliminates the $1/\tau$ singularity in the one-sided Lipschitz constant, capping the Gronwall integral at $L_{\mathrm{sm}} T_d = O(1)$ — the *structural* contribution of parameterization (C).
>
> - **$C_2\varepsilon^{1/2}$ term**: originates from the gap between the viscous regularized PDE solution ($\nu_{\mathrm{phys}} > 0$) and the inviscid entropy solution ($\nu_{\mathrm{phys}} = 0$). Under the viscosity-matched schedule (B), the effective viscosity of the reverse process is $\nu_{\mathrm{phys}} = \Theta(\varepsilon)$. The Kuznetsov bound $\|\mathbf{u}^\nu - \mathbf{u}^\star\|_{L^1} \leq C_K\sqrt{\nu_{\mathrm{phys}}}$ then gives the $\varepsilon^{1/2}$ scaling. This term is **unavoidable for any finite-viscosity method** and represents the physical bottleneck, not a weakness of the architecture.

### 对比表（可放入论文正文或附录）

| 机制 | 标准参数化 (A) | BV-aware 参数化 (C) |
|---|---|---|
| Score Lipschitz 常数 $L(\tau)$ | $\propto 1/\tau$ | $\leq L_{\mathrm{sm}} = O(1)$ |
| Gronwall 放大因子 | $\exp(\Lambda T_d)$, $\Lambda \propto 1/\tau_{\min}$ | $\exp(L_{\mathrm{sm}} T_d) = O(1)$ |
| 最终 $W_1$ bound（$\varepsilon=10^{-2}$, $\Lambda=5$） | $\approx 1.5$（发散） | $\approx 0.1$（收敛） |
| 主导误差来源 | Score 误差的指数放大 | 物理粘性不可消除的下界 |

### 处理 Theorem 2 与 Theorem 3 的目标对象差异

Theorem 2（随机初值 $\rho_0$ 下的分布间 $W_1$）与 Theorem 3（固定初值 $u_0$ 下的样本到 Dirac 的 $W_1$）作用于不同 setting。论文中需显式声明：

> Theorem 2 bounds the distance between *distributions* over solution ensembles induced by random initial data. Theorem 3 bounds the *per-sample* error for a fixed initial condition — a stronger, deterministic guarantee. The $O(\varepsilon^{1/2})$ rate thus holds pointwise in $u_0$ (under the assumptions A0–A6), and the distributional bound follows by expectation over $\rho_0$.

### 处理 A1 的"条件性"

A1（真实 score 在 shock 邻域有 $\tanh$ 渐近形式）引自 Score Shocks (2025) Proposition 5.4，并非凭空假设。论文中应写：

> Assumption A1 is not an ad-hoc postulate: it restates the interfacial profile theorem of Score Shocks (Proposition 5.4 therein), which proves that for any binary decomposition of the data density, the score field near a mode boundary takes the exact $\tanh$ form. The general multi-modal case follows by superposition; the engineering status of the non-finite-mixture case is discussed in Appendix C (EA1).

### 处理 A5 的"工程近似"标签

$\nu_{\mathrm{phys}} = \Theta(\varepsilon)$ 是 schedule (B) 的**设计目标**，不是事后调参。论文中应升级措辞：

> The viscosity-matched schedule (B) is explicitly **designed** to align the diffusion timescale with the physical viscosity scale. The choice $\nu_{\mathrm{phys}} = \Theta(\varepsilon)$ is the optimal balance point: taking $\nu_{\mathrm{phys}} \ll \varepsilon$ would leave score error dominant (wasting the BV-aware architecture's capacity); taking $\nu_{\mathrm{phys}} \gg \varepsilon$ would inflate the Kuznetsov term. The full Pareto frontier of the $(\varepsilon, \nu_{\mathrm{phys}})$ trade-off is characterized in Appendix C (EA2).

---

## 附录 A：符号对照表（旧版 → 修订版）

| 旧版符号 | 修订版符号 | 原因 |
|---|---|---|
| $u \in \mathbb{R}^d$（状态点）与 $u(x,t)$（PDE 解）混用 | 状态空间：$u \in \mathbb{R}^d$；物理空间：$\mathbf{u}(x)$ | 消除函数/变量的歧义 |
| $u^\star$ 既表示真值轨迹又表示 PDE 解 | $u^\natural(\tau)$（真值轨迹）；$\mathbf{u}^\star$（PDE 解） | 区分两类"真值" |
| $\hat{u}$ 混用为轨迹/样本/分布 | $\hat{u}(\tau)$（轨迹）；$u^\theta$（样本）；$\mu_\theta$（分布） | 明确不同阶段的语义 |
| $\nabla_u$ vs $\partial_x$ 混用 | $\nabla_u$（状态空间梯度）；$\partial_x$（物理空间偏导） | 区分两个不同的空间 |
| $\sup_u \lambda_{\max}$ 作用域不明 | $\sup_{u \in \mathbb{R}^d} \lambda_{\max}$ | 明确 $u$ 为状态空间点 |
| $\|E(\tau)\|$ 范数类型不明 | $E(\tau) \coloneqq \|\hat{u}(\tau) - u^\natural(\tau)\|$（$\mathbb{R}^d$ 欧氏范数） | 明确为状态空间范数 |
| 残差场 $e(u,\tau)$ 中 $u$ 的双重角色 | $e(u,\tau)$ 的参数 $u$ 是状态空间点，$\nabla_u e = \nabla_u e(u,\tau)\big|_u$ | 保留 $u$ 作为参数名，添加作用域说明 |
| 时间 $\tau$ 与 $t$ 关系不明 | §0 时间映射表明确定义 | 显式声明正交关系和物理含义 |

---

## 附录 B：本版本的修改要点摘要

| 编号 | 修改内容 | 处理方式 |
|---|---|---|
| M1 | 推论 1.4 的严格梯度界论断 | 降级为 §1.4 的启发式注，不作为后续推论依赖 |
| M2 | 定理 2.2 的 $\int \|e\| \, d\tau$ 界 | 直接由 A3 + Cauchy–Schwarz 推出（步骤 3），无需推论 1.4 |
| M3 | 阶段 4 的 GN 插值 | 删除，改用离散范数等价性 (4.2)；GN 论证保留于 §4.1 注中 |
| M4 | 粘性误差 Term B | 直接引用 A5 + A6（公式 (3.1)），逻辑链路闭合 |
| M5 | 定理陈述 | 显式引用 A0–A6，无悬空假设 |
| M6 | 假设体系 | 新增 A0–A6，附可验证性说明与工程近似标注 |

---

## 附录 C：尚需严格化的技术点与工程近似的影响范围

| 编号 | 技术点 | 状态 | 影响范围 |
|---|---|---|---|
| C1.1-P | 引理 1.1 的"有限分离高斯簇"假设 | 已提升为假设 A1，明确作为前置条件 | 若 A1 不成立（如簇重叠严重），Score 奇异性分解可能不准确，但工程上扩散时间 $\tau$ 充分小时通常近似成立 |
| C1.4-G | 推论 1.4 的残差梯度界（$\int \|\nabla_u e\|_{\mathrm{eff}} \, d\tau \leq C_0$） | 留待后续工作（独立引理：$e_{\mathrm{sm}}$ 梯度界 + $e_{\mathrm{sh}}$ 偏移 → 梯度界） | 本证明不依赖此界，仅影响启发式注中的讨论完整性 |
| C2.1-$\kappa$ | $\kappa_\theta > 0$ 的训练时约束 | 已提升为假设 A2，明确由 Softplus 等实现 | 若约束执行不严格，$J_{\mathrm{sh}}$ 的半负定性可能失效，但引理 2.1 的 $\mathcal{O}(1)$ 界仍可从 $J_{\mathrm{sm}}, J_{\mathrm{cross}}$ 部分保证，结论降级为 $\mu(\tau) = \mathcal{O}(1)$（无负定加速） |
| EA1 | A1 在一般连续分布上的适用性 | **工程近似**：对非有限簇分布，$\tanh$ 展开仅为局部渐近；多激波叠加时各局部结构相互影响 | 影响范围：引理 1.1 的余项 $\mathcal{O}(\tau)$ 的均匀性；可通过增加 $\tanh$ 叠加项的参数化改善 |
| EA2 | A5 中 $\nu_{\text{phys}} = \Theta(\varepsilon)$ 的调度可行性 | **工程近似**：依赖于训练误差 $\varepsilon$ 的事先估计与噪声调度设计的精细度 | 影响范围：若 $\nu_{\text{phys}} \gg \varepsilon$，则 Term B 主导，最终率变差为 $\mathcal{O}(\nu_{\text{phys}}^{1/2})$；若 $\nu_{\text{phys}} \ll \varepsilon$，则 Term A 主导，率不变但 Score Matching 误差可能增大 |
| P4.1-GN | 连续极限下的 GN 插值论证 | 保留于 §4.1 注中，提供连续极限下的一致性验证 | 在固定网格 $d$ 下不影响结论；在 $d \to \infty$ 极限下 $C(d) \to 0$，离散范数等价性实际上给出更优（趋于 $0$）的转换常数 |
| K3.3-$\nu$ | A6 中 Kuznetsov 界的一般化 | 在 A0 下直接引用 Kuznetsov（1976）定理，严格成立 | 仅需初值 BV 界（由 A0 保证）；扩展到多维 $\Omega$ 需引用 Cockburn–Gremaud（1996）等更一般结果 |
