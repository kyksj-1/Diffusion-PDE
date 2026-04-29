import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python3 -c "
import sys; sys.path.append('.')
import torch, math
from src.diffusion.losses import pde_residual

# Simulate one sampling step
device = torch.device('cuda')
shape = (1, 1, 128)
nu, tau_max = 1.0, 1.0
dx = 2.0 * math.pi / shape[-1]

u_tau = torch.randn(shape, device=device) * math.sqrt(2 * nu * tau_max)
print(f'u_tau range: [{u_tau.min():.3f}, {u_tau.max():.3f}]')

# Compute Godunov residual
res = pde_residual(u_tau, dx)
print(f'pde_residual range: [{res.min():.6f}, {res.max():.6f}]')

# Try gradient
u_tau = u_tau.clone().detach().requires_grad_(True)
res = pde_residual(u_tau, dx)
loss = res.pow(2).mean()
print(f'loss: {loss.item():.6f}')
try:
    grad = torch.autograd.grad(loss, u_tau)[0]
    print(f'grad range: [{grad.min():.6f}, {grad.max():.6f}] NaN={torch.isnan(grad).any()}')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())
print(stderr.read().decode()[:500])

ssh.close()
