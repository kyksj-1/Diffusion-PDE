import paramiko, time, numpy as np

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
base = '/home/liuyanzhi/ljz/EntroDiffCode'

# Run all missing evals in one go — standard Burger data (no IC models)
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
device = torch.device('cuda'); nu = 1.0

burger = np.load(env.data_dir / 'burgers_1d_N5000_Nx128.npy')
gt_b = burger[-500:,-1,:]
sharp = np.load(env.data_dir / 'burgers_sharp_N5000_Nx128.npy')
gt_s = sharp[-500:,-1,:]

tests = [
    ('ours_full 500ep', 'output/experiments/ours_full/entrodiff_ours_full_20260429_223734_ep500.pt', StandardScore, 1, burger, gt_b, None),
    ('mvp_base 500ep', 'output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_223736_ep500.pt', StandardScore, 1, burger, gt_b, None),
    ('bvaware 500ep', 'output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_223912_ep500.pt', BVAwareScore, 1, burger, gt_b, None),
    ('bvaware 200ep', 'output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_192226_ep200.pt', BVAwareScore, 1, burger, gt_b, None),
    ('mvp_base 50ep', 'output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_191021_ep50.pt', StandardScore, 1, burger, gt_b, None),
]

for label, ckpt, cls, ch, data, gt, ic_data in tests:
    try:
        if cls == BVAwareScore:
            m = BVAwareScore(in_channels=ch, dim=128, return_denoiser=True).to(device)
        else:
            m = StandardScore(in_channels=ch).to(device)
        m.load_state_dict(torch.load(str(ckpt), map_location=device))
        m.eval()
        ic_t = None
        if ic_data is not None:
            ic_t = torch.tensor(ic_data[:4], device=device).unsqueeze(1)
        gen = entrodiff_heun_sampler(m, (4,1,gt.shape[1]), 0.002, math.sqrt(2*nu), 1.0, nu, 50, device=device, ic=ic_t)
        gen = gen.squeeze().cpu().numpy()
        w1 = np.mean([wasserstein_distance(gt[i], gen[i]) for i in range(4)])
        l1 = np.mean([np.linalg.norm(gen[i]-gt[i],1)/(np.linalg.norm(gt[i],1)+1e-10) for i in range(4)])
        print(f'{{label:<20}} W1={{w1:.4f}}  L1={{l1:.4f}}')
    except Exception as e:
        print(f'{{label:<20}} ERROR: {{str(e)[:80]}}')
" 2>&1 | grep -v "FutureWarning\|paramiko\|Cryptography\|Heun Sampling\|cipher\|class"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
print(out)

ssh.close()
