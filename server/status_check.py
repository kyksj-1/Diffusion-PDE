import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmds = [
    # All checkpoints
    'find /home/liuyanzhi/ljz/EntroDiffCode/output/experiments -name "*ep*.pt" -printf "%s %p\n" 2>/dev/null | sort -k2',
    # All log files
    'find /home/liuyanzhi/ljz/EntroDiffCode/output/experiments -name "train_log*" -printf "%p\n" 2>/dev/null',
    # GPU
    'nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader',
    # E2 BV-aware log tail
    'tail -5 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/e2_bvaware_run/train_log_e2_bvaware_run_20260430_210312.txt 2>/dev/null || echo "NO_LOG"',
    # Sharp ours log tail
    'tail -3 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/sharp_ours/train.log 2>/dev/null || echo "NO_LOG"',
    # Sharp baseline log tail
    'tail -3 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/sharp_baseline/train.log 2>/dev/null || echo "NO_LOG"',
]
for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    print(f"--- {cmd[:60]} ---")
    print(out[:1000] if out else '(empty)')
    print()

ssh.close()
