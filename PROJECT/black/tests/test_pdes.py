"""测试 pdes/* 数据生成的正确性（W5 启用）。"""

from __future__ import annotations
import pytest


@pytest.mark.skip(reason="待 W5 实现 burgers.py 后启用")
def test_burgers_dataset_shapes() -> None:
    from entrodiff.pdes.burgers import BurgersConfig, generate_burgers_dataset

    cfg = BurgersConfig(N_x=64, N_t=21, n_samples=8)
    data = generate_burgers_dataset(cfg)
    assert data["u"].shape == (8, 21, 64)
    assert data["x"].shape == (64,)
    assert data["t"].shape == (21,)


@pytest.mark.skip(reason="待 W5 实现 burgers.py 后启用")
def test_burgers_total_variation_decay() -> None:
    """守恒律熵解满足 TV 不增（Kruzhkov 1970）。生成的 ground truth 应满足这一性质。"""
    from entrodiff.pdes.burgers import BurgersConfig, generate_burgers_dataset
    import numpy as np

    cfg = BurgersConfig(N_x=128, N_t=51, n_samples=4)
    data = generate_burgers_dataset(cfg)
    u = data["u"]                                              # (4, 51, 128)
    tv = np.abs(np.diff(u, axis=-1)).sum(axis=-1)              # (4, 51)
    # TV 在时间方向不应单调递增（允许小波动）
    assert (tv[:, 0] >= tv[:, -1] - 1e-6).all()
