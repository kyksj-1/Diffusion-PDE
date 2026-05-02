"""补传服务器缺失的 W5-C 修改文件 (losses.py 派遣等)."""
import paramiko
from pathlib import Path

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
sftp = ssh.open_sftp()

REMOTE_ROOT = '/home/liuyanzhi/ljz/EntroDiffCode'
LOCAL_ROOT = Path('D:/A-Nips-Diffussion/PROJECT/black')

# 补传 W5-C 阶段所有 modified 文件 (服务器可能回滚了部分)
files_to_upload = [
    "src/diffusion/losses.py",       # _resolve_flux_fn + pde_id
    "src/diffusion/samplers.py",     # pde_id 透传
    "src/models/dit_1d.py",          # DiT-1D backbone
    "src/models/foundation_score.py", # FoundationScore
    "src/data/mixed_pde_dataset.py", # MixedPDEDataset
    "scripts/train_foundation.py",   # foundation training
    "tests/test_dit_1d.py",
    "tests/test_mixed_pde_dataset.py",
    "tests/test_dit_scores.py",
    "configs/foundation/_pdes_template.yaml",
    "configs/foundation/tiny.yaml",
    "configs/foundation/small.yaml",
    "configs/foundation/base.yaml",
    "configs/foundation/smoke.yaml",
]

print(f"补传 {len(files_to_upload)} 个文件...")
for rel in files_to_upload:
    local_path = LOCAL_ROOT / rel
    remote_path = f"{REMOTE_ROOT}/{rel}"
    if not local_path.exists():
        print(f"  [SKIP] {rel}")
        continue
    sftp.put(str(local_path), remote_path)
    print(f"  [OK] {rel} ({local_path.stat().st_size:,} bytes)")

sftp.close()

# 验证: import + 跑全 W5 测试
print("\n=== 验证: 全 W5 测试 ===")
PYTHON = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python'
stdin, stdout, _ = ssh.exec_command(
    f'cd {REMOTE_ROOT} && '
    f'{PYTHON} -m pytest tests/test_dit_1d.py tests/test_mixed_pde_dataset.py '
    f'tests/test_dit_scores.py tests/test_shock_metrics.py tests/test_euler_pipeline.py '
    f'2>&1 | tail -5'
)
print(stdout.read().decode())

ssh.close()
