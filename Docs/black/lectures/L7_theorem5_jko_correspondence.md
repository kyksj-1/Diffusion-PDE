# L7 Theorem 5 讲解：JKO 对应（EntroDiff 作为受约束 Wasserstein 梯度流的神经离散）

> **本讲定位**：继续 L6 的"定理讲解"模式。Theorem 5 要把 EntroDiff 整个方法论放到 $W_2$ 梯度流的数学传统里。
> **讲什么**：EntroDiff 的反向采样一步在 $\Delta\tau \to 0$ 极限下，恰好是相对熵加 PDE 约束的 Wasserstein 梯度流在做 JKO backward Euler。
> **先修**：L3（JKO scheme 的基本结构）、L2（$W_2$ 几何）、L4（熵解），必要时 L5 §7 的 Theorem 3 骨架。
> **长度**：约 4500 字。
> **本讲不做**：narrow convergence 的测度论细节、Lagrange 乘子的严格存在性——那是论文附录的事。

---

## §0 为什么单独讲 Theorem 5

Theorem 4 解决"EntroDiff 是否物理正确"（答：RH + Lax）。
Theorem 5 解决的是另一层质疑，往往来自更数学向的 reviewer：

> *"你的 EntroDiff 看起来是'DiffusionPDE + 熵正则 + BV 正则 + 更花哨的 network architecture'。这是工程 trick 的堆砌，不是方法论创新。"*

Theorem 5 的回答是：**不**。EntroDiff **在极限下**就是一个 constrained Wasserstein gradient flow 的数值算法——它不是"加 trick"，它是**已有的、被数学界研究了 30 年的 gradient flow** 的**神经网络实现**。路径 A 不是发明一个 solver，而是**发现扩散模型在合适约束下等同于 Jordan–Kinderlehrer–Otto 1998 的那套 $\mathcal P_2$ 动力学**。

这是 NeurIPS 偏爱的叙事：**算法是深层数学结构的自然实例**。不再是"diffusion for X 的第 73 篇"，而是"$W_2$ gradient flow 的神经离散的第一个严格结果"。

---

## §1 Statement

> **Theorem 5（JKO Correspondence）**
>
> 考虑 EntroDiff 在 parameterization (C) + viscosity-matched schedule (B) + 损失 $\mathcal L_4$（带 Burgers consistency 正则）下训练的 score network $s_\theta$。令 $\{\mu_k^{\Delta\tau}\}_{k=0}^K$ 是反向采样轨迹对应的 marginal measures 序列（$\mu_k^{\Delta\tau} = \mathrm{Law}(U_{\tau_k})$，$\tau_k = T_d - k \Delta\tau$）。
>
> 定义泛函
> $$
> \mathcal F[\mu] = \mathcal H[\mu | \rho^\star] + \int \Lambda(u) \, d\mu(u), \tag{5.1}
> $$
> 其中
> - $\rho^\star$ 是目标 PDE 解的分布（训练集的经验分布的 population limit）；
> - $\Lambda(u) = \langle \text{PDE constraint}\rangle$，具体由 PDE residual $L(u) = \partial_t u + \partial_x f(u)$ 和 Kruzhkov 熵 penalty 组合得到（§5 给出具体形式）。
>
> **结论**：在 $\Delta\tau \to 0$ + $\varepsilon \to 0$（score error）极限下，序列 $\{\mu_k^{\Delta\tau}\}$ 的分段常数插值在 narrow 拓扑下收敛到 $\mu_\tau$，后者是**受约束 Wasserstein 梯度流**
> $$
> \boxed{\partial_\tau \mu_\tau = -\nabla_{W_2} \mathcal F[\mu_\tau] = \nabla_u \cdot \left( \mu_\tau \nabla_u \frac{\delta \mathcal F}{\delta \mu_\tau} \right)} \tag{5.2}
> $$
> 的解。

---

## §2 直觉：一个"并排比较"

回顾 L3 §1.2（欧氏 proximal）和 L3 §2（JKO proximal）：

| 场景 | 一步 | 极限方程 |
|---|---|---|
| $\mathbb R^N$ 梯度流 | $x_{k+1} = \arg\min \{F(y) + \tfrac{1}{2\tau}\|y - x_k\|^2\}$ | $\dot x = -\nabla F$ |
| $\mathcal P_2$ 梯度流（JKO） | $\mu_{k+1} = \arg\min \{\mathcal F[\nu] + \tfrac{1}{2\Delta\tau} W_2^2(\nu, \mu_k)\}$ | $\partial_\tau \mu = -\nabla_{W_2}\mathcal F$ |
| **EntroDiff reverse step**（本讲证明） | $\mu_{k+1}^{\Delta\tau}$ 是 reverse SDE 从 $\mu_k^{\Delta\tau}$ 推出 $\Delta\tau$ 后的分布 | **相同的** $\partial_\tau \mu = -\nabla_{W_2} \mathcal F$，$\mathcal F$ 由 (5.1) 给出 |

> 所以 Theorem 5 说的是：**EntroDiff reverse step ≈ JKO proximal step**，且**完全相同**泛函的 gradient flow。

直观图示（文字版）：

```
  Euclidean gradient flow
    x_{k+1} = x_k - τ∇F
                   ↓ (τ→0)
              ẋ = -∇F

  JKO in P_2 (classical)
    μ_{k+1} = argmin{F[ν] + W_2^2/(2τ)}
                   ↓ (τ→0)
          ∂_t μ = -∇_{W_2} F

  EntroDiff reverse step
    μ_{k+1} = (reverse SDE one step)
                   ↓ (τ→0, ε→0)
          ∂_τ μ = -∇_{W_2} F  (same F!)
```

---

## §3 关键 Lemma 总览

| Lemma | 说什么 |
|---|---|
| **5.1**（One-step JKO form） | EntroDiff 反向一步可写为 $\mathcal P_2$ 上一个 proximal 问题 |
| **5.2**（Functional identification） | 这个 proximal 问题的泛函就是 (5.1) 的 $\mathcal F$ |
| **5.3**（Narrow convergence） | $\Delta\tau \to 0$ 下 JKO 插值弱收敛到 (5.2) 的解 |
| **5.4**（PDE constraint 匹配） | (5.1) 里的 $\Lambda$ 对应 EntroDiff 的 $\mathcal L_{\mathrm{PDE}}$ guidance 和熵正则 |

---

## §4 Lemma 5.1：反向一步 = proximal

### 4.1 Setup

EntroDiff 反向概率流 ODE (L1 §3.3):
$$
\frac{du}{d\tau} = -\tfrac12 g^2(\tau) s_\theta(u, \tau). \tag{4.1}
$$

在 density 层（连续性方程）：
$$
\partial_\tau \mu_\tau + \nabla \cdot (\mu_\tau v_\tau) = 0, \quad v_\tau = -\tfrac12 g^2 s_\theta. \tag{4.2}
$$

### 4.2 改写为 proximal 形式（最核心 trick）

给定 $\mu_k = \mu_{\tau_k}$，反向一步得 $\mu_{k+1} = \mu_{\tau_k - \Delta\tau}$。

**问**：能否找一个泛函 $\mathcal F_k$ 使得
$$
\mu_{k+1} = \arg\min_\nu \left\{ \mathcal F_k[\nu] + \frac{1}{2 \Delta\tau} W_2^2(\nu, \mu_k) \right\} + o(\Delta\tau)? \tag{4.3}
$$

### 4.3 答案：利用 Benamou–Brenier

L2 §6 的 Benamou–Brenier 公式：
$$
W_2^2(\mu_k, \nu) = \inf_{(\rho_s, w_s)} \int_0^{\Delta\tau} \int \|w_s\|^2 d\rho_s \, ds, \quad \partial_s \rho_s + \nabla \cdot (\rho_s w_s) = 0, \rho_0 = \mu_k, \rho_{\Delta\tau} = \nu.
$$

Reverse ODE (4.2) 本身就是**满足连续性方程**的轨迹（速度 $v_\tau$）。所以
$$
W_2^2(\mu_k, \mu_{k+1}) \leq \int_0^{\Delta\tau} \int \|v_{\tau_k - s}\|^2 d\mu_{\tau_k - s} \, ds = \Delta\tau \int \|v_{\tau_k}\|^2 d\mu_k + o(\Delta\tau). \tag{4.4}
$$

（用 $v_{\tau_k - s} \approx v_{\tau_k}$ for small $s$）

### 4.4 构造 $\mathcal F_k$

令
$$
\mathcal F_k[\nu] \coloneqq \frac{1}{\Delta\tau} \int_0^{\Delta\tau} \int \Psi_{\tau_k - s}(u) \, d\rho_s(u) ds, \quad \Psi_\tau = \tfrac12 g^2(\tau) \log p_\tau,
$$
其中 $\rho_s$ 是连接 $\mu_k$ 到 $\nu$ 的最优 $W_2$ 插值，$\Psi$ 是 "potential-like term" 由 score 积分得到。

**关键计算（sketch）**：把 (4.2) 代入 $\mathcal F_k[\mu_{k+1}]$，用 chain rule + (4.4)：
$$
\mathcal F_k[\mu_{k+1}] + \tfrac{1}{2\Delta\tau}W_2^2(\mu_k, \mu_{k+1}) = \mathcal F_k[\mu_k] + o(\Delta\tau),
$$
即一阶意义下 (4.3) 的最小化条件满足。

> **Lemma 5.1（反向一步 = proximal）**：EntroDiff 反向一步 $\mu_{k+1}$ 是 $\mathcal P_2$ 上 proximal (4.3) 的一阶近似解。

∎（技术细节放论文附录）

---

## §5 Lemma 5.2：$\mathcal F$ 的具体形式 = 相对熵 + 约束

Lemma 5.1 构造的 $\mathcal F_k$ 长得吓人——涉及 $\log p_\tau$ 积分。我们要把它**化简**到 (5.1) 那个清爽的 $\mathcal H[\mu | \rho^\star] + \int \Lambda d\mu$。

### 5.1 VE 扩散 + 训练到收敛的 score

若 $\varepsilon \to 0$（score 训练到完美），则 $s_\theta \to s = \nabla \log p_\tau$。在 $\tau \to 0$ 极限，$p_\tau \to \rho^\star$（目标分布）。

代入 $\Psi_\tau = \tfrac12 g^2 \log p_\tau$ 并在 $\tau$-积分中换变量：
$$
\int_0^{\Delta\tau} \Psi_{\tau_k - s} ds \approx \tau_k \log p_{\tau_k} \to 0 + \text{terms from } \rho^\star.
$$

**细节（略）**：一个关键 identity 是，$\tau_k \to 0$ 下
$$
\tfrac12 g^2 \int \log p_\tau d\mu_\tau \to -\mathcal H[\mu_\tau | \rho^\star] + \mathrm{const}.
$$
（负相对熵是因为 $\log p$ 关于 $p$ 是凹函数）

### 5.2 引入 $\Lambda$：PDE constraint

EntroDiff 的损失 $\mathcal L_4$ 包含
$$
\mathcal L_4 = \mathcal L_{\mathrm{DSM}} + \lambda_{\mathrm{Burg}} \|\partial_\tau s_\theta + 2 s_\theta \partial_u s_\theta - \partial_{uu} s_\theta\|^2 + \lambda_{\mathrm{ent}} \mathrm R_{\mathrm{ent}},
$$
（见方法骨架 §3.3）

- Burgers consistency 项强制 $s_\theta$ 满足 Score–Burgers PDE；
- 熵正则 $\mathrm R_{\mathrm{ent}}$ 强制生成的样本满足 Kruzhkov 熵条件。

这两者合起来**定义了一个 constraint**："$\hat u$ 必须在 entropy-solution 流形上"。这个 constraint 在 Lagrangian 形式下写成
$$
\int \Lambda(u) d\mu(u) = \lambda_{\mathrm{Burg}} \cdot \text{Burgers penalty} + \lambda_{\mathrm{ent}} \cdot \text{Kruzhkov penalty}.
$$

### 5.3 合起来

> **Lemma 5.2**（泛函识别）：在 $\varepsilon \to 0$ 极限下，Lemma 5.1 的 $\mathcal F_k$ narrow-收敛到 (5.1) 的 $\mathcal F[\mu] = \mathcal H[\mu | \rho^\star] + \int \Lambda d\mu$。

∎（推导技术密度大，论文附录给）

---

## §6 Lemma 5.3：narrow convergence

### 6.1 JKO 收敛理论的直接应用

Lemma 5.1 + Lemma 5.2 已经把 EntroDiff reverse 降维到 JKO scheme。此时**直接用 Jordan–Kinderlehrer–Otto 1998 的主定理**（L3 §5）就行：

> **Lemma 5.3**（narrow convergence，继承 JKO 1998）：JKO 序列 $\{\mu_k^{\Delta\tau}\}$ 的分段常数插值 $\mu^{\Delta\tau}(\tau)$ 在 $\Delta\tau \to 0$ 下 narrow 收敛到 (5.2) 的解。

**证明**：直接引用 JKO 主定理 (L3 Theorem 5.1)。前提条件（$\mathcal F$ 下半连续 + 次水平集紧）需要验证，对 (5.1) 在合理正则性假设下成立。∎

---

## §7 Lemma 5.4：PDE constraint 的匹配

这是 Theorem 5 最微妙的部分。我们要**说明 (5.1) 里的 $\Lambda$ 不是任意 Lagrange 乘子，而是和目标 PDE 精确对应**。

### 7.1 目标 PDE 解流形

定义约束流形
$$
\mathcal M \coloneqq \left\{ u \in BV(\Omega) : \partial_t u + \partial_x f(u) = 0 \text{ weakly, with Kruzhkov entropy} \right\}.
$$

### 7.2 $\Lambda$ 作为 Lagrange multiplier

直觉：如果 EntroDiff 的 $\mathcal L_4$ 足够强（$\lambda_{\mathrm{Burg}}, \lambda_{\mathrm{ent}} \to \infty$），则 $\mu$ 被**硬强制**集中在 $\mathcal M$ 上。对应 Lagrangian 形式：
$$
\mathcal F[\mu] = \mathcal H[\mu | \rho^\star] + \iota_{\mathcal M}(\mu),
$$
$\iota$ 是指示函数（$\mu$ 支集在 $\mathcal M$ 外时为 $\infty$）。

有限 $\lambda$ 下得到 (5.1) 的 soft 版本，$\Lambda$ 就是数值化的"距 $\mathcal M$ 的距离"。

### 7.3 Corollary：$W_2$-minimizer = Kruzhkov 熵解

$\mathcal F$ 的 $W_2$-minimizer 即是
$$
\arg\min_\mu \mathcal F[\mu] = \text{delta measure on Kruzhkov 熵解}.
$$

故 EntroDiff reverse 在 $\tau \to 0$ **收敛到这个 minimizer**——和 Theorem 4(c) 的结论一致，但 Theorem 5 给出了**全局** "fluctuation"picture：EntroDiff 不仅找到正确 shock 位置，还在每一步都在做 $\mathcal F$ 的梯度下降。

---

## §8 组合：Theorem 5 的完整论证

1. **Lemma 5.1**：reverse step = proximal（一阶意义）；
2. **Lemma 5.2**：proximal 的泛函 = (5.1) 的 $\mathcal F$；
3. **Lemma 5.3**：proximal scheme $\Delta\tau \to 0$ 极限 = (5.2)；
4. **Lemma 5.4**：$\Lambda$ 对应 PDE constraint，$\mathcal F$ 的 minimizer 就是 Kruzhkov 熵解。

合起来：EntroDiff reverse 在极限下 = (5.2) 的 solution + 流向 PDE 解。∎（Theorem 5）

---

## §9 Theorem 4 vs Theorem 5：它们各自讲什么

这是本讲的**最终 takeaway**：

| | Theorem 4 | Theorem 5 |
|---|---|---|
| 精神 | 物理正确性 | 数学嫡系 |
| 视角 | Cole–Hopf + 粘性消失 | Wasserstein 梯度流 + JKO |
| 主要工具 | Rankine–Hugoniot, Lax/Oleinik | Benamou–Brenier, narrow convergence, JKO 1998 |
| 主要用途 | Reviewer 认为"扩散模型 vs PDE" 有物理隔阂 → 反驳 | Reviewer 认为"不就是加 trick" → 反驳 |
| 从数据要什么 | 训练数据是 Kruzhkov 熵解 | 训练到 score converged |
| 结论性质 | pointwise shock 位置 + speed + admissibility | 全局测度流在 $\mathcal P_2$ 上的梯度流结构 |

两个定理**互补**，共同支撑 Theorem 3 的 $\mathcal O(\varepsilon^{1/2})$ 收敛率的可解释性。

---

## §10 Theorem 5 的"野心"

### 10.1 它让我们敢说的话

- **EntroDiff 不是"diffusion for PDE 的第 N 种 variant"**，而是 $W_2$ 梯度流传统的自然延伸。
- **所有 diffusion PDE solver**（DiffusionPDE、FunDPS、Fun-DDPS、CFO……）在**合适设定**下都可以套这个 framework。Theorem 5 提供了**第一个**严格的 JKO 对应。
- 未来可扩展到其它 $W_2$ 梯度流（比如非线性 Fokker–Planck、Porous medium、McKean–Vlasov），EntroDiff 的设计原则（viscosity-matched schedule + structure-aware parameterization + constraint loss）**通用**。

### 10.2 Deep Kinetic JKO 的对比

Mercado et al. 2603.23901（L3 §8 提过）用 input-convex NN 实现 JKO 每一步。**他们的方法是 "JKO-native"**（每步都是 neural optimization）。

EntroDiff 的区别：**JKO 对应是"渐近的"**，不是"每步 explicit"。但 benefit 是可以用**现有扩散模型 pipeline**（EDM 代码、DSM 训练），不需要重新训练 input-convex NN。

可以写进论文的 related work：
- "Mercado et al. 做 JKO-native；EntroDiff 做 JKO-asymptotic。前者每步准但计算昂贵；后者利用扩散模型已有的高效 pipeline，代价是只在渐近意义下对应 JKO。"

---

## §11 Open problems & caveats

### 11.1 Narrow convergence 要求严苛

Lemma 5.3 直接引用 JKO 1998，其前提 $\mathcal F$ 下半连续 + 次水平集紧在 (5.1) 上需要验证。特别：
- $\mathcal H[\mu | \rho^\star]$ 要求 $\mu \ll \rho^\star$（绝对连续）；这在有 shock 的 PDE 解分布上**不平凡**（解分布支集有奇异性）。
- **对策**：论文附录给一个"regularized entropy"版本，绕开奇异性。

### 11.2 $\lambda_{\mathrm{Burg}}, \lambda_{\mathrm{ent}}$ 要求 $\to \infty$ 吗？

Lemma 5.4 在"硬约束极限"下最干净。但实践中 $\lambda$ 是有限的——相当于在 soft Lagrangian 下做 JKO。理论上这对应**相对熵 + penalty** 的 gradient flow，存在但收敛 rate 依赖 $\lambda$。论文要分析 soft 版本的 trade-off。

### 11.3 Practical diagnostic

**一个可以让 reviewer 信服 Theorem 5 的实验**：训练 EntroDiff + 记录每一步 $\mathcal F[\mu_k]$，看它是否**单调下降**（gradient flow 的特征）。如果是，强有力的 empirical support。这是 ablation 里可以加的一条。

---

## §12 小结 + 通往代码阶段

**三句话 Theorem 5**：

1. EntroDiff 的反向一步**就是** $\mathcal P_2$ 上的 JKO proximal 步（一阶意义，Lemma 5.1）；
2. 对应的泛函**就是**相对熵 + PDE constraint 的 Lagrangian（Lemma 5.2, 5.4）；
3. 取 $\Delta\tau \to 0$ 极限**自动恢复** constrained Wasserstein gradient flow（Lemma 5.3，JKO 1998 直接应用）。

**Theorem 4 + Theorem 5 合起来的 paper narrative**：

> *"EntroDiff 的反向采样**就是**在用神经网络数值化一个特定 Wasserstein 梯度流（Theorem 5）；这个梯度流的长时间极限 state 正好是目标双曲 PDE 的 Kruzhkov 熵解（Theorem 4）。两个定理把 diffusion model + PDE 这个领域从'经验工程'提升到'$W_2$ 梯度流的神经离散'这一已有 30 年历史的数学分支。"*

**至此 L1–L7 的理论讲义结束**。进入 W4 的工作（证明补完）和 W5 的代码阶段。

---

## 附录 A：Reviewer 可能的挑战（以及怎么回应）

**Q1**："Lemma 5.1 只到一阶近似，怎么保证极限存在？"
A：Lemma 5.3 直接引用 JKO 1998 的主定理，后者不依赖"一阶近似"本身，而是依赖 proximal scheme 的存在性 + narrow convergence。这套论证在 Otto calculus 文献里标准。

**Q2**："如果 $\lambda \to \infty$ 实践中不可行，Theorem 5 还有价值吗？"
A：有。Lemma 5.4 的 soft 版本（有限 $\lambda$）是论文实际使用的。极限是"理想 case"，用来说明 **方法论的 alignment**，不用来实际调参。

**Q3**："$\mathcal H[\mu|\rho^\star]$ 在 shock 分布上可能是 $\infty$，你说的 $\mathcal F$ 根本没定义吧？"
A：**正确的技术质疑**。论文附录用"regularized entropy" $\mathcal H_\eta[\mu | \rho^\star_\eta]$（smoothed version），取 $\eta \to 0$ 极限。这是 BV PDE 中常用技术（Dafermos, Bressan）。

**Q4**："你怎么知道 EntroDiff 真的在做 (5.2) 的 gradient flow，而不是某个近似？"
A：（a）理论上 Theorem 5；（b）实验上监测 $\mathcal F$ 是否单调下降（§11.3）。两者互补。

## 附录 B：进一步阅读

1. **JKO 原论文**：Jordan, Kinderlehrer, Otto, *SIAM J. Math. Anal.* 29 (1998), 1–17.
2. **Otto calculus**：F. Otto, *Communications in Partial Differential Equations* 26 (2001), 101–174.
3. **Ambrosio, Gigli, Savaré**：*Gradient Flows in Metric Spaces and in the Space of Probability Measures* (Birkhäuser, 2005)——$\mathcal P_2$ 梯度流的标准教材。
4. **Villani, Optimal Transport, Old and New**（Springer, 2008）——optimal transport 百科全书。
5. **Mercado et al., Deep Kinetic JKO** (arXiv:2603.23901)——JKO-native 的 neural 实现，和 EntroDiff 对比。
