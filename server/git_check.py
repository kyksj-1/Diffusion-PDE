import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmds = [
    'cd /home/liuyanzhi/ljz/EntroDiffCode && git log --oneline -8',
    'cd /home/liuyanzhi/ljz/EntroDiffCode && git status --short',
    'cd /home/liuyanzhi/ljz/EntroDiffCode && git remote -v',
    'cd /home/liuyanzhi/ljz/EntroDiffCode && git fetch origin 2>&1; git log --oneline origin/main -3 2>/dev/null || echo "fetch failed"',
    'cd /home/liuyanzhi/ljz/EntroDiffCode && git log --oneline main..origin/main 2>/dev/null || echo "no remote changes"',
    'cd /home/liuyanzhi/ljz/EntroDiffCode && git log --oneline origin/main..main 2>/dev/null || echo "no local ahead"',
]
for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    print(f"--- {cmd[:60]} ---")
    print(out[:600] if out else '(empty)')
    if err and 'fetch' not in cmd: print('ERR:', err[:200])
    print()

ssh.close()
