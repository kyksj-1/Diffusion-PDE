"""
W5-F 启动 foundation_small 训练 (服务器 RTX 3090, tmux).

策略:
    1. kill 多余的 gen_burgers 窗口 (数据已存在)
    2. 在 entrodiff session 创建新窗口 foundation_small
    3. 启动 small 配置训练 (BVAware + DiT, dim=256, n_layers=6, BL+Burgers 混合)
    4. 用 GPU 0 (其他 windows 已有任务在 GPU 1/2 — 通过 tmux ls 推断)
"""
import time
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    '202.121.181.105', port=227,
    username='liuyanzhi', password='HUBRtEeOFC8F0moC',
    timeout=15,
)

REMOTE_ROOT = '/home/liuyanzhi/ljz/EntroDiffCode'
PYTHON = '/home/liuyanzhi/miniconda3/envs/ljz_env/bin/python'

# 1. 先 kill gen_burgers (数据已存在, 无需生成)
print("=" * 60)
print("1. 关闭多余的 gen_burgers 窗口")
print("=" * 60)
stdin, stdout, _ = ssh.exec_command(
    'tmux kill-window -t entrodiff:gen_burgers 2>&1; tmux list-windows -t entrodiff'
)
print(stdout.read().decode())

# 2. 检查 GPU 当前使用
print("=" * 60)
print("2. GPU 状态 (选择空闲 GPU)")
print("=" * 60)
stdin, stdout, _ = ssh.exec_command(
    'nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader'
)
print(stdout.read().decode())

# 3. 启动 small 训练 in new tmux window
# nohup + tee 让日志可追溯; 用 small 配置 (dim=256 n_layers=6 ~7M params, 24GB 充裕)
# CUDA_VISIBLE_DEVICES=0 强制用 GPU 0
print("=" * 60)
print("3. 启动 foundation_small tmux 窗口 (GPU 0)")
print("=" * 60)

# tmux new-window: -d 不切到该窗口, 但当前窗口创建即默认前台
# 用单引号包 shell 命令避免转义麻烦
inner_cmd = (
    f"cd {REMOTE_ROOT} && "
    f"CUDA_VISIBLE_DEVICES=0 {PYTHON} scripts/train_foundation.py "
    f"--config configs/foundation/small.yaml 2>&1 | tee /tmp/foundation_small.log"
)
# 转义 inner_cmd 中的单引号 (此处无)
new_window_cmd = (
    f"tmux new-window -t entrodiff -n foundation_small '{inner_cmd}' && "
    f"echo TMUX_NEW_WINDOW_OK"
)
stdin, stdout, stderr = ssh.exec_command(new_window_cmd)
print(stdout.read().decode())
err = stderr.read().decode()
if err.strip(): print("STDERR:", err[:500])

# 4. 等 30s 让训练启动 (加载数据 + 第一个 batch)
print("等待 30s 让训练初始化...")
time.sleep(30)

# 5. 看初始日志
print("=" * 60)
print("4. 初始训练日志 (前 30 行)")
print("=" * 60)
stdin, stdout, _ = ssh.exec_command('cat /tmp/foundation_small.log 2>&1 | head -30')
print(stdout.read().decode())

# 6. tmux 确认
stdin, stdout, _ = ssh.exec_command('tmux list-windows -t entrodiff 2>&1')
print("--- tmux windows ---")
print(stdout.read().decode())

# 7. GPU 此时使用情况
stdin, stdout, _ = ssh.exec_command(
    'nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader'
)
print("--- GPU 状态 (训练启动后) ---")
print(stdout.read().decode())

ssh.close()
print()
print("[OK] foundation_small 训练已启动")
print("    远程附加: ssh -p 227 liuyanzhi@202.121.181.105")
print("              tmux attach -t entrodiff")
print("              Ctrl+b 3 (foundation_small 窗口)")
print("    日志: /tmp/foundation_small.log + output/experiments/foundation_small/train_log_*.txt")
