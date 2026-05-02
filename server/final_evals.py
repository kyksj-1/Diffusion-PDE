import paramiko, json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
py = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python3'
base = '/home/liuyanzhi/ljz/EntroDiffCode'

script = '''
import sys; sys.path.append("''' + base + '''")
import torch, math, numpy as np
from src.models.score_param import BVAwareScore, StandardScore
from src.diffusion.samplers import entrodiff_heun_sampler
from scipy.stats import wasserstein_distance
from src.utils.env_manager import env
device = torch.device("cuda"); nu = 1.0

burger = np.load(env.data_dir / "burgers_1d_N5000_Nx128.npy")
gt_b, ic_b = burger[-500:,-1,:], burger[-500:,0,:]
nx_b = burger.shape[-1]

results = {}

# ours_full 500ep (BVAwareScore, dim=256, in_channels=1)
m = BVAwareScore(in_channels=1, dim=256, return_denoiser=True).to(device)
m.load_state_dict(torch.load("''' + base + '''/output/experiments/ours_full/entrodiff_ours_full_20260429_223734_ep500.pt", map_location=device))
m.eval()
gen = entrodiff_heun_sampler(m, (4,1,nx_b), 0.002, math.sqrt(2*nu), 1.0, nu, 50, device=device)
gen = gen.squeeze().cpu().numpy()
results["ours_full 500ep"] = np.mean([wasserstein_distance(gt_b[i], gen[i]) for i in range(4)])

# e2_bl 200ep (StandardScore, in_channels=1)
bl = np.load(env.data_dir / "bl_1d_N5000_Nx128.npy")
gt_l, ic_l = bl[-500:,-1,:], bl[-500:,0,:]
nx_l = bl.shape[-1]
m2 = StandardScore(in_channels=1).to(device)
m2.load_state_dict(torch.load("''' + base + '''/output/experiments/e2_bl_run/entrodiff_e2_bl_run_20260429_224149_ep200.pt", map_location=device))
m2.eval()
gen2 = entrodiff_heun_sampler(m2, (4,1,nx_l), 0.002, math.sqrt(2*nu), 1.0, nu, 50, device=device)
gen2 = gen2.squeeze().cpu().numpy()
results["e2_bl Ours 200ep"] = np.mean([wasserstein_distance(gt_l[i], gen2[i]) for i in range(4)])

for k, v in results.items():
    print(f"{k}: W1={v:.4f}")
'''

with ssh.open_sftp() as sftp:
    with sftp.file('/tmp/eval_script.py', 'w') as f:
        f.write(script)

stdin, stdout, stderr = ssh.exec_command(f'cd {base}; {py} /tmp/eval_script.py 2>&1')
out = stdout.read().decode()
print(out)

ssh.close()
