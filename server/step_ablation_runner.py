# Server-side step ablation script
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'EntroDiffCode'))
import torch, math, numpy as np
from src.models.score_param import BVAwareScore, StandardScore
from src.diffusion.samplers import entrodiff_heun_sampler
from src.data.burgers_dataset import BurgersDataset
from src.utils.env_manager import env
from scipy.stats import wasserstein_distance

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
nu, tau_max = 1.0, 1.0
dp = env.data_dir / 'burgers_1d_N5000_Nx128.npy'
ds = BurgersDataset(dp, mode='test')
gt = ds.data[:4, -1, :]

for label, ckpt, cls, dim in [
    ('BV-aware 200ep', 'output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_192226_ep200.pt', BVAwareScore, 128),
    ('Baseline 50ep', 'output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_191021_ep50.pt', StandardScore, None),
]:
    print(f'\n=== {label} ===')
    kwargs = {'in_channels': 1}
    if dim: kwargs['dim'] = dim
    model = cls(**kwargs).to(device)
    model.load_state_dict(torch.load(ckpt, map_location=device))
    model.eval()
    
    for steps in [10, 25, 50, 100]:
        gen = entrodiff_heun_sampler(model, (4,1,128), 0.002, math.sqrt(2*nu*tau_max), tau_max, nu, num_steps=steps, device=device)
        gen = gen.squeeze().cpu().numpy()
        w1s = [wasserstein_distance(gt[i], gen[i]) for i in range(4)]
        l1s = [np.linalg.norm(gen[i]-gt[i],1)/(np.linalg.norm(gt[i],1)+1e-10) for i in range(4)]
        print(f'  {steps:3d} steps: W1={np.mean(w1s):.4f}  L1={np.mean(l1s):.4f}')
