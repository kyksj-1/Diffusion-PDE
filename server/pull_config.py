import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Pull config from server to local
sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/bvaware_server.yaml', 'r') as f:
    content = f.read()
sftp.close()

import os
local_path = r'D:\A-Nips-Diffussion\PROJECT\black\configs\experiment\bvaware_server.yaml'
os.makedirs(os.path.dirname(local_path), exist_ok=True)
with open(local_path, 'w') as f:
    f.write(content)
print("bvaware_server.yaml pulled from server")

ssh.close()
