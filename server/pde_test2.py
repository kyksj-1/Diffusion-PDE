import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Sync sampler
import os
local = r'D:\A-Nips-Diffussion\PROJECT\black\src\diffusion\samplers.py'
with open(local, 'r', encoding='utf-8') as f:
    content = f.read()
sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/EntroDiffCode/src/diffusion/samplers.py', 'w') as f:
    f.write(content)
sftp.close()
print("samplers.py synced")

# Test PDE guidance with StandardScore
tests = [
    ("StdScore zeta=0", "output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt", "standard", 0.0),
    ("StdScore zeta=0.1", "output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt", "standard", 0.1),
    ("StdScore zeta=0.5", "output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt", "standard", 0.5),
]

for label, ckpt, mtype, zpde in tests:
    cmd = f'''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_viz.py \
  --config configs/experiment/bvaware_server.yaml \
  --ckpt_ours {ckpt} \
  --model_type {mtype} \
  --heun_steps 50 --zeta_pde {zpde} \
  --n_samples 4 \
  2>&1 | grep "平均:"
'''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    print(f"  {label:<25} {out}")

ssh.close()
