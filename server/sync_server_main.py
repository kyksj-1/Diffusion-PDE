"""服务器端 git pull 同步最新代码 + 验证."""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

R = '/home/liuyanzhi/ljz/EntroDiffCode'
PYTHON = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python'

cmd = f'''
echo "=== 服务器同步前状态 ==="
cd {R}
git status --short | head -10
git log --oneline -2
echo ""

echo "=== git stash + pull origin main ==="
git stash 2>&1 | head -3
git pull origin main 2>&1 | tail -10

echo ""
echo "=== 同步后 ==="
git log --oneline -3

echo ""
echo "=== 新文件验证 ==="
ls scripts/sweep_*.py scripts/train_bvaware_euler.py 2>&1
ls src/utils/shock_metrics.py src/data/euler_dataset.py 2>&1
ls configs/experiment/e3_euler.yaml configs/foundation/multi_systems.yaml 2>&1
ls tests/test_shock_metrics.py tests/test_euler_pipeline.py 2>&1

echo ""
echo "=== 跑测试验证 ==="
{PYTHON} -m pytest tests/test_shock_metrics.py tests/test_euler_pipeline.py 2>&1 | tail -5
'''

stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
print(stdout.read().decode())
err = stderr.read().decode()
if err.strip(): print("STDERR:", err[:500])

ssh.close()
