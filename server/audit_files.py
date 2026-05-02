import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# List all untracked/modified files with some context
files_to_check = [
    'scripts/eval_shock_region.py',
    'scripts/eval_sr.py',
    'scripts/eval_step_ablation.py',
    'scripts/generate_bl_data.py',
    'scripts/generate_coarse_data.py',
    'scripts/generate_sharp_data.py',
    'scripts/test_time_loss.py',
    'configs/experiment/bvaware_server.yaml',
    'configs/experiment/baseline_full.yaml',
    'configs/experiment/e2_bl.yaml',
    'configs/experiment/ours_full.yaml',
    'launch.sh',
    'src/pdes/',
]

for f in files_to_check:
    if f.endswith('/'):
        cmd = f'ls /home/liuyanzhi/ljz/EntroDiffCode/{f}'
    else:
        cmd = f'head -3 /home/liuyanzhi/ljz/EntroDiffCode/{f} 2>/dev/null && echo "..." || echo "NOT_FOUND"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    print(f"\n=== {f} ===")
    print(out[:200])
    print()

ssh.close()
