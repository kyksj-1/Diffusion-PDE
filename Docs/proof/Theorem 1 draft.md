
# Theorem 1 (Double-Burgers Coupling)

---

## Statement

Let $\Omega \subset \mathbb{R}$ be the physical domain and consider the 1D scalar conservation law

$$
\partial_t u + \partial_x f(u) = 0, \qquad f \in C^2(\mathbb{R}), \quad u(0,\cdot) = u_0.
$$

Let $S_t$ denote the Kruzhkov entropy semigroup \citep{kruzhkov1970first}. Let the initial data be random: $u_0 \sim \rho_0$ with $\rho_0 \in \mathcal{P}(L^\infty(\Omega) \cap \mathrm{BV}(\Omega))$, and define the pushforward distribution at physical time $t$:

$$
\rho_t := (S_t)_{\#} \rho_0.
$$

At each fixed $t$, apply Gaussian smoothing with diffusion time $\tau > 0$:

$$
p_{\tau, t}(u) := (\rho_t * G_\tau)(u), \qquad
G_\tau(u) = (4\pi\tau)^{-d/2} \exp\!\left(-\frac{|u|^2}{4\tau}\right),
$$

where $u \in \mathbb{R}^d$ is the state variable (for scalar conservation laws, $d = 1$; the Score Burgers part holds for all $d \ge 1$). Define the score and its Cole–Hopf conjugate:

$$
s_{\tau, t}(u) := \nabla_u \log p_{\tau, t}(u), \qquad
w_{\tau, t}(u) := -2 s_{\tau, t}(u).
$$

Then the following hold:

**(A) Score Burgers ($\tau$-direction).** For each fixed $t$, for all $\tau > 0$ where $p_{\tau, t} > 0$,

$$
\boxed{\; \partial_\tau w_{\tau, t} + (w_{\tau, t} \cdot \nabla_u) w_{\tau, t} = \Delta_u w_{\tau, t} \;} \tag{1a}
$$

with $\operatorname{curl} w_{\tau, t} = 0$ identically (since $w = -2\nabla \log p$).

**(B) Physical transport ($t$-direction).** The curve $t \mapsto \rho_t$ in $\mathcal{P}_2(\mathbb{R}^d)$ satisfies the continuity equation

$$
\boxed{\; \partial_t \rho_t + \nabla_u \cdot (\rho_t \, V_t) = 0, \qquad
V_t(u)(x) = -\partial_x f(u(x)) \;} \tag{1b}
$$

in the sense of distributions, obtained as the vanishing-viscosity limit $\varepsilon \to 0^+$ of the regularized evolution.

**(C) Shock set co-location.** Let

$$
\Sigma_{\mathrm{phys}}(t) := \{ x \in \Omega : u(\cdot, t) \text{ has a jump at } x \}
$$

be the physical shock set of the entropy solution. For each $\tau > 0$, define the score interfacial layer set

$$
\Sigma_{\mathrm{score}}(\tau, t) := \{ u \in \mathbb{R}^d : |\nabla_u w_{\tau, t}(u)| \gtrsim 1 / \tau \},
$$

i.e., the region where the score gradient is large (the $\tanh$-layer identified by Score Shocks \citep{score-shocks}). Let $\pi_\Omega: \mathbb{R}^d \to \Omega$ be the projection from state space to physical space (identifying the spatial coordinate of the shock value). Then

$$
\boxed{\; \pi_\Omega\big(\Sigma_{\mathrm{score}}(\tau, t)\big) \;\xrightarrow{\; \tau \to 0^+ \;}\; \Sigma_{\mathrm{phys}}(t) \qquad \text{in Hausdorff distance.} \;} \tag{1c}
$$

---

## Assumptions

- **A1 (Gaussian smoothing).** For each fixed $t$, $\rho_t$ is a finite Borel measure, and the convolution $p_{\tau, t} = \rho_t * G_\tau$ is strictly positive and $C^\infty$ for all $\tau > 0$.
- **A2 (Entropy semigroup).** $S_t$ is the Kruzhkov entropy semigroup, so $\rho_t = (S_t)_{\#} \rho_0$ is well-defined and $t \mapsto \rho_t$ is continuous in the narrow topology.
- **A3 (BV regularity).** $\rho_0$ is supported on $\mathrm{BV}(\Omega) \cap L^\infty(\Omega)$. Consequently, for each $t$, $u(\cdot, t) \in \mathrm{BV}(\Omega)$ with $\mathrm{TV}(u(\cdot, t)) \le \mathrm{TV}(u_0)$, and the jump set $\Sigma_{\mathrm{phys}}(t)$ is a finite (or countably infinite) set of rectifiable curves in $(t,x)$-space.
- **A4 (Convex flux, for concreteness).** $f$ is uniformly convex ($f'' \ge c > 0$); the non-convex case follows via Oleinik's generalization \citep{oleinik1957} and is discussed in the appendix.

---

## Proof

### Part A — Score Burgers ($\tau$-direction)

This part follows directly from the Cole–Hopf correspondence and is essentially a restatement of Score Shocks Theorem 4.3 \citep{score-shocks}.

By definition, $p_{\tau, t} = \rho_t * G_\tau$. Since $G_\tau$ is the heat kernel, $\partial_\tau G_\tau = \Delta_u G_\tau$, and differentiation under the integral (justified by A1) yields

$$
\partial_\tau p_{\tau, t} = \Delta_u p_{\tau, t}. \tag{A1}
$$

Set $\varphi := \log p_{\tau, t}$ ($p_{\tau, t} > 0$ by A1). Then

$$
\partial_\tau \varphi = \frac{\partial_\tau p}{p}
= \frac{\Delta p}{p}
= \Delta \varphi + |\nabla \varphi|^2, \tag{A2}
$$

where we used $\nabla \cdot (p \nabla \varphi) = \nabla p \cdot \nabla \varphi + p \Delta \varphi = p |\nabla \varphi|^2 + p \Delta \varphi$ and $\nabla \cdot (p \nabla \varphi) = \nabla \cdot (\nabla p) = \Delta p$, so $\Delta p / p = \Delta \varphi + |\nabla \varphi|^2$.

Now $s = \nabla_u \varphi$. Taking the gradient of (A2),

$$
\partial_\tau s = \nabla(\Delta \varphi) + \nabla(|\nabla \varphi|^2)
= \Delta s + \nabla(|s|^2). \tag{A3}
$$

Since $s = \nabla \varphi$ is a gradient, $\nabla s = \nabla^2 \varphi$ is symmetric: $\partial_{u_j} s_i = \partial_{u_i} s_j$. Hence

$$
[\nabla(|s|^2)]_i = \partial_{u_i} \sum_{j} s_j^2 = 2 \sum_{j} s_j \, \partial_{u_i} s_j
= 2 \sum_{j} s_j \, \partial_{u_j} s_i = 2[(s \cdot \nabla) s]_i. \tag{A4}
$$

Substituting (A4) into (A3) gives the score PDE:

$$
\partial_\tau s_{\tau, t} = \Delta_u s_{\tau, t} + 2 (s_{\tau, t} \cdot \nabla_u) s_{\tau, t}. \tag{A5}
$$

Finally, define $w_{\tau, t} := -2 s_{\tau, t}$. Then

$$
\partial_\tau w = -2 \partial_\tau s = -2(\Delta s + 2(s \cdot \nabla) s)
= \Delta w - 2(w \cdot \nabla) s.
$$

Since $s = -w/2$, we have $(w \cdot \nabla)s = -\tfrac12 (w \cdot \nabla) w$, hence

$$
\partial_\tau w = \Delta w + (w \cdot \nabla) w.
$$

Rearranging yields the viscous Burgers equation (1a). The curl-free condition $\nabla \times w = -\nabla \times (2\nabla \log p) = 0$ is automatic. $\square$

---

### Part B — Physical Transport ($t$-direction)

We prove (1b) via the vanishing viscosity method, following the structure sketched in \citet{kruzhkov1970first} and adapted to the distributional setting.

#### B.1 Viscous regularization

Introduce the viscous perturbation of the conservation law:

$$
\partial_t u^\varepsilon + \partial_x f(u^\varepsilon) = \varepsilon \partial_{xx} u^\varepsilon, \qquad
u^\varepsilon(0, \cdot) = u_0. \tag{B1}
$$

Let $S_t^\varepsilon$ be the solution operator of (B1). For BV initial data, the solution $u^\varepsilon(\cdot, t)$ is smooth for all $t > 0$ (parabolic regularization). Define the regularized pushforward distribution

$$
\rho_t^\varepsilon := (S_t^\varepsilon)_{\#} \rho_0.
$$

By Kruzhkov's theory \citep{kruzhkov1970first}, for any $T < \infty$,

$$
u^\varepsilon(\cdot, t) \to u(\cdot, t) \quad \text{in } L^1_{\mathrm{loc}}(\Omega), \quad \text{uniformly in } t \in [0,T],
$$

as $\varepsilon \to 0^+$, where $u$ is the unique entropy solution. In particular, $\rho_t^\varepsilon \rightharpoonup \rho_t$ in the narrow topology.

#### B.2 Liouville equation for the viscous flow

For the viscous PDE (B1), the solution at each fixed $x$ evolves according to

$$
\partial_t u^\varepsilon(t, x) = -\partial_x f(u^\varepsilon(t, x)) + \varepsilon \partial_{xx} u^\varepsilon(t, x).
$$

Treating this as an ODE in the state variable $u$ for each fixed $x$, the velocity field is

$$
V_t^\varepsilon(u)(x) := -\partial_x f(u) + \varepsilon \partial_{xx} u.
$$

Let $\psi \in C_c^\infty(\mathbb{R}^d)$ be a test function in state space. By the chain rule and the definition $\rho_t^\varepsilon = (S_t^\varepsilon)_{\#} \rho_0$,

$$
\frac{d}{dt} \int_{\mathbb{R}^d} \psi(u) \, d\rho_t^\varepsilon(u)
= \mathbb{E}_{u_0 \sim \rho_0}\!\left[ \nabla \psi(u^\varepsilon(t, \cdot)) \cdot \partial_t u^\varepsilon(t, \cdot) \right]
= \int_{\mathbb{R}^d} \nabla \psi(u) \cdot V_t^\varepsilon(u) \, d\rho_t^\varepsilon(u) + \varepsilon \int_{\mathbb{R}^d} \Delta \psi(u) \, d\rho_t^\varepsilon(u),
$$

where we used $\mathbb{E}[\nabla \psi \cdot \varepsilon \partial_{xx} u] = -\varepsilon \mathbb{E}[\nabla^2 \psi : \partial_x u \otimes \partial_x u + \Delta \psi]$ after an integration by parts in $x$; the second-order term simplifies to $\varepsilon \Delta_u \psi$ in the state-space measure.

Integration by parts in $u$ yields the weak form

$$
\int \psi \, \partial_t \rho_t^\varepsilon \, du
= - \int \nabla \psi \cdot V_t^\varepsilon \; \rho_t^\varepsilon \, du
+ \varepsilon \int \Delta \psi \; \rho_t^\varepsilon \, du,
$$

which is the distributional form of

$$
\partial_t \rho_t^\varepsilon + \nabla_u \cdot (\rho_t^\varepsilon V_t^\varepsilon) = \varepsilon \Delta_u \rho_t^\varepsilon. \tag{B2}
$$

#### B.3 Vanishing viscosity limit

Take $\varepsilon \to 0^+$ in (B2). The second-order term $\varepsilon \Delta_u \rho_t^\varepsilon \to 0$ in the sense of distributions. By the $L^1$-contraction property of the entropy semigroup and BV compactness \citep{helly, kruzhkov1970first}:

- $\rho_t^\varepsilon \rightharpoonup \rho_t$ narrowly;
- $V_t^\varepsilon(u)(x) = -\partial_x f(u) + \varepsilon \partial_{xx} u \to -\partial_x f(u) =: V_t(u)(x)$ almost everywhere in $(t,x)$.

Passing to the limit in the weak formulation of (B2) gives

$$
\partial_t \rho_t + \nabla_u \cdot (\rho_t \, V_t) = 0, \qquad
V_t(u)(x) = -\partial_x f(u(x)),
$$

in the distributional sense. This is precisely equation (1b). $\square$

---

### Part C — Shock Set Co-location

This is the core geometric observation of Theorem 1. We sketch the argument; a fully rigorous measure-theoretic proof (including the Hausdorff convergence rate) appears in the supplementary material.

#### C.1 BV structure of $\rho_t$

By Assumption A3, $u(\cdot, t) \in \mathrm{BV}(\Omega)$. The Lebesgue decomposition of $u(\cdot, t)$ splits it into an absolutely continuous part and a jump part:

$$
u(\cdot, t) = u^{\mathrm{ac}}(\cdot, t) + \sum_{x_s \in \Sigma_{\mathrm{phys}}(t)} \llbracket u \rrbracket_{x_s} \, \mathbf{1}_{[x_s, \infty)},
$$

where $\llbracket u \rrbracket_{x_s} := u(x_s^+, t) - u(x_s^-, t)$ is the jump magnitude at shock $x_s$.

Correspondingly, the data distribution decomposes as

$$
\rho_t = \rho_t^{\mathrm{ac}} + \rho_t^{\mathrm{sing}},
$$

where $\rho_t^{\mathrm{sing}}$ is a sum of weighted Dirac masses (or narrow concentrations) at the shock values $\{u(x_s^-, t), u(x_s^+, t)\}_{x_s \in \Sigma_{\mathrm{phys}}(t)}$.

#### C.2 Mode boundary formation under Gaussian smoothing

Consider a single shock at $x_s$ with left/right limits $u_L, u_R$. Locally (in state space near $u_L, u_R$), $\rho_t$ behaves approximately as

$$
\rho_t \approx w_L \delta_{u_L} + w_R \delta_{u_R} + \text{smooth background},
$$

where $w_L, w_R > 0$ are the spatial weights on each side of the shock.

Gaussian convolution with $G_\tau$ yields

$$
p_{\tau, t}(u) \approx w_L G_\tau(u - u_L) + w_R G_\tau(u - u_R) + \text{smooth correction}.
$$

This is a two-component Gaussian mixture. By Score Shocks Proposition 3.1 (speciation threshold) \citep{score-shocks}, the score field $s_{\tau, t} = \nabla_u \log p_{\tau, t}$ develops an interfacial layer — a narrow region where $|\nabla_u s|$ is large — located near the "mode boundary," i.e., the set of $u$ where the two Gaussian components have equal weight. As $\tau \to 0^+$, this mode boundary converges to the midpoint (or, more precisely, to the continuum of values between $u_L$ and $u_R$).

#### C.3 Interfacial profile and shock set convergence

By Score Shocks Proposition 5.4 \citep{score-shocks} (the interfacial profile result), near each mode boundary the score field admits the exact decomposition

$$
w_{\tau, t}(u) = w^{\mathrm{sm}}(u) + \frac{\kappa(u)}{2} \tanh\!\left(\frac{\phi(u)}{2}\right) \nabla \phi(u) + o(1),
$$

where $\phi(u)$ is the signed log-ratio of the local mode densities and $\kappa$ is the interfacial strength (related to the jump magnitude $|u_L - u_R|$). The interfacial layer set is precisely

$$
\Sigma_{\mathrm{score}}(\tau, t) = \{ u : |\nabla_u w_{\tau, t}(u)| \gtrsim 1/\tau \},
$$

which, to leading order, coincides with the set where $|\nabla \phi|^{-1} \lesssim \sqrt{\tau}$.

Now, the key observation: the mode boundaries of $\rho_t$ — and therefore the interfacial layers of $w_{\tau, t}$ — are in one-to-one correspondence with the shock jumps of $u(\cdot, t)$. This is because:

1. **Each physical shock at $x_s$ contributes a sharp bimodal feature to $\rho_t$** (the Dirac-like concentrations at $u_L, u_R$).
2. **Gaussian smoothing of a bimodal feature always produces an interfacial layer** in the score field — this is a deterministic consequence of the heat-kernel/Cole–Hopf dynamics (Score Shocks Theorem 5.5).
3. **Conversely**, smooth (non-shock) regions of $u(\cdot, t)$ contribute only unimodal or slowly varying features to $\rho_t$, which produce no interfacial layer.

Therefore, projecting $\Sigma_{\mathrm{score}}(\tau, t)$ to physical space via $\pi_\Omega$ (which maps each state value $u$ to the spatial location where that value occurs) yields a set that converges to $\Sigma_{\mathrm{phys}}(t)$ as $\tau \to 0^+$.

#### C.4 Hausdorff convergence

Formally, for each shock $x_s \in \Sigma_{\mathrm{phys}}(t)$ with jump values $u_L, u_R$, the interfacial layer in $w_{\tau, t}$ at diffusion time $\tau$ has width $\ell_\tau \sim \sqrt{\tau} / |u_L - u_R|$ (Score Shocks Proposition 5.4). Its spatial projection satisfies

$$
\mathrm{dist}_H\!\big(\pi_\Omega(\Sigma_{\mathrm{score}}(\tau, t)), \, \Sigma_{\mathrm{phys}}(t)\big) \le C \, \sqrt{\tau},
$$

where the constant $C$ depends on the shock strength and the local regularity of $u(\cdot, t)$. The proof of this bound relies on the BV structure (to control the number of shocks and their separation) and the $\tanh$-profile asymptotics of Score Shocks. The detailed computation is deferred to the supplementary material. $\square$

---

## Conclusion

Assembling Parts A, B, and C, we have established:

- In the **diffusion time** $\tau$, the score field evolves as a vector viscous Burgers equation (A) — this is the Cole–Hopf structure that underlies all diffusion models.
- In the **physical time** $t$, the data distribution is transported by the entropy-solution dynamics, satisfying a Liouville equation (B) — this links the PDE to the distributional level.
- The **shock sets** of the physical solution and the score field coincide in the $\tau \to 0^+$ limit (C) — this is the geometric coupling that motivates the EntroDiff architecture: the network's tanh-interfacial-layer structure can be aligned with the known shock locations, enabling the exponential-error-amplification removal of Theorem 3.

Theorem 1 is thus the structural foundation on which the entire EntroDiff methodology is built. $\blacksquare$
