import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

config = """# BV-aware large-scale training config (server)
experiment:
  name: "bvaware_run"
  epochs: 500
  learning_rate: 2.0e-4
  nu: 1.0
  tau_max: 1.0
  lambda_bv: 0.1
  lambda_dsm: 1.0
  heun_steps: 50
  zeta_pde: 0.0
  data_file: "burgers_1d_N5000_Nx128.npy"
"""

sftp = ssh.open_sftp()
with sftp.file('/home/liuyanzhi/ljz/EntroDiffCode/configs/experiment/bvaware_server.yaml', 'w') as f:
    f.write(config)
sftp.close()
print('Config updated: epochs=500')

ssh.close()
