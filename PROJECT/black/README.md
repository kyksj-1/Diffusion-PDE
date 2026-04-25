# PROJECT/black · EntroDiff 代码工作区

> **Shock-aware diffusion for hyperbolic PDEs · NeurIPS 2026 投稿主代码**
> 本目录是项目主开发版（black box，自洽运行；用户讲解版镜像在 `PROJECT/white/`）。

## 1. 项目意义

为 NeurIPS 2026 投稿论文 EntroDiff 提供完整代码实现：用 **shock-aware diffusion model** 解 hyperbolic PDE，关键创新是把 Score Shocks 揭示的 tanh interfacial profile **直接植入网络架构**，从而在 Wasserstein-1 距离下对 Kruzhkov 熵解给出 $\mathcal{O}(\varepsilon^{1/2})$ 收敛率（去除 $\exp(\Lambda)$ 放大）。

数学骨架与论文章节对应见 `Docs/black/path_A_method_skeleton.md` 与 `paper/black/`。

## 2. 目录结构

```
PROJECT/black/
├── README.md            ← 本文件
├── REPORT.md            ← 实验日志（按时间倒序追加）
├── pyproject.toml       ← Python 包元数据 + 工具配置
├── requirements.txt     ← 锁定的依赖列表
├── .gitignore           ← 忽略 venv / ckpt / wandb / data / __pycache__
├── src/entrodiff/       ← 库源码
│   ├── pdes/            ← E1-E3 数据生成（Godunov / WENO5 ground truth）
│   │   ├── burgers.py
│   │   ├── buckley_leverett.py
│   │   └── euler_sod.py
│   ├── models/          ← score 网络（baseline + BV-aware）
│   │   ├── score_baseline.py    ← EDM standard
│   │   └── score_bvaware.py     ← 核心创新：tanh-embedded score
│   ├── losses/          ← 损失家族
│   │   ├── dsm.py               ← denoising score matching
│   │   ├── entropy_reg.py       ← Kruzhkov entropy 正则
│   │   ├── bv_reg.py            ← BV (TV) 正则
│   │   └── burgers_consistency.py ← score-Burgers 一致性
│   ├── samplers/        ← 反向采样
│   │   ├── reverse_ode.py       ← Heun 二阶 PF-ODE
│   │   └── godunov_guidance.py  ← Godunov-form PDE guidance
│   ├── schedules/       ← noise schedule
│   │   └── viscosity_matched.py ← σ²(τ) = 2 ν_phys τ
│   └── utils/
│       ├── metrics.py           ← W_1 / L1 / shock-location err
│       └── io.py                ← ckpt / config / logging
├── scripts/             ← 顶层执行脚本（CLI 入口）
│   ├── train.py
│   ├── sample.py
│   ├── eval.py
│   └── data_gen.py
├── config/              ← Hydra-style YAML
│   ├── default.yaml
│   ├── e1_burgers.yaml
│   ├── e2_buckley_leverett.yaml
│   └── e3_euler_sod.yaml
└── tests/               ← pytest 单元测试
    ├── test_pdes.py
    └── test_samplers.py
```

## 3. 安装

```bash
cd PROJECT/black
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
# 或 .venv\Scripts\activate   # Windows
pip install -e .              # 安装本地 package + 开发模式
```

或使用 `requirements.txt`：

```bash
pip install -r requirements.txt
pip install -e .
```

## 4. 多环境

参考 `Docs/black/多环境开发指南_从第一天就做对.md`。
- 本地（PC）：仅做小规模 1D 实验、debug
- Colab：中规模训练（E1-E2）
- 云服务器：完整规模 + 全部 5 个 benchmark

## 5. 使用方法（W5-W12 实施）

```bash
# 数据生成（一次性）
python scripts/data_gen.py --config config/e1_burgers.yaml

# 训练
python scripts/train.py     --config config/e1_burgers.yaml

# 推断 / 采样
python scripts/sample.py    --config config/e1_burgers.yaml --ckpt outputs/E1/ckpt.pt

# 评估
python scripts/eval.py      --config config/e1_burgers.yaml --ckpt outputs/E1/ckpt.pt
```

输出落到 `Output/balck/E{1..3}/`（仓库根目录的 Output/balck/，注意已有目录的拼写）。

## 6. 关键 class / function 索引

> 完整签名见各模块 docstring。

| 路径 | 角色 | 状态 |
|---|---|---|
| `src/entrodiff/pdes/burgers.py::generate_burgers_dataset` | E1 ground truth | ⚪ 占位 |
| `src/entrodiff/models/score_bvaware.py::BVAwareScoreNet` | **核心创新**（论文 Eq. 5.2） | ⚪ 占位 |
| `src/entrodiff/losses/entropy_reg.py::kruzhkov_entropy_loss` | 论文 §5.3 R_ent | ⚪ 占位 |
| `src/entrodiff/losses/bv_reg.py::tv_loss` | 论文 §5.3 BV penalty | ⚪ 占位 |
| `src/entrodiff/schedules/viscosity_matched.py::ViscosityMatchedSchedule` | 论文 Eq. 5.1 | ⚪ 占位 |
| `src/entrodiff/samplers/reverse_ode.py::HeunSampler` | EDM Heun PF-ODE | ⚪ 占位 |
| `src/entrodiff/samplers/godunov_guidance.py::godunov_guidance` | 论文 Eq. 5.4 | ⚪ 占位 |
| `src/entrodiff/utils/metrics.py::wasserstein_1` | $W_1$ 估计 | ⚪ 占位 |

## 7. 开发原则（项目 CLAUDE.md 一致）

- **三层解耦**：`src/`（库）、`scripts/`（CLI 入口）、`config/`（参数）
- **type hints 必备**，每个 public 函数有 docstring
- **关键行注释**：执行脚本不仅函数级注释，关键行也要有
- **测试**：每个 `src/entrodiff/<module>` 完成后写对应 `tests/test_<module>.py`
- **TDD 规范**（见全局 CLAUDE.md §3）：核心逻辑先写 test 再写实现

## 8. License

MIT，作者标注 `kyksj-1`。
