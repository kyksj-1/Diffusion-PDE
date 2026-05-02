import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

base = '/home/liuyanzhi/ljz/EntroDiffCode'

# Find exact checkpoint filenames
for d in ['e2_bvaware_run', 'sharp_ours', 'foundation_small']:
    stdin, stdout, stderr = ssh.exec_command(f'ls {base}/output/experiments/{d}/*ep*.pt 2>/dev/null | sort -V | tail -3')
    out = stdout.read().decode().strip()
    print(f"--- {d} checkpoints ---")
    print(out)

ssh.close()
