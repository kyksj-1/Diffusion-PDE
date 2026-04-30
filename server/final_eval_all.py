import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Run BV-aware eval on GPU 1 + E2 baseline training on GPU 2
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH

echo "=== BV-aware 500ep eval ==="
CUDA_VISIBLE_DEVICES=1 python scripts/eval_viz.py \
  --config configs/experiment/bvaware_server.yaml \
  --ckpt_ours output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_223912_ep500.pt \
  --ckpt_baseline output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_191021_ep50.pt \
  --model_type bvaware --model_dim 128 \
  --heun_steps 50 --zeta_pde 0.0 --n_samples 4 \
  2>&1 | grep -E "平均|W₁"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
print(out)

# Also queue E2 baseline training in background
cmd2 = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
# Need to modify train_baseline to use BL data
CUDA_VISIBLE_DEVICES=2 nohup python -c "
import sys; sys.path.append('.')
import torch, torch.optim as optim
from torch.utils.data import DataLoader
from src.utils.env_manager import env
from src.data.burgers_dataset import BurgersDataset
from src.models.score_param import StandardScore
from src.diffusion.schedules import BaselineSchedule
from src.diffusion.losses import get_dsm_loss
from datetime import datetime

device = torch.device('cuda')
batch_size = 64
data_path = env.data_dir / 'bl_1d_N5000_Nx128.npy'
output_dir = env.output_dir / 'e2_bl_baseline'
output_dir.mkdir(parents=True, exist_ok=True)

ds = BurgersDataset(data_path, mode='train')
loader = DataLoader(ds, batch_size=batch_size, shuffle=True)

model = StandardScore(in_channels=1).to(device)
opt = optim.Adam(model.parameters(), lr=2e-4)
schedule = BaselineSchedule()
ts = datetime.now().strftime('%Y%m%d_%H%M%S')

for ep in range(50):
    model.train()
    for batch in loader:
        x = batch[:, -1, :].unsqueeze(1).to(device)
        sigmas = schedule.sample_sigma(x.shape[0], device)
        opt.zero_grad()
        loss = get_dsm_loss(model, x, sigmas)
        loss.backward(); opt.step()
    if ep % 10 == 0: print(f'E2 BL Baseline ep {ep}')
    if (ep+1) % 10 == 0:
        torch.save(model.state_dict(), output_dir / f'entrodiff_e2bl_base_{ts}_ep{ep+1}.pt')

torch.save(model.state_dict(), output_dir / f'entrodiff_e2bl_base_{ts}_ep50.pt')
print('E2 BL Baseline done!')
" > /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/e2_bl_baseline.log 2>&1 &
echo "E2 baseline training queued on GPU 2"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2)
print(stdout.read().decode())

ssh.close()
