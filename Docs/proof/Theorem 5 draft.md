
# Theorem 5 (EntroDiff Reverse Sampler as JKO Gradient Flow)

---

## Statement

Let $p_\tau$ denote the density of the reverse sampler at diffusion time $\tau \in [0,T]$, and let $\rho^\star$ be the target distribution induced by the PDE solution in data space. Define the free energy functional

$$
\mathcal{F}(\rho) = \mathrm{Ent}(\rho \mid \rho^\star) + \lambda \mathcal{R}(\rho),
\qquad
\mathrm{Ent}(\rho \mid \rho^\star) = \int_{\mathbb{R}^N} \rho(x) \log \frac{\rho(x)}{\rho^\star(x)} \, dx,
$$

where $\mathcal{R}$ is a density functional encoding the PDE constraint and $\lambda \ge 0$.

Assume the following hypotheses:

1. **(Exact score limit)** After sufficient training, $s_\theta(x,\tau) = \nabla_x \log p_\tau(x)$ pointwise.
2. **(Viscosity-matched schedule)** $a(\tau) = g(\tau)^2 / 2 > 0$, aligned with the physical viscosity.
3. **(PDE constraint as a differentiable functional)** $\mathcal{R}$ is Fréchet-differentiable on $\mathcal{P}_2(\mathbb{R}^N)$, with first variation $\delta \mathcal{R} / \delta \rho$ well-defined; $\nabla_x (\delta \mathcal{R} / \delta \rho)$ is locally bounded.
4. **(Rigid $\mathcal{L}_4$ consistency)** The Burgers consistency penalty $\mathcal{L}_4$ is sufficiently strong that, in the infinite-capacity noiseless limit, the learned score field satisfies the viscous Burgers structure:

   $$
   \partial_\tau s_\tau + 2 s_\tau \cdot \nabla s_\tau = \Delta s_\tau.
   $$

   Moreover, $p_\tau \in \mathcal{P}_2(\mathbb{R}^N)$ is smooth in $(x,\tau)$ and strictly positive ($p_\tau > 0$).

5. **(PDE guidance as a gradient drift)** In the continuous-time limit, the combined PDE constraint losses $\mathcal{L}_2$ (Kruzhkov entropy penalty) and $\mathcal{L}_4$ (Burgers consistency) induce an additional guidance velocity $g_\tau(x)$ in the reverse ODE that converges to the spatial gradient of a functional. Specifically, the total effective velocity field of the EntroDiff reverse sampler is

   $$
   v_\tau(x) = -a(\tau)\Bigl[ \nabla_x \log p_\tau(x) + \nabla_x V(x) + \lambda \nabla_x \frac{\delta \mathcal{R}}{\delta \rho}(p_\tau)(x) \Bigr],
   $$

   where $V$ is the potential of the target distribution ($\rho^\star \propto e^{-V}$). The guidance contributions $\nabla V$ and $\lambda\nabla(\delta\mathcal{R}/\delta\rho)$ arise from the gradient of the PDE losses with respect to the sample trajectory, which by design converge to these functional-gradient limits when the losses are driven to zero in training.

Then the density evolution of the reverse sampler satisfies

$$
\partial_\tau p_\tau = \nabla \cdot \left( a(\tau) \, p_\tau \, \nabla \frac{\delta \mathcal{F}}{\delta p}(p_\tau) \right).
$$

Equivalently, under the time reparameterization $\theta(\tau) = \int_0^\tau a(r) \, dr$, we have

$$
\partial_\theta p_\theta = \nabla \cdot \left( p_\theta \, \nabla \frac{\delta \mathcal{F}}{\delta p}(p_\theta) \right),
$$

which is precisely the $W_2$-gradient flow of $\mathcal{F}$. Consequently, by the JKO theory, a single time-discrete step takes the variational form

$$
p^{n+1} = \arg\min_{p \in \mathcal{P}_2} \left\{ \mathcal{F}(p) + \frac{1}{2 \Delta \theta} W_2^2(p, p^n) \right\}.
$$

---

## Proof

### 1. Reverse Sampler as a Continuity Equation

Let $X_\tau$ denote the particle trajectory of the reverse sampler. If its continuous-time limit satisfies the ODE

$$
\frac{d X_\tau}{d\tau} = v_\tau(X_\tau),
$$

then by the standard pushforward formula, the particle distribution $p_\tau = \operatorname{Law}(X_\tau)$ satisfies the continuity equation

$$
\partial_\tau p_\tau + \nabla \cdot (p_\tau v_\tau) = 0.
$$

Thus, identifying the velocity field $v_\tau$ is the central task.

For any test function $\varphi \in C_c^\infty(\mathbb{R}^N)$, the identity follows from the chain rule:

$$
\frac{d}{d\tau} \int_{\mathbb{R}^N} \varphi(x) \, p_\tau(x) \, dx
= \frac{d}{d\tau} \mathbb{E}[\varphi(X_\tau)]
= \mathbb{E}[\nabla \varphi(X_\tau) \cdot v_\tau(X_\tau)]
= \int \nabla \varphi(x) \cdot v_\tau(x) \, p_\tau(x) \, dx.
$$

Integration by parts of the right-hand side yields

$$
\frac{d}{d\tau} \int \varphi \, p_\tau \, dx
= - \int \varphi(x) \, \nabla \cdot (p_\tau v_\tau)(x) \, dx,
$$

and since $\varphi$ is arbitrary, the continuity equation holds in the sense of distributions (and pointwise under the smoothness of $p_\tau$ and $v_\tau$).

---

### 2. Score Drift and PDE Guidance: the Total Effective Velocity

We identify $v_\tau$ as the sum of two contributions.

**(a) Score drift (from denoising score matching).** Under Hypothesis 1 (exact score) and Hypothesis 4 (rigid $\mathcal{L}_4$), the network score converges to the true score:

$$
s_\theta(x, \tau) = \nabla_x \log p_\tau(x).
$$

The probability flow ODE induced by score matching alone has the velocity

$$
v_\tau^{\mathrm{score}}(x) = -a(\tau) \, s_\theta(x,\tau) = -a(\tau) \, \nabla_x \log p_\tau(x). \tag{2.1}
$$

**(b) PDE guidance drift (from constraint losses).** The EntroDiff loss family includes PDE-constraint terms beyond denoising score matching: $\mathcal{L}_2$ (Kruzhkov entropy penalty) and $\mathcal{L}_4$ (Burgers consistency). These losses are functionals of the generated trajectory that penalize deviations from physical admissibility. In the continuous-time and infinite-data limit, their gradients with respect to the sample position induce an additional drift $g_\tau(x)$.

By Hypothesis 5, as the constraint losses are driven to zero, this guidance drift converges to the gradient of the potential that defines the target distribution plus the variational gradient of the PDE-constraint functional:

$$
g_\tau(x) = -\Bigl( \nabla_x V(x) + \lambda \nabla_x \frac{\delta \mathcal{R}}{\delta \rho}(p_\tau)(x) \Bigr). \tag{2.2}
$$

Here $\nabla V = -\nabla \log \rho^\star$ is the drift toward the target $\rho^\star \propto e^{-V}$, and $\lambda\nabla(\delta\mathcal{R}/\delta\rho)$ is the PDE-constraint drift (see Step 4 for the construction of $\mathcal{R}$).

**(c) Total effective velocity.** Summing (2.1) and (2.2), and absorbing the common factor $-a(\tau)$,

$$
v_\tau(x) = -a(\tau)\Bigl[ \nabla_x \log p_\tau(x) + \nabla_x V(x) + \lambda \nabla_x \frac{\delta \mathcal{R}}{\delta \rho}(p_\tau)(x) \Bigr]. \tag{2.3}
$$

Substituting into the continuity equation gives

$$
\partial_\tau p_\tau = \nabla \cdot \Bigl( a(\tau) \, p_\tau \bigl[ \nabla \log p_\tau + \nabla V + \lambda \nabla \tfrac{\delta \mathcal{R}}{\delta \rho} \bigr] \Bigr). \tag{2.4}
$$

We now show that the bracketed quantity in (2.3) is exactly $\nabla(\delta\mathcal{F}/\delta\rho)$.

---

### 3. First Variation of the Entropy Term

Consider the relative entropy

$$
\mathrm{Ent}(p \mid \rho^\star) = \int p \log \frac{p}{\rho^\star} \, dx.
$$

Take a perturbation $p_\varepsilon = p + \varepsilon \eta$ with $\int \eta \, dx = 0$. A first-order expansion gives

$$
\frac{d}{d\varepsilon} \Big|_{\varepsilon = 0} \mathrm{Ent}(p_\varepsilon \mid \rho^\star)
= \int \eta(x) \left( \log \frac{p(x)}{\rho^\star(x)} + 1 \right) dx.
$$

Hence the $L^2$ first variation is

$$
\frac{\delta}{\delta p} \mathrm{Ent}(p \mid \rho^\star) = \log \frac{p}{\rho^\star} + 1
$$

(the additive constant does not affect the gradient flow). Taking the spatial gradient,

$$
\nabla \frac{\delta}{\delta p} \mathrm{Ent}(p \mid \rho^\star)
= \nabla \log p - \nabla \log \rho^\star.
$$

Since $\rho^\star \propto e^{-V}$, we have $-\nabla \log \rho^\star = \nabla V$, and therefore

$$
\nabla \frac{\delta}{\delta p} \mathrm{Ent}(p \mid \rho^\star) = \nabla \log p + \nabla V. \tag{3.1}
$$

---

### 4. PDE Constraint as a Differentiable Functional

The PDE constraint (beyond $\mathcal{L}_4$) must be expressible as a density functional $\mathcal{R}(\rho)$. Under Hypothesis 3, $\mathcal{R}$ is Fréchet-differentiable on $\mathcal{P}_2$, so its first variation $\frac{\delta \mathcal{R}}{\delta \rho}$ exists and satisfies

$$
\frac{d}{d\varepsilon} \Big|_{\varepsilon = 0} \mathcal{R}(\rho_\varepsilon)
= \int \frac{\delta \mathcal{R}}{\delta \rho}(\rho) \, \eta \, dx
$$

for any zero-mass perturbation $\eta$.

In the Wasserstein setting, perturbations are generated by a transport field $\xi$ via the pushforward:

$$
T_\varepsilon(x) = x + \varepsilon \xi(x), \qquad
\rho_\varepsilon = (T_\varepsilon)_\# \rho.
$$

The corresponding variational formula is

$$
\frac{d}{d\varepsilon} \Big|_{\varepsilon = 0} \mathcal{R}\big((\mathrm{Id} + \varepsilon \xi)_\# \rho\big)
= \int \nabla \frac{\delta \mathcal{R}}{\delta \rho}(\rho) \cdot \xi \; \rho \, dx.
$$

Thus, the $\mathcal{R}$ gradient flow term contributes a drift $-\nabla(\delta\mathcal{R}/\delta\rho)$ in the velocity field (see (2.2)).

---

### 5. Identification with the Free Energy Gradient

Combining the entropy and PDE-constraint terms, the free energy is

$$
\mathcal{F}(\rho) = \mathrm{Ent}(\rho \mid \rho^\star) + \lambda \mathcal{R}(\rho).
$$

From (3.1) and Step 4, its spatial variational gradient is

$$
\nabla \frac{\delta \mathcal{F}}{\delta \rho}
= \nabla \frac{\delta}{\delta \rho} \mathrm{Ent}(\rho \mid \rho^\star)
+ \lambda \nabla \frac{\delta \mathcal{R}}{\delta \rho}
= \nabla \log \rho + \nabla V + \lambda \nabla \frac{\delta \mathcal{R}}{\delta \rho}. \tag{5.1}
$$

Comparing (2.3) with (5.1), the total effective velocity is exactly

$$
v_\tau(x) = - a(\tau) \, \nabla_x \frac{\delta \mathcal{F}}{\delta \rho}(p_\tau)(x). \tag{5.2}
$$

Substituting into the continuity equation (Step 1),

$$
\partial_\tau p_\tau + \nabla \cdot \left( p_\tau \left[ - a(\tau) \nabla \frac{\delta \mathcal{F}}{\delta \rho}(p_\tau) \right] \right) = 0,
$$

i.e.,

$$
\partial_\tau p_\tau = \nabla \cdot \left( a(\tau) \, p_\tau \, \nabla \frac{\delta \mathcal{F}}{\delta \rho}(p_\tau) \right).
$$

To eliminate the time-weight $a(\tau)$, define the reparameterized time

$$
\theta(\tau) = \int_0^\tau a(r) \, dr.
$$

Since $a(\tau) > 0$, $\theta$ is strictly increasing and locally invertible. By the chain rule,

$$
\partial_\tau p_\tau = \frac{d\theta}{d\tau} \, \partial_\theta p_\theta = a(\tau) \, \partial_\theta p_\theta.
$$

Cancelling $a(\tau)$ yields the canonical Wasserstein-2 gradient flow form

$$
\partial_\theta p_\theta = \nabla \cdot \left( p_\theta \, \nabla \frac{\delta \mathcal{F}}{\delta p}(p_\theta) \right).
$$

This completes the bridge from the EntroDiff reverse sampler to an exact Wasserstein gradient flow. $\square$

---

### 6. JKO Discretization from the Wasserstein Gradient Flow

We now show that the implicit Euler discretization of the above gradient flow is equivalent to the JKO variational scheme.

#### 6.1. Implicit Euler Discretization

Consider a uniform time grid with step $\Delta \theta$ (in reparameterized time). Given $p^n \approx p_{\theta_n}$, the implicit Euler discretization of the gradient flow is

$$
\frac{p^{n+1} - p^n}{\Delta \theta}
= \nabla \cdot \left( p^{n+1} \, \nabla \frac{\delta \mathcal{F}}{\delta \rho}(p^{n+1}) \right).
$$

#### 6.2. Proximal Step Analogy

In Euclidean space, the implicit Euler step for $\dot x = -\nabla F(x)$ is equivalent to the proximal minimization

$$
x^{n+1} = \arg\min_x \left\{ F(x) + \frac{1}{2 \Delta t} \|x - x^n\|^2 \right\}.
$$

The Wasserstein analogue replaces the Euclidean distance with $W_2$ and the Euclidean gradient with the continuity equation structure. The claim is that

$$
p^{n+1} = \arg\min_{p \in \mathcal{P}_2} \left\{ \mathcal{F}(p) + \frac{1}{2 \Delta \theta} W_2^2(p, p^n) \right\}
$$

is the JKO step corresponding to the implicit Euler discretization above.

#### 6.3. Variational Derivation

Define the augmented functional

$$
\mathcal{J}(p) = \mathcal{F}(p) + \frac{1}{2 \Delta \theta} W_2^2(p, p^n),
$$

and let $p^{n+1}$ be a minimizer. In Wasserstein space, admissible variations are generated by transport maps rather than additive perturbations. Define the perturbation

$$
T_\varepsilon(x) = x + \varepsilon \xi(x), \qquad
p_\varepsilon = (T_\varepsilon)_\# p^{n+1},
$$

where $\xi$ is an arbitrary smooth vector field compactly supported. Optimality requires

$$
\frac{d}{d\varepsilon} \Big|_{\varepsilon = 0} \mathcal{J}(p_\varepsilon) = 0.
$$

**Variation of $\mathcal{F}$.**  By the Wasserstein variational formula,

$$
\frac{d}{d\varepsilon} \Big|_{\varepsilon = 0} \mathcal{F}(p_\varepsilon)
= \int \nabla \frac{\delta \mathcal{F}}{\delta \rho}(p^{n+1}) \cdot \xi \; p^{n+1} \, dx.
$$

**Variation of the $W_2^2$ term.**  Let $\pi$ be the optimal transport plan from $p^{n+1}$ to $p^n$, with Kantorovich potential $\phi$. A classical result of optimal transport theory gives

$$
\frac{\delta}{\delta \rho} \left( \frac{1}{2} W_2^2(\rho, p^n) \right) = \phi,
$$

and therefore

$$
\frac{d}{d\varepsilon} \Big|_{\varepsilon = 0} \frac{1}{2} W_2^2(p_\varepsilon, p^n)
= \int \nabla \phi \cdot \xi \; p^{n+1} \, dx.
$$

**First-order condition.**  Combining both terms,

$$
\int \left[ \nabla \frac{\delta \mathcal{F}}{\delta \rho}(p^{n+1}) + \frac{1}{\Delta \theta} \nabla \phi \right] \cdot \xi \; p^{n+1} \, dx = 0.
$$

Since $\xi$ is arbitrary, the integrand must vanish $p^{n+1}$-almost everywhere, yielding

$$
\nabla \phi = - \Delta \theta \, \nabla \frac{\delta \mathcal{F}}{\delta \rho}(p^{n+1}).
$$

**Connection to the optimal transport map.**  The Brenier theorem gives the optimal transport map $T$ from $p^{n+1}$ to $p^n$ as $T(x) = x - \nabla \phi(x)$. Substituting the expression for $\nabla \phi$,

$$
T(x) = x + \Delta \theta \, \nabla \frac{\delta \mathcal{F}}{\delta \rho}(p^{n+1}).
$$

**Deriving the discrete continuity equation.**  By the pushforward relation $p^n = T_\# p^{n+1}$, we expand for small $\Delta \theta$ (using the Jacobian expansion of the pushforward):

$$
p^n(x) = p^{n+1}(x) - \Delta \theta \, \nabla \cdot \left( p^{n+1} \, \nabla \frac{\delta \mathcal{F}}{\delta \rho}(p^{n+1}) \right) + o(\Delta \theta).
$$

Rearranging,

$$
\frac{p^{n+1} - p^n}{\Delta \theta}
= \nabla \cdot \left( p^{n+1} \, \nabla \frac{\delta \mathcal{F}}{\delta \rho}(p^{n+1}) \right) + o(1).
$$

Taking $\Delta \theta \to 0$, we recover exactly the implicit Euler discretization of the Wasserstein gradient flow.

#### 6.4. Conclusion of JKO Derivation

Thus, a minimizer $p^{n+1}$ of the JKO functional satisfies the implicit Euler discretization of the Wasserstein gradient flow. The reverse sampler, whose density evolution was established in Steps 1–5 as the gradient flow of $\mathcal{F}$, therefore admits the JKO variational characterization in the discrete-time limit $\Delta \tau \to 0$. This completes the proof of Theorem 5. ∎

---

## Compact Fokker–Planck Expansion

For completeness, expanding the gradient flow structurally: using $\nabla \log p_\theta = \nabla p_\theta / p_\theta$ and the explicit form of the entropy variation from Step 3, the gradient flow PDE becomes

$$
\partial_\theta p_\theta
= \Delta p_\theta
+ \nabla \cdot (p_\theta \nabla V)
+ \lambda \, \nabla \cdot \left( p_\theta \, \nabla \frac{\delta \mathcal{R}}{\delta \rho} \right),
$$

exhibiting the standard decomposition into a diffusion term ($\Delta p_\theta$), an external potential drift ($\nabla \cdot (p_\theta \nabla V)$), and a PDE-constraint transport term.

---

## Remark (Relation to the Obukhov–Fokker–Planck Correspondence)

The identification (5.2) can be understood through the lens of entropy-dissipation balances. The pure reverse probability-flow ODE ($v = -a\nabla\log p$) is the Wasserstein gradient flow of the negative entropy $H(p) = \int p\log p$. Adding the PDE guidance terms $\nabla V + \lambda\nabla(\delta\mathcal{R}/\delta\rho)$ shifts the stationary point from the standard Gaussian to the target $\rho^\star$ while incorporating the physical constraint $\mathcal{R}$. The resulting free energy $\mathcal{F} = \mathrm{Ent}(\cdot|\rho^\star) + \lambda\mathcal{R}$ is the natural Lyapunov functional for the guided dynamics, and the JKO scheme is its canonical time discretization \citep{jordan1998variational}.
