"""
SCP 同步: 把本地 PROJECT/black 新代码上传到服务器
(GitHub 被墙, 走 SCP 直传).
"""
import paramiko
from pathlib import Path

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
sftp = ssh.open_sftp()

REMOTE_ROOT = '/home/liuyanzhi/ljz/EntroDiffCode'
LOCAL_ROOT = Path('D:/A-Nips-Diffussion/PROJECT/black')

# 1. 创建必要目录 (src/utils 可能不存在)
print("=" * 60)
print("1. 创建必要目录")
print("=" * 60)
stdin, stdout, _ = ssh.exec_command(
    f'mkdir -p {REMOTE_ROOT}/src/utils {REMOTE_ROOT}/configs/foundation {REMOTE_ROOT}/tests && echo OK'
)
print(stdout.read().decode())

# 2. 上传所有新文件 + 修改文件
files_to_upload = [
    # SA2 E3 Euler 管线 (新)
    ("src/data/euler_dataset.py", "src/data/euler_dataset.py"),
    ("scripts/train_bvaware_euler.py", "scripts/train_bvaware_euler.py"),
    ("configs/experiment/e3_euler.yaml", "configs/experiment/e3_euler.yaml"),
    ("tests/test_euler_pipeline.py", "tests/test_euler_pipeline.py"),
    # SA3 Robust shock metric (新)
    ("src/utils/shock_metrics.py", "src/utils/shock_metrics.py"),
    ("tests/test_shock_metrics.py", "tests/test_shock_metrics.py"),
    # SA4 Sweep orchestration (新)
    ("scripts/sweep_lambda_bv.py", "scripts/sweep_lambda_bv.py"),
    ("scripts/sweep_step_budget.py", "scripts/sweep_step_budget.py"),
    ("scripts/sweep_epoch_eval.py", "scripts/sweep_epoch_eval.py"),
    # SA1 简化 (新)
    ("configs/foundation/multi_systems.yaml", "configs/foundation/multi_systems.yaml"),
    # 修改文件
    ("src/models/score_param.py", "src/models/score_param.py"),     # SA2 out_channels 扩展
    ("scripts/eval_foundation.py", "scripts/eval_foundation.py"),    # SA3 集成
]

print()
print("=" * 60)
print(f"2. SCP 上传 {len(files_to_upload)} 个文件")
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

# 3. 服务器端验证: 跑全 W5 测试 (74+ 个)
print()
print("=" * 60)
print("3. 服务器跑全 W5 测试")
print("=" * 60)
PYTHON = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python'
test_cmd = (
    f'cd {REMOTE_ROOT} && '
    f'{PYTHON} -m pytest tests/test_dit_1d.py tests/test_mixed_pde_dataset.py '
    f'tests/test_dit_scores.py tests/test_shock_metrics.py tests/test_euler_pipeline.py '
    f'2>&1 | tail -10'
)
stdin, stdout, stderr = ssh.exec_command(test_cmd, timeout=120)
print(stdout.read().decode())
err = stderr.read().decode()
if err.strip(): print("STDERR:", err[:500])

# 4. 文件清单
print()
print("=" * 60)
print("4. 同步后文件清单")
print("=" * 60)
ls_cmd = (
    f'cd {REMOTE_ROOT} && '
    f'ls scripts/sweep_*.py scripts/train_bvaware_euler.py '
    f'src/utils/shock_metrics.py src/data/euler_dataset.py '
    f'configs/experiment/e3_euler.yaml configs/foundation/multi_systems.yaml '
    f'tests/test_shock_metrics.py tests/test_euler_pipeline.py 2>&1'
)
stdin, stdout, _ = ssh.exec_command(ls_cmd)
print(stdout.read().decode())

# 5. GPU 状态 + tmux 状态 (留给 cron 用)
print()
print("=" * 60)
print("5. GPU + tmux 状态 (cron 触发前)")
print("=" * 60)
stdin, stdout, _ = ssh.exec_command(
    'nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader && '
    'echo --- tmux --- && tmux ls'
)
print(stdout.read().decode())

ssh.close()
print("\n[DONE] 服务器代码同步完成. cron 21:23 触发时可以直接跑 train_bvaware_euler 等新脚本")
