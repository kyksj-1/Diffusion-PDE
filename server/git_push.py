import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Commit + push
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
git add -A
git commit -m "feat: BVAwareScore + PDE guidance fix + server configs"
echo "--- commit done ---"
git push origin main 2>&1
echo "--- push done ---"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode().strip()
err = stderr.read().decode().strip()
print("STDOUT:", out)
print("STDERR:", err[:500])

ssh.close()
