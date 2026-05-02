import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Check if eval_shock_region and eval_sr are same or different
cmd = '''
echo "=== eval_sr size ==="
wc -l /home/liuyanzhi/ljz/EntroDiffCode/scripts/eval_sr.py
echo "=== eval_shock_region size ==="
wc -l /home/liuyanzhi/ljz/EntroDiffCode/scripts/eval_shock_region.py
echo "=== src/pdes/ ==="
ls -la /home/liuyanzhi/ljz/EntroDiffCode/src/pdes/
echo "=== eval_sr first 20 ==="
head -20 /home/liuyanzhi/ljz/EntroDiffCode/scripts/eval_sr.py
echo "=== eval_shock_region first 20 ==="
head -20 /home/liuyanzhi/ljz/EntroDiffCode/scripts/eval_shock_region.py
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())
ssh.close()
