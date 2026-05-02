import paramiko, time, re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

base = '/home/liuyanzhi/ljz/EntroDiffCode'

# Simple direct eval using Python (bypass eval_viz.py's config issues)
# Test E2 BV-aware on Buckley-Leverett data
cmd = f'''
cd {base}
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python3 -c "
import sys; sys.path.append('.')
import torch, math, numpy as np
from src.models.score_param import BVAwareScore, StandardScore
from src.diffusion.samplers import entrodiff_heun_sampler
from scipy.stats import wasserstein_distance
from src.utils.env_manager import env

device = torch.device('cuda')
nu, tau_max = 1.0, 1.0

# Load BL test data
bl_data = np.load(env.data_dir / 'bl_1d_N5000_Nx128.npy')
gt = bl_data[-500:, -1, :]  # last 500 = test
print(f'BL test: {{gt.shape}}')

# E2 BV-aware
ckpt = 'output/experiments/e2_bvaware_run/entrodiff_e2_bvaware_run_20260430_210312_ep200.pt'
m = BVAwareScore(in_channels=1, dim=128, return_denoiser=True).to(device)
m.load_state_dict(torch.load(str(ckpt), map_location=device)); m.eval()

gen = entrodiff_heun_sampler(m, (4,1,128), 0.002, math.sqrt(2*nu), tau_max, nu, 50, device=device)
gen = gen.squeeze().cpu().numpy()

w1s = [wasserstein_distance(gt[i], gen[i]) for i in range(4)]
l1s = [np.linalg.norm(gen[i]-gt[i],1)/(np.linalg.norm(gt[i],1)+1e-10) for i in range(4)]
print(f'E2 BV-aware: W1={{np.mean(w1s):.4f}} L1={{np.mean(l1s):.4f}} range=[{{gen.min():.3f}},{{gen.max():.3f}}]')

# Sharp Ours BV-aware 500ep
ckpt2 = 'output/experiments/sharp_ours/entrodiff_sharp_ours_20260430_210638_ep500.pt'
m2 = BVAwareScore(in_channels=1, dim=128, return_denoiser=True).to(device)
m2.load_state_dict(torch.load(str(ckpt2), map_location=device)); m2.eval()

sharp_data = np.load(env.data_dir / 'burgers_sharp_N5000_Nx128.npy')
gt2 = sharp_data[-500:, -1, :]
gen2 = entrodiff_heun_sampler(m2, (4,1,128), 0.002, math.sqrt(2*nu), tau_max, nu, 50, device=device)
gen2 = gen2.squeeze().cpu().numpy()
w1s2 = [wasserstein_distance(gt2[i], gen2[i]) for i in range(4)]
print(f'Sharp Ours BV-aware 500ep: W1={{np.mean(w1s2):.4f}} range=[{{gen2.min():.3f}},{{gen2.max():.3f}}]')
" 2>&1 | grep -v "FutureWarning\|paramiko\|Cryptography\|Heun Sampling\|cipher"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
print(out)

ssh.close()
