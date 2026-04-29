# `pip install -e .[dev]` 从第一性原理拆解

> **写给**：物理系学生，用过 Python 但没做过工程化项目管理。
> **目标**：讲清楚为什么要这样做、发生了什么、下一步做什么。

---

## 1. 问题起点：没有 `pip install -e .` 时怎么 import 自己的代码？

假设你的项目结构是：

```
PROJECT/black/
├── src/
│   └── entrodiff/
│       ├── __init__.py
│       ├── data/
│       │   └── godunov.py
│       └── models/
│           └── unet.py
├── scripts/
│   └── train_mvp.py
```

在 `train_mvp.py` 里你想 `from entrodiff.data.godunov import generate_data`，但直接运行会报 `ModuleNotFoundError`。为什么？

**Python 的 import 搜索路径**：Python 只在 `sys.path` 里的目录中找包。`sys.path` 默认包含：
- 当前脚本所在的目录
- 系统装过的 site-packages（`pip install` 安装的地方）

`src/entrodiff/` 既不在当前脚本目录下，也不在 site-packages 里，所以 Python 找不到它。

**土办法**：在脚本开头加 `sys.path.insert(0, "../src")` 或 `os.chdir(...)`——但换个环境就炸、换个目录就报错。

---

## 2. `pip install -e .` 做了什么？

`-e` 是 `--editable`（可编辑模式），`.` 是当前目录（含 `pyproject.toml` 的那个目录）。

### 2.1 传统 pip install（非 -e）

传统的 `pip install .` 会把代码**复制**一份到 site-packages 里。之后你改了源码，site-packages 里的旧副本不动——你必须重新 `pip install .` 才能同步。开发阶段一天改几十次代码，这不可行。

### 2.2 可编辑模式（-e）

`pip install -e .` 不复制代码，而是在 site-packages 里创建一个**符号链接**（或 `.pth` 文件），指向你的 `src/` 目录。

这意味着：
- **你改了源码，import 就是改后的**，不需要重新安装
- **所有脚本**（无论放在哪个目录、用哪个 IDE 跑）都能 `from entrodiff import ...`
- **Jupyter Notebook** 里也能直接 `import entrodiff`

### 2.3 具体发生了什么

`pyproject.toml` 里有：

```toml
[project]
name = "entrodiff"

[tool.setuptools.packages.find]
where = ["src"]
```

`pip install -e .` 执行时：
1. 读 `pyproject.toml` 里的 `name`（包叫 `entrodiff`）
2. 从 `where = ["src"]` 找到 `src/entrodiff/`
3. 把 `src/` 加到 import 路径里
4. 安装 `dependencies` 里列的所有依赖（numpy, scipy, torch, matplotlib, tqdm, PyYAML）
5. 在 site-packages 里写一个 `entrodiff.pth` 文件，内容是一条路径指向你的 `src/` 目录

之后你 `import entrodiff`，Python 在 site-packages 找到这个 `.pth` 文件，沿着路径找到你的 `src/entrodiff/` 源码。

---

## 3. `[dev]` 是什么？

`pyproject.toml` 里有 `[project.optional-dependencies]`：

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4",      # 测试框架
    "ruff>=0.5",         # 静态检查 / 格式化
    "black>=24.3",       # 自动格式化
    "mypy>=1.8",         # 类型检查
    "ipykernel>=6.27",   # Jupyter 内核
    "jupyterlab>=4.0",   # Jupyter 交互界面
]
```

`[dev]` 就是 "把这一组包都装上"。你也可以有 `[viz]`、`[pde]` 等分组，按需装：

```bash
pip install -e .[dev]        # 开发用：代码 + 测试 + lint
pip install -e .[viz]         # 加绘图工具
pip install -e .[dev,viz,pde] # 全装
```

**为什么分组？** 服务器跑实验不需要 pytest/ruff/mypy，Colab 不需要 JupyterLab（自带），各环境各取所需。

---

## 4. 安装后下一步做什么？

### 4.1 验证安装

```bash
# 在任意目录运行
python -c "import entrodiff; print(entrodiff.__file__)"
```

应该打印出类似 `D:\A-Nips-Diffussion\PROJECT\black\src\entrodiff\__init__.py` 的路径——证明 import 的是你的源码而非某个副本。

### 4.2 跑第一个脚本

```bash
# 生成 Burgers 方程真值数据
python scripts/generate_data.py

# 训练 MVP
python scripts/train_mvp.py
```

此时脚本里 `from entrodiff import ...` 能正常工作了。

### 4.3 开发循环

```
你改 src/entrodiff/models/unet.py
   → 保存
      → 直接跑 python scripts/train_mvp.py
         → 自动使用最新代码（无需重新 pip install）
```

### 4.4 提交前检查（dev 工具）

```bash
ruff check src/ scripts/           # 静态检查
ruff format src/ scripts/          # 自动格式化（替代 black）
mypy src/                          # 类型检查
pytest tests/                      # 跑测试
```

---

## 5. 一句话总结

> `pip install -e .[dev]` 把你的 `src/` 变成 Python 全局可见的包，改代码即时生效，[dev] 顺手装上测试/格式化/类型检查工具。这是现代 Python 项目的标准起点。

---

## 6. 常见疑问

**Q: 能不能不装，每次用 `sys.path.insert`？**
A: 能，但每写一个脚本都要加，Jupyter 里也要加，换环境就忘，引入隐式依赖——工程上不建议。

**Q: 装在自己的 PC 上，上传到服务器后要重新装吗？**
A: 要。每台机器都要在自己的 Python 环境里 `pip install -e .`（或 `pip install -e .[dev]`）。但 pyproject.toml 和代码一样是 git 管理的，所以 clone 下来后一行命令即可。

**Q: `-e` 装的是什么东西？**
A: 装的是**你写的 code package**（即 `src/entrodiff/`）。不是装 numpy/torch，那些是 `dependencies` 自动顺带装的。

**Q: 为什么本项目没有用 `pyproject.toml` 的 `[project.scripts]` 定义 CLI 入口？**
A: MVP 阶段，直接用 `python scripts/train_mvp.py` 更直接。后续如果需要，可以用 `[project.scripts]` 定义 `entrodiff-train` 等命令行入口。
