import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python3 -c "
import torch
sd = torch.load('output/experiments/foundation_small/foundation_foundation_small_20260501_000735_ep200.pt', map_location='cpu')
print(type(sd).__name__)
for k, v in sd.items():
    print(f'{k}: type={type(v).__name__}', end='')
    if hasattr(v, 'keys'):
        print(f' keys={len(v)}', end='')
        for k2 in list(v.keys())[:3]:
            print(f' [{k2}]', end='')
    print()
" 2>&1
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
