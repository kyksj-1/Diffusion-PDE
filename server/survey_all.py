"""服务器实验全盘点."""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('202.121.181.105', port=227, username='liuyanzhi', password='HUBRtEeOFC8F0moC', timeout=15)

R = '/home/liuyanzhi/ljz/EntroDiffCode'
cmd = f'''
echo "=== 1. 实验目录 ==="
ls -la {R}/output/experiments/

echo ""
echo "=== 2. 每个实验的 ckpt 数量 + 最新 ckpt + 训练日志末尾 ==="
for d in {R}/output/experiments/*/; do
  name=$(basename "$d")
  echo "--- $name ---"
  ls "$d"*.pt 2>/dev/null | wc -l | xargs -I {{}} echo "  ckpt 数: {{}}"
  ls "$d"*.pt 2>/dev/null | sort | tail -1
  log=$(ls "$d"train_log*.txt 2>/dev/null | head -1)
  if [ -n "$log" ]; then
    echo "  日志: $(basename $log)"
    echo "  日志末 3 行:"
    tail -3 "$log" | sed 's/^/    /'
  fi
done

echo ""
echo "=== 3. 数据文件 ==="
ls -la {R}/output/data/

echo ""
echo "=== 4. eval 输出 (跨 PDE 表) ==="
find {R}/output/experiments -name "metrics_table.csv" -exec echo "--- {{}} ---" \\; -exec cat {{}} \\;

echo ""
echo "=== 5. 已有评估 figure ==="
find {R}/output/experiments -name "*.png" | head -20

echo ""
echo "=== 6. 服务器 git 当前分支 + head ==="
cd {R} && git branch --show-current && git log --oneline -5
'''
stdin, stdout, _ = ssh.exec_command(cmd, timeout=60)
print(stdout.read().decode())
ssh.close()
