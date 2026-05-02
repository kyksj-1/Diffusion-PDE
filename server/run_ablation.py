import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Upload script
import os
local = r'D:\A-Nips-Diffussion\server\step_ablation_runner.py'
with open(local, 'r', encoding='utf-8') as f:
    content = f.read()
sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/run_step_ablation.py', 'w') as fh:
    fh.write(content)
sftp.close()

# Run
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
CUDA_VISIBLE_DEVICES=1 python /home/liuyanzhi/ljz/run_step_ablation.py 2>&1
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        print(stdout.channel.recv(4096).decode(), end='', flush=True)
    time.sleep(0.5)
print(stdout.read().decode())

ssh.close()
