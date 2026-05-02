import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

cmd = '''
cd /home/liuyanzhi/ljz/EntroDiffCode
export PATH=/home/liuyanzhi/miniconda3/envs/ljz_env/bin:$PATH

echo "=== New files ==="
ls -la scripts/generate_sharp_data.py scripts/eval_step_ablation.py scripts/test_time_loss.py 2>/dev/null

echo "=== Verify time loss import ==="
python3 -c "from src.diffusion.losses import get_godunov_time_loss; print('L_time import OK')"

echo "=== Verify sharp data import ==="
python3 -c "import importlib.util; spec=importlib.util.spec_from_file_location('x','scripts/generate_sharp_data.py'); print('Sharp OK')"

echo "=== Git status ==="
git status --short | head -15
'''
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

ssh.close()
