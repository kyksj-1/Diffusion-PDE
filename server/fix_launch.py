import paramiko, os, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=30)

# Read both files from local
files = {
    'train_bvaware.py': 'D:/A-Nips-Diffussion/PROJECT/black/scripts/train_bvaware.py',
    'train_baseline.py': 'D:/A-Nips-Diffussion/PROJECT/black/scripts/train_baseline.py',
}

for name, local_path in files.items():
    with open(local_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Verify data_path is AFTER exp_cfg
    idx_data = content.find('data_path = env.data_dir')
    idx_cfg = content.find("exp_cfg = yaml.safe_load")
    print(f"  {name}: data_path line before config load? {idx_data < idx_cfg}")
    
    if idx_data < idx_cfg:
        print(f"  -> STILL WRONG ORDER! Skipping {name}")
        continue
    
    # Write to server using paramiko SFTP with explicit flush
    remote = f'/home/liuyanzhi/ljz/EntroDiffCode/scripts/{name}'
    sftp = ssh.open_sftp()
    f = sftp.file(remote, 'w')
    f.write(content)
    f.close()
    sftp.close()
    print(f"  -> Written {name} ({len(content)} bytes)")

# Verify
stdin, stdout, stderr = ssh.exec_command(
    'head -55 /home/liuyanzhi/ljz/EntroDiffCode/scripts/train_bvaware.py | tail -10'
)
print("\n--- Verify: last lines of init section ---")
print(stdout.read().decode())

# Kill old + relaunch
cmd = '''
pkill -f "train_bvaware|train_baseline" 2>/dev/null; sleep 2

cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
mkdir -p output/experiments/ours_full output/experiments/baseline_full

CUDA_VISIBLE_DEVICES=1 nohup python scripts/train_bvaware.py --config configs/experiment/ours_full.yaml --dim 256 > output/experiments/ours_full/nohup.log 2>&1 &
echo "Ours PID: $!"
CUDA_VISIBLE_DEVICES=2 nohup python scripts/train_baseline.py --config configs/experiment/baseline_full.yaml > output/experiments/baseline_full/nohup.log 2>&1 &
echo "Baseline PID: $!"
sleep 8
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader
echo "--- Ours ---"; head -5 output/experiments/ours_full/nohup.log
echo "--- Baseline ---"; head -5 output/experiments/baseline_full/nohup.log
'''
stdin2, stdout2, stderr2 = ssh.exec_command(cmd)
print("\n--- Launch ---")
print(stdout2.read().decode())

ssh.close()
