import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Check current experiment config (nu, epochs etc)
stdin, stdout, stderr = ssh.exec_command('cat /home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/mvp_burgers.yaml')
print("=== mvp_burgers.yaml ===")
print(stdout.read().decode())

# Also check if the experiment config exists
stdin, stdout, stderr = ssh.exec_command('ls /home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/')
print("=== configs/experiment/ ===")
print(stdout.read().decode())

ssh.close()
