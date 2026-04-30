import paramiko, time, os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# ======= 1. Sync ALL updated Python files =======
sync_files = [
    ('D:/A-Nips-Diffussion/PROJECT/black/src/diffusion/losses.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/src/diffusion/losses.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/src/diffusion/samplers.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/src/diffusion/samplers.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/src/models/score_param.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/src/models/score_param.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/src/models/unet_1d.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/src/models/unet_1d.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/scripts/train_mvp.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/scripts/train_mvp.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/scripts/train_bvaware.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/scripts/train_bvaware.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/scripts/train_baseline.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/scripts/train_baseline.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/scripts/eval_viz.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/scripts/eval_viz.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/scripts/eval_step_ablation.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/scripts/eval_step_ablation.py'),
    ('D:/A-Nips-Diffussion/PROJECT/black/scripts/generate_sharp_data.py',
     '/home/liuyanzhi/ljz/EntroDiffCode/scripts/generate_sharp_data.py'),
]

for local, remote in sync_files:
    try:
        with open(local, 'r', encoding='utf-8') as f:
            content = f.read()
        sftp = ssh.open_sftp()
        with sftp.file(remote, 'w') as f:
            f.write(content)
        sftp.close()
        print(f"  OK: {os.path.basename(local)}")
    except Exception as e:
        print(f"  FAIL: {os.path.basename(local)}: {e}")

# ======= 2. Write experiment configs =======
import yaml

# Ours full config
ours_cfg = {"experiment": {
    "name": "ours_full", "data_file": "burgers_sharp_N5000_Nx128.npy",
    "epochs": 500, "learning_rate": 2e-4,
    "nu": 1.0, "tau_max": 1.0,
    "lambda_dsm": 1.0, "lambda_bv": 0.1, "lambda_time": 1.0,
    "heun_steps": 50, "zeta_pde": 0.0,
}}
base_cfg = {"experiment": {
    "name": "baseline_full", "data_file": "burgers_sharp_N5000_Nx128.npy",
    "epochs": 500, "learning_rate": 2e-4,
    "nu": 1.0, "tau_max": 1.0,
    "lambda_dsm": 1.0, "lambda_bv": 0.0, "lambda_time": 0.0,
    "heun_steps": 50, "zeta_pde": 0.0,
}}

for label, cfg in [("ours_full.yaml", ours_cfg), ("baseline_full.yaml", base_cfg)]:
    sftp = ssh.open_sftp()
    with sftp.file(f'/home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/{label}', 'w') as f:
        f.write(yaml.dump(cfg, default_flow_style=False))
    sftp.close()
    print(f"  Config: {label}")

# ======= 3. Generate sharp data (if not exists) =======
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH

if [ ! -f output/data/burgers_sharp_N5000_Nx128.npy ]; then
    echo "=== Generating sharp IC data ==="
    python scripts/generate_sharp_data.py
else
    echo "Sharp data already exists"
fi
'''
stdin2, stdout2, stderr2 = ssh.exec_command(cmd)
print("\n--- Sharp data ---")
print(stdout2.read().decode()[-500:])

# ======= 4. Create tmux session and launch training =======
# Kill existing entrodiff session if any
ssh.exec_command('tmux kill-session -t entrodiff 2>/dev/null')
time.sleep(1)

# Create tmux session with 2 windows
tmux_cmd = '''
tmux new-session -d -s entrodiff -n train
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH

# Window 0: Ours training (GPU 1, BVAwareScore dim=256, 500 epochs)
tmux send-keys -t entrodiff "CUDA_VISIBLE_DEVICES=1 python scripts/train_bvaware.py --config configs/experiment/ours_full.yaml --dim 256 2>&1 | tee output/experiments/ours_full/train.log" C-m

# Window 1: Baseline training (GPU 2, StandardScore, 500 epochs)
tmux new-window -t entrodiff -n baseline
tmux send-keys -t entrodiff:baseline "CUDA_VISIBLE_DEVICES=2 python scripts/train_baseline.py --config configs/experiment/baseline_full.yaml 2>&1 | tee output/experiments/baseline_full/train.log" C-m

# Window 2: Monitor (nvidia-smi loop)
tmux new-window -t entrodiff -n monitor
tmux send-keys -t entrodiff:monitor "watch -n 10 nvidia-smi" C-m

echo "tmux session 'entrodiff' created"
tmux list-sessions
'''
stdin3, stdout3, stderr3 = ssh.exec_command(tmux_cmd)
print("\n--- tmux ---")
print(stdout3.read().decode())
err = stderr3.read().decode()
if err: print("ERR:", err[:300])

# ======= 5. Verify =======
time.sleep(5)
stdin4, stdout4, stderr4 = ssh.exec_command(
    'cd /home/liuyanzhi/ljz/EntroDiffCode; export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH; '
    'nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader'
)
print("\n--- GPU ---")
print(stdout4.read().decode())

ssh.close()
print("\nDone! 实验在 tmux session 'entrodiff' 中运行.")
print("重新连接: ssh -p 227 liuyanzhi@202.121.181.105")
print("查看: tmux attach -t entrodiff")
