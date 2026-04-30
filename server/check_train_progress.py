"""W5-F 训练进度快照 (单次)."""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

stdin, stdout, _ = ssh.exec_command('cat /tmp/foundation_small.log 2>&1 | head -40')
print("=== /tmp/foundation_small.log ===")
print(stdout.read().decode())

stdin, stdout, _ = ssh.exec_command(
    'find /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/foundation_small -name "train_log_*.txt" | head -1 | xargs cat 2>&1 | tail -10'
)
print("=== train_log txt ===")
print(stdout.read().decode())

stdin, stdout, _ = ssh.exec_command('nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader')
print("=== GPU ===")
print(stdout.read().decode())

ssh.close()
