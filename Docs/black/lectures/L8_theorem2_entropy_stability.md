# L8 Theorem 2 讲解：熵解稳定性（基线收敛率）

> **本讲定位**：补齐论文"三个定理的讲解三部曲"的最后一讲（L6 讲 Theorem 4，L7 讲 Theorem 5，本讲 L8 讲 Theorem 2）。
> **Theorem 2 的作用**：在**不用** EntroDiff 结构化设计（即只用 parameterization (A) + loss $\mathcal L_0$，相当于 naive diffusion PDE solver）的情形下，给出一个收敛率 —— 它是 Theorem 3 要改进的"基线"。**这定理的价值在于定位问题，而不是给出好结果**。
> **先修**：L1（反向 SDE、DSM、Tweedie）、L4（Kruzhkov 熵解、$L^1$-contraction）、L5（Score Shocks Theorem 6.3 的误差放大）。
> **长度**：约 4000 字。

---

## §0 为什么 Theorem 2 值得单独讲

直觉上会觉得"Theorem 2 是 baseline，不如 Theorem 3 impressive，跳过得了"。但**论文写作角度**上它极其重要：

1. **动机定位**：Theorem 2 明确告诉 reviewer 和读者——**不做结构化改进，收敛率有 $\exp(\Lambda T)$ 指数放大，实际中灾难性差**。这是 Theorem 3 存在的理由。
2. **机制揭示**：Theorem 2 的证明**精确地定位误差放大在哪里发生**（interfacial layer），这直接指导 Theorem 3 的 parameterization (C) 设计——网络该在哪里打补丁。
3. **数学工具库**：Theorem 2 用到的所有工具（Girsanov 传播、$L^1$-contraction、Gronwall），Theorem 3 都继承，只是把 Gronwall 常数压下来。**先学会"baseline 证明"**，再学"改进证明"容易得多。

所以 L8 的精神是：**把 baseline 证明讲得明白**，让你看清"哪一步把 $\exp(\Lambda T)$ 塞进来"——然后 L5 §7 Theorem 3 的证明骨架读起来就像是"精准拆掉那一步"。

---

## §1 Statement

> **Theorem 2（Entropy-Solution Stability，baseline version）**
>
> 假设：
> - 目标 PDE 为 1D 标量守恒律 $\partial_t u + \partial_x f(u) = 0$，$f \in C^2$；
> - EntroDiff 采用 parameterization (A)（标准 EDM 去噪器）+ 损失 $\mathcal L_0$（标准 DSM，无结构化正则）；
> - Score 网络训练误差 $\mathbb E_\tau \|s_\theta(\cdot, \tau) - s(\cdot, \tau)\|_{L^2(p_\tau)}^2 \leq \varepsilon^2$；
> - 反向采样总时间 $T_d$，对应 score amplification 指数 $\Lambda \approx \mathrm{SNR}/2$（由 Score Shocks Theorem 6.3）。
>
> **结论**：对任意物理时间 $t \in [0, T]$，
> $$
> \boxed{W_1\!\left(\mathrm{Law}(\hat u(\cdot, t)), \mathrm{Law}(u^\star(\cdot, t))\right) \leq C_1 \, \varepsilon \, \exp(\Lambda T_d).} \tag{2.1}
> $$
> 其中 $\hat u$ 是 EntroDiff 采样输出，$u^\star$ 是目标 PDE 的 Kruzhkov 熵解，$C_1$ 是仅依赖 $f$ 和初值分布的常数。

### 1.1 和 Theorem 3 的对比（一行）

- **Theorem 2**（baseline）：$W_1 \leq C_1 \varepsilon \exp(\Lambda T_d)$ — **指数放大**。
- **Theorem 3**（structured）：$W_1 \leq C_2 \varepsilon^{1/2}$ — **次线性**。

$\varepsilon$ 典型取 $10^{-3}$，$\Lambda T_d \sim 5$（$\mathrm{SNR} \sim 10$, $T_d \sim 1$）：
- Theorem 2 bound: $10^{-3} \cdot e^5 \approx 0.15$
- Theorem 3 bound: $\sqrt{10^{-3}} \approx 0.03$

**差 5 倍**。$\varepsilon$ 越小差距越大。

---

## §2 为什么度量选 $W_1$

L2 §4.4 表格已经讨论过，但值得在这里强调：

**$L^1$/TV/KL 不行**，因为它们对 **shock 位置小平移**饱和：shock 位置错 $\varepsilon$ 的话，
- $L^1$ 误差 $\sim |u_L - u_R| \cdot \varepsilon$（跳跃幅度 × 平移）—— 只要跳跃不是 0，这比 $\varepsilon$ 本身还要大的 order。
- TV/KL 在 shock 支集不重合的"极端"情形直接饱和到 $\mathcal O(1)$。

**$W_1$ 刚好合适**：shock 位置错 $\varepsilon$ 得到 $W_1 = |u_L - u_R| \cdot \varepsilon$（从 1D 分位数公式 L2 (3.1) 直接验证），这是**线性**。所以 $W_1$ 是**区分 "shock 位置正确" 和 "shock 跳跃正确"** 的最自然度量。

**路径 A 的整个收敛率分析都在 $W_1$ 下进行**。

---

## §3 证明骨架（3 步）

先给一个高空俯瞰：

```
(Score error ε)
      │  Step 1: 反向 SDE 的误差传播（Girsanov/Chen-Chewi）
      ▼
(Sample measure error: W_1(Law(û), ρ_T) ≤ ...)
      │  Step 2: 把样本误差推到 PDE 层（L¹-contraction）
      ▼
(PDE trajectory error: W_1(Law(û(·,t)), Law(u*(·,t))) ≤ ...)
      │  Step 3: 组合 + Gronwall
      ▼
(Final: W_1 ≤ C · ε · exp(Λ T_d))
```

下面逐步展开。

---

## §4 Step 1：Score error → sample error

### 4.1 反向 SDE 误差传播的经典 bound

**标准结果（Chen–Chewi–Salim–Zhang 2023; Benton–De Bortoli et al. 2024）**：反向 SDE 从 initial Gaussian $\pi$ 演到 $\hat u$ ~ Law($\hat u$)，而 true 反向 SDE 会演到 $\rho_T$（目标数据分布）。两者 TV 距离（或 KL）满足
$$
\mathrm{KL}\!\left(\mathrm{Law}(\hat u) \,\|\, \rho_T\right) \leq C \int_0^{T_d} \mathbb E_{u \sim p_\tau} \|s_\theta(u, \tau) - s(u, \tau)\|^2 d\tau + \mathrm{err}(\pi), \tag{4.1}
$$
$\mathrm{err}(\pi)$ 是初始 Gaussian approximation error（$\mathrm{err}(\pi) \to 0$ 当 $T_d \to \infty$，通常忽略）。

用 $W_1 \leq C \sqrt{\mathrm{KL}}$ 的 Pinsker-class 不等式（在 bounded support 下）：
$$
W_1(\mathrm{Law}(\hat u), \rho_T) \leq C \varepsilon. \tag{4.2}
$$

这是一个**线性**的 $\varepsilon$ 关系。**$\exp(\Lambda T_d)$ 还没出现**——它不在 Step 1 里。

### 4.2 细节的 caveat

(4.1) 的"$C$"其实包含了 Score Shocks 的放大因子，但在 $L^2$ global average 的意义下被**平摊**掉。从 naive 的角度看 Step 1 是线性的。真正的麻烦在 Step 2（下一节）。

---

## §5 Step 2：Sample error → PDE trajectory error

### 5.1 目标

我们有 $\hat u \sim \mathrm{Law}(\hat u)$（初值的 approximate 样本），需要得到其在 PDE 演化后的分布 $\mathrm{Law}(\hat u(\cdot, t))$，并与真实 $\mathrm{Law}(u^\star(\cdot, t))$ 比较。

### 5.2 把 $\hat u$ 推进物理时间

设 $S_t: BV(\Omega) \to BV(\Omega)$ 是目标 PDE 的 Kruzhkov 熵解半群。对**任意两个初值** $v_0, w_0 \in BV$，L4 §4.4 的 $L^1$-contraction (4.3) 说
$$
\|S_t v_0 - S_t w_0\|_{L^1} \leq \|v_0 - w_0\|_{L^1}. \tag{5.1}
$$

**跳步**：把 (5.1) 的 $L^1$ 换成 $W_1$——好消息是在 1D BV 上 $W_1 \leq \|v_0 - w_0\|_{L^1}$（实际上 $W_1(\delta_v, \delta_w) = \|v - w\|_{L^1}$，这是 1-Lipschitz 下的 Kantorovich-Rubinstein (L2 §4.5) 的简单推论），所以
$$
W_1(\mathrm{Law}(S_t v_0), \mathrm{Law}(S_t w_0)) \leq \mathbb E \|v_0 - w_0\|_{L^1}. \tag{5.2}
$$

### 5.3 把初始 sample error 映射到 $L^1$

(4.2) 给的是 $W_1$ 距离。从 $W_1$ 到 $L^1$ 之间有个 **gap**（$W_1 \leq L^1$ 但不反过来）。在 BV 环境下我们有：

**Lemma**（BV estimate）：若 $v_0, w_0 \in BV(\Omega)$ 有一致 BV bound $M$，则
$$
\|v_0 - w_0\|_{L^1} \leq C_M \sqrt{W_1(\delta_{v_0}, \delta_{w_0})} \quad \text{或} \quad \leq C_M W_1(\delta_{v_0}, \delta_{w_0}). \tag{5.3}
$$

（后者在 1D 下由分位数公式直接成立；论文给出精确常数）

### 5.4 组合 Step 2

(5.2) + (5.3) + (4.2) 给：
$$
W_1(\mathrm{Law}(\hat u(\cdot, t)), \mathrm{Law}(u^\star(\cdot, t))) \leq C_M \cdot C \cdot \varepsilon. \tag{5.4}
$$

**问题来了**：(5.4) 没有 $\exp(\Lambda T_d)$！线性 $\varepsilon$！这看起来比 (2.1) 好很多。**那 (2.1) 的 $\exp(\Lambda T_d)$ 是哪来的？**

答：**(4.1) 的 $C$ 实际上依赖 $\Lambda$**——Score Shocks Theorem 6.3 的放大因子在 score 估计误差的 pointwise 意义下是指数放大。在 $L^2$ global 意义下它被平滑掉，但**在 interfacial layer 附近**（权重最大的区域）它一直是指数的。

下一节把这点说清楚。

---

## §6 Step 3：$\exp(\Lambda T_d)$ 从哪一步塞进来

### 6.1 Score Shocks Theorem 6.3 的精确陈述

回顾 L5 §3(iii)：对反向轨迹通过 interfacial layer 的那部分，
$$
\|\hat u - u\|_{\text{pointwise near shock}} \leq \varepsilon \exp(\Lambda T_d). \tag{6.1}
$$

**关键**：(6.1) 是 **pointwise** 放大，不是 $L^2$-averaged 放大。如果我们用 (4.1) 的 $L^2$-averaged 误差 bound，这个放大被**隐藏**。但**一旦要把 $W_1$ 控制到 shock 位置这种"局部"量**，(6.1) 就冒出来。

### 6.2 精细 bound 的修正

正确的 Step 1 bound **不是** (4.2) 那么简单。实际上
$$
W_1(\mathrm{Law}(\hat u), \rho_T) \leq C \sqrt{ \int_0^{T_d} \lambda(\tau) \|s_\theta - s\|^2 d\tau }, \tag{6.2}
$$
其中 $\lambda(\tau)$ 是**权重函数**，在 interfacial layer 附近 $\lambda \sim \exp(2\Lambda(\tau_{\text{layer}} - \tau))$。

**当 $\tau$ 离 speciation time 近时**，$\lambda$ 爆炸。这是 Score Shocks Theorem 6.3 在 $L^2$ bound 里的体现。

### 6.3 Gronwall 整合

(6.2) 把 score 误差通过权重 $\lambda(\tau)$ 放大。精细 bound：
$$
W_1(\mathrm{Law}(\hat u), \rho_T) \leq C \varepsilon \sqrt{\int_0^{T_d} \lambda(\tau) d\tau} \leq C' \varepsilon \exp(\Lambda T_d). \tag{6.3}
$$

代入 Step 2 的 (5.2)+(5.3)：
$$
W_1(\mathrm{Law}(\hat u(\cdot, t)), \mathrm{Law}(u^\star(\cdot, t))) \leq C_M \cdot C' \varepsilon \exp(\Lambda T_d). \tag{6.4}
$$

这就是 Theorem 2 的 (2.1)。∎（Theorem 2）

---

## §7 关键观察：$\exp(\Lambda T_d)$ 的"定位"

上面证明最精华的一点是：**$\exp(\Lambda T_d)$ 的来源可以被精确定位到 Step 1 的 (6.2)——specifically 到 interfacial layer 附近的权重 $\lambda(\tau)$**。

这个"定位"给路径 A Theorem 3 的 parameterization (C) 一个明确的修复目标：

> *(C) 的 tanh 结构让 interfacial layer 附近的 $\|s_\theta - s\|$ 变小（因为结构已经 built-in，网络不需要从头学），从而 (6.2) 里 $\lambda(\tau) \|s_\theta - s\|^2$ 的乘积在 interfacial layer 处也被压下。于是 $\exp(\Lambda T_d)$ 不再放大任何 error，最终收敛率改善为 $\varepsilon^{1/2}$。*

这就是为什么 L5 §7 Theorem 3 的 Step 3 ("去除 $\exp$ 放大") 听上去玄，但**本质上就是把 (6.2) 的 interfacial-weighted error 替换成 $\mathcal O(\varepsilon^2)$**（见 L5 (7.2)）。

---

## §8 三个定理的"故事闭合"

Theorem 2 / 3 / 4 / 5 合起来讲的 paper narrative：

| 定理 | 作用 |
|---|---|
| **Theorem 2**（baseline） | 揭示 naive 方法的 $\exp(\Lambda T_d)$ 灾难性放大 —— **motivation** |
| **Theorem 1**（结构） | Double-Burgers 耦合，几何上指出物理 shock 和 score shock 同址 —— **核心观察** |
| **Theorem 3**（主定理） | parameterization (C) 把 $\exp(\Lambda T_d)$ 换成 $\mathcal O(\varepsilon^{1/2})$ —— **核心贡献** |
| **Theorem 4**（物理） | 生成的 shock 满足 RH + Lax —— **物理正确性** |
| **Theorem 5**（数学嫡系） | EntroDiff = 受约束 Wasserstein 梯度流的神经离散 —— **数学地位** |

**读者/reviewer 心路**：
1. 为什么要管这个问题？(Theorem 2 回答：naive 方法不够好)
2. 你的新观察是什么？(Theorem 1 回答：双 Burgers 耦合)
3. 你用这个观察做了什么？(C2: parameterization (C))
4. 效果怎么量化？(Theorem 3 回答：$\varepsilon^{1/2}$)
5. 物理正确吗？(Theorem 4 回答：满足 RH + Lax)
6. 数学有深度吗？(Theorem 5 回答：是 $W_2$ gradient flow 的神经离散)

**每一个定理回答一个 reviewer 问题**。五个定理形成**闭合的论证链条**。

---

## §9 证明工具的分类

五个定理的证明用到的工具（方便你记忆 & 在论文写作时引用）：

| 工具 | 出现在 | 难度 |
|---|---|---|
| Anderson 反向 SDE | L1, T2-T5 都用 | 标准 |
| Denoising Score Matching + Tweedie | L1, T3 关键 | 标准 |
| Kantorovich–Rubinstein ($W_1$ 对偶) | L2, T2-T3 | 标准 |
| Brenier 定理 ($W_2$ 最优 map) | L2, T5 | 中等 |
| Benamou–Brenier 动力学 | L2, T5 | 中等 |
| JKO 1998 主定理（narrow convergence） | L3, T5 | 中等 |
| Kruzhkov $L^1$-contraction | L4, T2-T3 | 中等 |
| 粘性消失法 + BV 紧性 (Helly) | L4, T4 | 中等 |
| Rankine–Hugoniot + Lax | L4, T4 | 标准 |
| Score–Burgers 恒等式 (Cole–Hopf) | L5, T1-T5 | 中等 |
| Score Shocks Theorem 6.3（误差放大） | L5, T2-T3 | 论文化技术 |
| Chen–Chewi–Salim–Zhang 误差传播 | T2-T3 | 前沿 |

**绝大部分是"标准 PDE + OT + score-based diffusion 的组合拳"**。没有需要新发明的数学工具——这**对 NeurIPS 非常友好**（reviewer 不用学新东西就能 follow）。

---

## §10 为什么 Theorem 2 在论文里值得 1 页

给论文写作的参考意见：

- **放在 Theorem 3 之前**：intro 讲完 motivation 后，第一个 formal 结果就是 Theorem 2，说"看，直接做会指数放大"。
- **证明放在正文给 sketch**（1/2 页），完整证明附录（3-4 页）。
- **强调"我们把它作为 baseline，用来定位问题在哪"**——这个姿态比"我们证明了这个事"更加 powerful。
- 对比 Theorem 3 时画一张图：横轴 $\varepsilon$ 对数尺度，纵轴 $W_1$，两条线：$\varepsilon \exp(\Lambda T_d)$ vs $\sqrt\varepsilon$。这张图是整篇论文的 hero figure 候选。

---

## §11 小结

**Theorem 2 三句话**：

1. **Statement**：naive diffusion PDE solver 在 $W_1$ 下对熵解的误差是 $\varepsilon \exp(\Lambda T_d)$，**指数放大**。
2. **证明**：Girsanov/Chen-Chewi 把 score error 传播到 initial distribution error，再用 Kruzhkov $L^1$-contraction 推到 PDE trajectory error；Score Shocks Theorem 6.3 的 interfacial weight 给出 $\exp(\Lambda T_d)$ 的精确来源。
3. **作用**：**机制定位 + Theorem 3 motivation**，不是独立的好结果。

**全 8 讲闭合**：

```
L1: 扩散 ⇔ FP                    理论基石：反向 SDE, DSM, Tweedie
L2: OT + W_2                    理论基石：Brenier, Otto calculus
L3: JKO                          理论基石：W_2 proximal, JKO 1998
L4: 熵解 + BV + 粘性消失         理论基石：Kruzhkov, L¹-contraction, RH, Lax
L5: Score-Burgers + Theorem 1   桥梁 + 核心观察
L6: Theorem 4                    物理正确性
L7: Theorem 5                    数学嫡系
L8: Theorem 2                    baseline (motivation)
```

Theorem 3（主定理）的讲解留作 L9 待开（用户之前选"补 Theorem 2"优先，Theorem 3 骨架在 L5 §7，完整讲解可以以后做）。

至此理论讲义完整闭合。你应该能：
- 独立陈述全部 5 个定理；
- 独立复述各自的证明骨架；
- 看懂论文写作时的 narrative flow；
- 在 reviewer 讨论中为每个定理找到对应的质疑回应。

---

## 附录 A：Theorem 2 的"副产物"

Theorem 2 的证明给了一些"非预期"的副产物，有些可以直接用在论文里，有些留作 future work：

1. **Score Shocks Theorem 6.3 的另一种表述**：我们的 (6.3) 可以看作 Score Shocks 原论文结果在 $W_1$ distance 下的 reformulation。是一个 mini contribution。

2. **TV regularization 的 PDE 意义**：若不用 Parameterization (C)，而只在 loss 里加 TV regularizer（方法骨架的 $\mathcal L_3$ 的 BV 项），可以让 $\exp(\Lambda T_d)$ 的常数**降**（但不完全消）。这部分理论在路径 A 作为 *Corollary 2.1* 附录给。

3. **Chaotic PDE 情形（future）**：若目标 PDE 是混沌的（比如 Kuramoto-Sivashinsky），Kruzhkov $L^1$-contraction 不成立，Step 2 崩。需要新工具（比如 Bedrossian–Blumenthal 类型的概率性 stability）。Statistical Error Bounds 论文 (2602.18794) 在这方面有启示，**是我们 future work 的一个方向**。

## 附录 B：进一步阅读

1. **Chen, Chewi, Salim, Zhang 2023**：*Sampling is as easy as learning the score*, ICLR 2023 —— Step 1 的核心技术。
2. **Benton et al. 2024**：*Nearly $d$-linear convergence bounds for diffusion models via stochastic localization*, ICLR 2024 —— 更 sharp 的 dim-dependent bounds。
3. **Kruzhkov 1970**：*First order quasilinear equations in several independent variables*, Math. USSR Sbornik 10, 217–243 —— $L^1$-contraction 的原论文。
4. **Score Shocks (2604.07404) §6**：Theorem 6.3 误差放大的完整推导。
