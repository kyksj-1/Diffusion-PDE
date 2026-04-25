"""1D Euler 方程 / Sod 激波管数据生成（论文 §7.3 实验 E3）。

守恒律系统:
    ∂_t U + ∂_x F(U) = 0,    U = (ρ, ρu, E),    F = (ρu, ρu^2 + p, (E+p)u)

参考解算法：HLLC 通量 + WENO5 重构。
Sod 初值: 左态 (ρ, u, p) = (1.0, 0.0, 1.0); 右态 (0.125, 0.0, 0.1).
解中同时含 shock + contact + rarefaction，是双曲方程的标准 benchmark。
"""

from __future__ import annotations
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class EulerSodConfig:
    """Euler / Sod 配置。"""

    N_x: int = 256
    N_t: int = 101
    T: float = 0.2
    gamma: float = 1.4
    n_samples: int = 1024
    seed: int = 0


def generate_euler_sod_dataset(cfg: EulerSodConfig) -> dict[str, np.ndarray]:
    """生成 Sod 激波管数据集。

    Returns:
        dict 含键 "U" (n_samples, N_t, 3, N_x), "x", "t", "U0"
    """
    raise NotImplementedError("Will be implemented in Week 9 (cf. path_A_method_skeleton §6).")
