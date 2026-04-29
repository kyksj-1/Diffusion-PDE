import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

bvaware_ckpt = "output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_192226_ep200.pt"
baseline_ckpt = "output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_191021_ep50.pt"

# Multi-step + PDE guidance comparison
tests = [
    ("BV-aware (no PDE)", bvaware_ckpt, "bvaware", 50, 0.0),
    ("BV-aware + PDE 0.1", bvaware_ckpt, "bvaware", 50, 0.1),
    ("BV-aware + PDE 0.5", bvaware_ckpt, "bvaware", 50, 0.5),
    ("Baseline EDM", baseline_ckpt, "standard", 50, 0.0),
    ("BV-aware 25step", bvaware_ckpt, "bvaware", 25, 0.1),
    ("Baseline 25step", baseline_ckpt, "standard", 25, 0.0),
    ("BV-aware 10step", bvaware_ckpt, "bvaware", 10, 0.1),
    ("Baseline 10step", baseline_ckpt, "standard", 10, 0.0),
]

for label, ckpt, mtype, steps, zpde in tests:
    print(f"\n{'='*60}")
    print(f"  {label} (steps={steps}, zeta_pde={zpde})")
    print(f"{'='*60}")
    
    cmd = f'''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_viz.py \
  --config configs/experiment/bvaware_server.yaml \
  --ckpt_ours {ckpt} \
  --model_type {mtype} --model_dim 128 \
  --heun_steps {steps} --zeta_pde {zpde} \
  --n_samples 4 \
  2>&1 | grep -E "W₁|L¹|Shock|平均|指标|Saved"
'''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            print(stdout.channel.recv(4096).decode(), end='', flush=True)
        time.sleep(1)
    print(stdout.read().decode())

ssh.close()
