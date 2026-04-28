# MISSION · 当前阶段指令

> **即写即用即换**。持续性内容请去 `CLAUDE.md`；进度请去 `REPORT.md`；状态 / 决策日志请去 `MEMORY.md`。

---

## 本阶段任务

- 本阶段我们先完成论文的写作。我会根据REPORT中的东西对你进行指导
- [x] 结构修改：03 Preliminaries和04 Double-Burgers不要单独开一个section，部分内容合并到 02 部分内容合并到 Theory部分
- [x] 论文前三节精修 (§1 Introduction / §2 Related Work / §5 Methodology)
- [x] 定理处理：5 大定理证明从 `Docs/proof/` 完整迁入 LaTeX 附录 `A1_proofs.tex`
- [x] §5 Method 完整实写（4 子节 + loss table + Algorithm 1 + Godunov flux）
- [x] §6 Theory 5 段 proof sketch 全部实写
- [x] notation.tex 全部 11 个 `[planned]` 宏落地
- [ ] §7 Experiments 实写（W4 待办）
- [ ] §8 Conclusion 实写（W4 待办）
- [ ] 全文 `\todo{}` 清除 + 最终 polish
- 数学符号：
  - **全文已统一**。`SYMBOL.md` 已建立并维护；所有 `[planned]` 宏已落地 `notation.tex`
  - 确保符号高级性，保持数学味儿和行业黑话，体现出专业感
- 具体的语言可以参照 EXAMPLE PAPERS 文件夹中的内容。里面写得很好，可以加油，参考它们的语言和华丽程度
- 如果涉及到五大定理中的任意一项，需要引用、或者本身需要提及，先在后面留一个占位符；或者干脆本段注释相关的内容等我完成。证明已经证了很多了

---

## 本轮产出摘要（2026-04-28 W3）

| 文件 | 状态 |
|---|---|
| `sections/01_intro.tex` | ✓ 精修（强化 GAP 诊断、符号统一） |
| `sections/02_related_work.tex` | ✓ 精修（VE-SDE 链补全、宏统一） |
| `sections/05_method.tex` | ✓ **完整实写**（4 子节 + Table 1 + Algorithm 1） |
| `sections/06_theory.tex` | ✓ proof sketch 全实写（5 段思想线 + 附录 ref） |
| `sections/A1_proofs.tex` | ✓ 5 定理完整 LaTeX 证明（5 子文件 + 主控） |
| `proofs/thm1_proof.tex` | ✓ 290 行 |
| `proofs/thm2_proof.tex` | ✓ 391 行 |
| `proofs/thm3_proof.tex` | ✓ 635 行（主定理，待用户 review） |
| `proofs/thm4_proof.tex` | ✓ 357 行 |
| `proofs/thm5_proof.tex` | ✓ 471 行 |
| `macros/notation.tex` | ✓ 11 个 `[planned]` 宏全部落地 |
| `SYMBOL.md` | ✓ 同步更新 |
| `PLAN/W3_sections_refine_plan.md` | ✓ 新计划 |
| `REPORT.md` / `MEMORY.md` | ✓ 全面刷新 |

---

## 注意事项清单（**给下次会话的 AI 用**）

> **2026-04-26 晚定**。

### 不要做的事（别忘）

- ❌ 本地编译 LaTeX（用户用 Overleaf；CLAUDE.md §LaTeX 编译工作流）
- ❌ 实装 PROJECT/black/ 下任何核心代码（用户：留给后续 session）
- ❌ 写新讲义
- ❌ 自动合并 main

### 建议做的事

- ✅ 任何任务遇到大不确定，**停下问用户**（CLAUDE.md "90% 把握再行动"）
- ✅ 用 sub-agent + worktree 并行修订各阶段
- ✅ 完成后跑 merge dry-run，等用户审批
- **同步刷新 REPORT.md §2.6 + MEMORY.md §C**：把 Theorem 3 完成度从 15% 推进到对应数值（视实际进度估）

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
