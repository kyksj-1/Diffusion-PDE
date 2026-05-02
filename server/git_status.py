import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
echo "=== git log (last 5) ==="
git log --oneline -5
echo "=== git remote ==="
git remote -v
echo "=== git status ==="
git status --short | head -30
echo "=== vs origin ==="
git log --oneline origin/main -3 2>/dev/null || echo "Cannot fetch"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
