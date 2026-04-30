import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Find baseline checkpoint
cmd = 'ls /home/liuyanzhi/ljz/EntroDiffCode/output/experiments/mvp_baseline/*ep500* 2>/dev/null'
stdin, stdout, stderr = ssh.exec_command(cmd)
base_ckpt_path = stdout.read().decode().strip()
print(f"Baseline ckpt: {base_ckpt_path or 'NOT FOUND'}")

ours_ckpt = "output/experiments/ours_full/entrodiff_ours_full_20260429_223734_ep500.pt"

# Run comparison eval at multiple step counts
tests = [
    (ours_ckpt, "bvaware", 256, 10),
    (ours_ckpt, "bvaware", 256, 25),
    (ours_ckpt, "bvaware", 256, 50),
    (base_ckpt_path, "standard", None, 10),
    (base_ckpt_path, "standard", None, 25),
    (base_ckpt_path, "standard", None, 50),
]

print("\n======== Multi-step Comparison (Sharp IC Data) ========")
results = {}

for ckpt, mtype, dim, steps in tests:
    dim_arg = f"--model_dim {dim}" if dim else ""
    label = f"{mtype:10} {steps:2}step"
    
    cmd = f'''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_viz.py \
  --config configs/experiment/ours_full.yaml \
  --ckpt_ours {ckpt} \
  --model_type {mtype} {dim_arg} \
  --heun_steps {steps} --zeta_pde 0.0 \
  --n_samples 8 \
  2>&1 | grep "平均:"
'''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # Wait for completion
    while not stdout.channel.exit_status_ready():
        time.sleep(1)
    out = stdout.read().decode().strip()
    print(f"  {label}: {out}")
    
    import re
    m = re.search(r'W₁=(\S+)', out)
    if m: results[label] = float(m.group(1))

# Summary table
print("\n" + "="*60)
print("  Final Results: Sharp IC, 500 epochs")
print("="*60)
print(f"  {'Method':<25} {'10-step':<10} {'25-step':<10} {'50-step':<10}")
for method in ["bvaware", "standard"]:
    vals = []
    for s in [10, 25, 50]:
        key = f"{method:10} {s:2}step"
        v = results.get(key, "N/A")
        vals.append(f"{v:.4f}" if isinstance(v, float) else v)
    print(f"  {method:<25} {vals[0]:<10} {vals[1]:<10} {vals[2]:<10}")

# Show advantage
if "bvaware      10step" in results and "standard     50step" in results:
    gap = results["standard     50step"] - results["bvaware      10step"]
    print(f"\n  BV-aware 10-step beats Baseline 50-step by W1: {gap:.4f}")

ssh.close()
