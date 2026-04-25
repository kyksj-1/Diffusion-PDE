"""scripts/data_gen.py · 一次性生成训练 / 测试数据。

调用 pdes/<exp>.py 中的 generator，把数据存成 .npy / .npz 落到本地，
然后训练时从这里加载（避免每次重算 WENO5）。
"""

from __future__ import annotations
import argparse


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="EntroDiff dataset generation (WENO5 ground truth)")
    p.add_argument("--config", type=str, required=True,
                   help="config 决定生成哪个 PDE（e1/e2/e3）")
    p.add_argument("--output_dir", type=str, default="data")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    print(f"[EntroDiff/data_gen] config={args.config} → {args.output_dir}")
    raise NotImplementedError("Data generation will be implemented in Week 5.")


if __name__ == "__main__":
    main()
