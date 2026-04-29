import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

env_config = """\
# EntroDiff 服务器环境配置
# 所有路径统一在 /home/liuyanzhi/ljz/ 下
paths:
  data_dir: "/home/liuyanzhi/ljz/data"
  output_dir: "/home/liuyanzhi/ljz/experiments"

hardware:
  device: "cuda"
  max_batch_size: 128
  num_workers: 4
"""

cmd = f'cat > /home/liuyanzhi/ljz/EntroDiffCode/configs/env_config.yaml << "ENVEOF"\n{env_config}\nENVEOF'
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
err = stderr.read().decode()
if err: print("ERR:", err)

# Verify
stdin, stdout, stderr = ssh.exec_command('cat /home/liuyanzhi/ljz/EntroDiffCode/configs/env_config.yaml')
print(stdout.read().decode())

ssh.close()
