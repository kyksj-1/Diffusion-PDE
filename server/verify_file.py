import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=30)

# Verify the file on server is correct
stdin, stdout, stderr = ssh.exec_command(
    "head -55 /home/liuyanzhi/ljz/EntroDiffCode/scripts/train_bvaware.py | tail -5"
)
lines = stdout.read().decode().strip()
print(f"--- Server train_bvaware.py lines 51-55 ---\n{lines}")

# Also check line 48 (data_path)
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '46,56p' /home/liuyanzhi/ljz/EntroDiffCode/scripts/train_bvaware.py"
)
print(f"\n--- Server lines 46-56 ---\n{stdout.read().decode()}")

ssh.close()
