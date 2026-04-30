import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Sync fixed scripts
for local, remote in [
    ('D:/A-Nips-Diffussion/PROJECT/black/scripts/train_bvaware.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/scripts/train_bvaware.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/scripts/train_baseline.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/scripts/train_baseline.py'),
]:
    with open(local, 'r', encoding='utf-8') as f:
        content = f.read()
    sftp = ssh.open_sftp()
    with sftp.file(remote, 'w') as f:
        f.write(content)
    sftp.close()
    print(f"  SYNC: {remote.split('/')[-1]}")

# Stop old processes, relaunch
cmd = '''
# Kill old training processes
pkill -f train_bvaware.py 2>/dev/null; pkill -f train_baseline.py 2>/dev/null
sleep 2

cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
mkdir -p output/experiments/ours_full output/experiments/baseline_full

echo "=== Launching Ours (GPU 1, BVAwareScore dim=256, sharp data, 3 losses) ==="
CUDA_VISIBLE_DEVICES=1 nohup python scripts/train_bvaware.py --config configs/experiment/ours_full.yaml --dim 256 > output/experiments/ours_full/nohup.log 2>&1 &
echo "Ours PID: $!"

echo "=== Launching Baseline (GPU 2, StandardScore, sharp data, pure EDM) ==="
CUDA_VISIBLE_DEVICES=2 nohup python scripts/train_baseline.py --config configs/experiment/baseline_full.yaml > output/experiments/baseline_full/nohup.log 2>&1 &
echo "Baseline PID: $!"

sleep 10
echo "=== GPU ==="
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader
echo "=== Ours log ==="
cat output/experiments/ours_full/nohup.log 2>/dev/null | head -10
echo "=== Baseline log ==="
cat output/experiments/baseline_full/nohup.log 2>/dev/null | head -10
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
