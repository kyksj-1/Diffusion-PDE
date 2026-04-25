"""IO / checkpoint / config 工具。"""

from __future__ import annotations
from pathlib import Path

import torch
import yaml


def load_yaml(path: str | Path) -> dict:
    """加载 YAML config。"""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_checkpoint(model: torch.nn.Module, optimizer: torch.optim.Optimizer, path: str | Path,
                     **extra) -> None:
    """保存训练 checkpoint（model, optimizer, 任意额外字段）。"""
    payload = {
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        **extra,
    }
    torch.save(payload, path)


def load_checkpoint(path: str | Path, model: torch.nn.Module,
                     optimizer: torch.optim.Optimizer | None = None) -> dict:
    """加载 ckpt，返回 extra 字段。"""
    payload = torch.load(path, map_location="cpu")
    model.load_state_dict(payload["model"])
    if optimizer is not None and "optimizer" in payload:
        optimizer.load_state_dict(payload["optimizer"])
    return {k: v for k, v in payload.items() if k not in {"model", "optimizer"}}
