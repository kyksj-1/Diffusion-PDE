# MISSION · 当前阶段指令

> **即写即用即换**。持续性内容请去 `CLAUDE.md`；进度请去 `REPORT.md`；状态 / 决策日志请去 `MEMORY.md`。

---

## AI总结本阶段任务

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

## 人类跟进（新任务）

当前论文撰写已经搭好框架，在 `D:\A-Nips-Diffussion\paper\black` 中，是完整的论文项目，且单独git管理（已经加入了父文件夹的gitignore），且连接到了远程


- [x] 必须先阅读 `D:\A-Nips-Diffussion\Docs\path_A_method_skeleton.md` 框架，以及目前已经写好的论文，领会我工作的意思
- [x] 需要你根据我的工作设计代码：
	- 你的任务是写文档，让别的AI执行。直接跟在CLAUDE.md文件后面
	- 让AI先选择一名角色进行扮演，要求真实存在，且说明理由
	- 你来根据论文需求设计实验。
	- 从最简单的实验开始做起。不设计太多（或或者备注明确这是优先级较低的远期规划），先从最小的、能跑通的、能出结果的开始做起 （MVP思想）
	- 要有设计思维，尽量要让实验能跑通、让论文站得住脚。同时要提醒AI开发者理解论文、代码实现要贴近论文，产出成果要符合论文
	- 在开发者文档中，说明可以如何去获取代码、用别人写好的代码或者库（仅仅是给建议，不要写死）
	- 注意跨环境的工作需求（见 `D:\A-Nips-Diffussion\Docs\多环境开发指南_从第一天就做对.md` ）
	- 在PLAN中简要（注意，简要！）说说你设计的计划，在我同意后再写CLAUDE.md
- 代码满足产业需求，工业级别代码
- 你作为代码专家，代码注释、鲁棒性、git管理、可迁移性等要求，同样再CLAUDE.md中体现
- 对别的AI的要求要保持我对你的要求，甚至更高

---

现在md文档已经撰写好了，请你开始开发！


