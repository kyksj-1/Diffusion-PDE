# W4 实验代码与MVP开发计划 (Experiment & Code Plan)

> **目标**：验证 EntroDiff (Path A) 核心理念（双 Burgers 耦合与熵正则/BV感知参数化），兼顾工业级代码规范与多环境兼容。秉承 MVP (Minimum Viable Product) 思想，从最小可行实验跑通全链路。

## 1. MVP 实验设计 (最小可行产品)

为了在最短时间内验证理论并出图，我们锁定最能体现 shock 行为的 **1D Inviscid Burgers Equation**。根据论文 `03_method.tex` 中的设定，我们需要验证理论中提到的几个核心组件。

*   **数据生成 (Data)**：
    *   **设置**：1D 周期边界，初始条件为多个正弦波叠加或阶跃函数，演化出明显 Shock。
    *   **生成方式**：使用传统的 Godunov/WENO 格式有限体积法（或直接复用 `dedalus` / `PDEBench` 的生成脚本）生成 Ground Truth 数据。
*   **模型骨架 (Backbone)**：
    *   调用轻量级的 1D U-Net（充当 $\phi_{\theta}^{\mathrm{sm}}$ 光滑背景势能）。
*   **对比方法 (Ablation/Baselines)**：
    *   **Baseline**：标准 EDM 扩散模型（仅使用常规去噪损失 $\mathcal{L}_{\mathrm{DSM}}$）。
    *   **Ours (MVP版)**：标准 EDM + **Viscosity-matched schedule ($\sigma^2(\tau) = 2\nu_{\mathrm{phys}}\tau$)** + **Kruzhkov Entropy Loss ($\mathcal{L}_{\mathrm{ent}}$)** + **Godunov-form guidance**。
    *   *(注：最复杂的 Parameterization (C) 即 $\tanh$ 拟合作为进阶目标，MVP阶段先不实装，以防卡流程)*。
*   **评估指标 (Metrics)**：
    *   Wasserstein-1 ($W_1$) 距离（体现对 Shock 位置的捕捉能力）。
    *   Total Variation (TV) 趋势。

## 2. 工业级代码架构规划 (PROJECT/black)

严格遵守《多环境开发指南》的规范，实现配置与代码、代码与数据的双重解耦：

```text
PROJECT/black/
├── configs/
│   ├── env_config.yaml         # PC/Server/Colab 环境路径、精度配置
│   └── exp_burgers_mvp.yaml    # MVP实验参数 (lr, batch_size, diff_steps)
├── src/
│   ├── data/
│   │   └── burgers_1d.py       # 数据加载与动态预处理
│   ├── models/
│   │   ├── unet_1d.py          # 1D U-Net 封装
│   │   └── score_param.py      # Score参数化 (Standard vs BV-aware)
│   ├── diffusion/
│   │   ├── schedules.py        # 包含 Viscosity-matched 噪声表
│   │   ├── losses.py           # 核心！L0 (DSM), L2 (Kruzhkov), L3 (BV)
│   │   └── samplers.py         # Heun + Godunov guided sampler
│   └── utils/
│       ├── env_manager.py      # 多环境路径与设备解析
│       └── logger.py           # Wandb / TensorBoard 集成
├── scripts/
│   ├── generate_data.py        # 调用经典求解器造数据
│   ├── train_mvp.py            # MVP 主训练脚本
│   └── eval_viz.py             # 读取 checkpoint 出图 (PDE演化与Shock对比)
└── requirements.txt
```

## 3. 开发者 (AI) 角色扮演提议

*   **拟定角色**：**Zongyi Li (李宗沂)** (Caltech / NVIDIA)。
*   **理由**：他是 Neural Operator (FNO, PINO) 的核心一作，拥有顶级的 AI4PDE 工程落地能力。他的 `neuraloperator` 代码库是该领域的 industrial-grade 标杆（OOP设计、多端支持极佳）。让他来“写”代码，能保证代码具备数学和物理的严谨性，同时又极其符合大厂开源库的干净规范。

## 4. 执行步骤预期

1.  编写 `env_manager.py` 和构建配置系统（夯实多环境地基）。
2.  实现并拉通 `generate_data.py` 和 1D Dataset Loader。
3.  组装 1D U-Net，跑通 Baseline ($\mathcal{L}_0$) 的训练和采样。
4.  加入 $\mathcal{L}_2$ 和 Viscosity-matched schedule，对比 Baseline 的 $W_1$ 距离指标。

---
请审核上述计划，若同意，我将此作为规范写入 `CLAUDE.md` 并开始后续工作。