"""PDE 数据生成模块。

为论文 §7 的 toy 实验提供 ground-truth 数据集：

- ``burgers``           : 1D inviscid Burgers (E1)
- ``buckley_leverett``  : 1D Buckley–Leverett (E2)
- ``euler_sod``         : 1D Euler / Sod 激波管 (E3)

所有生成器都用经典 entropy-preserving 数值方法（Godunov / WENO5）作为参考解。
"""
