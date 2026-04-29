import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

# Read local files and write to server
files_to_sync = {
    'PROJECT/black/src/models/score_param.py': '/home/liuyanzhi/ljz/EntroDiffCode/src/models/score_param.py',
    'PROJECT/black/src/models/unet_1d.py': '/home/liuyanzhi/ljz/EntroDiffCode/src/models/unet_1d.py',
    'PROJECT/black/scripts/train_bvaware.py': '/home/liuyanzhi/ljz/EntroDiffCode/scripts/train_bvaware.py',
    'PROJECT/black/scripts/eval_viz.py': '/home/liuyanzhi/ljz/EntroDiffCode/scripts/eval_viz.py',
}

import os
base = r'D:\A-Nips-Diffussion'
for local_rel, remote in files_to_sync.items():
    local = os.path.join(base, local_rel)
    with open(local, 'r', encoding='utf-8') as f:
        content = f.read()
    # Escape for shell
    sftp = ssh.open_sftp()
    with sftp.file(remote, 'w') as f:
        f.write(content)
    sftp.close()
    print(f"  OK: {local_rel} → {remote}")

# Now create server experiment config
config_content = """\
# BV-aware 训练配置 (服务器专用, 大模型 + 多 epoch)
experiment:
  name: "bvaware_run"
  epochs: 200                   # 服务器全量训练
  learning_rate: 2.0e-4
  nu: 1.0
  tau_max: 1.0
  lambda_bv: 0.1
  lambda_dsm: 1.0
  heun_steps: 50
  zeta_pde: 0.1                 # Godunov PDE guidance (Ours 独有)
  data_file: "burgers_1d_N5000_Nx128.npy"
"""

sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/bvaware_server.yaml', 'w') as f:
    f.write(config_content)
sftp.close()
print("  OK: bvaware_server.yaml")

ssh.close()
print("\nAll files synced!")
