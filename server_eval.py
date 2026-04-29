import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH

python scripts/eval_viz.py \
  --ckpt_ours "./output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt" \
  --ckpt_baseline "./output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_191021_ep50.pt" \
  --n_samples 4 --heun_steps 50
'''
stdin, stdout, stderr = ssh.exec_command(cmd)

# Stream output
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        data = stdout.channel.recv(4096).decode()
        print(data, end='', flush=True)
    if stderr.channel.recv_stderr_ready():
        err = stderr.channel.recv_stderr(4096).decode()
        print(err, end='', flush=True)
    time.sleep(0.3)

print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()
