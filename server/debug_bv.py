import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python3 -c "
import sys; sys.path.append('.')
import torch, math, numpy as np
from src.models.score_param import BVAwareScore
from src.diffusion.samplers import entrodiff_heun_sampler
from src.utils.env_manager import env

device = torch.device('cuda')
nu, tau_max = 1.0, 1.0

model = BVAwareScore(in_channels=1, dim=128, return_denoiser=True).to(device)
ckpt = 'output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_192226_ep200.pt'
model.load_state_dict(torch.load(ckpt, map_location=device))
model.eval()

# Test single step
shape = (1, 1, 128)
u_tau = torch.randn(shape, device=device) * math.sqrt(2 * nu * tau_max)
print(f'Init range: [{u_tau.min():.3f}, {u_tau.max():.3f}]')

for step in range(3):
    sigma_t = math.sqrt(2 * nu * tau_max) * (50 - step) / 50
    D_u = model(u_tau, torch.tensor([sigma_t], device=device))
    has_nan = torch.isnan(D_u).any()
    print(f'  Step {step}: sigma={sigma_t:.3f} D_u range=[{D_u.min():.3f}, {D_u.max():.3f}] NaN={has_nan}')
    if has_nan:
        print('  → NaN detected! Aborting.')
        break
    # Simple denoising step
    score = (D_u - u_tau) / (sigma_t ** 2)
    u_tau = u_tau - sigma_t * score * (tau_max / 50)
" 2>&1 | grep -v "FutureWarning\|paramiko\|Cryptography"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode().strip()
err = stderr.read().decode().strip()
print(out)
if err: print("ERR:", err[:500])

ssh.close()
