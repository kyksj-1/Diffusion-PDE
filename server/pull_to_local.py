import paramiko, os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# List of new/modified files on server that should come to local
server_files = [
    'scripts/eval_shock_region.py',
    'src/pdes/__init__.py',
    'src/pdes/bl_flux.py',
    'src/pdes/bl_solver.py',
    'configs/experiment/ours_full.yaml',
    'configs/experiment/baseline_full.yaml',
    'configs/experiment/e2_bl.yaml',
    'configs/experiment/bvaware_server.yaml',
]

base_local = r'D:\A-Nips-Diffussion\PROJECT\black'
base_server = '/home/liuyanzhi/ljz/EntroDiffCode'

for rel_path in server_files:
    local_path = os.path.join(base_local, rel_path)
    server_path = os.path.join(base_server, rel_path)
    
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    sftp = ssh.open_sftp()
    try:
        with sftp.file(server_path, 'r') as f:
            content = f.read()
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK: {rel_path} ({len(content)} bytes)")
    except Exception as e:
        print(f"  FAIL: {rel_path}: {e}")
    sftp.close()

# Also sync modified training scripts (data_file fix + time loss)
modified_files = [
    'scripts/train_bvaware.py',
    'scripts/train_baseline.py',
    'scripts/train_mvp.py',
    'src/diffusion/losses.py',
]

for rel_path in modified_files:
    local_path = os.path.join(base_local, rel_path)
    server_path = os.path.join(base_server, rel_path)
    
    sftp = ssh.open_sftp()
    try:
        with sftp.file(server_path, 'r') as f:
            content = f.read()
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK (mod): {rel_path} ({len(content)} bytes)")
    except Exception as e:
        print(f"  FAIL: {rel_path}: {e}")
    sftp.close()

ssh.close()
print("\n=== Done pulling from server ===")
