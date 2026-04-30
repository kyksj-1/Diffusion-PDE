import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=30)

# Clear old logs and launch Ours
cmd_ours = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
mkdir -p output/experiments/ours_full
> output/experiments/ours_full/nohup.log
CUDA_VISIBLE_DEVICES=1 nohup python scripts/train_bvaware.py --config configs/experiment/ours_full.yaml --dim 256 >> output/experiments/ours_full/nohup.log 2>&1 &
echo "Ours PID: $!"
'''
stdin, stdout, stderr = ssh.exec_command(cmd_ours)
print("Ours:", stdout.read().decode())

# Launch Baseline
cmd_base = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
mkdir -p output/experiments/baseline_full
> output/experiments/baseline_full/nohup.log
CUDA_VISIBLE_DEVICES=2 nohup python scripts/train_baseline.py --config configs/experiment/baseline_full.yaml >> output/experiments/baseline_full/nohup.log 2>&1 &
echo "Baseline PID: $!"
'''
stdin, stdout, stderr = ssh.exec_command(cmd_base)
print("Baseline:", stdout.read().decode())

import time; time.sleep(10)

# Check GPU
stdin, stdout, stderr = ssh.exec_command('nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader')
print("\nGPU:", stdout.read().decode())

# Check processes
stdin, stdout, stderr = ssh.exec_command('ps aux | grep -E "train_bvaware|train_baseline" | grep -v grep | awk "{print \$2, \$11, \$12, \$13}"')
print("\nProcesses:", stdout.read().decode())

# Check logs
stdin, stdout, stderr = ssh.exec_command('head -3 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/ours_full/nohup.log')
print("\nOurs log:", stdout.read().decode())

stdin, stdout, stderr = ssh.exec_command('head -3 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/baseline_full/nohup.log')
print("Baseline log:", stdout.read().decode())

ssh.close()
