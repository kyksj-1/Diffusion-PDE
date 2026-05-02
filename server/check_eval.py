import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
py = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python3'
base = '/home/liuyanzhi/ljz/EntroDiffCode'

# Check eval output
for cmd in [
    f'ls -laR {base}/output/experiments/foundation_eval/ 2>/dev/null | head -30',
    f'cat {base}/output/experiments/foundation_eval/*/eval_results.json 2>/dev/null | head -100',
    f'cat {base}/output/experiments/foundation_eval/eval_log.txt 2>/dev/null | head -50',
    f'cat {base}/output/experiments/foundation_small/eval_results.json 2>/dev/null',
]:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    if out.strip():
        print(f"=== {cmd[:60]} ===")
        print(out[:500])

# Try running eval_foundation.py
stdin, stdout, stderr = ssh.exec_command(f'cd {base}; {py} scripts/eval_foundation.py --help 2>&1')
print("=== eval_foundation.py help ===")
print(stdout.read().decode()[:500])

ssh.close()
