import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=30)

# Write bash script to server
script = '''#!/bin/bash
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
mkdir -p output/experiments/ours_full output/experiments/baseline_full

echo "=== Ours (GPU 1, BVAwareScore dim=256, sharp data, 500ep) ==="
> output/experiments/ours_full/nohup.log
CUDA_VISIBLE_DEVICES=1 nohup python scripts/train_bvaware.py --config configs/experiment/ours_full.yaml --dim 256 >> output/experiments/ours_full/nohup.log 2>&1 &
echo "Ours PID: $!"

echo "=== Baseline (GPU 2, StandardScore, sharp data, 500ep) ==="
> output/experiments/baseline_full/nohup.log
CUDA_VISIBLE_DEVICES=2 nohup python scripts/train_baseline.py --config configs/experiment/baseline_full.yaml >> output/experiments/baseline_full/nohup.log 2>&1 &
echo "Baseline PID: $!"

sleep 12
echo "DONE_LAUNCH"
'''

sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/EntroDiffCode/launch.sh', 'w') as f:
    f.write(script)
sftp.close()
print("Script written to server")

# Execute
stdin, stdout, stderr = ssh.exec_command('bash /home/liuyanzhi/ljz/EntroDiffCode/launch.sh')
out = stdout.read().decode()
err = stderr.read().decode()
print(out)
if err: print("ERR:", err[:300])

# Verify
stdin, stdout, stderr = ssh.exec_command(
    'nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader; '
    'ps aux | grep -E "train_bvaware|train_baseline" | grep -v grep | head -3'
)
print("\n--- Final State ---")
print(stdout.read().decode())

ssh.close()
