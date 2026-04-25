# L4 双曲 PDE 的弱解理论：熵解、BV 空间与粘性消失法

> **本讲定位**：为路径 A 的"目标 PDE 类"建立数学语言。扩散模型面对的双曲 PDE（Burgers、Euler、Buckley–Leverett、shallow water）解在有限时间内必然不光滑（shock），需要 weak solution + entropy condition 框架。本讲把这套经典数学整理给物理系学生。
> **先修**：基本 PDE 知识（分类、特征线）；本科电动力学里"激波"的物理图像。
> **后续依赖**：L5（Score–Burgers）、路径 A Theorem 2/3/4（熵解稳定性、shock 位置一致性）。
> **长度**：约 4500 字。

---

## §0 本讲目标

L1–L3 帮我们把扩散模型放到 FP / $W_2$-梯度流的框架里。这些框架处理的是**光滑扩散 PDE**（椭圆、抛物）。但路径 A 的对象是**双曲 PDE**——解可以有跳跃不连续（shock），处理方式完全不同。

本讲要回答三件事：

1. **为什么 shock 是双曲 PDE 的必然产物？**（§1–§2：特征线交汇）
2. **shock 解在什么数学意义下仍是"解"？**（§3：弱解；§4：Kruzhkov 熵解；§5：粘性消失）
3. **shock 解在哪个函数空间里？**（§6：BV 空间）

读完本讲，你应该能独立陈述：**给一个 1D 标量守恒律 + 初值，它的熵解是什么、为什么唯一、与粘性解的极限是同一个东西**。这是路径 A Theorem 2/3/4 的数学对象。

---

## §1 复习：特征线法（光滑情形）

考虑 1D 标量守恒律
$$
\partial_t u + \partial_x f(u) = 0, \quad u(x, 0) = u_0(x), \quad x \in \mathbb R, \ t \geq 0. \tag{1.1}
$$
$f$ 是光滑通量函数。改写为
$$
\partial_t u + f'(u) \partial_x u = 0. \tag{1.2}
$$

### 1.1 特征线

沿曲线 $x = X(t)$ 观察 $u$ 的全导数：
$$
\frac{d u(X(t), t)}{dt} = \partial_t u + \dot X \partial_x u.
$$
若取 $\dot X = f'(u)$，则 (1.2) 给出 $\frac{du}{dt} = 0$——$u$ 沿这条曲线**保持常数**。

**推论（特征线是直线）**：由于 $u$ 沿 $X$ 是常数，$\dot X = f'(u)$ 也是常数，故 $X(t) = x_0 + f'(u_0(x_0)) t$。

### 1.2 隐式解公式

从 $x_0 = X^{-1}(x, t)$ 得
$$
u(x, t) = u_0(x_0), \quad x = x_0 + f'(u_0(x_0)) t. \tag{1.3}
$$

只要 $x \mapsto x_0$ 可逆（即特征线不交汇），这个公式给出光滑解。

---

## §2 Shock：特征线交汇的必然后果

### 2.1 Burgers 方程的经典例子

$f(u) = u^2/2$，即 $\partial_t u + u \partial_x u = 0$。特征线速度 $f'(u) = u$：**值大的地方走得快，值小的地方走得慢**。

**初值**：$u_0(x) = 1 - x$（$x \in [0,1]$ 内线性下降，外为 $0/1$）。

- 左边（$u_0 = 1$ 区域）的特征线以速度 $1$ 向右；
- 右边（$u_0 = 0$ 区域）的特征线以速度 $0$；
- 中间线性区的特征线以 $u_0(x_0) = 1-x_0$ 为速度，**越靠左越快**。

后果：快的特征线追上慢的。$t = t^\star \coloneqq 1$（= 初值梯度绝对值的倒数）时它们在 $x = 1$ 点交汇。**$t > t^\star$ 之后，(1.3) 给出**多值**"解"——物理上不可接受**。

### 2.2 一般原理

**命题 2.1**：设 $u_0$ 光滑，某处 $\frac{d}{dx}[f'(u_0)] < 0$（即 $f'$ 的初值在该点递减）。则存在有限 $t^\star$ 使 (1.1) 的光滑解在 $t = t^\star$ 处 blow up（$\partial_x u \to \infty$）。

**证明**：沿特征线 $\partial_x u$ 满足 Riccati 方程 $\frac{d}{dt}(\partial_x u) = -f''(u)(\partial_x u)^2$；初值负时有限时间 blow up。

### 2.3 物理对应

Burgers 方程是可压缩无粘流体**动量方程**的简化模型。特征线交汇对应流体微元叠加——物理上产生**激波**（压强 / 密度跳跃）。$u$ 在 shock 处不连续。

---

## §3 弱解：放宽"解"的定义

经典意义下 (1.1) 在 $t > t^\star$ 后没有解。怎么办？**分部积分**。

### 3.1 弱解的定义

把 (1.1) 乘以光滑测试函数 $\varphi \in C_c^\infty(\mathbb R \times [0, \infty))$ 并在 $\mathbb R \times [0,\infty)$ 上积分，分部积分：
$$
\int_0^\infty \int_{\mathbb R} \left[ u \partial_t \varphi + f(u) \partial_x \varphi \right] dx \, dt + \int_{\mathbb R} u_0(x) \varphi(x, 0) \, dx = 0. \tag{3.1}
$$

**定义 3.1（弱解）**：$u \in L^\infty(\mathbb R \times [0,\infty))$ 称为 (1.1) 的**弱解**，如果 (3.1) 对所有 $\varphi \in C_c^\infty$ 都成立。

**意义**：只要 $u, f(u)$ 局部可积，(3.1) 就有意义，不要求 $u$ 光滑。(1.1) 的 "解" 被从 $C^1$ 松弛到 $L^\infty$。

### 3.2 Rankine–Hugoniot 条件

假设 $u$ 是分段 $C^1$ 弱解，在曲线 $x = s(t)$ 上有跳跃 $u_L = u(s^-, t), u_R = u(s^+, t)$。把 (3.1) 限制在跳跃附近分部积分，得

$$
\boxed{\dot s(t) (u_L - u_R) = f(u_L) - f(u_R),} \tag{3.2}
$$

即**跳跃速度 = 通量差 / 变量跳跃**。这是 **Rankine–Hugoniot 跳跃条件**，物理上是通量守恒的直接结果。

### 3.3 弱解不唯一！

坏消息：弱解**不唯一**。

**例子（Burgers）**：$u_0(x) = 0$ 对 $x < 0$，$u_0 = 1$ 对 $x > 0$。

- **解 A**：**Shock 解**。$u_L = 0, u_R = 1$，(3.2) 给 $\dot s = 1/2$，即 $u = 0$ ($x < t/2$)、$u = 1$ ($x > t/2$)。这是一个有效弱解。
- **解 B**：**Rarefaction 解**（光滑过渡）。$u(x, t) = 0$ ($x \leq 0$), $x/t$ ($0 < x < t$), $1$ ($x \geq t$)。这也是一个有效弱解。

两者都满足 (3.1)。物理上，(B) 是熵增的（特征线分开，散出），(A) 是熵减的（特征线 converge 回来，不物理）。

**教训**：弱解太多，需要额外条件挑出"物理的"那一个。这个条件就是**熵条件**。

---

## §4 Kruzhkov 熵解

### 4.1 熵对 (entropy / entropy flux pair)

**定义 4.1**：设 $\eta: \mathbb R \to \mathbb R$ 凸，$q: \mathbb R \to \mathbb R$ 满足 $q'(u) = \eta'(u) f'(u)$。称 $(\eta, q)$ 是 (1.1) 的一个**熵对**。

**动机**：若 $u$ 光滑，则 $\partial_t \eta(u) + \partial_x q(u) = \eta'(u)[\partial_t u + f'(u)\partial_x u] = 0$——$\eta$ 沿解守恒。这类似统计物理里的 $H$-定理。

### 4.2 熵不等式

对 $u$ 存在跳跃的弱解，$\eta(u)$ 不再守恒。**物理熵**应该满足一个不等式（类比 $H$-定理：$H$ 不增）。但这里符号是反的：物理上我们要 entropy 增（耗散），对应数学上
$$
\partial_t \eta(u) + \partial_x q(u) \leq 0 \text{ (in distributions).} \tag{4.1}
$$

**注意符号**：因为传统 $\eta$ 取**凸**而非**凹**，(4.1) 是 "$\leq 0$"。

### 4.3 Kruzhkov 熵（1970）

**精选**：取 $\eta_k(u) = |u - k|$（关于 $u$ 分段线性凸），对应 $q_k(u) = \mathrm{sgn}(u - k)(f(u) - f(k))$。这叫 **Kruzhkov 熵**，$k$ 取遍 $\mathbb R$。

**定义 4.2（Kruzhkov 熵解）**：$u \in L^\infty$ 称 (1.1) 的**熵解**，如果它是弱解且对所有 $k \in \mathbb R$，
$$
\partial_t |u - k| + \partial_x \big[\mathrm{sgn}(u - k)(f(u) - f(k))\big] \leq 0 \text{ (in distributions).} \tag{4.2}
$$

### 4.4 唯一性

**定理 4.3（Kruzhkov 1970）**：对 $u_0 \in L^\infty$，(1.1) 的熵解存在、唯一，且对两个熵解 $u, v$ 有 $L^1$-contraction
$$
\|u(\cdot, t) - v(\cdot, t)\|_{L^1} \leq \|u_0 - v_0\|_{L^1}, \quad \forall t \geq 0. \tag{4.3}
$$

**这是古典 PDE 理论的王冠之一**。唯一性由 Kruzhkov 的"doubling variables" 技巧证明。

### 4.5 意义（对路径 A）

- $L^1$-contraction (4.3) 是路径 A Theorem 2 的工具：把 Wasserstein 距离控制到 $L^1$ 距离，再用 (4.3) 控制时间演化——这是"扩散模型误差不在 PDE 时间轴上爆炸"的关键。
- Kruzhkov 熵作为正则项（路径 A loss 里的 $\mathcal L_2$）是有理论依据的：最小化这个正则就是把解推向熵解流形。

---

## §5 粘性消失法（Vanishing Viscosity）

这一节给路径 A 最重要的物理图像。

### 5.1 粘性化的 PDE

考虑**正则化**的 (1.1)：
$$
\partial_t u^\varepsilon + \partial_x f(u^\varepsilon) = \varepsilon \partial_{xx} u^\varepsilon, \quad \varepsilon > 0. \tag{5.1}
$$

$\varepsilon$ 是"人工粘性"。(5.1) 是**抛物方程**，标准理论保证存在唯一光滑解。

### 5.2 粘性极限

**定理 5.1**：在 $f$ 合适条件下（比如 $f \in C^2$，$u_0 \in L^\infty \cap BV$），
$$
u^\varepsilon \to u \text{ in } L^1_{\mathrm{loc}}, \quad \varepsilon \to 0^+,
$$
且 $u$ 是 (1.1) 的**Kruzhkov 熵解**。

**证明梗概**：
1. (5.1) 的光滑解 $u^\varepsilon$ 对任意凸 $\eta$ 满足
$$
\partial_t \eta(u^\varepsilon) + \partial_x q(u^\varepsilon) = \varepsilon \eta'(u^\varepsilon) \partial_{xx} u^\varepsilon = \varepsilon \partial_{xx} \eta(u^\varepsilon) - \varepsilon \eta''(u^\varepsilon)(\partial_x u^\varepsilon)^2.
$$
最后一项 $\leq 0$（$\eta$ 凸）。
2. 取 $\varepsilon \to 0$：左边形式上变为 $\partial_t \eta + \partial_x q \leq 0$。
3. BV 估计保证 $u^\varepsilon$ 有一致 BV 紧，抽子列收敛。

### 5.3 物理解读

粘性极限选出的唯一解就是熵解。**物理：真实流体有极小粘性（比如空气 $\nu \sim 10^{-5}$ m²/s），极限下得到的理想流体 shock 就是熵条件选出的唯一一个**。

### 5.4 对路径 A 的启示（关键）

L1 §2.6 我们已经把 VE 扩散的前向过程写成
$$
\partial_{\tilde\tau} p = \Delta p, \quad \tilde\tau = \sigma^2(\tau)/2.
$$
这是一个扩散 PDE。**扩散模型的前向"噪声水平" $\sigma^2$ 本质就是一个人工粘性**。

现在把这个观察和路径 A 骨架的 **parameterization (B)**（viscosity-matched schedule）串起来：
$$
\sigma^2(\tau) = 2 \nu_{\mathrm{phys}} \tau.
$$
这样扩散的人工粘性和目标 PDE 的物理粘性**同量级**地衰减。当反向采样走到 $\tau = 0$ 时，扩散的粘性归零，与目标 PDE 的无粘极限一致——**我们的 schedule 自然对齐了粘性消失法**。这是 Theorem 4 的物理本质。

---

## §6 BV 空间：shock 解的自然栖息地

### 6.1 全变差

**定义 6.1**：$u: \mathbb R \to \mathbb R$ 的**全变差**
$$
\mathrm{TV}(u) = \sup \left\{ \sum_{i=1}^{k-1} |u(x_{i+1}) - u(x_i)| : x_1 < \cdots < x_k \right\}.
$$

**例子**：$u = \mathbb 1_{[0,1]}$ 有 $\mathrm{TV}(u) = 2$（0→1 + 1→0 两次跳跃）。光滑 $u$ 有 $\mathrm{TV}(u) = \int |u'|$。

### 6.2 BV 空间

**定义 6.2**：$BV(\mathbb R) = \{u \in L^1_{\mathrm{loc}} : \mathrm{TV}(u) < \infty\}$，配范数 $\|u\|_{BV} = \|u\|_{L^1} + \mathrm{TV}(u)$。

### 6.3 BV 解的几个性质

- **Helly 选取定理**：$BV$ 中一致 bounded 的序列有几乎处处收敛子列。这在"粘性极限取子列"论证里被反复使用。
- **熵解在 BV**：若 $u_0 \in BV$，则 (1.1) 的熵解 $u(\cdot, t) \in BV$ 且 $\mathrm{TV}(u(\cdot, t)) \leq \mathrm{TV}(u_0)$（全变差不增）。
- **shock 的几何**：BV 函数的跳跃集是**可数个 rectifiable 曲线**——这给路径 A parameterization (C) 中"signed distance to shock set"一个几何基础。

### 6.4 路径 A 的用处

路径 A 的损失
$$
\mathcal L_3 = \mathcal L_{\mathrm{DSM}} + \lambda_{\mathrm{BV}} \mathrm{TV}(D_\theta)
$$
把网络输出的 Tweedie 预测 $D_\theta \approx u_0$ 限制在 BV 空间里。这使得**生成样本至少是一个 BV 函数**，从而：
1. 和目标熵解处于同一空间；
2. 在 Theorem 3 证明里可以用 Helly 抽紧子列。

---

## §7 Lax 熵条件：Shock 的可解释版本

Kruzhkov 熵条件对所有凸 $\eta$ 一致要求，数学上优雅但不直观。对单个 shock 有一个等价的**几何条件**。

**定义 7.1（Lax 熵条件，1957）**：$f$ 凸。弱解的 shock 曲线 $s(t)$ 上跳跃 $(u_L, u_R)$ 满足 **Lax 熵条件**当且仅当
$$
\boxed{f'(u_L) \geq \dot s(t) \geq f'(u_R).} \tag{7.1}
$$

**直观**：(7.1) 说 shock **左右两边的特征线都走向 shock**（$f'(u_L)$ 是左边特征线速度，比 shock 快；$f'(u_R)$ 慢于 shock）。即**shock 是 characteristic-absorbing**，不是 characteristic-emitting。

对凸 $f$，Lax 条件 ⇔ Kruzhkov 熵条件（Oleinik 1957）。

### 7.2 路径 A Theorem 4 的声明

Theorem 4 要证：在 $\sigma(\tau) \to 0$ 极限下，EntroDiff 生成的解的 shock 位置满足 (3.2) 的 Rankine–Hugoniot + (7.1) 的 Lax 条件。证明思路：

- 用 Score Shocks Theorem 5.5 给出 score 层 interfacial layer 的跳跃结构；
- 用路径 A 的 parameterization (C) 将 interfacial layer 和物理 shock 对齐；
- 从 Score Shocks 的 "speciation time" 推出物理 shock 形成时间；
- Lax 条件由 score layer 的 profile 方向决定（tanh profile 的符号）。

---

## §8 一些常用标量守恒律（实验 benchmark 的候选）

路径 A 的 5 个实验 benchmark 里有三个是 1D 标量守恒律：

| 方程 | $f(u)$ | 性质 |
|---|---|---|
| Burgers | $u^2/2$ | 凸通量；shock 为 compression wave |
| Buckley–Leverett | $u^2 / (u^2 + M(1-u)^2)$ | **非凸通量**；shock + rarefaction 混合结构 |
| Traffic flow (LWR) | $u(1-u)$ | 凹通量；shock = 堵车波 |
| Linear advection | $au$ | 平凡例（无 shock） |

**Buckley–Leverett 的意义**：非凸通量下 Lax 条件不足以确定唯一 shock；需要更强的 Oleinik 条件（或等价 Kruzhkov）。这是路径 A 把理论推广到 non-convex 情形的关键案例。

---

## §9 小结 + L5 预告

**L4 一句话**：双曲 PDE 的解可以有 shock；shock 解不唯一，需要 **Kruzhkov 熵条件** 选出物理上正确的一个；熵解 = 粘性消失极限 = 全变差有界的 BV 函数。

**三件核心**：
1. Rankine–Hugoniot (3.2) + Lax 熵条件 (7.1)：刻画 shock；
2. Kruzhkov 熵 (4.2) + $L^1$-contraction (4.3)：刻画熵解唯一性 + 稳定性；
3. 粘性消失法 (5.1)：物理极限下选出熵解。

**L5 要做的事**：
- 把 L1 §6 留下的 Score–Burgers 对应彻底展开（Theorem 4.1 & 4.3 of Score Shocks）；
- 讲清楚**为什么 score 层的 shock（speciation）和物理层的 shock（Kruzhkov）在我们的路径 A 里是同一个几何对象**；
- 给出路径 A Theorem 1（Double-Burgers Coupling）的完整陈述和证明 sketch；
- 最后把前四讲 + L5 串成一条叙事：物理 Burgers shock → 数据分布的 mode 分界 → score interfacial layer → Score Shocks 结构 → EntroDiff parameterization (C) 的设计。

---

## 附录 A：常见疑问

**Q1**：我能不能不用 Kruzhkov，只用 Lax？
A：$f$ 凸时可以（Oleinik 证明等价）。$f$ 非凸时必须用 Kruzhkov（考虑 Buckley–Leverett）。路径 A benchmark 包含非凸通量，所以我们统一用 Kruzhkov。

**Q2**：Systems（Euler, shallow water）怎么办？
A：Systems 的熵解理论复杂得多（Lax–Friedrichs shock admissibility, Glimm scheme, BV estimates 局限）。路径 A 在 Theorem 2/3 里先做**scalar**情形；systems 作为实验（E3/E4）验证 + 定理的一般化留作 future work。这点写作时明确。

**Q3**："粘性消失法"和 JKO 有关系吗？
A：间接关系。粘性消失的 $\varepsilon \to 0$ 极限是**时间方向**的奇异极限；JKO 是**时间离散**的极限。两者在"都用到 $W_2$ 估计 / BV 紧性"技术上相似，但属于不同数学问题。路径 A Theorem 5（JKO 对应）主要处理光滑 schedule 下的扩散；Theorem 4（shock 一致性）处理粘性消失极限。

**Q4**：路径 A 的 loss $\mathcal L_2$（Kruzhkov 熵正则）具体怎么写？
A：
$$
\mathrm R_{\mathrm{ent}}(u) = \mathbb E_k \left[ \max\!\big\{ 0, \partial_t |u - k| + \partial_x (\mathrm{sgn}(u - k)(f(u) - f(k))) \big\} \right],
$$
其中 $k \sim \mathcal U(u_{\min}, u_{\max})$ 随机采样。训练时对每个 minibatch 采一组 $k$。这是一种 "soft enforcement"——把 (4.2) 的不等式的 positive part 作为惩罚。具体实现细节留给路径 A 代码阶段。

**Q5**：BV 正则在神经网络上怎么算？
A：输出 $D_\theta$ 在网格上，$\mathrm{TV}$ 用 finite difference 的 $\ell^1$ 范数近似：$\mathrm{TV}(D_\theta) \approx \sum_i |D_\theta(x_{i+1}) - D_\theta(x_i)|$。梯度可传。细节到代码阶段再讨论。
