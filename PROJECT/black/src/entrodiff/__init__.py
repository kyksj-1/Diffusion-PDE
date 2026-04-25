"""EntroDiff · Shock-aware diffusion solvers for hyperbolic PDEs.

NeurIPS 2026 投稿主代码包。子模块概览（详见各子包 docstring）:

- ``pdes``      : 双曲守恒律数据生成（Godunov / WENO5 ground truth）
- ``models``    : score 网络（baseline + BV-aware 核心创新）
- ``losses``    : 损失家族（DSM + 熵正则 + BV 正则 + Burgers 一致性）
- ``samplers``  : 反向 PF-ODE 采样 + Godunov-form PDE guidance
- ``schedules`` : noise schedule（viscosity-matched）
- ``utils``     : 度量（W_1 / L^1 / shock-location err）+ IO
"""

__version__ = "0.0.1"
