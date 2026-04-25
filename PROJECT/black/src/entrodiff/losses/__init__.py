"""损失家族（论文 §5.3 / Eq. 5.3）。

最终复合损失:
    L = L_DSM + λ_ent · R_ent + λ_BV · TV + λ_Burg · L_BurgConsistency

各子模块对应论文的物理 / 数学角色:
- ``dsm``                  : Denoising score matching（baseline 训练目标）
- ``entropy_reg``          : Kruzhkov entropy regularizer（强制熵解）
- ``bv_reg``               : Total variation 正则（保 BV → 进入 Kruzhkov 框架）
- ``burgers_consistency``  : score-Burgers 方程一致性正则（提升泛化）
"""
