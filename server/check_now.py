import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
echo "=== GPU ==="
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader

echo "=== Processes ==="
ps aux | grep -E "train_bvaware|train_baseline" | grep -v grep | wc -l

echo "=== Ours last 5 lines ==="
tail -5 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/ours_full/nohup.log 2>/dev/null

echo "=== Baseline last 5 lines ==="
tail -5 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/baseline_full/nohup.log 2>/dev/null

echo "=== Ours ckpts ==="
ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/ours_full/*.pt 2>/dev/null | wc -l
ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/ours_full/*ep*.pt 2>/dev/null | tail -3

echo "=== Baseline ckpts ==="
ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/baseline_full/*.pt 2>/dev/null | wc -l
ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/baseline_full/*ep*.pt 2>/dev/null | tail -3
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
