import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

base = '/home/liuyanzhi/ljz/EntroDiffCode'

# 1. All tmux sessions
stdin, stdout, stderr = ssh.exec_command('tmux ls 2>&1')
tmux_list = stdout.read().decode().strip()
print("=== tmux 会话 ===")
print(tmux_list)

# 2. GPU status
stdin, stdout, stderr = ssh.exec_command('nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader')
print("\n=== GPU 状态 ===")
print(stdout.read().decode())

# 3. All training log files with last line
for exp_dir in ['e2_bvaware_run', 'sharp_ours', 'sharp_baseline', 'foundation_small', 'bvaware_run', 'ours_full', 'e2_bl_run', 'mvp_baseline']:
    stdin, stdout, stderr = ssh.exec_command(
        f'ls {base}/output/experiments/{exp_dir}/train_log* 2>/dev/null | while read f; do echo "--- $f ---"; tail -1 "$f"; done'
    )
    out = stdout.read().decode().strip()
    if out:
        print(f"\n=== {exp_dir} ===")
        print(out)

# 4. Check if any training process still running
stdin, stdout, stderr = ssh.exec_command('ps aux | grep -E "train_|train_mvp|train_bv|train_found" | grep -v grep')
procs = stdout.read().decode().strip()
print("\n=== 运行中的训练进程 ===")
print(procs if procs else "无")

ssh.close()
