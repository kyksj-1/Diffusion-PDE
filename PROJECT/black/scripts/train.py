"""scripts/train.py · EntroDiff 训练入口。

使用:
    python scripts/train.py --config config/e1_burgers.yaml

设计原则（按项目 CLAUDE.md "执行脚本必须有细颗粒度注释"）:
    - 仅做参数解析、流程编排、调用 src/entrodiff 中的函数
    - 不在脚本里写核心业务逻辑
    - 关键行均有注释（不仅函数级）
"""

from __future__ import annotations
import argparse
from pathlib import Path

# 解析 CLI 参数
def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    p = argparse.ArgumentParser(description="EntroDiff training")
    p.add_argument("--config", type=str, required=True,
                   help="YAML config 路径，如 config/e1_burgers.yaml")
    p.add_argument("--output_dir", type=str, default="outputs",
                   help="本地输出目录（最终归位到仓库根的 Output/balck/）")
    p.add_argument("--resume", type=str, default=None,
                   help="ckpt 路径，断点续训")
    return p.parse_args()


def main() -> None:
    """训练主流程占位。

    实际实现（Week 5-6）会按以下顺序:
        1. 加载 config（utils.io.load_yaml）
        2. 构建 PDE 数据加载器（pdes.<exp>.generate_<exp>_dataset）
        3. 构建 score 网络（models.score_baseline 或 models.score_bvaware）
        4. 构建 noise schedule（schedules.viscosity_matched）
        5. 构建损失（losses.dsm + losses.entropy_reg + losses.bv_reg + losses.burgers_consistency）
        6. 训练循环（含 EMA、checkpoint、早停）
        7. 保存 ckpt 到 Output/balck/E{N}/
    """
    args = parse_args()
    print(f"[EntroDiff] config = {args.config}")
    print(f"[EntroDiff] output_dir = {args.output_dir}")
    if args.resume is not None:
        print(f"[EntroDiff] resuming from {args.resume}")
    raise NotImplementedError("Training pipeline will be implemented in Week 5-6.")


if __name__ == "__main__":
    main()
