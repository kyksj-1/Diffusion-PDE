import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Commit persistent files only, exclude temporary ones
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode

# Add persistent new files
git add scripts/eval_shock_region.py
git add src/pdes/
git add configs/experiment/ours_full.yaml
git add configs/experiment/baseline_full.yaml
git add configs/experiment/e2_bl.yaml

# Add modified files (data_file fix, time loss, etc.)
git add scripts/train_bvaware.py
git add scripts/train_baseline.py
git add scripts/train_mvp.py
git add src/diffusion/losses.py
git add configs/experiment/bvaware_server.yaml

git status --short
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
print(out)

# Now commit
cmd2 = 'cd /home/liuyanzhi/ljz/EntroDiffCode; git commit -m "feat: shock region eval + E2 pdes module + full experiment configs + time loss"'
stdin2, stdout2, stderr2 = ssh.exec_command(cmd2)
print(stdout2.read().decode())
print(stderr2.read().decode())

# Show what's left untracked
stdin3, stdout3, stderr3 = ssh.exec_command('cd /home/liuyanzhi/ljz/EntroDiffCode; git status --short')
print("\n--- Remaining untracked (will NOT commit) ---")
print(stdout3.read().decode())

ssh.close()
