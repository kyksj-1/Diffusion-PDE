"""scripts/eval.py · 在 ground-truth 数据集上评估生成样本。

计算论文 §7 中的指标 (W_1 / L^1 / shock-location err)，
对比 EntroDiff vs EDM baseline vs DiffusionPDE vs FNO。
"""

from __future__ import annotations
import argparse


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="EntroDiff evaluation")
    p.add_argument("--config", type=str, required=True)
    p.add_argument("--ckpt",   type=str, required=True)
    p.add_argument("--baselines", type=str, nargs="*", default=["edm", "diffusionpde", "fno"])
    return p.parse_args()


def main() -> None:
    args = parse_args()
    print(f"[EntroDiff/eval] config={args.config} ckpt={args.ckpt}")
    print(f"[EntroDiff/eval] baselines={args.baselines}")
    raise NotImplementedError("Evaluation pipeline will be implemented in Week 7.")


if __name__ == "__main__":
    main()
