import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
git add scripts/eval_step_ablation.py scripts/generate_sharp_data.py scripts/generate_coarse_data.py scripts/test_time_loss.py scripts/train_mvp.py scripts/eval_viz.py src/diffusion/losses.py src/diffusion/samplers.py src/models/score_param.py src/models/unet_1d.py -A
git commit -m "feat: time loss + sharp/coarse data + step ablation (synced via SCP from local PC)"
echo "--- commit done ---"
git log --oneline -3
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
