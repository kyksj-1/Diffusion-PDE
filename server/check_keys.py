import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

py = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python3'

stdin, stdout, stderr = ssh.exec_command(
    f'{py} -c "import torch; sd=torch.load(\'/home/liuyanzhi/ljz/EntroDiffCode/output/experiments/ours_full/entrodiff_ours_full_20260429_223734_ep500.pt\',map_location=\'cpu\'); [print(k,list(v.shape)) for k,v in list(sd.items())[:5]]"'
)
print("ours_full:", stdout.read().decode()[:300])

stdin, stdout, stderr = ssh.exec_command(
    f'{py} -c "import torch; sd=torch.load(\'/home/liuyanzhi/ljz/EntroDiffCode/output/experiments/e2_bl_run/entrodiff_e2_bl_run_20260429_224149_ep200.pt\',map_location=\'cpu\'); [print(k,list(v.shape)) for k,v in list(sd.items())[:5]]"'
)
print("e2_bl:", stdout.read().decode()[:300])

ssh.close()
