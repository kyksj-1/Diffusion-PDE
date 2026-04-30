"""
W5-F 部署: 上传 W5 新文件到服务器, 检查数据.

步骤:
    1. 检查服务器 data 目录 (找 burgers / bl 数据)
    2. SCP 上传 W5 新文件:
       - src/models/dit_1d.py (新)
       - src/models/foundation_score.py (新)
       - src/data/mixed_pde_dataset.py (新)
       - src/models/score_param.py (改: 加 backbone)
       - src/diffusion/losses.py (改: 加 pde_id + flux dispatch)
       - src/diffusion/samplers.py (改: 加 pde_id + flux_type)
       - scripts/train_foundation.py (新)
       - scripts/eval_foundation.py (新)
       - configs/foundation/{tiny,small,base,smoke,_pdes_template}.yaml (新)
       - tests/test_dit_1d.py + test_mixed_pde_dataset.py + test_dit_scores.py (新)
    3. 创建必要目录 (configs/foundation/, tests/)
"""
import os
import paramiko
from pathlib import Path

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    '202.121.181.105', port=227,
    username='liuyanzhi', password='HUBRtEeOFC8F0moC',
    timeout=15,
)
sftp = ssh.open_sftp()

REMOTE_ROOT = '/home/liuyanzhi/ljz/EntroDiffCode'
LOCAL_ROOT = Path('D:/A-Nips-Diffussion/PROJECT/black')

# 1. 检查服务器数据
print("=" * 60)
print("1. 服务器数据目录检查")
print("=" * 60)
stdin, stdout, _ = ssh.exec_command(
    f'ls -la {REMOTE_ROOT}/../output/data/ 2>/dev/null || ls -la /home/liuyanzhi/ljz/output/data/ 2>/dev/null || ls -la /home/liuyanzhi/data/ 2>/dev/null || find {REMOTE_ROOT} -name "*.npy" -size +10M 2>/dev/null | head -10'
)
print(stdout.read().decode())

stdin, stdout, _ = ssh.exec_command(
    f'cat {REMOTE_ROOT}/configs/env_config.yaml 2>/dev/null'
)
print("--- 服务器 env_config.yaml ---")
print(stdout.read().decode())

# 2. 创建必要目录
print("=" * 60)
print("2. 创建 configs/foundation/ + tests/ 目录")
print("=" * 60)
stdin, stdout, stderr = ssh.exec_command(
    f'mkdir -p {REMOTE_ROOT}/configs/foundation {REMOTE_ROOT}/tests && echo OK'
)
print(stdout.read().decode())

# 3. 上传文件 (本地路径 → 服务器路径)
files_to_upload = [
    # 新模型 / 数据
    ("src/models/dit_1d.py", "src/models/dit_1d.py"),
    ("src/models/foundation_score.py", "src/models/foundation_score.py"),
    ("src/data/mixed_pde_dataset.py", "src/data/mixed_pde_dataset.py"),
    # 改动现有 (W5-C)
    ("src/models/score_param.py", "src/models/score_param.py"),
    ("src/diffusion/losses.py", "src/diffusion/losses.py"),
    ("src/diffusion/samplers.py", "src/diffusion/samplers.py"),
    # 训练 / 评估
    ("scripts/train_foundation.py", "scripts/train_foundation.py"),
    ("scripts/eval_foundation.py", "scripts/eval_foundation.py"),
    # 配置
    ("configs/foundation/tiny.yaml", "configs/foundation/tiny.yaml"),
    ("configs/foundation/small.yaml", "configs/foundation/small.yaml"),
    ("configs/foundation/base.yaml", "configs/foundation/base.yaml"),
    ("configs/foundation/smoke.yaml", "configs/foundation/smoke.yaml"),
    ("configs/foundation/_pdes_template.yaml", "configs/foundation/_pdes_template.yaml"),
    # 测试
    ("tests/test_dit_1d.py", "tests/test_dit_1d.py"),
    ("tests/test_mixed_pde_dataset.py", "tests/test_mixed_pde_dataset.py"),
    ("tests/test_dit_scores.py", "tests/test_dit_scores.py"),
]

print("=" * 60)
print(f"3. 上传 {len(files_to_upload)} 个文件")
print("=" * 60)
for local_rel, remote_rel in files_to_upload:
    local_path = LOCAL_ROOT / local_rel
    remote_path = f"{REMOTE_ROOT}/{remote_rel}"
    if not local_path.exists():
        print(f"  [SKIP] 本地不存在: {local_path}")
        continue
    sftp.put(str(local_path), remote_path)
    sz = local_path.stat().st_size
    print(f"  [OK] {local_rel}  ({sz:,} bytes)")

sftp.close()

# 4. 在服务器上验证
print()
print("=" * 60)
print("4. 服务器上验证 + Python sanity import")
print("=" * 60)
verify_cmd = f'''
cd {REMOTE_ROOT}
ls scripts/train_foundation.py scripts/eval_foundation.py 2>&1
echo "---"
ls configs/foundation/
echo "---"
ls src/models/ src/data/ | grep -E "(dit_1d|foundation_score|mixed_pde)" 2>&1
echo "---"
/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python -c "
import sys; sys.path.insert(0, '.')
from src.models.dit_1d import DiT1D
from src.models.foundation_score import FoundationScore
from src.data.mixed_pde_dataset import MixedPDEDataset
print('imports OK')
import torch
m = DiT1D(in_channels=2, out_channels=1, Nx=128, dim=64, n_layers=2, n_heads=4, patch_size=4, n_pde_types=2)
n = sum(p.numel() for p in m.parameters())
print(f'DiT1D tiny params: {{n:,}}')
"
'''
stdin, stdout, stderr = ssh.exec_command(verify_cmd)
print(stdout.read().decode())
err = stderr.read().decode()
if err.strip(): print("STDERR:", err[:500])

ssh.close()
print("\n[deploy] 完成. 下一步: 检查数据 → 决定先 smoke test 还是直接 small 配置训练")
