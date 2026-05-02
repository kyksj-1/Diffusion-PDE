import paramiko, os, base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

server_files = [
    ('scripts/eval_shock_region.py', False),
    ('src/pdes/__init__.py', True),
    ('src/pdes/bl_flux.py', True),
    ('src/pdes/bl_solver.py', True),
    ('configs/experiment/ours_full.yaml', False),
    ('configs/experiment/baseline_full.yaml', False),
    ('configs/experiment/e2_bl.yaml', False),
    ('configs/experiment/bvaware_server.yaml', False),
    ('scripts/train_bvaware.py', False),
    ('scripts/train_baseline.py', False),
    ('scripts/train_mvp.py', False),
    ('src/diffusion/losses.py', False),
]

base_local = r'D:\A-Nips-Diffussion\PROJECT\black'
base_server = '/home/liuyanzhi/ljz/EntroDiffCode'

for rel_path, is_new_dir in server_files:
    local_path = os.path.join(base_local, rel_path)
    
    if is_new_dir:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    server_path = f"{base_server}/{rel_path}"
    
    # Use base64 encoding to avoid special character issues
    cmd = f'cat {server_path} | base64'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    b64 = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    
    if err and 'No such file' in err:
        print(f"  MISSING: {rel_path}")
        continue
    elif err:
        print(f"  ERR: {rel_path}: {err[:100]}")
        continue
    
    try:
        content = base64.b64decode(b64).decode('utf-8')
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK: {rel_path} ({len(content)} bytes)")
    except Exception as e:
        print(f"  DECODE_ERR: {rel_path}: {e}")

ssh.close()
print("\nDone!")
