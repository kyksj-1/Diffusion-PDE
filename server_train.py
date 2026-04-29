import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

time.sleep(5)

# Check if processes are still running and training started
cmd = '''
echo "--- Processes ---"
ps aux | grep -E "train_mvp|train_baseline" | grep -v grep

echo "--- GPU status ---"
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader

echo "--- Ours log tail ---"
tail -10 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/ours_nohup.log 2>/dev/null || echo "no log yet"

echo "--- Baseline log tail ---"
tail -10 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/baseline_nohup.log 2>/dev/null || echo "no log yet"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
