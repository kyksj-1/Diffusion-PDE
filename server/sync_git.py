import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Step 1: stash local server changes that local doesn't have (to avoid conflicts on pull)
# Step 2: pull from GitHub to get the 5 missing commits
# Step 3: unstash and add new files, then commit

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode

# Stash user-modified files (but not new untracked files)
git stash

# Pull latest from GitHub
git pull origin main 2>&1

# Pop stash to restore user changes
git stash pop 2>&1
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
err = stderr.read().decode()
print(out)
if err: print("ERR:", err[:500])

ssh.close()
