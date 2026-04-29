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

# Test
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python3 -c "
import sys; sys.path.append('.')
import torch, math, numpy as np
from src.models.score_param import StandardScore
from src.diffusion.samplers import entrodiff_heun_sampler
device = torch.device('cuda')
nu, tau_max = 1.0, 1.0
model = StandardScore(in_channels=1).to(device)
model.load_state_dict(torch.load('output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt', map_location=device))
model.eval()
for zpde in [0.0, 0.1, 0.5, 1.0]:
    gen = entrodiff_heun_sampler(model, (1,1,128), 0.002, math.sqrt(2*nu*tau_max), tau_max, nu, num_steps=50, device=device, zeta_pde=zpde)
    gen = gen.squeeze().cpu().numpy()
    has_nan = 'NaN' if np.isnan(gen).any() else 'OK'
    print(f'zeta_pde={zpde:.1f} range=[{gen.min():.3f},{gen.max():.3f}] {has_nan}')
" 2>&1 | grep "zeta_pde"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
