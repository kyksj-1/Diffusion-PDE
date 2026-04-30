import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# E2: Ours vs Baseline on Buckley-Leverett data
cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH

echo "=== E2 BL Ours vs Baseline ==="
CUDA_VISIBLE_DEVICES=1 python scripts/eval_viz.py \
  --config configs/experiment/e2_bl.yaml \
  --ckpt_ours output/experiments/e2_bl_run/entrodiff_e2_bl_run_20260429_224149_ep200.pt \
  --ckpt_baseline output/experiments/e2_bl_baseline/entrodiff_e2bl_base_20260430_170845_ep50.pt \
  --model_type standard \
  --heun_steps 50 --zeta_pde 0.0 --n_samples 4 \
  2>&1 | grep -E "平均|W₁|Saved"
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
err = stderr.read().decode()
print(out)
if err: print("ERR:", err[:300])

ssh.close()
