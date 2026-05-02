import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
base = '/home/liuyanzhi/ljz/EntroDiffCode'

cmd = f'''
cd {base}
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python3 -c "
import torch, math, numpy as np
from src.models.score_param import StandardScore, BVAwareScore
from src.diffusion.samplers import entrodiff_heun_sampler
from scipy.stats import wasserstein_distance
from src.utils.env_manager import env
device = torch.device('cuda'); nu = 1.0
burger = np.load(env.data_dir / 'burgers_1d_N5000_Nx128.npy')
gt_b, ic_b = burger[-500:,-1,:], burger[-500:,0,:]
sharp = np.load(env.data_dir / 'burgers_sharp_N5000_Nx128.npy')
gt_s, ic_s = sharp[-500:,-1,:], sharp[-500:,0,:]
bl = np.load(env.data_dir / 'bl_1d_N5000_Nx128.npy')
gt_l, ic_l = bl[-500:,-1,:], bl[-500:,0,:]

# Check ourselves_full channels
sd = torch.load('output/experiments/ours_full/entrodiff_ours_full_20260429_223734_ep500.pt', map_location='cpu')
ch = sd['net.init_conv.weight'].shape[1]
print(f'ours_full in_channels={{ch}}')

# ours_full with IC
m = StandardScore(in_channels=ch).to(device)
m.load_state_dict(torch.load('output/experiments/ours_full/entrodiff_ours_full_20260429_223734_ep500.pt', map_location=device)); m.eval()
ic_t = torch.tensor(ic_b[:4], device=device).unsqueeze(1) if ch==2 else None
gen = entrodiff_heun_sampler(m, (4,1,burger.shape[-1]), 0.002, math.sqrt(2*nu), 1.0, nu, 50, device=device, ic=ic_t)
gen = gen.squeeze().cpu().numpy()
w1 = np.mean([wasserstein_distance(gt_b[i], gen[i]) for i in range(4)])
print(f'ours_full 500ep (ch={{ch}}): W1={{w1:.4f}}')

# E2 StandardScore Ours 200ep
sd2 = torch.load('output/experiments/e2_bl_run/entrodiff_e2_bl_run_20260429_224149_ep200.pt', map_location='cpu')
if 'net.init_conv.weight' in sd2:
    ch2 = sd2['net.init_conv.weight'].shape[1]
elif 'phi_sm_net.init_conv.weight' in sd2:
    ch2 = sd2['phi_sm_net.init_conv.weight'].shape[1]
else:
    ch2 = 1
print(f'e2_bl_run in_channels={{ch2}}')
m2 = StandardScore(in_channels=ch2).to(device) if 'net.init_conv' in sd2 else BVAwareScore(in_channels=ch2, dim=128, return_denoiser=True).to(device)
m2.load_state_dict(torch.load('output/experiments/e2_bl_run/entrodiff_e2_bl_run_20260429_224149_ep200.pt', map_location=device)); m2.eval()
ic_l_t = torch.tensor(ic_l[:4], device=device).unsqueeze(1) if ch2==2 else None
gen2 = entrodiff_heun_sampler(m2, (4,1,bl.shape[-1]), 0.002, math.sqrt(2*nu), 1.0, nu, 50, device=device, ic=ic_l_t)
gen2 = gen2.squeeze().cpu().numpy()
w1b = np.mean([wasserstein_distance(gt_l[i], gen2[i]) for i in range(4)])
print(f'e2_bl_run 200ep (ch={{ch2}}): W1={{w1b:.4f}}')

# E2 baseline 50ep
sd3 = torch.load('output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_191021_ep50.pt', map_location='cpu')
ch3 = sd3['net.init_conv.weight'].shape[1]
m3 = StandardScore(in_channels=ch3).to(device)
m3.load_state_dict(torch.load('output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_191021_ep50.pt', map_location=device)); m3.eval()
gen3 = entrodiff_heun_sampler(m3, (4,1,burger.shape[-1]), 0.002, math.sqrt(2*nu), 1.0, nu, 50, device=device)
gen3 = gen3.squeeze().cpu().numpy()
w1c = np.mean([wasserstein_distance(gt_b[i], gen3[i]) for i in range(4)])
print(f'baseline 50ep (ch={{ch3}}): W1={{w1c:.4f}}')
" 2>&1 | grep -v "FutureWarning\|paramiko\|Cryptography\|Heun Sampling\|cipher\|class"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
