# REPORT.md · EntroDiff 实验日志

> 按时间倒序追加。每次实验完成、关键 milestone 达成时更新。
> 与 `MEMORY.md` 的分工：本文件记**实验事实**（数字、ckpt 路径、超参组合、observations），`MEMORY.md` 记**决策与状态**。

---

## 状态总览

- **当前周次**：W1（理论基石阶段）
- **代码阶段**：⚪ 骨架已搭，所有模块 `NotImplementedError`
- **下一里程碑**：W5 — 复现 EDM + DiffusionPDE baseline

---

## 实验日志（最新 → 最旧）

### 2026-04-26 · 代码工作区初始化

| 项 | 状态 |
|---|---|
| 目录结构 | ✓ src/scripts/config/tests 三层解耦完成 |
| 包元数据 | ✓ pyproject.toml + requirements.txt |
| 模块占位 | ✓ 所有 .py 文件给出顶部 docstring + 占位签名 |
| 实际实现 | ⚪ W5 启动 |

无实验数据。

---

## 模板（每次实验追加用）

```markdown
### YYYY-MM-DD · 实验 E{N} · {简述}

**配置**：
- config: `config/eX_xxx.yaml`
- ckpt: `Output/balck/EX/ckpt-YYYYMMDD-NNNNNN.pt`
- 训练时长：N 小时（GPU 型号）
- 训练 step / epoch 数：

**关键超参**（与 default 不同的）：
| 名 | 值 |
|---|---|
| ν_phys | ... |
| λ_BV | ... |

**指标**：
| 指标 | EntroDiff | EDM baseline | DiffusionPDE | FNO |
|---|---|---|---|---|
| W_1 | ... | ... | ... | ... |
| L^1 | ... | ... | ... | ... |
| shock-location err | ... | ... | ... | ... |

**观察**：
- ...

**下一步**：
- ...
```

---

## 已知问题与待办

> 不重要的待办放 `git issue` / TODO 注释；这里只记**会影响实验复现**的问题。

- (无)
