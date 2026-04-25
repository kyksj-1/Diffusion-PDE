"""**核心创新**：BV-aware score parameterization（论文 §5.2 / Eq. 5.2 / Theorem 3）。

参数化（数学公式）:
    s_θ(u, τ) = ∇φ_sm(u, τ) + κ_θ(u, τ) / 2 · tanh(φ_sh(u, τ) / 2) · ∇φ_sh(u, τ)

其中：
- φ_sm  : 光滑背景势能（远离 shock 的平滑梯度）
- φ_sh  : 到 shock 的有符号距离（在 shock 处过零）
- κ_θ   : 局部跳跃强度（受 Rankine–Hugoniot 约束）

设计动机：Score Shocks Proposition 5.4 证明 VE 扩散在 interfacial layer
附近 score 的精确形式就是 (1/2) tanh(φ/2) ∇φ。把这个结构嵌入网络架构后，
Theorem 3 中的 Gronwall 常数从 exp(Λ) 退化到 O(1)，得到 W_1 ≤ ε^{1/2}。
"""

from __future__ import annotations

import torch
from torch import nn


class BVAwareScoreNet(nn.Module):
    """BV-aware score 网络。

    内部由三个子网络组成：
        - phi_sm_net :  smooth background potential
        - phi_sh_net :  signed distance to shock set
        - kappa_net  :  jump magnitude

    Args:
        in_channels: 物理通道数
        hidden_dim: 隐藏维数（共用）
    """

    def __init__(self, in_channels: int = 1, hidden_dim: int = 128) -> None:
        super().__init__()
        self.in_channels = in_channels
        self.hidden_dim = hidden_dim
        # TODO[Week 6] · 实现三个子网络
        # self.phi_sm_net  = ...
        # self.phi_sh_net  = ...
        # self.kappa_net   = ...

    def forward(self, u: torch.Tensor, tau: torch.Tensor) -> torch.Tensor:
        """前向：按 Eq. (5.2) 组装 score。

        Args:
            u: shape (B, C, N_x)
            tau: shape (B,)

        Returns:
            shape (B, C, N_x) — s_θ(u, τ)

        Implementation notes:
            φ_sm 和 φ_sh 都用标量势能网络 + 数值梯度（finite difference）。
            tanh 在 |φ_sh| 大时饱和，自动给出"远离 shock 时主项 = ∇φ_sm"。
        """
        raise NotImplementedError("Will be implemented in Week 6 (this is the paper's main novelty).")
