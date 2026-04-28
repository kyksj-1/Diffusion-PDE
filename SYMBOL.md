# SYMBOL.md · EntroDiff 论文符号 Master Sheet

> **阅读对象**：AI（跨 session 对齐写作）+ 人（review）
> **维护节奏**：每轮论文写作前必读；新增 / 改名符号必须三处同步：本文件 ↔ `paper/black/macros/notation.tex` ↔ `Docs/path_A_method_skeleton.md §3.1`
> **首版**：2026-04-26（W2，重构版）
> **角色**：Anima Anandkumar 教授（项目级 CLAUDE.md）

---

## 0 · 设计原则（不变）

1. **正交命名**：
   - 扩散时间 $\tau \in [0, T_d]$ ⊥ 物理时间 $t \in [0, T_{\mathrm{phys}}]$；
   - 状态空间 $u \in \R^d$（$d = N_x$，整个 PDE 解的网格离散）；
   - 物理空间 $x \in \Omega \subset \R$（连续坐标）；
   - 不同空间使用不同字体：$u$（状态向量，可视作 $\R^d$ 点）vs $\mathbf{u}(x)$（物理空间上的函数）。
2. **专业 vocabulary**：score field / push-forward / Kantorovich–Rubinstein duality / viscosity-matched schedule / Kruzhkov entropy solution / Rankine–Hugoniot / BV-aware parameterization。
3. **一处定义，全文引用**：所有专业符号必须通过 `macros/notation.tex` 的 LaTeX 宏调用；sections 中**禁**裸写 `W_1`、`s_\theta`、`\nu_{\mathrm{phys}}` 等。
4. **作用域显式**：每符号标注首次出现章节；同名异义须在不同作用域中显式声明（如 $\rho_t$ 物理 vs $\rho_\tau$ 扩散）。
5. **未来扩展**：本表中带 `[planned]` 的符号尚未在 `notation.tex` 中定义；写到对应章节时同步新增。

---

## 1 · 数集与基础概率（block A）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| `\R` | $\R$ | 实数集 | 全文 |
| `\N` | $\N$ | 自然数集 | 全文 |
| `\Z` | $\Z$ | 整数集 | 全文 |
| `\E` | $\E$ | 期望 | 全文 |
| `\Prob` | $\Prob$ | 概率测度 | 全文 |
| `\Law` | $\Law$ | 法则 / 分布映射；$\Law(X) = $ rv $X$ 的分布 | 全文 |

## 2 · 概率距离与函数空间（block B）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| `\Wass{p}` | $W_p$ | $p$-Wasserstein 距离（$p=1,2$ 用得最多） | 全文 |
| `\KL` | $\KL$ | Kullback–Leibler 散度 | 主要 §6 / 附录 |
| `\TV` | $\TV$ | 全变差半范数 $\TV(f) = \int |\partial_x f|\,dx$ | §3 / §5 / §6 |
| `\BV` | $\BV$ | 有界变差函数空间 | §3 / §6 |
| `\Ent` | $\Ent$ | 相对熵 | §6（Theorem 5） |
| `\Lip` | $\Lip$ | Lipschitz 常数 / 类 | §6 |

## 3 · 扩散过程与时间轴（block C）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| `\tau` | $\tau$ | 扩散时间，$\tau \in [0, T_d]$；$\tau = T_d$ 噪声端，$\tau = 0$ 数据端 | 全文 |
| —（直接写 `T_d`） | $T_d$ | 扩散时间上界 | §3 / §5 / §6 |
| —（直接写 `\tau_{\mathrm{end}}`） | $\tau_{\text{end}}$ | early-stopping 终端，$\tau_{\text{end}} > 0$ | 附录 A1 |
| `\sigtau` | $\sigma(\tau)$ | 噪声尺度 | 全文 |
| `\Gtau` | $G_\tau$ | 热核 $(4\pi\tau)^{-d/2}\exp(-\|u\|^2/4\tau)$ | §3 / 附录 A1 |
| `\ptau` | $p_\tau$ | noised 状态密度 $p_\tau = \rho^\star \ast G_\tau$ | §3 / §6 |
| `\rhotau` | $\rho_\tau$ | 扩散时间 $\tau$ 处的分布（与 $p_\tau$ 同物） | §3 / 附录 |
| `\rhotrue` | $\rho^\star$ | 目标 solution 分布（push-forward of init dist） | 全文 |
| `\rhotphys` | $\rho_t$ | PDE 物理时间 $t$ 处的分布（initial 分布的 PDE-flow push-forward） | §6 / §4 整合 |

## 4 · Score field 与神经网络（block D）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| `\score` | $s$ | 真实 score field $s = \nabla_u \log p_\tau$ | 全文 |
| `\sth` | $s_\theta$ | 神经网络 score（参数化 (A)/(B)/(C)） | 全文 |
| `\Dth` | $D_\theta$ | EDM-style 去噪器；$s_\theta = (D_\theta - u)/\sigma^2$ | §5 / §6 |
| `[planned]` `\errsc` | $e$ | score 残差 $e = s_\theta - s$ | §6（Thm 2/3） / 附录 |

## 5 · PDE 物理空间（block E）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| —（直接写 `x \in \Omega`） | $x \in \Omega \subset \R$ | 物理空间坐标 | §2 末尾起 |
| —（直接写 `t`） | $t \in [0, T_{\mathrm{phys}}]$ | 物理时间 | §2 / §6 |
| `\dt` | $\partial_t$ | 物理时间偏导 | 全文 |
| `\dx` | $\partial_x$ | 物理空间偏导 | 全文 |
| `\dtau` | $\partial_\tau$ | 扩散时间偏导 | 全文 |
| `\Lap` | $\Delta$ | Laplace 算子 | 全文 |
| `\flux` | $f$ | 通量函数（如 Burgers 的 $f(u) = u^2/2$） | §2 末尾 / §6 |
| `\physvis` | $\nu_{\mathrm{phys}}$ | PDE 物理黏性 | 全文 |
| `\physsol` | $\mathbf{u}^\star$ | Kruzhkov 熵解（在固定 $T_{\mathrm{phys}}$） | §6 / 附录 A1 |
| `\physsolvis` | $\mathbf{u}^\nu$ | 带粘性 $\physvis$ 的 PDE 解 | 附录 A1 |
| `\initdat` | $\mathbf{u}_0$ | PDE 初值 | §6（Thm 1）/ 附录 |

## 6 · 几何对象（block F）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| `\Shockphys` | $\Sigma_{\mathrm{phys}}(t)$ | 物理 shock 集（在物理时间 $t$） | §6.0 / §6.4 |
| `\Shockscore` | $\Sigma_{\mathrm{score}}(\tau)$ | score-level interfacial layer（在扩散时间 $\tau$） | §6.0 / 附录 |
| `\dShock` | $d_\Sigma(u, \tau)$ | 到 $\Sigma_{\mathrm{score}}(\tau)$ 的符号距离 | 附录 A1 |

## 7 · 训练误差与放大因子（block G）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| —（直接写 `\varepsilon`） | $\varepsilon$ | score-matching 训练误差，$\E\|\sth - s\|^2 \le \varepsilon^2$ | §6 全部 / 附录 |
| `\snr` | $\mathrm{SNR}$ | signal-to-noise ratio | §6（Thm 2） |
| `\amp` | $\Lambda$ | Score Shocks 的指数放大因子（$\Lambda = \sup_\tau \snr/2$） | §1 / §6 |

## 8 · 损失家族（block H）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| `\Ldsm` | $\mathcal L_{\mathrm{DSM}}$ | denoising score matching | §5 / §6 |
| `\Lpde` | $\mathcal L_{\mathrm{PDE}}$ | PDE residual guidance（DiffusionPDE 风格） | §2 (related) / §5 |
| `\Lent` | $\mathcal L_{\mathrm{ent}}$ | Kruzhkov 熵正则项 | §5 |
| `\Lbv` | $\mathcal L_{\mathrm{BV}}$ | TV 正则项 | §5 / §6 |
| `\Lburg` | $\mathcal L_{\mathrm{Burg}}$ | score-Burgers consistency | §5 / §6 |
| `\Rent` | $\mathrm R_{\mathrm{ent}}$ | Kruzhkov 熵 indicator（$\Lent$ 内核） | §5 / §6 |
| —（直接写 `\lambda_{\cdot}`） | $\lambda_{\mathrm{ent}}, \lambda_{\mathrm{BV}}, \lambda_{\mathrm{Burg}}$ | 损失项权重 | §5 |

## 9 · BV-aware 参数化（block I · 论文核心算法）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| `\phisbg` | $\phi^{\mathrm{sm}}_\theta$ | 平滑背景势函数 | §5 / §6 / 附录 |
| `\phissh` | $\phi^{\mathrm{sh}}_\theta$ | shock 符号距离场（zero on shock） | §5 / §6 / 附录 |
| `\jumpamp` | $\kappa_\theta$ | 局部跳跃强度（R–H 约束） | §5 / §6 / 附录 |

## 10 · 轨迹与生成样本（block J · 附录 A1 主用）

| LaTeX 宏 | 数学呈现 | 含义 | 作用域 |
|---|---|---|---|
| `\unat` | $u^\natural(\tau)$ | 真实 score 驱动的反向 ODE 轨迹 | 附录 A1 |
| `\uhat` | $\widehat{u}(\tau)$ | 网络 score 驱动的反向 ODE 轨迹 | 附录 A1 |
| `\uth` | $u^\theta = \widehat{u}(0)$ | 最终生成样本（$\tau = 0$ 时刻） | §6 / 附录 |
| `\muth` | $\mu_\theta = \Law(u^\theta)$ | 生成分布 | §6 / 附录 |

## 11 · 状态向量与物理函数的对应（block K · 跨空间约定）

| 量 | 状态空间表示 | 物理空间表示 | 关系 |
|---|---|---|---|
| 解向量 | $u = (u_1, \dots, u_d) \in \R^d$ | $\mathbf{u}(x), x \in \Omega$ | $u_i = \mathbf{u}(x_i)$；$\Delta x = \abs{\Omega}/d$ |
| 范数（向量） | $\|u\|$（欧氏） | $\|\mathbf{u}\|_{L^p(\Omega)}$ | $\|\mathbf{u}\|_{L^1} = \Delta x \sum_i |u_i|$，$\|\mathbf{u}\|_{L^2}^2 = \Delta x \sum_i u_i^2$ |
| 全变差 | $\sum_i |u_{i+1} - u_i|$ | $\TV(\mathbf{u}) = \int_\Omega |\partial_x \mathbf{u}|\,dx$ | 离散到连续极限一致 |

> 重要：连续–离散等价性使阶段 4 中的"$L^1$–欧氏"放缩在 $\Delta x \to 0$ 极限下与维度 $d$ 无关（详 `Docs/proof/Theorem 3 revised.md` §4.1）。

---

## 12 · 与 `paper/black/macros/notation.tex` 同步映射

> 检查命令：`grep -E '\\\\newcommand' paper/black/macros/notation.tex`

**全部已定义**（见 `notation.tex`，W3 落地的所有宏）：

```
\R, \N, \Z, \E, \Prob, \Law, \KL, \Wass, \TV, \BV, \Ent, \Lip,
\rhotrue, \rhotau, \ptau, \score, \sth, \Dth, \sigtau, \Gtau,
\dt, \dx, \dtau, \Lap, \flux, \physvis, \snr, \amp,
\Ldsm, \Lpde, \Lent, \Lbv, \Lburg, \Rent,
\Shockphys, \Shockscore,
\physsol, \physsolvis, \initdat, \rhotphys,
\errsc,
\dShock,
\phisbg, \phissh, \jumpamp,
\unat, \uhat, \uth, \muth,
\abs, \norm,
\eg, \ie, \cf, \todo, \note
```

---

## 13 · 与 `Docs/path_A_method_skeleton.md §3.1` 同步检查

`path_A` §3.1 当前的 Notation 表与本文件**一致**（基础符号），未列入：
- `\rhotphys` / `\physsol` / `\physsolvis` / `\initdat`（来自 Theorem 3 revised 的物理–扩散正交化）
- BV-aware 分量（`\phisbg / \phissh / \jumpamp`）
- 轨迹细化（`\unat / \uhat / \uth / \muth`）

**约定**：`path_A_method_skeleton.md` 是论文骨架的"高层快照"，本文件 SYMBOL.md 是"实操符号字典"。两者层级不同；当 `path_A` §3.1 与本文件冲突时，**以本文件为准**（CONVENTIONS.md §3）。

---

## 14 · 跨章节符号一致性 checklist

提交前 grep 检查（每写完一节做一次）：

```bash
# 禁止裸写
grep -nE '\$W_[12]\$|\\$W_\{[12]\}\$' paper/black/sections/*.tex     # 应空
grep -nE 's_\\theta' paper/black/sections/*.tex                       # 应空（用 \sth）
grep -nE '\\nu_\\\{?\\mathrm\\\{phys' paper/black/sections/*.tex      # 应空（用 \physvis）
grep -nE '\\rho\^\\\\?star' paper/black/sections/*.tex                # 应空（用 \rhotrue）
```

---

## 15 · 变更日志

| 日期 | 变更 | 决策者 |
|---|---|---|
| 2026-04-28（W3） | 11 个 `[planned]` 宏全部落地 notation.tex：`\physsolvis / \rhotphys / \errsc / \dShock / \phisbg / \phissh / \jumpamp / \unat / \uhat / \uth` (已有) `\muth / \abs / \norm`；§12 更新为"全部已定义" | AI 执行，待用户 review |
| 2026-04-26（W2 · session #N+1） | 首版建立；列入 §1–§11 全文符号；§12 标注 11 个 `[planned]` 宏待加；§13 注明与 path_A §3.1 的层级关系 | AI 起草，待用户 review |
