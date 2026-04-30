import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=30)

# Check current config
stdin, stdout, stderr = ssh.exec_command('cat /home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/ours_full.yaml')
print("Current ours_full.yaml:")
print(stdout.read().decode())

# Fix configs - write proper YAML
import yaml

ours_cfg = {
    "experiment": {
        "name": "ours_full",
        "epochs": 500,
        "learning_rate": 0.0002,
        "nu": 1.0,
        "tau_max": 1.0,
        "lambda_dsm": 1.0,
        "lambda_bv": 0.1,
        "lambda_time": 1.0,
        "heun_steps": 50,
        "zeta_pde": 0.0,
        "data_file": "burgers_sharp_N5000_Nx128.npy",
    }
}

base_cfg = {
    "experiment": {
        "name": "baseline_full",
        "epochs": 500,
        "learning_rate": 0.0002,
        "nu": 1.0,
        "tau_max": 1.0,
        "lambda_dsm": 1.0,
        "lambda_bv": 0.0,
        "lambda_time": 0.0,
        "heun_steps": 50,
        "zeta_pde": 0.0,
        "data_file": "burgers_sharp_N5000_Nx128.npy",
    }
}

for name, cfg in [("ours_full.yaml", ours_cfg), ("baseline_full.yaml", base_cfg)]:
    sftp = ssh.open_sftp()
    with sftp.file(f'/home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/{name}', 'w') as f:
        f.write(yaml.dump(cfg, default_flow_style=False))
    sftp.close()
    print(f"Written: {name}")

# Verify
stdin, stdout, stderr = ssh.exec_command('cat /home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/ours_full.yaml')
print("\n--- verified ---")
print(stdout.read().decode())

# Kill and restart
cmd = '''
pkill -f "train_bvaware|train_baseline" 2>/dev/null
sleep 3
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
mkdir -p output/experiments/ours_full output/experiments/baseline_full

echo "=== Ours ==="
> output/experiments/ours_full/nohup.log
CUDA_VISIBLE_DEVICES=1 nohup python scripts/train_bvaware.py --config configs/experiment/ours_full.yaml --dim 256 >> output/experiments/ours_full/nohup.log 2>&1 &
echo "PID: $!"

echo "=== Baseline ==="
> output/experiments/baseline_full/nohup.log
CUDA_VISIBLE_DEVICES=2 nohup python scripts/train_baseline.py --config configs/experiment/baseline_full.yaml >> output/experiments/baseline_full/nohup.log 2>&1 &
echo "PID: $!"
sleep 10

nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader
echo "--- Ours head ---"
head -5 output/experiments/ours_full/nohup.log
echo "--- Base head ---"
head -5 output/experiments/baseline_full/nohup.log
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print("\n--- Restart ---")
print(stdout.read().decode())

ssh.close()
