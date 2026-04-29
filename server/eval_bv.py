import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Sync fixed score_param.py
import os
local = r'D:\A-Nips-Diffussion\PROJECT\black\src\models\score_param.py'
with open(local, 'r', encoding='utf-8') as f:
    content = f.read()
sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/EntroDiffCode/src/models/score_param.py', 'w') as f:
    f.write(content)
sftp.close()
print("score_param.py synced")

# Now run BV-aware eval 50 steps with PDE 0.1
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_viz.py \
  --config configs/experiment/bvaware_server.yaml \
  --ckpt_ours output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_192226_ep200.pt \
  --model_type bvaware --model_dim 128 \
  --heun_steps 50 --zeta_pde 0.1 \
  --n_samples 4 \
  2>&1 | grep -v "FutureWarning\|paramiko\|Cryptography\|cipher\|class"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        print(stdout.channel.recv(4096).decode(), end='', flush=True)
    if stderr.channel.recv_stderr_ready():
        print(stderr.channel.recv_stderr(4096).decode(), end='', flush=True)
    time.sleep(0.5)
print(stdout.read().decode())
print(stderr.read().decode()[:300] if stderr.read().decode() else '')

ssh.close()
