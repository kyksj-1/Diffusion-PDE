import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=30)

# 生成数据 — 服务器配置好，直接跑
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
mkdir -p ./output/data ./output/experiments
python scripts/generate_data.py
'''
stdin, stdout, stderr = ssh.exec_command(cmd)

import time, select
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        data = stdout.channel.recv(4096).decode()
        print(data, end='', flush=True)
    if stderr.channel.recv_stderr_ready():
        err = stderr.channel.recv_stderr(4096).decode()
        print(err, end='', flush=True)
    time.sleep(0.5)

# Get any remaining output
print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()
