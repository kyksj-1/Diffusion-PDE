import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

script = '''#!/usr/bin/env python3
import sys; sys.path.append('.')
import torch, math, numpy as np
from scipy.stats import wasserstein_distance
from src.utils.env_manager import env
from src.data.burgers_dataset import BurgersDataset
from src.models.score_param import StandardScore, BVAwareScore
from src.diffusion.samplers import entrodiff_heun_sampler

dev = torch.device('cuda')
nu, tau = 1.0, 1.0
n, r = 8, 10
x = np.linspace(0, 2*np.pi, 128, endpoint=False)
ds = BurgersDataset(env.data_dir/"burgers_sharp_N5000_Nx128.npy", mode='test')
gt = ds.data[:n, -1, :]

def sw1(g, p, r=10):
    i = np.argmax(np.abs(np.gradient(g, x)))
    l, h = max(0,i-r), min(128,i+r+1)
    return wasserstein_distance(g[l:h], p[l:h])

# Ours: dim=256 (same as training)
m_ours = BVAwareScore(in_channels=1, dim=256, return_denoiser=True).to(dev)
m_ours.load_state_dict(torch.load("output/experiments/ours_full/entrodiff_ours_full_20260429_223734_ep500.pt", map_location=dev))
m_ours.eval()

# Baseline: StandardScore
m_base = StandardScore(in_channels=1).to(dev)
m_base.load_state_dict(torch.load("output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_223736_ep500.pt", map_location=dev))
m_base.eval()

print("\\n======== Shock-Region Comparison (sharp IC, 500ep) ========")
print(f"{'Method':<6} {'Stp':>3} {'W1_glob':>8} {'W1_shk':>8} {'MaxErr':>8} {'TV_r':>6}")
print("-"*46)

for s in [50, 25, 10, 5]:
    for nm, m in [("OURS", m_ours), ("BASE", m_base)]:
        g = entrodiff_heun_sampler(m, (n,1,128), 0.002, math.sqrt(2*nu*tau), tau, nu, num_steps=s, device=dev, zeta_pde=0.0).squeeze().cpu().numpy()
        wg = np.mean([wasserstein_distance(gt[i], g[i]) for i in range(n)])
        ws = np.mean([sw1(gt[i], g[i], r) for i in range(n)])
        me = np.mean([np.max(np.abs(gt[i]-g[i])) for i in range(n)])
        tv = np.mean([np.sum(np.abs(np.diff(g[i])))/(np.sum(np.abs(np.diff(gt[i])))+1e-10) for i in range(n)])
        print(f"{nm:<6} {s:>3} {wg:>8.4f} {ws:>8.4f} {me:>8.4f} {tv:>6.3f}")

print("\\nW1_shk = shock-region W1 (20 grid points around max |grad|)")
print("MaxErr = max pointwise |u_pred - u_gt| in shock region")
'''

sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/EntroDiffCode/scripts/eval_sr.py', 'w') as f:
    f.write(script)
sftp.close()

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_sr.py 2>&1 | grep -v "FutureWarning\|paramiko\|Cryptography\|cipher\|class\|BurgersDataset\|Heun Sampling"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        print(stdout.channel.recv(2048).decode(), end='', flush=True)
    time.sleep(0.3)
print(stdout.read().decode())

ssh.close()
