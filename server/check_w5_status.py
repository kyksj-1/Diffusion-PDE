"""
W5-F 服务器现状检查 + Foundation Model 部署准备.

目的:
    1. 验证 SSH 连通
    2. nvidia-smi 看哪块 GPU 空闲 (W5-F 部署用)
    3. tmux ls 看现有 session, 决定新 session 名称
    4. 检查 /home/liuyanzhi/ljz/EntroDiffCode 当前 git branch
    5. 检查 conda env 与 PyTorch 版本

不做任何修改 — 仅 diagnostic.
"""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    '202.121.181.105', port=227,
    username='liuyanzhi', password='HUBRtEeOFC8F0moC',
    timeout=15,
)

cmd = '''
echo "=== HOSTNAME ==="
hostname

echo ""
echo "=== NVIDIA-SMI ==="
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader

echo ""
echo "=== TMUX SESSIONS ==="
tmux ls 2>/dev/null || echo "(no sessions)"

echo ""
echo "=== EntroDiffCode REPO STATUS ==="
cd /home/liuyanzhi/ljz/EntroDiffCode 2>/dev/null && {
    echo "branch: $(git branch --show-current)"
    echo "head:   $(git log --oneline -1)"
    echo "git status (short):"
    git status --short | head -10
    echo "PROJECT/black branch:"
    cd PROJECT/black 2>/dev/null && {
        echo "  branch: $(git branch --show-current)"
        echo "  head:   $(git log --oneline -1)"
    } || echo "  (PROJECT/black not present)"
} || echo "(EntroDiffCode 不存在)"

echo ""
echo "=== CONDA ENV ==="
ls /home/liuyanzhi/miniconda3/envs/ljz_env/ 2>/dev/null | head -3
/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python --version
/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python -c "import torch; print('torch', torch.__version__, 'cuda', torch.version.cuda, 'gpus', torch.cuda.device_count())"
'''

stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
err = stderr.read().decode()
print(out)
if err.strip():
    print("STDERR:", err[:1000])

ssh.close()
