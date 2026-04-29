import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Test BV-aware EVAL with zeta_pde=0 (no guidance) + test at different configs
tests = [
    ("zeta=0", 0.0, 50),
    ("zeta=0.1", 0.1, 50),
]

for label, zpde, steps in tests:
    print(f"\n{'='*50}")
    print(f"  BV-aware {label} ({steps} steps)")
    print(f"{'='*50}")
    cmd = f'''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH
python scripts/eval_viz.py \
  --config configs/experiment/bvaware_server.yaml \
  --ckpt_ours output/experiments/bvaware_run/entrodiff_bvaware_run_20260429_192226_ep200.pt \
  --model_type bvaware --model_dim 128 \
  --heun_steps {steps} --zeta_pde {zpde} \
  --n_samples 4 \
  2>&1 | grep -E "加载|指标|平均|W₁|NaN|Error|Traceback|File "
'''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    print(out)
    
ssh.close()
