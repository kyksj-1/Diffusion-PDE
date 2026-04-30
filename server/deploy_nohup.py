import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Kill old tmux session
ssh.exec_command('tmux kill-session -t entrodiff 2>/dev/null')
time.sleep(1)

# Create output dirs and launch both trainings
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
mkdir -p output/experiments/ours_full output/experiments/baseline_full

echo "=== Launching Ours (GPU 1, BVAwareScore dim=256, 500ep) ==="
CUDA_VISIBLE_DEVICES=1 nohup python scripts/train_bvaware.py --config configs/experiment/ours_full.yaml --dim 256 > output/experiments/ours_full/nohup.log 2>&1 &
echo "Ours PID: $!"

echo "=== Launching Baseline (GPU 2, StandardScore, 500ep) ==="
CUDA_VISIBLE_DEVICES=2 nohup python scripts/train_baseline.py --config configs/experiment/baseline_full.yaml > output/experiments/baseline_full/nohup.log 2>&1 &
echo "Baseline PID: $!"

sleep 8
echo "=== GPU ==="
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader
echo "=== Ours first lines ==="
head -5 output/experiments/ours_full/nohup.log 2>/dev/null
echo "=== Baseline first lines ==="
head -5 output/experiments/baseline_full/nohup.log 2>/dev/null
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
err = stderr.read().decode()
print(out)
if err: print("STDERR:", err[:500])

ssh.close()
