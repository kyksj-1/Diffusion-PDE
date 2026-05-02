import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Fix script — change dim from 128 to 256
cmd = "sed -i 's/dim=128)/dim=256)/' /home/liuyanzhi/ljz/EntroDiffCode/scripts/eval_shock_region.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("Fixed dim")

# Re-run
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_shock_region.py 2>&1 | grep -v "FutureWarning\|paramiko\|Cryptography\|cipher\|class\|BurgersDataset\|Heun Sampling"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        print(stdout.channel.recv(2048).decode(), end='', flush=True)
    time.sleep(0.3)
print(stdout.read().decode())

ssh.close()
