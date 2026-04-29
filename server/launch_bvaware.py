import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
mkdir -p output/experiments/bvaware_run

CUDA_VISIBLE_DEVICES=1 nohup python scripts/train_bvaware.py --config configs/experiment/bvaware_server.yaml --dim 128 \
    > output/experiments/bvaware_run/bvaware_nohup.log 2>&1 &
echo "BV-aware PID: $!"

sleep 5
echo "--- GPU ---"
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader
echo "--- Log tail ---"
tail -5 /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/bvaware_run/bvaware_nohup.log 2>/dev/null || echo "no log yet"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode().strip()
err = stderr.read().decode().strip()
print(out)
if err: print("ERR:", err[:500])

ssh.close()
