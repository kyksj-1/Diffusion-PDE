# MISSION · 当前阶段指令

> **即写即用即换**。持续性内容请去 `CLAUDE.md`；进度请去 `REPORT.md`；状态 / 决策日志请去 `MEMORY.md`。

---

## 一句话现状

**W2 · 论文撰写 + 实验启动同步推进**：路径 A 已选定（EntroDiff），基础设施就位，进入"写论文 + 跑实验"双线作战。

---

## 本阶段任务（W2）

### 双线并行（推荐用 worktree 隔离开两个分支）

| # | 线 | 任务 | 产物 | 优先级 |
|---|---|---|---|---|
| **A** | 论文（理论）| Theorem 3 主定理草稿迭代——**用户已有 v2 + critique 在 `Docs/proof/`**，需按 critique 修订 | `Docs/black/proofs/thm3.md` | **P0** |
| B | 论文（写作）| `paper/black/sections/01_intro.tex` 与 `05_method.tex` 草稿 | 替换 `\todo{}` 为真正段落 | P1 |
| C | 代码（baseline）| 复现 EDM + DiffusionPDE，作为 E1 baseline | `PROJECT/black/src/entrodiff/models/score_baseline.py` 实装 + smoke test | P1 |
| D | 代码（数据）| 实装 `pdes/burgers.py` Godunov + WENO5 ground truth | `PROJECT/black/src/entrodiff/pdes/burgers.py` + 通过 `tests/test_pdes.py` | P0（C 的前置）|

### 本 session 下一动作

1. 把 `Docs/proof/` 下的 Theorem 3 草稿 + critique 迁到 `Docs/black/proofs/`（统一归位）
2. 决定先做哪条线（A vs C/D）；建议 **A 优先**——理论一旦定稿，后续 method/experiments 章节可大量复用其符号与 lemma

---

## 接下来（W3 之后）

参见 `CLAUDE.md §12 周时间表`。**当前不需要重复**——只在切阶段时刷新本文件的"本阶段任务"。

---

## 历史 · MISSION 已迁出的内容

> 以下原本在 MISSION.md，现已迁到对应文件，本节仅作迁移备忘。下次清空本文件时可以连这一节一起删。

- 工作区目录约定 → `CLAUDE.md §工作区目录约定`
- NeurIPS 排版规范 → `CLAUDE.md §NeurIPS 2026 排版规范`
- 12 周时间表 → `CLAUDE.md §12 周时间表`
- 用户身份 / 痛点 → `CLAUDE.md §用户身份`
- 原始 IDEA 演化的归宿 → `CLAUDE.md §原始 IDEA 演化的归宿`
- 角色选择理由 → `MEMORY.md §A`
- 决策日志 → `MEMORY.md §B`
- 风险簿 → `MEMORY.md §D`
- 进度报告（完成 / 未完成） → `REPORT.md`
