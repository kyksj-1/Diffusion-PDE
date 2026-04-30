import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Step 1: Generate BL data (CPU, ~60s)
print("=== Step 1: Generating BL data ===")
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/generate_bl_data.py 2>&1
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        data = stdout.channel.recv(4096).decode()
        print(data, end='', flush=True)
    time.sleep(0.5)
print(stdout.read().decode())

# Step 2: Create tmux session with 3 windows
print("\n=== Step 2: Setting up tmux ===")
cmd2 = '''
# Kill existing if any
tmux kill-session -t entrodiff 2>/dev/null

# Create new session (detached)
tmux new-session -d -s entrodiff -n monitor
tmux send-keys -t entrodiff:0 'cd /home/liuyanzhi/ljz/EntroDiffCode && export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH && watch -n 5 nvidia-smi' Enter

# Window 1: BVAwareScore + time loss on sharp Burgers (GPU 1)
tmux new-window -t entrodiff -n bvaware_sharp
tmux send-keys -t entrodiff:1 'cd /home/liuyanzhi/ljz/EntroDiffCode && export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH && CUDA_VISIBLE_DEVICES=1 python scripts/train_bvaware.py --config configs/experiment/bvaware_server.yaml --dim 128 2>&1 | tee output/experiments/bvaware_sharp.log' Enter

# Window 2: E2 Buckley-Leverett Ours (GPU 2)
tmux new-window -t entrodiff -n e2_bl_ours
# Need to modify train_mvp to use BL data file → create a quick inline script
tmux send-keys -t entrodiff:2 'cd /home/liuyanzhi/ljz/EntroDiffCode && export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH && CUDA_VISIBLE_DEVICES=2 python scripts/train_mvp.py --config configs/experiment/e2_bl.yaml 2>&1 | tee output/experiments/e2_bl_ours.log' Enter

echo "Tmux session 'entrodiff' created with 3 windows:"
echo "  Window 0: nvidia-smi monitor"
echo "  Window 1: BVAwareScore + time loss on sharp Burgers (GPU 1)" 
echo "  Window 2: E2 Buckley-Leverett Ours (GPU 2)"
echo ""
echo "Connect: tmux attach -t entrodiff"
echo "Detach: Ctrl+B then D"
echo "Switch window: Ctrl+B then 0/1/2"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2)
out = stdout.read().decode()
err = stderr.read().decode()
print(out)
if err: print("ERR:", err[:300])

# Verify tmux is running
stdin, stdout, stderr = ssh.exec_command('tmux ls 2>&1')
print("\n=== Tmux sessions ===")
print(stdout.read().decode())

ssh.close()
