import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
echo "=== Process ==="
ps aux | grep train_bvaware | grep -v grep | head -1

echo "=== Latest epoch ==="
tail -3 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/bvaware_run/bvaware_nohup.log

echo "=== GPU ==="
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader

echo "=== Latest ckpt ==="
ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/bvaware_run/*.pt 2>/dev/null | tail -3
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
