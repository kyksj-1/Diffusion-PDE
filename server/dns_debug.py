import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

commands = [
    'cat /etc/resolv.conf 2>/dev/null',
    'nslookup github.com 2>&1 | head -8',
    'ping -c 1 -W 3 8.8.8.8 2>&1',
    'ping -c 1 -W 3 140.82.121.3 2>&1',
    'dig github.com 2>&1 | head -10',
    'host github.com 2>&1',
    'cat /etc/hosts | grep github',
    'ip route show default 2>/dev/null',
]
for cmd in commands:
    stdin, stdout, stderr = ssh.exec_command(cmd + '\n')
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    print(f'--- {cmd[:50]} ---')
    print(out[:300] if out else '(empty)')
    if err: print('ERR:', err[:200])
    print()

ssh.close()
