import paramiko, os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Files to sync (exclude env_config.yaml — server keeps its own)
files = [
    'scripts/eval_step_ablation.py',
    'scripts/generate_sharp_data.py',
    'scripts/generate_coarse_data.py',
    'scripts/test_time_loss.py',
    'scripts/train_mvp.py',
    'scripts/eval_viz.py',
    'scripts/train_bvaware.py',
    'scripts/train_baseline.py',
    'scripts/generate_data.py',
    'src/diffusion/losses.py',
    'src/diffusion/samplers.py',
    'src/diffusion/schedules.py',
    'src/models/score_param.py',
    'src/models/unet_1d.py',
    'src/data/burgers_dataset.py',
    'src/data/burgers_1d_solver.py',
    'src/utils/env_manager.py',
    'configs/experiment/mvp_burgers.yaml',
]

base = r'D:\A-Nips-Diffussion\PROJECT\black'
sftp = ssh.open_sftp()
synced = 0
for f in files:
    local = os.path.join(base, f)
    remote = f'/home/liuyanzhi/ljz/EntroDiffCode/{f}'
    if os.path.exists(local):
        with open(local, 'r', encoding='utf-8') as lf:
            content = lf.read()
        with sftp.file(remote, 'w') as rf:
            rf.write(content)
        synced += 1
        print(f'  OK: {f}')
    else:
        print(f'  SKIP (nolocal): {f}')

sftp.close()
ssh.close()
print(f'\n{synced} files synced to server!')
