import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
echo "=== tmux ==="
tmux list-sessions 2>/dev/null || echo "no sessions"

echo "=== processes ==="
ps aux | grep -E "train_bvaware|train_baseline" | grep -v grep | head -5

echo "=== ours_full dir ==="
ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/ours_full/ 2>/dev/null || echo "not created"

echo "=== baseline_full dir ==="  
ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/baseline_full/ 2>/dev/null || echo "not created"

echo "=== GPU ==="
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
