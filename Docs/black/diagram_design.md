# 论文示意图设计文档

> 日期 2026-04-29 | 项目 EntroDiff | NeurIPS 2026

---

## Figure 1 · 双 Burgers 耦合 (Double-Burgers Coupling)

**位置**: `paper/black/sections/01_intro.tex` §1 Introduction, 在 Contributions 之前

**目的**: 用一图让 reviewer 在 10 秒内理解论文的核心结构观察（C1）。这是读者读完 abstract 后看到的第一个科学内容——必须一目了然。

### 布局（三栏横向）

```
+------------------+     +-------------------+     +----------------------+
|  物理域 (x, t)    |     |  扩散域 (u, τ)      |     |  几何对应 (耦合)        |
|                  |     |                   |     |                      |
|   Burgers PDE    |     |   Score Burgers    |     |  Σ_phys(t) ↕ Σ_score(τ)|
|   ∂_t u + u∂_x u = 0|  |  ∂_τ s + 2s·∇s = Δs|    |                      |
|                  |     |                   |     |  物理 shock 位置        |
|   t ↑            |     |   τ ↑              |     |  决定 score 界面层       |
|   |  ╱╲ shock    |     |   |  /‾‾\ tanh      |     |                      |
|   | ╱  ╲         |     |   | /    \          |     |  [红色箭头连接两边]      |
|   |╱    ╲________|     |   |/______\_________|     |                      |
|   +----------→ x |     |   +----------→ u    |     |                      |
+------------------+     +-------------------+     +----------------------+
```

### 左栏 · 物理域
- 画 1D Burgers 的时空图: 横轴 x (空间), 纵轴 t (时间)
- 初值光滑正弦波, 随时间演化在 t_c 处形成 shock (红色加粗线)
- 标注: "shock at t = t_c"

### 中栏 · 扩散域 (score 域)
- 横轴: 函数值 u (高维状态空间), 纵轴: 扩散时间 τ
- 画 score 场 s(u, τ) 的演化: 在 τ → 0 时出现 tanh 形状的界面层
- 红色虚线标注界面层位置 Σ_score(τ)
- 标注: "tanh interfacial layer at τ → 0"

### 右栏 · 几何对应
- 画两个 shock 集之间的双向箭头 ↕
- Σ_phys(t): 物理空间中的不连续位置 (红色)
- Σ_score(τ): 状态空间中的 score 界面 (蓝色)
- 箭头标注: "geometric correspondence (Theorem 1)"
- 底行标注: "Physical shock determines score-layer location"

### 配色
- 红色: 物理域 shock
- 蓝色: score 域 interfacial layer
- 灰色虚线: 对应关系
- 黑色: PDE 轨迹

### 亮点
1. **一目了然**: 三栏并行, 读图 10 秒理解"两个 Burgers 耦合"的核心 idea
2. **定理锚定**: 右栏直接标注 "Theorem 1", 把图和主定理绑定
3. **论文辨识度**: 左侧教科书式的时空图 + 右侧高维 score 界面, 两者并置是 NeurIPS 上少见的路子

---

## Figure 2 · BV-aware 参数化架构 (BV-aware Parameterization)

**位置**: `paper/black/sections/03_method.tex` §3.2, 紧接 Eq. 3.2 之后

**目的**: 展示网络结构的核心 novelty——三个子网络 + tanh 硬编码。这是 reviewer 在方法节能看到的第一个图, 必须专业清晰。

### 布局（纵向流程 + 右侧输出）

```
输入: u ∈ R^N_x, σ ∈ R
        |
   ┌────┼────┐
   │    │    │
   ▼    ▼    ▼
┌──────┐ ┌──────┐ ┌──────┐
│φ_sm  │ │φ_sh  │ │ κ    │
│UNet  │ │Conv1d│ │Conv1d│
│      │ │      │ │+Softplus│
│  ↓   │ │  ↓   │ │  ↓   │
│∇φ_sm │ │∇φ_sh │ │ κ>0  │
└──┬───┘ └──┬───┘ └──┬───┘
   │        │        │
   │   ┌────┘        │
   │   │  ┌──────────┘
   │   │  │
   ▼   ▼  ▼
   s_θ = ∇φ_sm  +  (κ/2) · tanh(φ_sh / 2σ²) · ∇φ_sh
   │
   ▼
   D_x = x + σ²·s_θ  (Tweedie)
```

### 上部: 输入
- 左侧: u ∈ R^{128} (噪声解的 1D 剖面, 画一条曲线)
- 右侧: σ (噪声水平, 标注 "viscosity-matched: σ²=2ντ")

### 中部: 三个子网络（并排）
1. **φ_sm (左)**: U-Net 1D backbone, 输出光滑背景势, 求梯度得 ∇φ_sm
   - 画一个小 U-Net 图标 (编码器-解码器结构)
2. **φ_sh (中)**: 两层 Conv1d, 输出 signed distance to shock
   - 画一个红色曲线在 shock 处过零
   - 标注 "zero at shock"
3. **κ (右)**: 两层 Conv1d + Softplus, 输出局部跳跃强度
   - 标注 "κ ≥ κ₀ > 0 (Softplus)"
   - 标注 "↔ Rankine-Hugoniot condition"

### 下部: 组合
- 用公式 s_θ = ∇φ_sm + (κ/2)·tanh(φ_sh/2σ²)·∇φ_sh 把三个组件连接
- tanh 因子高亮, 标注 "hard-coded NOT learned!"
- 最终输出 D_x 标注 "Tweedie: D_x = x + σ²·s_θ"

### 配色
- 绿色框: φ_sm (光滑背景)
- 红色框: φ_sh (shock 几何)  
- 蓝色框: κ (跳跃强度)
- 金色高亮: tanh 因子 (核心 novelty)
- 灰色: 输入/输出

### 亮点
1. **直接的 novelty 展示**: tanh 因子用不同颜色 + "not learned!" 标注, 强调与标准 EDM 的区别
2. **公式与图的对应**: Eq. 3.2 的每一项在图中都有视觉对应
3. **物理直觉**: κ 旁边标注 Rankine-Hugoniot, 连接 Theorem 4
4. **NeurIPS 风格**: 干净、信息密度高、每个标注都有意义

---

## 制作建议

### 工具
- 矢量图用 **TikZ** (LaTeX 内嵌, 字体一致, 数学符号完美)
- 或 **matplotlib + Inkscape** 导出 PDF (简单但字体可能不一致)
- 推荐方案: 先手绘草图, 再用 TikZ 精准实现

### 尺寸
- NeurIPS 正文宽度 ≈ 15.5cm
- Figure 1: 占满单栏宽, 高度 ≈ 5.5cm
- Figure 2: 占 0.95 单栏宽, 高度 ≈ 4.5cm

### 字体
- 所有标注用 \small 或 \footnotesize
- 数学符号与正文宏完全一致 (`\flux`, `\sth`, `\phissh`, etc.)
- 中文字体不可用 (英文学术论文)
