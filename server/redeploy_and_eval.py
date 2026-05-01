"""W5 R7 修复后: 上传 score_param.py + 重跑 eval."""
import paramiko
from pathlib import Path

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

REMOTE_ROOT = '/home/liuyanzhi/ljz/EntroDiffCode'
PYTHON = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python'
LOCAL_ROOT = Path('D:/A-Nips-Diffussion/PROJECT/black')

# 1. 上传修复后的 score_param.py + 测试更新
sftp = ssh.open_sftp()
for fp in ['src/models/score_param.py', 'tests/test_dit_scores.py']:
    sftp.put(str(LOCAL_ROOT / fp), f'{REMOTE_ROOT}/{fp}')
    print(f"[OK] uploaded {fp}")
sftp.close()

# 2. 服务器跑测试 + eval
print("\n=== 服务器测试 ===")
stdin, stdout, _ = ssh.exec_command(
    f'cd {REMOTE_ROOT} && {PYTHON} -m pytest tests/test_dit_scores.py 2>&1 | tail -3'
)
print(stdout.read().decode())

print("\n=== 跑 eval_foundation (ep200, 50 Heun 步, 16 samples per PDE) ===")
eval_cmd = (
    f'cd {REMOTE_ROOT} && '
    f'CKPT=$(ls output/experiments/foundation_small/*ep200*.pt | head -1) && '
    f'CUDA_VISIBLE_DEVICES=0 {PYTHON} scripts/eval_foundation.py '
    f'--ckpt "$CKPT" --n_samples 16 --num_steps 50 2>&1'
)
stdin, stdout, stderr = ssh.exec_command(eval_cmd, timeout=900)
out = stdout.read().decode()
print(out)
err = stderr.read().decode()
if err.strip(): print("STDERR:", err[:1000])

ssh.close()
