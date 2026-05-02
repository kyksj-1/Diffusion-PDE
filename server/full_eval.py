import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

base = '/home/liuyanzhi/ljz/EntroDiffCode'

# Check foundation model training status
stdin, stdout, stderr = ssh.exec_command(f'tail -5 {base}/output/experiments/foundation_small/train_log_foundation_small_20260501_000735.txt 2>/dev/null')
print("=== Foundation Model Status ===")
print(stdout.read().decode())

stdin, stdout, stderr = ssh.exec_command(f'ls {base}/output/experiments/foundation_small/*ep*.pt 2>/dev/null | tail -5')
print("Foundation ckpts:", stdout.read().decode())

# Now run quick eval on ALL key checkpoints
checks = [
    ("E2 BV-aware 200ep", f"{base}/output/experiments/e2_bvaware_run/entrodiff_e2_bvaware_run_20260430_210312_ep200.pt", "bvaware", 128),
    ("Sharp Ours 500ep", f"{base}/output/experiments/sharp_ours/entrodiff_sharp_ours_20260430_210638_ep500.pt", "bvaware", 128),
    ("Sharp Baseline 500ep", f"{base}/output/experiments/sharp_baseline/entrodiff_sharp_baseline_20260430_210542_ep500.pt", "standard", None),
    ("E2 Baseline 50ep", f"{base}/output/experiments/e2_bl_baseline/entrodiff_mvp_baseline_*.pt", "standard", None),  # glob
]

for label, ckpt, mtype, dim in checks:
    dim_arg = f"--model_dim {dim}" if dim else ""
    cmd = f'''
cd {base}
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_viz.py \
  --config configs/experiment/bvaware_server.yaml \
  --ckpt_ours {ckpt} \
  --model_type {mtype} {dim_arg} \
  --heun_steps 50 --zeta_pde 0 --n_samples 4 \
  2>&1 | grep -E "加载|平均:|指标"
'''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    print(f"\n=== {label} ===")
    print(out[-400:] if out else '(no output)')

ssh.close()
