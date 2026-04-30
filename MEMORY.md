# MEMORY · 项目活档案（给 AI 看）

> **阅读对象 · AI**。给人看的进度报告在 `REPORT.md`。

---

## A · 角色选择

当前角色：**Anima Anandkumar 教授**（Caltech / NVIDIA）。理由见 `CLAUDE.md`。

---

## B · 决策日志

### 2026-04-30 · E2 闭环 + 少步消融系统化 + REPORT 大刷新

- E2 Buckley-Leverett 全栈完成：flux → solver → 数据 → 训练 → eval
- **少步消融核心发现**：BV-aware 10 步 (W₁=0.681) > Baseline 50 步 (0.706) → 论文级亮点
- BV-aware 500ep 过拟合（W₁=0.778 vs 200ep 的 0.729）→ 退回 200ep
- E2 上 Ours 比 Baseline 好 7.4%（W₁ 0.163 vs 0.176）
- 服务器 3 台 RTX 3090 全部可用，已熟练使用 tmux 编排
- MISSION.md 重写为三线并行计划（sharp IC + 少步消融 + E2 BV-aware）
- 决定：现有数字足够写论文 §5，不再硬调参

### 2026-04-29 · 代码 MVP 跑通 + 服务器上线

- 本地 PC RTX 4060 完成 E1 数据+训练+eval 全闭环
- 服务器 3×RTX 3090 部署，完成 3 轮大规模训练
- BVAwareScore 梯度真值化 + Godunov PDE guidance + 梯度裁剪
- Time loss 轻量版实现（~40 行）
- PDE guidance 对无条件采样无益（推往零解），正确用途是逆问题

### 2026-04-28 · 论文前三节精修 + 定理附录完整迁入 LaTeX

- §1/§2/§3 (§5 Method) / §4 (§6 Theory) 全实写
- A1 5 大定理 LaTeX 证明完整
- notation.tex 全部宏落地

---

## C · 状态快照

### C.1 当前阶段

- **周次**：W4–W5（12 周时间表的中段）
- **本阶段主任务**：实验完成 → 论文 §5 Experiments 实写
- **下一里程碑**：论文 §5/§6 实写 + `\todo` 清零

### C.2 已完成

- 路径 A 选定 + 项目基础设施
- 论文 §1–§4 + A1 附录 100% 实写
- E1 Burgers 全闭环（数据/训练/eval/消融）
- E2 Buckley-Leverett StandardScore 闭环
- 少步消融系统化
- Time loss / sharp IC / coarse grid 脚本就绪
- 服务器 tmux 实验编排

### C.3 待做

- 论文 §5 Experiments 实写（数字已就绪）
- 论文 §6 Conclusion 实写
- Sharp IC 数据上训练对比
- E2 BVAwareScore 训练

---

## D · 风险簿

| ID | 描述 | 状态 |
|---|---|---|
| R3 | Baseline 作者审稿 | 已准备：主实验用对方代码+数据作 baseline |
| R5 | 实验时间紧 | 已缓解：E1+E2 闭环 |
| R6 | "只是 Score Shocks 应用" | 少步优势 + E2 跨方程验证可反驳 |

---

## E · 维护规则

重大决策/里程碑/风险变化时更新。进度数字去 REPORT.md。

---

> 若你正在读这份文件却不知接下来该做什么——读 `MISSION.md`。
