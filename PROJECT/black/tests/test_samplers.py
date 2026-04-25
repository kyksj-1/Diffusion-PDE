"""测试 samplers/* 的反向采样正确性（W5 启用）。"""

from __future__ import annotations
import pytest


@pytest.mark.skip(reason="待 W5 实现 reverse_ode.py 后启用")
def test_heun_sampler_shape() -> None:
    """采样器返回的张量 shape 应与 declared shape 一致。"""
    pass


@pytest.mark.skip(reason="待 W5 实现 reverse_ode.py 后启用")
def test_heun_sampler_with_zero_score_returns_noise() -> None:
    """Sanity check: 当 score ≡ 0 时反向 PF-ODE 退化为恒等映射。"""
    pass
