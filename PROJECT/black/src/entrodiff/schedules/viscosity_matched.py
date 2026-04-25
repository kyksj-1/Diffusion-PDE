"""Viscosity-matched noise schedule（论文 Eq. 5.1）。

σ²(τ) = 2 · ν_phys · τ,    τ ∈ [0, T_d]

动机：根据 Score Shocks (★)，扩散模型的 effective viscosity 恰好是
g(τ)²/2。让它与目标 PDE 的物理黏性 ν_phys 对齐 → score 层 Burgers 与
solution 层 Burgers 共享 viscous profile，shock 形成时间在两个时间方向
上对应。
"""

from __future__ import annotations
from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class ViscosityMatchedSchedule:
    """σ²(τ) = 2 ν_phys τ 的实现。

    Attributes:
        nu_phys: 目标 PDE 的物理黏性 ν_phys
        T_d:     最大扩散时间 τ_max
    """

    nu_phys: float
    T_d: float = 1.0

    def sigma(self, tau: torch.Tensor) -> torch.Tensor:
        """σ(τ) = sqrt(2 ν_phys τ)."""
        return torch.sqrt(2.0 * self.nu_phys * tau.clamp(min=0.0))

    def sigma_dot(self, tau: torch.Tensor) -> torch.Tensor:
        """σ̇(τ) = ν_phys / σ(τ)（链式法则；τ → 0 时奇异，需小阈值保护）."""
        sig = self.sigma(tau)
        eps = 1e-8
        return self.nu_phys / sig.clamp(min=eps)

    def sample_tau(self, batch_size: int, device: str | torch.device) -> torch.Tensor:
        """训练时均匀采样 τ ~ U[0, T_d]."""
        return torch.rand(batch_size, device=device) * self.T_d
