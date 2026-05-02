import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)
py = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python3'
base = '/home/liuyanzhi/ljz/EntroDiffCode'

# Check eval outputs
evdir = f'{base}/output/experiments/foundation_eval/foundation_foundation_small_20260501_000735_ep200'
for cmd in [
    f'ls -la {evdir}/',
    f'cat {evdir}/*.json 2>/dev/null',
    f'cat {evdir}/*.txt 2>/dev/null',
]:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    if out.strip():
        print(f"=== {cmd[:50]} ===")
        print(out[:800])

# Actually run the eval since there are PNGs but maybe no JSON
stdin, stdout, stderr = ssh.exec_command(
    f'cd {base}; {py} scripts/eval_foundation.py '
    f'--ckpt output/experiments/foundation_small/foundation_foundation_small_20260501_000735_ep200.pt '
    f'--n_samples 8 --num_steps 50 2>&1'
)
out = stdout.read().decode()
err = stderr.read().decode()
print("=== Running eval ===")
print(out[-1000:] if out else "(no output)")
print("ERR:", err[:500] if err else "none")

ssh.close()
