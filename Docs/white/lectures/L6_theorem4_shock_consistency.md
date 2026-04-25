# L6 Theorem 4 讲解：Shock 位置一致性

> **本讲定位**：把路径 A **Theorem 4** 讲成一个你能向同学复述的故事，不是论文附录里塞 10 页分部积分。
> **讲什么**：EntroDiff 在 $\sigma \to 0$ 极限下，为什么生成的解在 shock 位置上精确满足 Rankine–Hugoniot 跳跃条件和 Lax 熵条件？
> **先修**：L1–L5；特别是 L4 的 RH/Lax（§3、§7）、粘性消失（§5）、L5 的 Score–Burgers 对应（§1–§3）和 parameterization (C)（§6）。
> **长度**：约 4500 字。
> **本讲不做**：完整严格证明（那是论文附录的事）；只给直觉链条 + 关键 lemma 的几何含义。

---

## §0 为什么这个定理值得单独讲

路径 A 的三大贡献 C1/C2/C3 对应 Theorem 1 / parameterization (C) / Theorem 3。Theorem 4 不在这三之中，但它**对 reviewer 特别有冲击力**，原因：

- Theorem 3 证收敛率（$W_1 \leq C \varepsilon^{1/2}$），但收敛到什么其实是 *Theorem 4* 回答的。
- 单说"收敛到熵解"还不够具体——**具体**是 *shock 位置 / shock 速度 / admissibility* 都满足经典 PDE 条件。这就是 Theorem 4 的作用。
- Reviewer 看到 "我们的方法不但给出了 $\mathcal O(\varepsilon^{1/2})$ 的收敛，还保证了 Rankine–Hugoniot + Lax 熵条件"，物理合理性和数学严谨性同时满足，这是 NeurIPS 上很罕见的正经物理 PDE 工作的标志。

所以 Theorem 4 是 **Theorem 3 的"物理化精修"**：把抽象的 $W_1$ 收敛落地为经典 PDE 条件。

---

## §1 Statement（本讲要证明的东西）

先把要证的事讲清楚，一会儿再逐块剖析。

> **Theorem 4（Shock Location Consistency）**
>
> 设以下条件成立：
> - 目标 PDE $\partial_t u + \partial_x f(u) = 0$，$f \in C^2$（非必需凸，允许 Buckley–Leverett 型非凸通量）；
> - 初值分布 $\rho_0 \in \mathcal P_2(BV(\Omega))$；
> - EntroDiff 采用 parameterization (C) + viscosity-matched schedule (B)：$\sigma^2(\tau) = 2 \nu_{\mathrm{phys}} \tau$，$\nu_{\mathrm{phys}}$ 是一个下降到 0 的参数；
> - Score 网络训练误差 $\|s_\theta - s\|_{L^2} \leq \varepsilon$。
>
> 令 $\hat u$ 为反向采样生成的样本，$u^\star$ 是目标 PDE 的 Kruzhkov 熵解。
>
> **结论**：在 $\varepsilon \to 0$ + $\nu_{\mathrm{phys}} \to 0$ 极限下，$\hat u$ 的 shock 集合 $\Sigma_{\hat u}(t)$ 和 shock 跳跃 $(\hat u_L, \hat u_R)$ 几乎处处满足：
>
> **(a) Rankine–Hugoniot 条件**：
> $$
> \dot s(t) = \frac{f(\hat u_L) - f(\hat u_R)}{\hat u_L - \hat u_R}. \tag{4.1}
> $$
>
> **(b) Lax 熵条件**（凸 $f$）或 **Oleinik 条件**（非凸 $f$）：
> $$
> f'(\hat u_L) \geq \dot s(t) \geq f'(\hat u_R). \tag{4.2}
> $$
>
> **(c) Shock 位置收敛**：$\Sigma_{\hat u}(t) \to \Sigma_{u^\star}(t)$ 在 Hausdorff 距离下。

---

## §2 直觉：为什么会这样？一幅图

从 L5 §5 Theorem 1 的 (C) "Shock 集合同址"观察出发，本定理其实就是把那句抽象的"同址"精确化到 Rankine–Hugoniot + Lax。

把所有要用的东西画在一张图上（文字版）：

```
                        (扩散时间 τ → 0)
                               │
                         ┌─────┴─────┐
                         │           │
      Score-Burgers      │           │        Parameterization (C) 硬编码
      (L5 §1–§2)         │           │        tanh interfacial layer
            │            │           │             │
            ▼            ▼           ▼             ▼
     w = -2s 满足       Cole-Hopf 映射          s_θ = ∇φ^sm + (κ/2)tanh(φ^sh/2) ∇φ^sh
     粘性 Burgers        ↔ 热方程                         │
            │                                             │
            └───────────────┬─────────────────────────────┘
                            │
                    Viscosity-matched schedule
                    σ²(τ) = 2 ν_phys τ
                            │
                            ▼
                  (扩散 PDE) ←→ (物理 PDE) 
                     的 vanishing-viscosity 极限同构
                            │
                            ▼
              Shock 速度 = Cole-Hopf 反推的 RH
              Lax 方向 = tanh 的 sign 选择
                            │
                            ▼
                    Theorem 4
```

**一句话**：EntroDiff 的 reverse step 在粘性消失极限下退化为目标 PDE 本身的粘性消失极限；而**目标 PDE 的粘性消失极限 = Kruzhkov 熵解**（L4 §5）；所以 EntroDiff 自动继承 RH + Lax。

下面逐块展开。

---

## §3 证明 ingredients 总览

整个证明分 4 个 Lemma，外加一个组合步骤。

| Lemma | 内容 | 所依赖的讲义 |
|---|---|---|
| L-1 | **Reverse step → viscous PDE on score level**：EntroDiff 的反向 ODE 在 (B)+(C) 下等价于目标 PDE 的粘性化（viscosity $= \nu_{\mathrm{phys}}$）的求解步骤 | L1 §3, L5 §1 |
| L-2 | **Interfacial width matching**：parameterization (C) 里 tanh 层的宽度 = 目标 PDE 粘性 shock 宽度（同阶） | L5 §3(ii) |
| L-3 | **Cole–Hopf 反推**：$\tanh$ 的跳跃幅度与速度场跳跃满足 Burgers 的 RH | L5 §1.4 |
| L-4 | **$\nu_{\mathrm{phys}} \to 0$ 极限下 BV-compactness + Lax 符号判据** | L4 §5, §6, §7 |

组合 L-1 到 L-4 即得 Theorem 4。

---

## §4 Lemma 4.1（L-1）：EntroDiff ≡ 粘性 PDE 的反向求解

### 4.1 Setup

EntroDiff 的反向 probability flow ODE（L1 (3.2)）在 VE 设定下：
$$
\frac{du}{d\tau} = -\tfrac12 g^2(\tau) s_\theta(u, \tau), \quad u_{\tau = T_d} \sim \mathcal N(0, \sigma^2 I). \tag{4.3}
$$

对应 density 层（L1 §3）：
$$
\partial_\tau p_\tau + \nabla \cdot (p_\tau v_\tau) = 0, \quad v_\tau(u) = -\tfrac12 g^2(\tau) s_\theta. \tag{4.4}
$$

对应 score 层（L5 §1）：
$$
\partial_\tau w_\tau + (w_\tau \cdot \nabla) w_\tau = \Delta w_\tau, \quad w_\tau = -2 s_\theta. \tag{4.5}
$$

### 4.2 Viscosity-matched schedule 下的关键观察

取 schedule (B)：$\sigma^2(\tau) = 2 \nu_{\mathrm{phys}} \tau$，即 $g^2(\tau) = 2 \nu_{\mathrm{phys}}$（常数）。代入 (4.5)：
$$
\partial_\tau w_\tau + (w_\tau \cdot \nabla) w_\tau = \Delta w_\tau. \tag{4.6}
$$

这依旧是粘性 Burgers，**单位粘性**（因为我们用累计时间 $\tilde\tau = \sigma^2/2 = \nu_{\mathrm{phys}} \tau$）。

**关键步**：用 Cole–Hopf 反推 (L5 §1.4)。(4.6) 在空间一维下对应
$$
\partial_{\tilde\tau} \log \varphi = \nu_{\mathrm{phys}} \partial_{uu} \log \varphi + \ldots \quad (\varphi \text{ 是 density 的某种 proxy})
$$

事实上可以证明：**(4.6) 的演化等价于目标双曲 PDE + 人工粘性 $\nu_{\mathrm{phys}}$ 的 forward evolution**（放在 $w$-空间上）。

形式化为：

> **Lemma 4.1**：在 parameterization (C) + schedule (B) 下，$w_\tau = -2 s_\theta$ 的演化方程 (4.6) 等价于粘性 PDE
> $$
> \partial_t W + \partial_x (F(W)) = \nu_{\mathrm{phys}} \partial_{xx} W \tag{4.7}
> $$
> 其中 $W, F$ 由 $(w, \text{tanh profile in (C)})$ 明显确定。

**证明 sketch**：
- 在 parameterization (C) 下，$w_\tau(u, \cdot) = \nabla \phi^{\mathrm{sm}} + \tfrac{\kappa}{2}\tanh(\phi^{\mathrm{sh}}/2) \nabla\phi^{\mathrm{sh}}$。
- tanh 部分是 shock 的 "soft description"，其内部结构精确对应粘性 Burgers 的 traveling wave shock profile（L4 §5 粘性消失的 traveling-wave solution）。
- 把 (4.6) 代入，用 $\phi^{\mathrm{sh}}$ 的 eikonal 条件 $|\nabla \phi^{\mathrm{sh}}| = 1$，整理即得 (4.7)。∎

### 4.3 推论

(4.7) 是**目标 PDE 的粘性化**。这意味着：

> **EntroDiff 的反向 ODE 在 (B)+(C) 下，本质上就是在用神经网络 wrap 一个粘性 PDE 求解器。** 粘性大小 $= \nu_{\mathrm{phys}}$，对应 schedule；网络的作用是给出 $\phi^{\mathrm{sm}}, \phi^{\mathrm{sh}}, \kappa$ 这三个"慢变 field"。

这是 Theorem 4 的**第一块砖**：把抽象的"神经网络反向采样"坍缩到具体的"粘性 PDE 数值解"。之后一切都可以用 L4 的经典工具处理。

---

## §5 Lemma 4.2（L-2）：Interfacial 宽度匹配

### 5.1 Score Shocks 的 interfacial 宽度

L5 §3(ii) 给出 interfacial profile (3.1)：
$$
w = \nabla \phi^{\mathrm{sm}} + \tfrac{\kappa}{2}\tanh(\phi^{\mathrm{sh}}/2) \nabla\phi^{\mathrm{sh}},
$$
其 tanh 层的**宽度** $\ell_{\mathrm{score}} \sim |\nabla \phi^{\mathrm{sh}}|^{-1}$（把 $\tanh(x/2)$ 的过渡区看成 $\sim 1$ 宽）。

### 5.2 物理 shock 的粘性宽度

L4 §5 的粘性 PDE (5.1) 对 Burgers 型有经典的 traveling-wave shock：
$$
u^\varepsilon(\xi) = \bar u - \tfrac{u_L - u_R}{2}\tanh\!\left(\frac{\xi (u_L - u_R)}{4 \nu_{\mathrm{phys}}}\right),
$$
其宽度 $\ell_{\mathrm{phys}} = 4 \nu_{\mathrm{phys}} / (u_L - u_R)$。

### 5.3 匹配

> **Lemma 4.2**：parameterization (C) 下，若训练 loss $\mathcal L_3$ 的 BV term 已收敛，则 $\ell_{\mathrm{score}} = \ell_{\mathrm{phys}} + \mathcal O(\nu_{\mathrm{phys}}^2)$，即 score 层 interfacial 宽度和物理 shock 宽度同阶。

**证明 sketch**：
- Viscosity-matched schedule 下两者的粘性都是 $\nu_{\mathrm{phys}}$。
- Score Shocks 的 (3.1) tanh profile 和 Burgers traveling-wave shock 的 tanh profile **除了变量替换外完全相同**（都是热方程 Cole–Hopf 的副产物）。
- 网络 $\phi^{\mathrm{sh}}_\theta$ 在 DSM 训练下收敛到 signed distance to shock set，即 $|\nabla \phi^{\mathrm{sh}}| \to (u_L - u_R)/(4\nu_{\mathrm{phys}})$。代入得 $\ell_{\mathrm{score}} \to 4\nu_{\mathrm{phys}}/(u_L - u_R) = \ell_{\mathrm{phys}}$。∎

### 5.4 意义

Lemma 4.2 说 **EntroDiff 在 shock 附近的"噪声层"和 PDE 在 shock 附近的"粘性层"同宽**。在粘性消失极限 $\nu_{\mathrm{phys}} \to 0$ 时两者同步收缩到 0——所以 score 层 shock 位置收敛到物理 shock 位置。这是 Theorem 4(c) 的由来。

---

## §6 Lemma 4.3（L-3）：Rankine–Hugoniot 的由来

这是 Theorem 4(a) 的核心。

### 6.1 Cole–Hopf 下的跳跃关系

设 $w(u, \cdot)$ 在 $u = u_s(\tau)$ 处有跳跃 $w_L, w_R$。shock 速度 $\dot u_s$ 由 Burgers 方程 RH 给出：
$$
\dot u_s = \frac{(w_L^2/2) - (w_R^2/2)}{w_L - w_R} = \frac{w_L + w_R}{2}. \tag{4.8}
$$
（Burgers 的 RH，$f(w) = w^2/2$）

### 6.2 把 Burgers RH 翻译回物理 PDE

**关键**：在 Lemma 4.1 下，$w_\tau$ 的跳跃 $(w_L, w_R)$ 和物理 PDE 解的跳跃 $(u_L, u_R)$ 有一一对应。具体关系由 Lemma 4.1 的映射 $w \to W$ 给出：$W = \mathcal T(w)$，$\mathcal T$ 是 tanh 层 unpeel 的映射。

对 $W$ 的 RH（直接来自 (4.7)）：
$$
\dot u_s = \frac{F(W_L) - F(W_R)}{W_L - W_R}. \tag{4.9}
$$

### 6.3 Composition

$(w_L, w_R) \xrightarrow{\mathcal T} (W_L, W_R) \xrightarrow{(4.9)} \dot u_s \xrightarrow{\text{identify } W \leftrightarrow u, F \leftrightarrow f}$
$$
\dot u_s = \frac{f(u_L) - f(u_R)}{u_L - u_R}. \tag{4.10}
$$

**这就是目标 PDE 的 Rankine–Hugoniot 条件 (4.1)。** ∎

---

## §7 Lemma 4.4（L-4）：Lax 熵条件的由来

这是 Theorem 4(b) 的核心。

### 7.1 为什么"自动"满足 Lax？

Lax 条件 (4.2) 说**特征线被 shock "吸收"**。对 Burgers $f = u^2/2$，Lax = "$u_L > u_R$"（上游值大于下游）。

**关键问**：EntroDiff 生成的 $(\hat u_L, \hat u_R)$ 为什么总有 $u_L > u_R$（而不是 $u_L < u_R$——后者对应不物理的 "rarefaction shock"）？

### 7.2 答案藏在 $\phi^{\mathrm{sh}}$ 的符号方向

Parameterization (C)：
$$
w = \nabla\phi^{\mathrm{sm}} + \tfrac{\kappa}{2}\tanh(\phi^{\mathrm{sh}}/2) \nabla\phi^{\mathrm{sh}}.
$$

$\phi^{\mathrm{sh}}$ 是 **signed** distance：$\phi^{\mathrm{sh}} > 0$ 在一侧，$< 0$ 在另一侧。tanh 从 $-1$ 到 $+1$ 的过渡**方向**由 $\phi^{\mathrm{sh}}$ 的符号决定。

训练时（Lemma 4.2 证明里提到），$\phi^{\mathrm{sh}}$ 被监督为"指向上游"（$u_L > u_R$ 那边为正）。这是数据驱动：训练集里的 shock 都是物理的 Lax 熵 shock，所以监督信号自动注入正确的符号。

### 7.3 正式化

> **Lemma 4.4**：假设训练集里的 shock 全部是目标 PDE 的 Kruzhkov 熵解的 shock（即全部满足 Lax 条件）。则在 parameterization (C) 下，$\phi^{\mathrm{sh}}_\theta$ 的符号方向被**训练**到与 Lax 一致，从而生成的 $\hat u$ 的 shock 也满足 Lax。

**证明思路**：
- 标准 EDM 训练下，$s_\theta$ 通过 DSM 收敛到 $\nabla \log p_\tau$，$p_\tau = \rho_t * G_\tau$。
- $\rho_t$ 只包含 Kruzhkov 熵解（数据物理），故 $p_\tau$ 的 mode boundary 就是 Lax 熵 shock 的位置。
- $\phi^{\mathrm{sh}}_\theta$ 在训练后的收敛值是 mode boundary 的 signed distance，自动继承 Lax 方向。∎

### 7.4 非凸 $f$（Buckley–Leverett）的推广

非凸通量下 Lax 不足，需 **Oleinik 条件** (L4 §8 脚注)：
$$
\frac{f(u) - f(u_L)}{u - u_L} \geq \dot s \geq \frac{f(u) - f(u_R)}{u - u_R}, \quad \forall u \in [\min, \max](u_L, u_R).
$$

Lemma 4.4 的证明在非凸情形下仍然成立，只是 "Lax 方向" 替换为 "Oleinik 方向"。因为数据集里的 shock 已经是 Kruzhkov 熵解（Oleinik 满足），训练自动对齐。

---

## §8 组合：从 Lemma 到 Theorem

把四个 Lemma 拼起来：

1. **Lemma 4.1**：EntroDiff reverse step = 目标粘性 PDE 的数值解（粘性 $\nu_{\mathrm{phys}}$）。
2. **Lemma 4.2**：interfacial 宽度 $\ell_{\mathrm{score}} \to \ell_{\mathrm{phys}}$。
3. 取 $\nu_{\mathrm{phys}} \to 0^+$：由 L4 §5 粘性消失法，数值解 $\hat u$ 收敛到目标 PDE 的 Kruzhkov 熵解 $u^\star$（$L^1_{\mathrm{loc}}$ 意义）。
4. **Lemma 4.3 + Lemma 4.4**：在这个极限过程中，$\hat u$ 的 shock 满足 RH (4.1) 和 Lax/Oleinik (4.2)。
5. **BV compactness** (L4 §6)：$\hat u \in BV$ 通过 Lemma 4.1 保持一致 bounded；Helly 抽紧子列 → 全序列收敛。
6. **Hausdorff 距离下 shock 位置收敛**：由 Lemma 4.2 的宽度匹配 + Step 3 的 $L^1$ 收敛得到。

$\square$（Theorem 4）

---

## §9 为什么这个证明"漂亮"？

几个值得品味的点：

### 9.1 物理和数学的精准咬合

- **Viscosity-matched schedule (B)** 一开始像是个工程小技巧，现在看它**物理意义**很深：让扩散模型的"反向粘性"和目标 PDE 的粘性**精确对齐**。
- **Parameterization (C)** 一开始像是让训练更稳定的神经网络 trick，现在看它**是把物理 shock 的 traveling wave 结构嵌入 architecture**。
- 两个设计**同时**起作用：(B) 让两套粘性同步衰减，(C) 让两套 profile 结构一致。

### 9.2 Lax 条件"免费"

Lax 熵条件是物理 shock admissibility 的关键——很多数值方法需要**人工强制**（比如 Godunov 通量的 upwinding）。但在 EntroDiff 里：**训练数据是熵解，就自动继承 Lax**。这是数据驱动方法的一个**无偿红利**。

### 9.3 粘性消失法的双重身份

L4 §5 里粘性消失是**物理正则化**；L1 §2.6 里 $\sigma^2$ 是**扩散模型的噪声水平**。Theorem 4 的证明让这两者**同一化**——"噪声水平归零"就是"粘性归零"——所以扩散模型从一开始就"自带粘性消失"，只是之前没人意识到。

---

## §10 风险与 open problems

### 10.1 Systems（Euler, MHD）

本讲义假设 1D scalar 守恒律。Systems 的熵解理论（Glimm, Bressan, Dafermos）复杂得多。Lemma 4.1 的 "$w \to W$" 在 systems 下**未必存在**同样干净的形式——Burgers 是标量特殊性。

**路径 A 对策**：主定理先证 scalar case；systems 作为"experimental extension"（E3 Euler Sod、E4 shallow-water），未必有理论保证，看 reviewer 能否接受。

### 10.2 非凸通量的细节

Buckley–Leverett 的 Oleinik 条件的 "方向继承" 论证（Lemma 4.4 §7.4）比凸情况复杂。论文里可能需要把这部分展开到 2–3 页证明。

### 10.3 训练数据假设

Lemma 4.4 依赖"训练数据里的 shock 都是 Kruzhkov 熵解"。若数据生成用 WENO/Godunov（标准做法），这自动满足；但若有噪声 / 错误标注，符号方向可能错乱。论文的 Limitations 要提这一点。

---

## §11 小结

**三句话总结 Theorem 4**：

1. EntroDiff 在 (B)+(C) 下的反向采样，**数学上等价**于目标 PDE 带粘性 $\nu_{\mathrm{phys}}$ 的前向演化（Lemma 4.1）。
2. Score 层的 tanh interfacial 和物理 shock 的粘性 traveling-wave 在**宽度、形状、速度**上都匹配（Lemma 4.2 + 4.3）。
3. 粘性消失 $\nu_{\mathrm{phys}} \to 0$ 的极限下，**Rankine–Hugoniot 自动满足**（Lemma 4.3 的 Cole–Hopf 反推），**Lax 熵条件也自动满足**（Lemma 4.4 的数据驱动符号继承）。

**下一讲预告（L7）**：Theorem 5 是另一个精致定理——它把 EntroDiff 整个方法论**嵌入到 Wasserstein 梯度流传统**。如果说 Theorem 4 是"让 reviewer 信服物理正确性"，Theorem 5 就是"让 reviewer 信服数学严肃性"。L7 讲怎么把 reverse SDE 的一步写成 constrained JKO proximal。

---

## 附录 A：为什么我在本讲多次"跳过"技术细节？

- Lemma 4.1 的"$w \to W$ 映射"需要 Cole–Hopf 变换和 tanh profile 的精确展开，涉及 3-4 页 PDE 技术代数；
- Lemma 4.2 的"宽度匹配"需要 Score Shocks 原论文 Theorem 5.11 的精确使用；
- BV compactness 的应用需要 Bressan / Dafermos 的经典论证。

这些细节放在论文的 **附录 B** 里写就行。本讲的目标是让你**理解为什么证明走得通** + **四个 Lemma 各自在做什么** + **数据结构和物理结构如何咬合**——这些思想性的东西是 review 讨论、答辩、写 intro 时要用的。数学细节可以查书。

## 附录 B：进一步阅读

1. **L. Evans, PDE**（2010 年版第 3 章）——弱解、Rankine–Hugoniot、Lax 熵的标准教材。
2. **C. Dafermos, Hyperbolic Conservation Laws in Continuum Physics**——systems 的熵解理论。
3. **Score Shocks (arXiv:2604.07404) §5**——interfacial profile 的完整推导。
4. **Sods shock tube 的 Godunov 数值解**——实验 E3 的 ground truth 生成。
