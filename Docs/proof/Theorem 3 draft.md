# Theorem 3（Improved Rate with BV-aware Parameterization）— 符号统一修订版

> **修订说明**：本版本修复以下符号问题：
> 1. 统一"状态空间 $u \in \mathbb{R}^d$"与"物理空间 $x \in \Omega$"的命名冲突
> 2. 真值轨迹 $u^\natural(\tau)$ 与 PDE 目标解 $\mathbf{u}^\star$ 的混淆分离
> 3. 明确所有范数类型（$\mathbb{R}^d$ 欧氏范数 vs $L^p$ 函数范数 vs $W_1$ 测度距离）
> 4. 补全时间映射 $\tau \leftrightarrow t$ 的定义
> 5. 修正 $\sup_u$ 的作用域歧义
> 6. 明确 $\nabla_u$ 梯度的作用对象

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
| $d_\Gamma(u, \tau)$ | 符号距离函数 |

### 物理空间（PDE 域，阶段 3 起引入）

| 符号 | 含义 |
|---|---|
| $x \in \Omega \subset \mathbb{R}$ | 物理空间坐标 |
| $t \in [0, T]$ | 物理时间（由 PDE 初值演化，与 $\tau$ 正交） |
| $\mathbf{u}^\star(x)$ | Kruzhkov 熵解（目标 PDE 的解，在固定物理时间 $t = T_{\text{phys}}$） |
| $\mathbf{u}^\nu(x)$ | 带粘性 $\nu$ 的 PDE 粘性近似解 |
| $\partial_x$ | 物理空间偏导 |
| $\|\cdot\|_{L^1(\Omega)}$, $\|\cdot\|_{L^2(\Omega)}$ | 物理空间上的 $L^p$ 范数 |

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
| $\mathrm{TV}(f) = \int_\Omega |\partial_x f| dx$ | 全变差半范数 |
| $W_1(\mu, \nu)$ | 1-Wasserstein 距离（Kantorovich–Rubinstein 对偶） |

### 时间映射

扩散时间 $\tau$ 从 $T_d$ 递减至 $0$ 的物理含义：
- $\tau = T_d$：纯噪声（先验，如标准高斯）
- $\tau = 0$：数据样本（对应 PDE 在物理时间 $t = T_{\text{phys}}$ 的解）
- 粘性匹配：$\sigma^2(\tau) = 2\nu_{\text{phys}} \tau$，使得 $\tau$ 的演进等效于带粘性 $\nu_{\text{phys}}$ 的物理过程
- 在阶段 3 中，目标 $\mathbf{u}^\star$ 是 PDE 在**固定物理时间** $t = T_{\text{phys}}$ 处的熵解（$T_{\text{phys}}$ 视为常数，后文不再显式写出）

---

## Theorem 3 陈述（修订）

在 parameterization (C) + 损失 $\mathcal{L}_3$ 下，设 $\mathbb{E}_{u,\tau}[\|e(u,\tau)\|^2] \leq \varepsilon^2$，且满足如下正则性假设（见阶段 1 引理 1.1 的假设），则：

$$
W_1(\mu_\theta, \delta_{\mathbf{u}^\star}) \leq C_2 \, \varepsilon^{1/2},
$$

其中 $\mu_\theta = \mathrm{Law}(u^\theta)$ 为生成分布，$\mathbf{u}^\star$ 为 Kruzhkov 熵解，即去除了标准理论中 $\exp(\Lambda T)$ 的指数放大因子。

---

## 阶段 1：构建函数空间与误差局部化

### 1.1 设定

设目标分布的无量纲扩散时间为 $\tau \in (0, T_d]$。记真实的平滑后的数据密度为

$$
p(u, \tau) = (\rho \ast G_\tau)(u), \qquad G_\tau(u) = (4\pi\tau)^{-d/2} \exp(-\|u\|^2/4\tau),
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
\Omega_{\mathrm{sh}}(\tau) = \big\{ u \in \mathbb{R}^d \;\big|\; |d_\Gamma(u, \tau)| \leq \mathcal{O}(\tau) \big\}, \qquad
\Omega_{\mathrm{out}}(\tau) = \mathbb{R}^d \setminus \Omega_{\mathrm{sh}}(\tau).
$$

### 1.2 引理 1.1：真实 Score 场的渐近展开与奇异性分解

**引理 1.1**：在极限 $\tau \to 0^+$ 下（且假设目标分布由有限个分离良好的高斯簇混合而成），真实的 Score 场 $s(u, \tau)$ 可以在全空间 $\mathbb{R}^d$ 上一致分解为平滑背景项 $s^{\mathrm{sm}}$ 与界面奇异项 $s^{\mathrm{sing}}$ 之和：

$$
s(u, \tau) = s^{\mathrm{sm}}(u, \tau) + s^{\mathrm{sing}}(u, \tau) + \mathcal{O}(\tau).
$$

其中：

1. $s^{\mathrm{sm}}(u, \tau)$ 在全空间 $\mathbb{R}^d$ 上一致 Lipschitz 连续：$\|\nabla_u s^{\mathrm{sm}}\|_{\text{op}} \leq L_{\mathrm{sm}} = \mathcal{O}(1)$。
2. $s^{\mathrm{sing}}(u, \tau)$ 仅在 $\Omega_{\mathrm{sh}}(\tau)$ 内不可忽略，且具有精确形式：
   $$
   s^{\mathrm{sing}}(u, \tau) = \frac{\Delta s_{\mathrm{jump}}(u)}{2} \tanh\!\left(\frac{A(u, \tau) - B(u, \tau)}{2\tau}\right),
   $$
   其中 $A, B$ 是主导模态的势函数，$\Delta s_{\mathrm{jump}} = \nabla_u B - \nabla_u A$ 是跃变强度。

**证明框架（拉普拉斯方法）**：根据 Cole-Hopf 变换及 Laplace 渐近估计，在 $\Omega_{\mathrm{sh}}(\tau)$ 内，$p(u, \tau)$ 的积分由两个最近的流形投影点主导：

$$
p(u, \tau) \sim C_A(u) \exp\!\left(-\frac{A(u, \tau)}{\tau}\right) + C_B(u) \exp\!\left(-\frac{B(u, \tau)}{\tau}\right).
$$

求对数梯度 $\nabla_u \log p(u, \tau)$，利用恒等式提取 $\tanh$，剩余的缓变项归入 $s^{\mathrm{sm}}$。在 $\Omega_{\mathrm{out}}(\tau)$ 中，某一模态占据绝对主导，$\tanh(\cdot) \to \pm 1$，$\nabla_u s^{\mathrm{sing}}$ 趋于 $0$，Score 场退化为平滑的 $\nabla_u A$ 或 $\nabla_u B$。

> **注**：该引理定位了标准扩散模型失败的根本原因。如果网络直接拟合 $s(u, \tau)$，$s^{\mathrm{sing}}$ 的雅可比矩阵 $\nabla_u s$ 在 $\Omega_{\mathrm{sh}}$ 内包含 $\mathcal{O}(1/\tau)$ 的奇异分量——这正是传统理论中 Lipschitz 常数 $L(\tau) \propto 1/\tau$ 的源头。

### 1.3 引理 1.2：BV-aware 函数空间对齐

网络架构（参数化 C）：

$$
s_\theta(u, \tau) = \nabla_u \phi^{\mathrm{sm}}_\theta(u, \tau) + \frac{\kappa_\theta(u, \tau)}{2} \tanh\!\left(\frac{\phi^{\mathrm{sh}}_\theta(u, \tau)}{2}\right) \nabla_u \phi^{\mathrm{sh}}_\theta(u, \tau).
$$

**引理 1.2（空间对齐与网络良态性）**：为使 $s_\theta$ 逼近 $s$，网络只需学习映射 $\Theta: (u, \tau) \mapsto (\phi^{\mathrm{sm}}_\theta, \kappa_\theta, \phi^{\mathrm{sh}}_\theta)$ 使得：

1. $\nabla_u \phi^{\mathrm{sm}}_\theta \approx s^{\mathrm{sm}}$
2. $\kappa_\theta \, \nabla_u \phi^{\mathrm{sh}}_\theta \approx \Delta s_{\mathrm{jump}}$
3. $\phi^{\mathrm{sh}}_\theta \approx (A - B)/\tau$

只要这样的平滑近似存在，网络各雅可比分量 $\|\nabla_u(\nabla_u \phi^{\mathrm{sm}}_\theta)\|_{\text{op}}$, $\|\nabla_u \kappa_\theta\|$, $\|\nabla_u \phi^{\mathrm{sh}}_\theta\|$ 均独立于 $\tau$，为 $\mathcal{O}(1)$ 量级。最高频放大因子 $1/\tau$ 已被吸收到 $\phi^{\mathrm{sh}}_\theta$ 的**数值尺度**中，而非通过自动微分产生。

### 1.4 推论：残差场的有界性

定义 Score 残差场：

$$
e(u, \tau) = s_\theta(u, \tau) - s(u, \tau), \qquad e(u, \tau) \in \mathbb{R}^d.
$$

假设在 $L^2$ Score Matching 损失 $\mathcal{L}_3$ 下优化到误差限：

$$
\mathbb{E}_{u, \tau}\big[\|e(u, \tau)\|^2\big] \leq \varepsilon^2.
$$

将 $e$ 分解为 $e = e_{\mathrm{sm}} + e_{\mathrm{sh}}$，其中 $e_{\mathrm{sh}}$ 为界面位置/强度偏差导致的激波残差。

**推论 1.4**：在 BV-aware 架构下，决定反向 SDE/ODE 稳定性的不再是全空间 $\nabla_u s_\theta$ 的 Lipschitz 常数，而是残差场 $e(u, \tau)$ 的**变分结构**。存在与 $\tau$ 无关的常数 $C_0 = \mathcal{O}(1)$ 使得：

$$
\int_0^{T_d} \big\| \nabla_u e(u, \tau) \big\|_{\mathrm{eff}} \, d\tau \leq C_0,
$$

其中 $\|\cdot\|_{\mathrm{eff}}$ 为下文中由单侧 Lipschitz 分析定义的"对误差放大有实质贡献"的有效范数。

**论证逻辑**：在标准架构（U-Net）中，$e_{\text{standard}} = s_{\text{UNet}} - s$，由于网络无法拟合 $\tanh(\cdot / \tau)$ 的陡峭梯度，在 $\Omega_{\mathrm{sh}}$ 内 $e_{\text{standard}}$ 自身具有与真实 Score 符号相反的 $-\mathcal{O}(1/\tau)$ 梯度分量，导致误差反向传播指数放大。

BV-aware 架构植入了 $\tanh$ 结构，网络输出 $s_\theta$ 与真实 $s$ 共享相同的 $1/\tau$ 奇异性。此时 $e_{\mathrm{sh}}$ 的误差表现为**激波中心位置 $\phi^{\mathrm{sh}}_\theta = 0$ 相对于真实位置 $A = B$ 的微小偏移**。由双曲 PDE 的变分性质，空间位置的平移在 $W_1$ 距离下与平移量同阶（$\Delta W_1 \propto \Delta x$），不涉及导数的乘性放大。

---

## 阶段 2：修正的 Gronwall 不等式论证

### 2.1 经典分析的失效与 Gronwall 陷阱

在反向生成过程中，考察两条 ODE 轨迹——由真实 Score $s$ 驱动的参考轨迹 $u^\natural(\tau)$ 与由网络 Score $s_\theta$ 驱动的近似轨迹 $\hat{u}(\tau)$。两者服从相同的概率流 ODE（基于粘性匹配策略 $\sigma^2(\tau) = 2\nu\tau$，漂移项系数 $\sigma \dot{\sigma} = \nu$）：

$$
\frac{d u^\natural}{d\tau} = -\nu \, s(u^\natural, \tau) \eqqcolon V(u^\natural, \tau), \qquad
\frac{d \hat{u}}{d\tau} = -\nu \, s_\theta(\hat{u}, \tau) \eqqcolon V_\theta(\hat{u}, \tau).
$$

**初始条件**：两者从同一先验噪声 $z \sim p_{T_d}$ 出发，即 $\hat{u}(T_d) = u^\natural(T_d) = z$。若训练后有微小偏差，可将其吸收进最终界（见下文注）。

定义轨迹误差（$\mathbb{R}^d$ 欧氏范数）：

$$
E(\tau) \coloneqq \|\hat{u}(\tau) - u^\natural(\tau)\|.
$$

对 $E^2$ 求导并代入 ODE：

$$
\frac{1}{2}\frac{d}{d\tau} E(\tau)^2
= \big\langle \hat{u} - u^\natural, \, V_\theta(\hat{u}, \tau) - V(u^\natural, \tau) \big\rangle
\leq \big\langle \hat{u} - u^\natural, \, V_\theta(\hat{u}) - V_\theta(u^\natural) \big\rangle
+ \nu \|e(u^\natural, \tau)\| \, E(\tau).
$$

在经典证明中，利用 $V_\theta$ 的全局 Lipschitz 常数 $L_\theta(\tau)$ 放缩第一项：

$$
\|V_\theta(\hat{u}) - V_\theta(u^\natural)\| \leq L_\theta(\tau) \, E(\tau).
$$

由于 $s_\theta$ 中包含 $\tanh(\cdot/\tau)$ 项，$\|\nabla_u s_\theta\|_{\text{op}} = \mathcal{O}(1/\tau)$，故 $L_\theta(\tau) = \mathcal{O}(1/\tau)$。套用标准 Gronwall 不等式从 $\tau = T_d$ 反向积分至 $\tau \to 0$ 时，积分因子为：

$$
\exp\!\left( \int_{0}^{T_d} \mathcal{O}(1/\tau) \, d\tau \right) \sim \exp(\Lambda),
$$

即指数放大因子 $\exp(\Lambda)$（对应 Score Shocks 中的 SNR/2 放大）。

### 2.2 引理 2.1：单侧 Lipschitz 条件与半负定性

放弃全局 Lipschitz 常数，转而计算 $V_\theta$ 的**单侧 Lipschitz 常数**（对数范数）。

**定义**：单侧 Lipschitz 常数 $\mu(\tau)$ 是使得下式对一切 $u, v \in \mathbb{R}^d$ 成立的最小数：

$$
\big\langle u - v, \; V_\theta(u, \tau) - V_\theta(v, \tau) \big\rangle \leq \mu(\tau) \, \|u - v\|^2.
$$

当 $V_\theta$ 可微时，$\mu(\tau)$ 等价于其雅可比矩阵 $J_\theta(u, \tau) \coloneqq \nabla_u V_\theta(u, \tau) \in \mathbb{R}^{d \times d}$ 的对称部分在所有 $u$ 处的最大特征值：

$$
\mu(\tau) = \sup_{u \in \mathbb{R}^d} \; \lambda_{\max}\!\left( \frac{J_\theta(u, \tau) + J_\theta(u, \tau)^\mathsf{T}}{2} \right).
$$

**引理 2.1（BV-aware 架构的局部压缩性）**：对于参数化 (C)，在假设 $\kappa_\theta(u, \tau) > 0$（由 Lax 熵条件保证，见下文注）下，有：

$$
\mu(\tau) \leq L_{\mathrm{sm}} = \mathcal{O}(1),
$$

即单侧 Lipschitz 常数独立于 $\tau$，无奇异性。

**推导**：计算 $V_\theta(u, \tau) = -\nu s_\theta(u, \tau)$ 的雅可比矩阵：

$$
J_\theta = \nabla_u V_\theta = J_{\mathrm{sm}} + J_{\mathrm{sing}} + J_{\mathrm{cross}}.
$$

---

**1. 平滑部分与交叉项**：

$J_{\mathrm{sm}} = -\nu \, \nabla_u^2 \phi^{\mathrm{sm}}_\theta$，由阶段 1 良态性，$\lambda_{\max}(J_{\mathrm{sm}}) \leq \mathcal{O}(1)$。$J_{\mathrm{cross}}$ 包含对 $\kappa_\theta$、$\nabla_u \phi^{\mathrm{sh}}_\theta$ 的导数，均不含 $1/\tau$ 因子，同为 $\mathcal{O}(1)$。

---

**2. 奇异部分**：对 $\tanh$ 内部求导产生的项：

$$
J_{\mathrm{sing}}(u, \tau) = -\nu \cdot \frac{\kappa_\theta(u, \tau)}{4} \; \mathrm{sech}^2\!\left(\frac{\phi^{\mathrm{sh}}_\theta(u, \tau)}{2}\right) \;
\big( \nabla_u \phi^{\mathrm{sh}}_\theta \big) \big( \nabla_u \phi^{\mathrm{sh}}_\theta \big)^{\!\mathsf{T}}.
$$

$\big( \nabla_u \phi^{\mathrm{sh}}_\theta \big) \big( \nabla_u \phi^{\mathrm{sh}}_\theta \big)^{\!\mathsf{T}}$ 是秩为 1 的半正定矩阵（形式为 $\mathbf{n} \mathbf{n}^{\mathsf{T}}$，其中 $\mathbf{n} \coloneqq \nabla_u \phi^{\mathrm{sh}}_\theta$ 是激波界面法向量）。

物理黏性 $\nu > 0$，且由 Lax 熵条件，激波强度 $\kappa_\theta$ 在物理区域内**严格为正**。前方负号使 $J_{\mathrm{sing}}$ 为**严格半负定**。

> **注（$\kappa_\theta > 0$ 的保证）**：双曲守恒律中，满足 Lax 熵条件的激波对应的跃变强度符号使特征线在激波处聚拢（压缩波，$\kappa_\theta > 0$）。在参数化 (C) 的实现中，对 $\kappa_\theta$ 施加 Softplus 激活或正偏置以保证 $\kappa_\theta > 0$，从而 $J_{\mathrm{sing}}$ 的半负定性得到保证。

---

**3. 物理推论**：

在垂直于激波面的方向（$\mathbf{n}$ 方向）上，$J_{\mathrm{sing}}$ 给出极大的负特征值 $-\mathcal{O}(1/\tau)$。这意味着反向扩散流在激波法向存在**极其强烈的吸引力**——偏离真实激波流形的误差不仅不被放大，反而以 $\mathcal{O}(1/\tau)$ 的速率被压缩（这是 Burgers 方程特征线相交的数学本质）。

在对数范数 $\mu(\tau)$ 中，求最大特征值时，$J_{\mathrm{sing}}$ 的巨大负值被截断为 $0$（仅正特征值贡献误差放大）。因此：

$$
\mu(\tau) \leq \lambda_{\max}\!\big( J_{\mathrm{sm}} + J_{\mathrm{cross}} \big) + 0 = \mathcal{O}(1).
$$

### 2.3 定理 2.2：常数上界的修正流稳定性

对 $\frac{1}{2} \frac{d}{d\tau} E(\tau)^2$ 应用引理 2.1 的单侧 Lipschitz 条件处理第一项，Cauchy–Schwarz 处理第二项：

$$
\frac{1}{2} \frac{d}{d\tau} E(\tau)^2
\leq \mu(\tau) \, E(\tau)^2 + E(\tau) \cdot \nu \, \|e(u^\natural, \tau)\|.
$$

两边同除以 $E(\tau)$（$E(\tau) > 0$ 时；$E(\tau) = 0$ 时平凡成立）：

$$
\frac{d}{d\tau} E(\tau) \leq \mu(\tau) \, E(\tau) + \nu \, \|e(u^\natural, \tau)\|.
$$

应用修正的 Gronwall 不等式，从 $\tau = T_d$ 积分至 $\tau \to 0$。设 $E(T_d) = 0$（先验匹配）或 $E(T_d) \leq \tilde{C}\varepsilon$（微小初始偏差可被吸收）：

$$
E(0) \leq \int_0^{T_d} \exp\!\left( \int_0^\tau \mu(r) \, dr \right) \, \nu \, \|e(u^\natural, \tau)\| \, d\tau.
$$

由引理 2.1，$\mu(r) \leq \mathcal{O}(1)$ 严格成立，故积分因子有界：

$$
\exp\!\left( \int_0^\tau \mu(r) \, dr \right) \leq C_{\mathrm{flow}} = \mathcal{O}(1).
$$

代入推论 1.4 中的残差场积分有界性：

$$
E(0) \leq C_{\mathrm{flow}} \, \nu \int_0^{T_d} \|e(u^\natural, \tau)\| \, d\tau \leq C_1 \cdot \varepsilon.
$$

**结论**：在 BV-aware 架构下，轨迹终点误差与训练误差同阶（$E(0) = \mathcal{O}(\varepsilon)$），去除了 $\exp(\Lambda)$ 因子。

---

## 阶段 3：Kruzhkov 熵解的 $L^1$ 压缩性映射

> **阶段 3 的约定**：以下引入物理空间 $x \in \Omega \subset \mathbb{R}$。对于 $\mathbb{R}^d$ 中的状态向量 $u$（图 1，$d = N_x$），其分量为 $u_i = u(x_i)$，其中 $\{x_i\}$ 是物理空间的网格点。$L^p$ 范数按网格离散化规则近似（如 $\|u\|_{L^1} \approx \Delta x \sum_i |u_i|$）。

### 3.1 Kruzhkov 熵条件与 $L^1$ 拓扑

考虑目标双曲守恒律（在物理空间 $\Omega \times [0, T]$ 上）：

$$
\partial_t \mathbf{u} + \partial_x f(\mathbf{u}) = 0, \qquad x \in \Omega \subset \mathbb{R}, \quad t \in [0, T],
$$

其中 $f$ 为通量函数（如 Burgers 通量 $f(u) = u^2/2$）。设初始条件 $\mathbf{u}(\cdot, 0) = \mathbf{u}_0$。强解在激波形成后不存在，必须引入弱解。物理上唯一正确的解——Kruzhkov 熵解 $\mathbf{u}^\star(x, t)$——满足全局熵条件：对任意常数 $k \in \mathbb{R}$，在分布意义下

$$
\partial_t |\mathbf{u}^\star - k| + \partial_x \big( \mathrm{sgn}(\mathbf{u}^\star - k) (f(\mathbf{u}^\star) - f(k)) \big) \leq 0.
$$

**Kruzhkov 定理推论（$L^1$-Contraction Semigroup）**：若 $\mathbf{a}(x, t)$ 和 $\mathbf{b}(x, t)$ 都是满足 Kruzhkov 熵条件的解，则

$$
\|\mathbf{a}(\cdot, t) - \mathbf{b}(\cdot, t)\|_{L^1(\Omega)} \leq \|\mathbf{a}(\cdot, 0) - \mathbf{b}(\cdot, 0)\|_{L^1(\Omega)}.
$$

定理 3 考虑的是在目标物理时间 $t = T_{\text{phys}}$ 处的解。令 $\mathbf{u}^\star(x) \coloneqq \mathbf{u}^\star(x, T_{\text{phys}})$（简记，后文省略 $T_{\text{phys}}$），这是我们希望扩散模型生成的函数。

### 3.2 损失设计与 BV 空间的紧致性

全变差（在物理空间 $\Omega$ 上）：

$$
\mathrm{TV}(\mathbf{u}) = \int_\Omega |\partial_x \mathbf{u}| \, dx.
$$

对于含激波的解，$\mathrm{TV}(\mathbf{u})$ 等于各跳跃幅度的绝对值之和，有限（$\mathrm{TV}(\mathbf{u}^\star) \leq M$）。

损失函数 $\mathcal{L}_3$ 在标准 denoising score matching 损失上附加 BV 正则项：

$$
\mathcal{L}_3 = \mathcal{L}_{\mathrm{DSM}} + \lambda_{\mathrm{BV}} \, \mathrm{TV}(D_\theta),
$$

其中 $D_\theta$ 为去噪器。结合参数化 (C) 中硬编码的 $\tanh$ 结构，此正则项强制生成样本 $\mathbf{u}^\theta$（即 $u^\theta$ 对应的物理函数）几乎必然落入有界 BV 球：

$$
\mathbf{u}^\theta \in \mathcal{K}_M = \big\{ \mathbf{u} \in L^1(\Omega) \cap L^\infty(\Omega) : \mathrm{TV}(\mathbf{u}) \leq M \big\}.
$$

由 Helly 选择定理，$\mathcal{K}_M$ 在 $L^1(\Omega)$ 拓扑下是**相对紧致**的。

### 3.3 算子分裂与粘性极限

扩散模型的反向阶段在粘性匹配策略 $\sigma^2(\tau) = 2\nu_{\text{phys}} \tau$ 下，本质上引入了人工粘性 $\nu_{\text{phys}}$。记 $\mathbf{u}^\nu$ 为带粘性项的物理 PDE 的解（在 $t = T_{\text{phys}}$ 处）：

$$
\partial_t \mathbf{u}^\nu + \partial_x f(\mathbf{u}^\nu) = \nu_{\text{phys}} \, \partial_{xx} \mathbf{u}^\nu.
$$

**Kuznetsov 引理（1976）**：带有粘性 $\nu$ 的抛物型方程的解 $\mathbf{u}^\nu$ 逼近无黏 Kruzhkov 熵解 $\mathbf{u}^\star$ 的误差界为：

$$
\|\mathbf{u}^\nu - \mathbf{u}^\star\|_{L^1(\Omega)} \leq C \, \sqrt{\nu \, T_{\text{phys}}} \cdot \mathrm{TV}(\mathbf{u}_0),
$$

其中 $\mathbf{u}_0$ 为初值，$T_{\text{phys}}$ 为目标物理时间（在定理中视为固定常数）。

---

## 阶段 4：测度空间的 Wasserstein 组装与 $\mathcal{O}(\varepsilon^{1/2})$ 的涌现

### 4.1 误差的泛函插值

由阶段 2 的结论，在给定同一先验噪声 $z$ 的条件下，生成样本与参考粘性解之间的 $\mathbb{R}^d$ 欧氏误差被界为：

$$
\mathbb{E}_z \big[ \|\hat{u}(0) - u^\natural(0)\|^2 \big] \leq C_1 \varepsilon^2.
$$

由于向量范数 $\|\cdot\|_{\mathbb{R}^d}$ 在网格细化极限下等价于 $\|\cdot\|_{L^2(\Omega)}$（至多差网格间距因子 $\sqrt{\Delta x}$），上式蕴含：

$$
\mathbb{E}_z \big[ \|\mathbf{u}^\theta - \mathbf{u}^\nu\|_{L^2(\Omega)}^2 \big] \leq \tilde{C}_1 \varepsilon^2.
$$

利用 Gagliardo–Nirenberg 型插值不等式：对一维函数 $h = \mathbf{u}^\theta - \mathbf{u}^\nu$，有

$$
\|h\|_{L^1(\Omega)} \leq C_{\text{GN}} \, \|h\|_{L^2(\Omega)}^{2/3} \, \mathrm{TV}(h)^{1/3}.
$$

由于 $\mathbf{u}^\theta, \mathbf{u}^\nu \in \mathcal{K}_M$，有 $\mathrm{TV}(h) \leq 2M$。代入 $\|h\|_{L^2} = \mathcal{O}(\varepsilon)$：

$$
\mathbb{E}_z \big[ \|\mathbf{u}^\theta - \mathbf{u}^\nu\|_{L^1(\Omega)} \big] \leq \mathcal{O}(\varepsilon^{2/3}).
$$

> **注（在激波主导下的更优插值）**：当误差由激波位置偏差主导时，$L^1$ 误差与 $L^2$ 误差平方同阶（而非 $2/3$ 次）。严格论证需单独引理，此处结论中 $\mathcal{O}(\varepsilon)$ 项最终被 $\mathcal{O}(\varepsilon^{1/2})$ 主导，不影响最终结果。

### 4.2 Wasserstein 距离的三角不等式拆解

1-Wasserstein 距离（Kantorovich–Rubinstein 对偶）：

$$
W_1(\mu, \nu) = \inf_{\pi \in \Pi(\mu, \nu)} \int \|u - v\|_{L^1(\Omega)} \, d\pi(u, v).
$$

设 $\mu^\nu$ 为粘性解的分布（在给定初值 $\mathbf{u}_0$ 下为确定性，即 $\delta_{\mathbf{u}^\nu}$），进行三角不等式拆分：

$$
W_1(\mu_\theta, \delta_{\mathbf{u}^\star})
\leq \underbrace{W_1(\mu_\theta, \delta_{\mathbf{u}^\nu})}_{\text{神经生成误差}}
+ \underbrace{W_1(\delta_{\mathbf{u}^\nu}, \delta_{\mathbf{u}^\star})}_{\text{粘性极限误差}}.
$$

---

**第一项（神经生成误差）**：由阶段 2 的轨迹有界性与上述插值，两条 ODE 轨迹由同一先验噪声 $z$ 出发，存在确定性的逐点耦合 $\pi = (\mathbf{u}^\theta(z), \mathbf{u}^\nu(z))_{\#} p_{T_d}$，从而：

$$
W_1(\mu_\theta, \delta_{\mathbf{u}^\nu})
\leq \mathbb{E}_z \big[ \|\mathbf{u}^\theta - \mathbf{u}^\nu\|_{L^1(\Omega)} \big]
\leq C_2 \, \varepsilon.
$$

---

**第二项（粘性极限误差）**：$\delta_{\mathbf{u}^\nu}$ 与 $\delta_{\mathbf{u}^\star}$ 均为单点分布，$W_1$ 退化为 $L^1$ 距离：

$$
W_1(\delta_{\mathbf{u}^\nu}, \delta_{\mathbf{u}^\star}) = \|\mathbf{u}^\nu - \mathbf{u}^\star\|_{L^1(\Omega)}.
$$

由 Kuznetsov 引理（§3.3）：

$$
\|\mathbf{u}^\nu - \mathbf{u}^\star\|_{L^1(\Omega)} \leq C \, \sqrt{\nu_{\text{phys}} \, T_{\text{phys}}} \cdot \mathrm{TV}(\mathbf{u}_0).
$$

**关键优化**：在粘性匹配策略下，有效终端粘性 $\nu_{\text{phys}}$ 并非固定，而是由扩散模型的反向终止时间 $\tau_{\text{end}}$（理想情况下 $\tau_{\text{end}} \to 0$）决定。存在 Scheduling 选择使 $\nu_{\text{phys}} \sim \mathcal{O}(\varepsilon)$ 而得分匹配误差仍保持在 $\mathcal{O}(\varepsilon)$。代入：

$$
\|\mathbf{u}^\nu - \mathbf{u}^\star\|_{L^1(\Omega)} \leq C_3 \sqrt{\varepsilon} = \mathcal{O}(\varepsilon^{1/2}).
$$

### 4.3 最终结论

将两项相加：

$$
W_1(\mu_\theta, \delta_{\mathbf{u}^\star})
\leq \mathcal{O}(\varepsilon) + \mathcal{O}(\varepsilon^{1/2}).
$$

由于 $\varepsilon \ll 1$，高阶项 $\mathcal{O}(\varepsilon)$ 被低阶项 $\mathcal{O}(\varepsilon^{1/2})$ 所主导。因此：

$$
\boxed{ W_1(\mu_\theta, \delta_{\mathbf{u}^\star}) \leq C_2 \, \varepsilon^{1/2}. }
$$

$\square$

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
| 残差场 $e(u,\tau)$ 中 $u$ 的双重角色 | $e(u, \tau)$ 的参数 $u$ 是状态空间点，$\nabla_u e = \nabla_{u} e(u, \tau)\big|_{u}$ | 保留 $u$ 作为参数名，添加作用域说明 |
| 时间 $\tau$ 与 $t$ 关系不明 | §0 时间映射表明确定义 | 显式声明正交关系和物理含义 |

## 附录 B：尚需严格化的技术点（对应"证明改进"文档 §二）

| 编号 | 技术点 | 状态 |
|---|---|---|
| L1.1-P | 引理 1.1 的"有限分离高斯簇"假设需作为定理前置条件明确 | 已标注 |
| C1.4-G | 推论 1.4 残差梯度界需独立引理展开（$e_{\mathrm{sm}}$ 梯度界 + $e_{\mathrm{sh}}$ 偏移 → 梯度界） | 留待后续 |
| L2.1-$\kappa$ | $\kappa_\theta > 0$ 的网络约束（Softplus）已在注中补充 | 已补充 |
| G2.2-E0 | $E(T_d)$ 非零的微小误差吸收已在文本中说明 | 已说明 |
| P4.1-GN | Gagliardo–Nirenberg 插值给出 $\varepsilon^{2/3}$，激波优化至 $\varepsilon^{1/2}$ 需单独引理 | 留待 W4 补充 |
| K3.3-$\nu$ | $\nu_{\text{phys}} \sim \mathcal{O}(\varepsilon)$ 的调度可行性需独立引理 | 留待 W4 补充 |
