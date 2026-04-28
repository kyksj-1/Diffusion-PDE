# PLAN · W3 · 论文前三节精修 + 定理附录 + Theory 实写

> 起草：2026-04-28（W3）
> 主控对应：用户指令（5 点任务）
> 角色：**Anima Anandkumar 教授**（项目级 CLAUDE.md 钦定）
> 目标章节：`01_intro.tex / 02_related_work.tex / 05_method.tex / 06_theory.tex / A1_proofs.tex`
> 状态：**Draft → 执行中**

---

## 0 · 输入条件复盘

| 项 | 状态 | 备注 |
|---|---|---|
| §1 Intro | ✓ 实写完毕 W2，Gap/Insight/Contribution 三段 + (C1)(C2)(C3) | 需精修：检查符号一致性、优化 GAP 段论证节奏 |
| §2 Related Work + Background | ✓ 实写完毕 W2，4 组 RW + 3 段 Background | 需精修：VE-SDE prelim 段需更精确 |
| §5 Method | 仅模板骨架 + `\todo` 6 处 | 本步 **完整实写** 4 子节 + 表格 + Algorithm |
| §6 Theory | §6.1 桥段 + 5 个 Thm statement（proof sketch 留 `\todo`） | 本步填满 5 个 proof sketch 段 |
| A1 Proofs | 仅模板骨架 | 本步将 `Docs/proof/` 下 Theorem 1-5 迁入 LaTeX |
| `macros/notation.tex` | 已有 30 个宏；11 个 `[planned]` 待加 | 本步全部落地 |
| | | `Docs/proof/Theorem 1/2/3/4/5` 证明均已完备 |

---

## 1 · 执行顺序（解决强依赖）

```
Step 0: 创建本 PLAN + 新建分支
Step 1: 补 macros/notation.tex（无依赖，其他步骤都需引用）
Step 2: 精修 §1 Intro（仅依赖 macros，可与 S1 并行）
Step 3: 精修 §2 Related Work + Background（同上）
Step 4: 实写 §5 Method（依赖 S2 S3 中对 §5 的 ref 锚已就位）
Step 5: 迁入 A1_proofs.tex（依赖 S1 的 macros + S4 的 ref 锚）
Step 6: 填满 §6 Theory 5 个 proof sketch（依赖 S5 的附录 ref）
Step 7: 更新 REPORT / MEMORY
```

---

## 2 · 各步骤详细要求

### Step 1 · 补全 notation.tex

按 SYMBOL.md §12 的 `[planned]` 列表，新增以下 11 个宏：
- `\rhotphys`, `\errsc`, `\physsol`, `\physsolvis`, `\initdat`
- `\dShock`, `\phisbg`, `\phissh`, `\jumpamp`
- `\unat`, `\uhat`, `\uth`, `\muth`
- `\abs`, `\norm`

同步更新 SYMBOL.md §12（删 `[planned]` 标记）+ §15 变更日志。

### Step 2 · 精修 §1 Intro

强化点：
- GAP 段补齐具体 failure mode：DiffusionPDE 的 central-diff PDE residual 在 shock 处 ill-defined
- Insight 段引入更精确的双 Burgers 几何对应
- Contribution 列表更新 ref 锚（§5 ref 现在可用）

### Step 3 · 精修 §2 Related Work + Background

强化点：
- VE-SDE prelim 段补全 Tweedie 公式 + Cole-Hopf 对应
- Function-space diffusion 段更精确地指出 Benchmark 空白
- 确保 `\eqref` 锚全部解析

### Step 4 · 实写 §5 Method

按 `W2_method_plan.md` §3 的段落计划：
- §5.0 Overview（4-5 行 lead-in，锚定 4 组件 → 4 Theorems）
- §5.1 Viscosity-matched schedule（~10 行 + `eq:visc-matched`）
- §5.2 BV-aware parameterization（~18 行 + `eq:bv-aware`，核心 novelty）
- §5.3 Loss family（~12 行 + `eq:loss-final` + Table `tab:loss-family`）
- §5.4 Sampler with Godunov-form guidance（~14 行 + `eq:reverse-ode` + Algorithm 1）
- 整体严控 ≤ 2 页正文

### Step 5 · 迁入 A1_proofs.tex

从 `Docs/proof/` 迁入 Theorem 1–5 完整证明（Markdown → LaTeX）：
- **Theorem 1**（Double-Burgers coupling）：3 部分证明 + A1–A4 假设
- **Theorem 2**（Entropy-solution stability）：9 步 Gronwall + (A1)–(A5) 假设
- **Theorem 3**（Improved rate，主定理）：A0–A6 假设 + 6 阶段证明
- **Theorem 4**（Shock-location admissibility）：4 引理 + Godunov 弱形式
- **Theorem 5**（JKO correspondence）：continuity → gradient flow → JKO step

### Step 6 · 填满 §6 Theory proof sketch 段

替换 `\todo` 为 1 段/Thm 的 proof sketch，每段 ≤ 8 行：
- §6.1（Thm 1）已有桥段；补 1 段 sketch
- §6.2–§6.5 各补 1 段思想线

### Step 7 · 更新进度文档

- REPORT.md §2.3 刷新各 section 完成度
- REPORT.md §3.2 刷新未完成项
- MEMORY.md §B 新增决策日志
- MEMORY.md §C 刷新状态快照

---

## 3 · 文件修改清单

| 文件 | 操作 | 说明 |
|---|---|---|
| `macros/notation.tex` | 编辑 | 新增 11 个宏 |
| `SYMBOL.md` | 编辑 | §12 删 `[planned]` + §15 变更 |
| `sections/01_intro.tex` | 编辑 | 精修三段 |
| `sections/02_related_work.tex` | 编辑 | 精修 VE-SDE + RW |
| `sections/05_method.tex` | **重写** | 4 子节 + table + algorithm |
| `sections/06_theory.tex` | 编辑 | 填满 5 proof sketch |
| `sections/A1_proofs.tex` | **重写** | 5 定理完整证明 |
| `REPORT.md` | 编辑 | §2/§3 进度刷新 |
| `MEMORY.md` | 编辑 | §B/C 日志 |
