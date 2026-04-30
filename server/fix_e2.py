import paramiko, time
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Read current train_mvp.py
sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/EntroDiffCode/scripts/train_mvp.py', 'r') as f:
    content = f.read().decode('utf-8')
sftp.close()

# Find and fix the problematic line
if 'exp_cfg.get("data_file"' in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'exp_cfg.get("data_file"' in line:
            lines[i] = '    data_path = env.data_dir / "burgers_1d_N5000_Nx128.npy"  # default, E2 overrides below'
        if 'lambda_time = float(exp_cfg.get("lambda_time"' in line and 'bl_data' not in content:
            lines[i] = line + '\n    if exp_cfg.get("data_file", "").startswith("bl_"): data_path = env.data_dir / exp_cfg["data_file"]'
    content = '\n'.join(lines)
else:
    print("Line not found, checking...")
    import re
    m = re.search(r'data_path.*burgers', content)
    if m: print(f"Current data_path: {m.group()}")

# Write back
sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/EntroDiffCode/scripts/train_mvp.py', 'w') as f:
    f.write(content)
sftp.close()
print("train_mvp.py fixed")

# Restart E2
cmd = """tmux send-keys -t entrodiff:2 C-c 2>/dev/null; sleep 1
tmux send-keys -t entrodiff:2 'cd /home/liuyanzhi/ljz/EntroDiffCode && export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH && CUDA_VISIBLE_DEVICES=2 python scripts/train_mvp.py --config configs/experiment/e2_bl.yaml 2>&1 | tee output/experiments/e2_bl_ours.log' Enter
sleep 4
tail -5 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/e2_bl_ours.log"""
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
