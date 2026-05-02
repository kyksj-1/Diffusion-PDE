import paramiko, subprocess, tempfile, os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=30)

# Tar specific dirs on local, pipe to server
local_base = r'D:\A-Nips-Diffussion\PROJECT\black'
dirs_to_sync = [
    'scripts',
    'src',
    'configs',
    'pyproject.toml',
    'requirements.txt',
]

# Create tar of local files (no .git, no __pycache__)
import tarfile, io
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w:gz') as tar:
    for item in dirs_to_sync:
        full = os.path.join(local_base, item)
        if os.path.isdir(full):
            for root, dirs, files in os.walk(full):
                dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.egg-info', 'entrodiff.egg-info')]
                for f in files:
                    if f.endswith('.pyc'): continue
                    fpath = os.path.join(root, f)
                    arcname = os.path.relpath(fpath, local_base)
                    tar.add(fpath, arcname=arcname)
        elif os.path.isfile(full):
            tar.add(full, arcname=item)

# Write tar to temp file
tar_data = buf.getvalue()
print(f"Tar size: {len(tar_data)} bytes")

# Send tar to server via sftp
sftp = ssh.open_sftp()
sftp.putfo(io.BytesIO(tar_data), '/home/liuyanzhi/ljz/EntroDiffCode/code_sync.tar.gz')
sftp.close()

# Extract on server
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
tar xzf code_sync.tar.gz
rm code_sync.tar.gz
echo "DONE"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode().strip())

# Verify
stdin, stdout, stderr = ssh.exec_command(
    'ls /home/liuyanzhi/ljz/EntroDiffCode/scripts/train_bvaware.py && echo "OK"'
)
print(stdout.read().decode().strip())

ssh.close()
print("Sync complete!")
