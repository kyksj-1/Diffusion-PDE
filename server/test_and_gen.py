"""
W5-F 服务器端测试 + 数据生成 + tmux 训练启动.
"""
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

# ---- 1. 跑 W5 单元测试 ----
print("=" * 60)
print("1. 服务器端单元测试 (39 个)")
print("=" * 60)
stdin, stdout, stderr = ssh.exec_command(
    f'cd {REMOTE_ROOT} && {PYTHON} -m pytest tests/test_dit_1d.py tests/test_mixed_pde_dataset.py tests/test_dit_scores.py -v 2>&1 | tail -20'
)
print(stdout.read().decode())
err = stderr.read().decode()
if err.strip(): print("STDERR:", err[:500])

# ---- 2. 数据情况确认 ----
print("=" * 60)
print("2. 数据状态 (servers output/data/)")
print("=" * 60)
stdin, stdout, _ = ssh.exec_command(
    f'cd {REMOTE_ROOT} && ls -la output/data/ 2>/dev/null && echo "--- 现有 *.npy:" && find output -name "*.npy" 2>/dev/null'
)
print(stdout.read().decode())

# ---- 3. 启动 burgers 数据生成 (后台 tmux window in 'entrodiff' session) ----
# 用 tmux send-keys 在已有 entrodiff session 里开一个新窗口
print("=" * 60)
print("3. 生成 burgers 数据 (tmux 新窗口)")
print("=" * 60)
gen_cmd = (
    f"tmux new-window -t entrodiff -n gen_burgers "
    f"'cd {REMOTE_ROOT} && {PYTHON} scripts/generate_data.py 2>&1 | tee /tmp/gen_burgers.log'"
)
stdin, stdout, _ = ssh.exec_command(gen_cmd + " && echo TMUX_WINDOW_CREATED")
print(stdout.read().decode())

# ---- 4. tmux 状态确认 ----
stdin, stdout, _ = ssh.exec_command('tmux ls 2>&1; tmux list-windows -t entrodiff 2>&1')
print(stdout.read().decode())

ssh.close()
print("\n[启动] burgers 数据生成已在 tmux 'entrodiff:gen_burgers' 窗口运行")
print("[下一步] 等数据生成完成后启动 tiny 配置训练 (RTX 3090, GPU 0)")
