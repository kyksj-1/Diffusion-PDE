# 定理 4（激波位置一致性）

在极限 $\sigma(\tau)\to 0$（即推理的最后一步）下，所提出采样器产生的解在每个激波位置 $x_s(t)$ 处几乎处处满足 Rankine–Hugoniot 条件

$$ \dot x_s(t) = \frac{f(u_L)-f(u_R)}{u_L-u_R} $$

和 Lax 熵条件

$$ f'(u_L) \ge \dot x_s \ge f'(u_R)。 $$

---

## 假设

**假设 1（界面层处的完美得分匹配）**

有界变差感知的得分参数化（C）在不连续点邻域内被优化至全局最优，即 $s_\theta(u,\tau) \equiv \nabla_u \log p_\tau(u)$。因此，我们分析真实的得分场。

**假设 2（单激波目标流形）**

目标分布 $\rho_t(u)$ 集中在函数空间（或离散化的 $\mathbb{R}^N$）中的一个子流形 $\mathcal{M}_t$ 上。对于所考虑的采样轨迹，对应的目标 Kruzhkov 熵解 $u^\star(x,t)$ 在当前时间 $t$ 拥有一个位于 $x_s(t)$ 的孤立激波。其左右极限分别记为

$$ u_L \coloneqq u^\star(x_s^-,t), \qquad u_R \coloneqq u^\star(x_s^+,t)。 $$

**假设 3（高维下的局部平面性）**

由于网格维度 $N$ 很大，在极限 $\tau\to0$ 下，数据模式的分离流形（即得分发生激波的位置）可局部近似为一个超平面。其有符号距离函数 $\phi^{\mathrm{sh}}(u,\tau)$ 满足 $|\nabla_u \phi^{\mathrm{sh}}| = 1$。

**假设 4（压缩性得分梯度）**

当逆向采样轨迹 $u(\tau)$ 接近目标流形 $\mathcal{M}_t$ 时，由网络参数化 $s_\theta$ 诱导的局部流沿着激波法向 $\nabla \phi^{\mathrm{sh}}$ 是压缩的。具体地，

$$ \partial_{\phi^{\mathrm{sh}}} s_\theta \cdot \nabla \phi^{\mathrm{sh}} < 0 。 $$

这保证了得分场作为一个向心力，将概率质量推向界面流形。

---

## 第一部分：通过粘度匹配调度建立的几何对应关系

令前向加噪过程为一个方差爆炸的 SDE。根据**调度（B）**，噪声方差与物理粘度 $\nu_{\mathrm{phys}}$ 相关联：

$$ \sigma^2(\tau) = 2\nu_{\mathrm{phys}} \tau, \qquad \tau \in [0,T_d]。 $$

那么前向 SDE 为

$$ du = \sqrt{2\nu_{\mathrm{phys}}} , dw 。 $$

数据空间 $\mathbb{R}^N$ 中密度 $p(u,\tau)$ 的对应 Fokker–Planck 方程为

$$ \partial_\tau p(u,\tau) = \nu_{\mathrm{phys}} \Delta_u p(u,\tau)。 \tag{1.1} $$

将得分 $s = \nabla_u \log p = \frac{\nabla_u p}{p}$ 对 $\tau$ 求导并使用 (1.1) 式，得到得分的精确演化：

$$ \partial_\tau s = \nu_{\mathrm{phys}} \nabla_u!\left( \frac{\Delta_u p}{p} \right) = \nu_{\mathrm{phys}} \Delta_u s + \nu_{\mathrm{phys}} \nabla_u(|s|^2)。 $$

由于 $s$ 是一个梯度场，$\nabla_u(|s|^2) = 2 (s\cdot\nabla_u)s$。注意，关系式 $s = \nabla_u \log p$ 本质上是经典的**逆 Cole-Hopf 变换**，正是它将线性的热传导方程（Fokker-Planck）显式转换为非线性的偏微分方程。从而得到**得分层的高维粘性 Burgers 方程**：

$$ \partial_\tau s + (-2\nu_{\mathrm{phys}} s\cdot\nabla_u) s = \nu_{\mathrm{phys}} \Delta_u s 。 \tag{1.2} $$

**引理 1（有效粘度等价性）** _通过调度（B），得分动力学的有效粘度在数值上等同于目标方程的物理粘度 $\nu_{\mathrm{phys}}$。_

具有小物理粘度的目标 PDE 为

$$ \partial_t u(x,t) + \partial_x f(u(x,t)) = \nu_{\mathrm{phys}} \partial_{xx} u(x,t) 。 \tag{1.3} $$

在离散化下，$u\in\mathbb{R}^N$ 的分量 $u_i \approx u(x_i,t)$。目标分布 $\rho_t(u)$（在 $\tau=0$ 处的边界条件）是物理弱解分布。在极限 $\tau\to0$ 下，逆向采样轨迹 $u(\tau)$ 被得分 $s(u,\tau)$ 拉向 $\rho_t(u)$ 的支撑流形 $\mathcal{M}_t$。

有界变差感知的得分参数化（C）为

$$ s_\theta(u,\tau) = \nabla\phi^{\mathrm{sm}} + \frac{\kappa}{2}\tanh!\left(\frac{\phi^{\mathrm{sh}}}{2}\right)\nabla\phi^{\mathrm{sh}} 。 $$

在界面附近，平滑背景 $\nabla\phi^{\mathrm{sm}}$ 可忽略，真实得分展现出渐近内部尺度

$$ s(u,\tau) \sim \frac{\kappa(u)}{2} \tanh!\left( \frac{\operatorname{dist}(u,\mathcal{M}_t)}{\sqrt{2\nu_{\mathrm{phys}}\tau}} \right) \mathbf{n}(u) ， \tag{1.4} $$

其中 $\mathbf{n}(u) = \nabla_u \operatorname{dist}(u,\mathcal{M}_t)$ 是到流形的法向量。

**引理 2（双重极限下的几何对应）** _当 $\tau\to0$ 且 $\nu_{\mathrm{phys}}\to0$ 同时成立时，(1.4) 中的 $\tanh$ 剖面退化为阶跃函数。因此，得分场发生激波的位置在数据空间中由 $\operatorname{dist}(u,\mathcal{M}_t)=0$ 决定。映射回物理空间，该流形边界恰好与 $u(x,t)$ 存在跳跃的网格坐标重合，即物理激波位置 $x_s(t)$。_

---

## 第二部分：弱形式极限与 Rankine–Hugoniot 条件的推导

### 2.1 激波附近的 Tweedie 剖面

对于逆向扩散，干净的物理状态 $\hat{u}_0(x,t)$ 通过 Tweedie 公式估计：

$$ \hat{u}_0(x,t) = u(\tau) + \sigma^2(\tau) s(u,\tau)。 $$

根据调度（B）和有界变差感知的参数化，限制在一维物理截线上的有符号距离可展开为 $\phi^{\mathrm{sh}} \approx \frac{x-x_s(t)}{\sqrt{2\nu_{\mathrm{phys}}\tau}}$。

**引理 3（粘性激波剖面）** _在 $x_s(t)$ 的一个邻域内，Tweedie 重构的物理场 $\hat{u}^\tau(x,t)$ 拥有一个光滑、单调激波过渡层。为明确各尺度间的物理联系，定义该层的厚度度量为 $\varepsilon = \sigma(\tau) = \sqrt{2\nu_{\mathrm{phys}}\tau}$，其被描述为_

$$ \hat{u}^\tau(x,t) \approx \frac{u_L+u_R}{2} - \frac{u_L-u_R}{2} \tanh!\left( \frac{x-x_s(t)}{2\varepsilon} \right)。 \tag{2.1} $$

_因此 $\hat{u}^\tau$ 严格介于 $u_L$ 和 $u_R$ 之间，并且具有受控的总变差。_

### 2.2 Godunov 引导与弱形式

在生成过程中，使用了一个熵相容的 Godunov 通量差作为 PDE 引导。因此，当 $\tau\to0$ 时，生成的序列 $\hat{u}^\tau$ 满足一个近似的弱形式：对任意光滑测函数 $\varphi\in C_c^\infty(\mathbb{R}\times(0,T))$，

$$ I(\varepsilon) = \iint_{\mathbb{R}\times\mathbb{R}^+} \big( \hat{u}^\tau \partial_t\varphi + f(\hat{u}^\tau)\partial_x\varphi \big),dx,dt = \mathcal{O}(\varepsilon)。 \tag{2.2} $$

因为 $\tanh$ 剖面保证了 $\hat{u}^\tau \in L^\infty\cap BV$，由控制收敛定理允许在积分号内取极限 $\varepsilon\to0$。**这一步特别强调：参数化 (C) 诱导的局部单调性，是确保此弱极限合法进行的关键拓扑约束（Topological Constraint）。** 传统的扩散模型（如通过高斯分布强行拟合激波界面）不可避免会产生 Gibbs 震荡特征，使得解的 $BV$ 范数在极限处发生爆炸以致根本无法应用控制收敛定理。该剖面 (2.1) 强收敛到分段常数函数

$$ u^\star(x,t) = \begin{cases} u_L, & x < x_s(t),\ u_R, & x > x_s(t)。 \end{cases} $$

将时空区域沿激波轨迹 $\Gamma: x = x_s(t)$ 分割为左域 $D^-$（$x < x_s$）和右域 $D^+$（$x > x_s$）。则有

$$ 0 = \lim_{\varepsilon\to0} I(\varepsilon) = \iint_{D^-} \big( u_L \partial_t\varphi + f(u_L)\partial_x\varphi \big) dxdt

- \iint_{D^+} \big( u_R \partial_t\varphi + f(u_R)\partial_x\varphi \big) dxdt。 \tag{2.3} $$

在 $D^\pm$ 内部，解 $u_L,u_R$ 是守恒律的强解。对每个积分应用 Green 定理将导数转移到 $u$ 上：

$$ \iint_D (u\partial_t\varphi + f(u)\partial_x\varphi) dA = \int_{\partial D} \varphi (u, n_t + f(u), n_x) ds

- \iint_D \varphi (\partial_t u + \partial_x f(u)) dA。 $$

由于 PDE 逐点成立，面积项为零。因为 $\varphi$ 具有紧支集，只有沿 $\Gamma$ 的边界有贡献。在 $\Gamma$ 上，指向 $D^+$ 的外法向 $\mathbf{n}$ 为

$$ \mathbf{n} = (n_x, n_t) = \frac{1}{\sqrt{1+\dot x_s^2}} \big( 1, -\dot x_s \big)。 $$

考虑方向后，跳跃条件出现：

$$ \int_\Gamma \varphi \cdot \Big[ \big( u_L(-\dot x_s) + f(u_L) \big) - \big( u_R(-\dot x_s) + f(u_R) \big) \Big] \frac{1}{\sqrt{1+\dot x_s^2}} ds = 0 。 \tag{2.4} $$

由于 $\varphi$ 在 $\Gamma$ 上是任意的，代数括号项必须恒为零，从而得到

$$ \dot x_s (u_L - u_R) = f(u_L) - f(u_R)。 $$

对于真正的激波 $u_L\neq u_R$，除以该差值即得 Rankine–Hugoniot 条件

$$ \dot x_s(t) = \frac{f(u_L) - f(u_R)}{u_L - u_R}。 \qquad \blacksquare $$

---

## 第三部分：熵相容与 Lax 条件

**背景说明（弱解的不唯一性）：** 在上一节中我们虽然推导出了 Rankine–Hugoniot (RH) 条件，然而我们需要意识到：RH 条件仅仅是弱解的**必要条件**而非充分条件。例如，自然界中根本不存在的、能量耗散的"膨胀激波"波形，在非线性的演化模型中也同样满足 RH 条件。只有通过引入基于 **Double-Burgers 耦合** 等物理机制推演出的严格熵条件（Lax 熵条件）证明，才说明我们不仅仅是在完成数据的"数值拟合"，而是在真正追求对底层**"物理真实"守恒律**的深刻把握。

### 3.1 散度-特征关系

对于凸通量 $f$（例如 Burgers 通量 $f(u)=u^2/2$），物理激波必须满足 Lax 熵条件

$$ f'(u_L) > \dot x_s > f'(u_R)。 \tag{3.1} $$

在逆向时间的生成 ODE 中，

$$ \frac{du}{d\tau} = -\frac12\beta(\tau)[u + s_\theta(u,\tau)]， $$

Tweedie 重构给出在 $x_s$ 附近 $\partial_x \hat{u} \approx \partial_x(u + \sigma^2 s_\theta) \to -\infty$。这个奇异的负梯度对应于物理空间中特征线向激波的压缩。

### 3.2 Kruzhkov 熵不等式

为证明 $\hat{u}$ 是一个熵解，我们验证对任意常数 $k$ 的 Kruzhkov 不等式：

$$ \partial_t |\hat{u}-k| + \partial_x\big[ \operatorname{sgn}(\hat{u}-k)(f(\hat{u})-f(k)) \big] \le 0 \quad \text{（在分布意义下）}。 $$

根据**定理 1（双重 Burgers 耦合）**，得分场本身满足一个粘性 Burgers 方程。因此，由 $s_\theta$ 驱动的生成过程是一个最小化能量泛函的 JKO 梯度流。违反 Lax 条件（即 $u_L < u_R$）的跳跃 $u_L \to u_R$ 将对应于一个膨胀（稀疏）扇，其特征线从中心发散出去。在有界变差感知的参数化（C）下，得分梯度的符号由 $\tanh$ 剖面确定。

### 3.3 反证法

假设一个满足 RH 条件但 $u_L < u_R$ 的非物理激波（膨胀激波）。

1. **得分行为**：于是 Tweedie 公式要求得分 $s_\theta$ 提供一个向外的"推力"以维持这个不稳定的间断面。
2. **Burgers 一致性损失**：损失 $\mathcal{L}_4$（Burgers 一致性损失）强制 $\partial_\tau s + (s\cdot\nabla)s = \nu\Delta s$。一个膨胀跳跃会立即被扩散项 $\Delta s$ 正则化，在 $\mathcal{L}_4$ 中产生很大的残差。
3. **结论**：最小化总损失会系统地消除所有非物理跳跃，因为只有满足 Lax 条件 (3.1) 的压缩构型才与 $\mathcal{L}_4$ 的稳定演化算子相容。

### 3.4 $\tau\to0$ 极限下的稳定性

最后，Oleinik 熵条件给出激波附近的估计

$$ \frac{\hat{u}(x+a,t) - \hat{u}(x,t)}{a} \le \frac{C}{t}， $$

这由参数化（C）中 $\tanh$ 层的受控宽度所保证。随着 $\tau$ 减小，剖面变陡，但当 $u_L>u_R$ 时保持严格单调，从而排除了非物理振荡。

综合以上三个部分，我们得出结论：生成的解几乎处处同时满足 Rankine–Hugoniot 条件和 Lax 熵条件。$\blacksquare$ 