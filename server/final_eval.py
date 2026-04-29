import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Final comprehensive comparison
configs = [
    # (label, ckpt, model_type, dim, steps, zpde)
    ("BV-aware 50ep 50step", "output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_192226_ep200.pt", "bvaware", 128, 50, 0.0),
    ("BV-aware 50ep 25step", "output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_192226_ep200.pt", "bvaware", 128, 25, 0.0),
    ("StdScore Ours 50ep 50step", "output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt", "standard", None, 50, 0.0),
    ("Baseline 50ep 50step", "output/experiments/mvp_baseline/entrodiff_mvp_baseline_20260429_191021_ep50.pt", "standard", None, 50, 0.0),
]

results = {}
for label, ckpt, mtype, dim, steps, zpde in configs:
    print(f"\n>>> {label}")
    dim_arg = f"--model_dim {dim}" if dim else ""
    cmd = f'''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_viz.py \
  --config configs/experiment/bvaware_server.yaml \
  --ckpt_ours {ckpt} \
  --model_type {mtype} {dim_arg} \
  --heun_steps {steps} --zeta_pde {zpde} \
  --n_samples 4 \
  2>&1 | grep -E "平均:"
'''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    print(out)
    
    # Parse W1 from output
    import re
    m = re.search(r'W₁=(\S+)', out)
    results[label] = m.group(1) if m else 'N/A'

print("\n" + "="*70)
print("  最终对比表 (W₁)")
print("="*70)
for label, w1 in results.items():
    print(f"  {label:<35} W₁={w1}")

ssh.close()
