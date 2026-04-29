import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Wait for training to finish
print("Waiting for training to complete...")
for i in range(30):
    time.sleep(20)
    stdin, stdout, stderr = ssh.exec_command('ps aux | grep -E "train_mvp|train_baseline" | grep -v grep | wc -l')
    count = stdout.read().decode().strip()
    
    if count == '0':
        print("Training complete!")
        break
    print(f"  Check {i+1}: {count} training processes still running...")

# Check final status
time.sleep(2)
cmd = '''
echo "--- Ours final log ---"
tail -5 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/ours_nohup.log 2>/dev/null

echo "--- Baseline final log ---"
tail -5 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/baseline_nohup.log 2>/dev/null

echo "--- Checkpoints ---"
ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/entrodiff_mvp_run1/ 2>/dev/null | grep ep50
ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/mvp_baseline/ 2>/dev/null | grep ep50
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
