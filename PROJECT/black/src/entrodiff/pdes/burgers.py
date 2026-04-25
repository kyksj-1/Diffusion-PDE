"""1D inviscid Burgers 方程数据生成（论文 §7.1 实验 E1）。

PDE:
    ∂_t u + ∂_x (u^2 / 2) = 0,    x ∈ [0, 1], t ∈ [0, T]

参考解算法：Godunov + WENO5 通量重构（见 Shu 1999）。

模块对应：
    论文 §3.2 公式 (3.2)（标量守恒律）
    path_A_method_skeleton.md §5 实验 E1
"""

from __future__ import annotations
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BurgersConfig:
    """Burgers 数据生成配置。

    Attributes:
        N_x: 空间格点数（默认 256）
        N_t: 时间步数（包含 t=0）
        T: 终止物理时间
        x_min: 空间左端
        x_max: 空间右端
        n_samples: 生成的 trajectory 数（每条对应一个随机初值）
        ic_type: 初值类型 ("riemann" | "sin" | "random_fourier")
        seed: 随机种子
    """

    N_x: int = 256
    N_t: int = 101
    T: float = 0.5
    x_min: float = 0.0
    x_max: float = 1.0
    n_samples: int = 1024
    ic_type: str = "random_fourier"
    seed: int = 0


def generate_burgers_dataset(cfg: BurgersConfig) -> dict[str, np.ndarray]:
    """生成 Burgers 训练 / 测试数据集。

    Args:
        cfg: 数据生成配置（见 :class:`BurgersConfig`）

    Returns:
        dict 含键:
            - "u": shape (n_samples, N_t, N_x)，物理解
            - "x": shape (N_x,)，空间网格
            - "t": shape (N_t,)，时间网格
            - "u0": shape (n_samples, N_x)，初值（= u[:, 0, :]）

    Notes:
        参考解使用 5 阶 WENO + 显式 RK3 时间推进，CFL = 0.4。
        Shock 通过 Godunov 通量自动捕捉，无需显式跟踪。
    """
    raise NotImplementedError("Will be implemented in Week 5 (cf. path_A_method_skeleton §6).")
