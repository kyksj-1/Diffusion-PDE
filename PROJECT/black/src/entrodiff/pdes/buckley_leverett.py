"""1D Buckley–Leverett 方程数据生成（论文 §7.2 实验 E2）。

PDE:
    ∂_t u + ∂_x f(u) = 0,    f(u) = u^2 / (u^2 + (1-u)^2)

非凸通量 → 解中同时出现 shock + rarefaction wave。
参考解算法：Godunov + WENO5。
"""

from __future__ import annotations
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BuckleyLeverettConfig:
    """Buckley–Leverett 数据生成配置（语义同 BurgersConfig）。"""

    N_x: int = 256
    N_t: int = 101
    T: float = 0.5
    n_samples: int = 1024
    seed: int = 0


def generate_bl_dataset(cfg: BuckleyLeverettConfig) -> dict[str, np.ndarray]:
    """生成 Buckley–Leverett 数据集。"""
    raise NotImplementedError("Will be implemented in Week 8 (cf. path_A_method_skeleton §6).")
