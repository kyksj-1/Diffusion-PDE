"""scripts/sample.py · 从训练好的 ckpt 生成样本。

使用:
    python scripts/sample.py --config config/e1_burgers.yaml --ckpt outputs/E1/ckpt.pt
"""

from __future__ import annotations
import argparse


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="EntroDiff sampling")
    p.add_argument("--config", type=str, required=True)
    p.add_argument("--ckpt",   type=str, required=True)
    p.add_argument("--n_samples", type=int, default=1024)
    p.add_argument("--output_dir", type=str, default="outputs")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    print(f"[EntroDiff/sample] config={args.config} ckpt={args.ckpt}")
    raise NotImplementedError("Sampling pipeline will be implemented in Week 5-6.")


if __name__ == "__main__":
    main()
