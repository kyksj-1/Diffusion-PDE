import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Test PDE guidance with StandardScore (no BV-aware autograd conflict)
tests = [
    ("StandardScore zeta=0", "output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt", "standard", 0.0),
    ("StandardScore zeta=0.1", "output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt", "standard", 0.1),
    ("StandardScore zeta=0.5", "output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt", "standard", 0.5),
    ("StandardScore zeta=1.0", "output/experiments/entrodiff_mvp_run1/entrodiff_entrodiff_mvp_run1_20260429_191018_ep50.pt", "standard", 1.0),
]

for label, ckpt, mtype, zpde in tests:
    cmd = f'''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_viz.py \
  --config configs/experiment/bvaware_server.yaml \
  --ckpt_ours {ckpt} \
  --model_type {mtype} \
  --heun_steps 50 --zeta_pde {zpde} \
  --n_samples 4 \
  2>&1 | grep -E "平均:"
'''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    print(f"  {label:<30} {out}")

ssh.close()
