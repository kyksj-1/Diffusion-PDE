import paramiko, os, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Sync all new/updated files to server
base = r'D:\A-Nips-Diffussion\PROJECT\black'
remote_base = '/home/liuyanzhi/ljz/EntroDiffCode'

files = [
    'src/diffusion/losses.py',
    'scripts/train_mvp.py',
    'src/pdes/__init__.py',
    'src/pdes/bl_flux.py',
    'src/pdes/bl_solver.py',
    'scripts/generate_bl_data.py',
    'scripts/eval_step_ablation.py',
    'scripts/generate_sharp_data.py',
    'scripts/generate_coarse_data.py',
    'configs/experiment/e2_bl.yaml',
    'scripts/test_time_loss.py',
]

sftp = ssh.open_sftp()
for f in files:
    local_path = os.path.join(base, f)
    remote_path = f'{remote_base}/{f}'
    # Ensure parent dir exists
    remote_parent = '/'.join(remote_path.split('/')[:-1])
    try:
        sftp.stat(remote_parent)
    except:
        stdin, stdout, stderr = ssh.exec_command(f'mkdir -p {remote_parent}')
        stdout.read()
    
    with open(local_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    with sftp.file(remote_path, 'w') as fh:
        fh.write(content)
    print(f'  OK: {f}')
sftp.close()
print('\nAll files synced!')

# Now check server resources
cmd = '''
echo "=== GPU ==="
nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader
echo "=== RAM ==="
free -h | head -2
echo "=== Disk ==="
df -h /home | tail -1
echo "=== tmux ==="
tmux ls 2>/dev/null || echo "No tmux sessions"
echo "=== Data files ==="
ls -lh /home/liuyanzhi/ljz/EntroDiffCode/output/data/ 2>/dev/null
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print('\n' + stdout.read().decode())

ssh.close()
