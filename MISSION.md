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

## 下次 session 接力清单（**给下次会话的 AI 用**）

> **2026-04-26 晚定**。下次会话进来后，按 `CLAUDE.md §启动 session 必读顺序` 读完 4 个 .md 之后，从这里开始执行。
> 用户指示："不能一次性做这么多工作。把想法、计划和任务写好就够了，下一个会话会解决的。"

### 起手 4 步（按顺序）

1. **迁移 Theorem 3 草稿**：
   ```bash
   mkdir -p Docs/black/proofs
   git mv "Docs/proof/Theorem 3 draft.md"       "Docs/black/proofs/thm3_draft_v2.md"
   git mv "Docs/proof/Theorem 3 证明改进.md"     "Docs/black/proofs/thm3_critique.md"
   rmdir Docs/proof
   ```
   归位后 commit：`docs(proofs): 迁移 Theorem 3 草稿与 critique 至 Docs/black/proofs/`

2. **精读 Theorem 3 v2 + critique**：把 6 项符号问题 + 5 项论证漏洞列成 todo 清单（写入新建的 `Docs/black/proofs/thm3_revision_plan.md`）

3. **按 critique 修订**：在 `Docs/black/proofs/thm3_v3.md` 出 v3 草稿，逐项消除 critique 中的问题
   - 符号体系全文统一（按 `paper/black/macros/notation.tex` 与 `Docs/black/path_A_method_skeleton.md §3.1`）
   - 阶段 4–6 推导补全（v2 似乎只到阶段 3）
   - 主定理陈述与论文 `paper/black/sections/06_theory.tex` Theorem 3 完全对齐

4. **同步刷新 REPORT.md §2.6 + MEMORY.md §C**：把 Theorem 3 完成度从 15% 推进到对应数值（视实际进度估）

### 不要做的事（别忘）

- ❌ 本地编译 LaTeX（用户用 Overleaf；CLAUDE.md §LaTeX 编译工作流）
- ❌ 实装 PROJECT/black/ 下任何核心代码（用户：留给后续 session）
- ❌ 写新讲义
- ❌ 自动合并 main

### 建议做的事

- ✅ 如果 Theorem 3 修订到一半遇到大不确定，**停下问用户**（CLAUDE.md "90% 把握再行动"）
- ✅ 用 sub-agent + worktree 并行修订各阶段（Theorem 3 草稿很长，可拆）
- ✅ 完成后跑 merge dry-run，等用户审批

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
