import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
py = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python3'
base = '/home/liuyanzhi/ljz/EntroDiffCode'

# 1. Check foundation model structure and PDE list
cmd1 = f'''
{py} -c "
import torch
ckpt = torch.load('{base}/output/experiments/foundation_small/foundation_foundation_small_20260501_000735_ep200.pt', map_location='cpu')
print('ckpt keys:', list(ckpt.keys()))
print('pde_names:', ckpt.get('pde_names', 'NOT FOUND'))
print('config:', ckpt.get('config', {{}}))
print('model keys count:', len(ckpt.get('model', {{}})))
print('first 5 model keys:')
for k in list(ckpt['model'].keys())[:8]:
    print(' ', k, list(ckpt['model'][k].shape) if hasattr(ckpt['model'][k], 'shape') else 'scalar')
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd1)
print("=== Foundation Model Structure ===")
print(stdout.read().decode())
print(stderr.read().decode()[:500])

# 2. Check ALL experiment directories and their contents
cmd2 = f'find {base}/output/experiments -name "train_log_*" -exec echo "{{}}" \\; -exec tail -1 "{{}}" \\; 2>/dev/null'
stdin, stdout, stderr = ssh.exec_command(cmd2)
print("=== ALL Training Runs ===")
print(stdout.read().decode()[:2000])

ssh.close()
