import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
echo "=== ls scripts ==="
ls /home/liuyanzhi/ljz/EntroDiffCode/scripts/ | head -20
echo "=== ls src/pdes ==="
ls /home/liuyanzhi/ljz/EntroDiffCode/src/pdes/ 2>/dev/null || echo "no pdes dir"
echo "=== ls configs/experiment ==="
ls /home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/ | head -10
echo "=== git log ==="
cd /home/liuyanzhi/ljz/EntroDiffCode && git log --oneline -3
echo "=== git status ==="
cd /home/liuyanzhi/ljz/EntroDiffCode && git status --short | head -20
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
