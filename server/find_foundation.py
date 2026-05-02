import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
py = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python3'
base = '/home/liuyanzhi/ljz/EntroDiffCode'

# Find foundation model source files
stdin, stdout, stderr = ssh.exec_command(f'find {base} -name "*foundation*" -o -name "*dit*" -o -name "*mixed*" 2>/dev/null | grep -v __pycache__ | grep -v ".pt"')
print("=== Foundation model source files ===")
print(stdout.read().decode())

# Check all Python files
stdin, stdout, stderr = ssh.exec_command(f'ls {base}/src/models/ {base}/scripts/*found* {base}/scripts/*mixed* 2>/dev/null')
print("=== Model and script files ===")
print(stdout.read().decode())

ssh.close()
