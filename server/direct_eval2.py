import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

base = '/home/liuyanzhi/ljz/EntroDiffCode'

cmd = f'''
cd {base}
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python3 -c "
import sys; sys.path.append('.')
import torch, math, numpy as np
from src.models.score_param import BVAwareScore
from src.diffusion.samplers import entrodiff_heun_sampler
from scipy.stats import wasserstein_distance
from src.utils.env_manager import env
device = torch.device('cuda'); nu = 1.0

# ==== E2 Buckley-Leverett BV-aware (in_channels=2, IC-conditioned) ====
bl = np.load(env.data_dir / 'bl_1d_N5000_Nx128.npy')
gt_bl, ic_bl = bl[-500:,-1,:], bl[-500:,0,:]

m = BVAwareScore(in_channels=2, dim=128, return_denoiser=True).to(device)
m.load_state_dict(torch.load('output/experiments/e2_bvaware_run/entrodiff_e2_bvaware_run_20260430_210312_ep200.pt', map_location=device)); m.eval()

gen = entrodiff_heun_sampler(m, (4,1,128), 0.002, math.sqrt(2*nu), 1.0, nu, 50, device=device, ic=torch.tensor(ic_bl[:4], device=device).unsqueeze(1))
gen = gen.squeeze().cpu().numpy()
w1 = [wasserstein_distance(gt_bl[i], gen[i]) for i in range(4)]
print(f'E2 BV-aware+IC 200ep: W1={{np.mean(w1):.4f}}')

# ==== Sharp Ours BV-aware (in_channels=1? check) ====
ckpt2 = 'output/experiments/sharp_ours/entrodiff_sharp_ours_20260430_210638_ep500.pt'
# Check in_channels
sd = torch.load(ckpt2, map_location='cpu')
ch = sd['phi_sm_net.init_conv.weight'].shape[1]
print(f'Sharp Ours in_channels={{ch}}')

m2 = BVAwareScore(in_channels=ch, dim=128, return_denoiser=True).to(device)
m2.load_state_dict(torch.load(ckpt2, map_location=device)); m2.eval()

sharp = np.load(env.data_dir / 'burgers_sharp_N5000_Nx128.npy')
gt_s, ic_s = sharp[-500:,-1,:], sharp[-500:,0,:]

ic_arg = torch.tensor(ic_s[:4], device=device).unsqueeze(1) if ch==2 else None
gen2 = entrodiff_heun_sampler(m2, (4,1,128), 0.002, math.sqrt(2*nu), 1.0, nu, 50, device=device, ic=ic_arg)
gen2 = gen2.squeeze().cpu().numpy()
w1s = [wasserstein_distance(gt_s[i], gen2[i]) for i in range(4)]
print(f'Sharp BV-aware 500ep (ch={{ch}}): W1={{np.mean(w1s):.4f}}')

# ==== Foundation small 200ep ====
ckpt3 = 'output/experiments/foundation_small/foundation_foundation_small_20260501_000735_ep200.pt'
sd3 = torch.load(ckpt3, map_location='cpu')
# Find first key to check architecture
for k in list(sd3.keys())[:3]: print(f'Found key: {{k}} shape={{sd3[k].shape}}')
" 2>&1 | grep -v "FutureWarning\|paramiko\|Cryptography\|Heun Sampling\|cipher"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
print(out)

ssh.close()
