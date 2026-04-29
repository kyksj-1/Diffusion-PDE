import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Poll until training completes
print("等待 BV-aware 训练完成 (200 epoch)...")
for i in range(120):  # max 60 min
    time.sleep(30)
    stdin, stdout, stderr = ssh.exec_command(
        'ps aux | grep train_bvaware | grep -v grep | wc -l'
    )
    count = stdout.read().decode().strip()
    if count == '0':
        print(f"\n训练完成! (check #{i+1})")
        break
    if i % 4 == 0:
        stdin2, stdout2, stderr2 = ssh.exec_command(
            'tail -1 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/bvaware_run/bvaware_nohup.log'
        )
        print(f"  {stdout2.read().decode().strip()}")

# Show final results
cmd = '''
echo "=== 最终 checkpoint ==="
ls -la /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/bvaware_run/*ep200* 2>/dev/null
ls -la /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/bvaware_run/*ep19* 2>/dev/null | tail -3
echo "=== 最终 epoch loss ==="
tail -3 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/bvaware_run/bvaware_nohup.log
echo "=== GPU ==="
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
