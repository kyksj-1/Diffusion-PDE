import paramiko, os, stat

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
sftp = ssh.open_sftp()

server_base = '/home/liuyanzhi/ljz/EntroDiffCode'
local_base = r'D:\A-Nips-Diffussion\PROJECT\black'

# Collect all files that differ between server and local
# Strategy: pull ALL server files (server is canonical)
def pull_dir(remote_dir, local_dir):
    """Recursively pull all files from server to local"""
    try:
        for entry in sftp.listdir_attr(remote_dir):
            rpath = remote_dir + '/' + entry.filename
            lpath = os.path.join(local_dir, entry.filename)
            if stat.S_ISDIR(entry.st_mode):
                os.makedirs(lpath, exist_ok=True)
                pull_dir(rpath, lpath)
            else:
                os.makedirs(local_dir, exist_ok=True)
                sftp.get(rpath, lpath)
                print(f'  OK: {os.path.relpath(lpath, local_base)}')
    except Exception as e:
        print(f'  SKIP: {remote_dir} ({e})')

# Pull critical new/updated files from server
critical_paths = [
    'src/models/dit_1d.py',
    'src/models/foundation_score.py',
    'src/data/mixed_pde_dataset.py',
    'scripts/train_foundation.py',
    'scripts/eval_foundation.py',
    'scripts/eval_shock_region.py',
    'tests/test_dit_1d.py',
    'tests/test_dit_scores.py',
    'tests/test_mixed_pde_dataset.py',
    'configs/foundation',
    'tests',
]

for path in critical_paths:
    remote = f'{server_base}/{path}'
    local = os.path.join(local_base, path)
    
    try:
        attr = sftp.stat(remote)
        if stat.S_ISDIR(attr.st_mode):
            os.makedirs(local, exist_ok=True)
            pull_dir(remote, local)
        else:
            os.makedirs(os.path.dirname(local), exist_ok=True)
            sftp.get(remote, local)
            print(f'OK: {path}')
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'FAIL: {path} — {e}')

# Also pull modified files from server
modified = [
    'src/diffusion/losses.py',
    'src/diffusion/samplers.py',
    'src/models/score_param.py',
    'src/models/unet_1d.py',
    'src/pdes/bl_flux.py',
    'src/pdes/bl_solver.py',
    'src/pdes/__init__.py',
    'scripts/train_baseline.py',
    'scripts/train_bvaware.py',
    'src/data/burgers_dataset.py',
]
print("\n--- Updated core files ---")
for path in modified:
    remote = f'{server_base}/{path}'
    local = os.path.join(local_base, path)
    try:
        sftp.get(remote, local)
        print(f'OK: {path}')
    except Exception as e:
        print(f'FAIL: {path} — {e}')

sftp.close()
ssh.close()
print("\nSync complete!")
