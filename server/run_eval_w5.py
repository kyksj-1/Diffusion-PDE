"""W5 训练完成 → 跑 eval_foundation 出跨 PDE 表."""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

REMOTE_ROOT = '/home/liuyanzhi/ljz/EntroDiffCode'
PYTHON = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python'

# 1. 找最新 ckpt
print("=" * 60)
print("1. 找 ep200 ckpt")
print("=" * 60)
stdin, stdout, _ = ssh.exec_command(
    f'ls -la {REMOTE_ROOT}/output/experiments/foundation_small/*.pt 2>&1 | tail -5'
)
print(stdout.read().decode())

# 2. 跑 eval (50 Heun 步, 8 samples per PDE)
print("=" * 60)
print("2. 启动 eval_foundation (CUDA_VISIBLE_DEVICES=0, num_steps=50, n_samples=16)")
print("=" * 60)
eval_cmd = (
    f'cd {REMOTE_ROOT} && '
    f'CKPT=$(ls output/experiments/foundation_small/*ep200*.pt | head -1) && '
    f'echo "USING: $CKPT" && '
    f'CUDA_VISIBLE_DEVICES=0 {PYTHON} scripts/eval_foundation.py '
    f'--ckpt "$CKPT" --n_samples 16 --num_steps 50 2>&1'
)
stdin, stdout, stderr = ssh.exec_command(eval_cmd, timeout=900)
out = stdout.read().decode()
err = stderr.read().decode()
print(out)
if err.strip(): print("STDERR:", err[:1000])

ssh.close()
