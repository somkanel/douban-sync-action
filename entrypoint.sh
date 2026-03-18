#!/bin/sh
set -e

echo "=== Douban Sync Action Started ==="
echo "User ID: ${INPUT_ID}"
echo "Output Dir: ${INPUT_DIR}"

# 创建输出目录
mkdir -p "${INPUT_DIR}"

# 切换到我们放置代码的目录，或者直接设置 PYTHONPATH
export PYTHONPATH="/action_app"

# 运行 Python 脚本
python -m src.douban_client \
    "${INPUT_ID}" \
    "${INPUT_DIR}" \
    "${DOUBAN_COOKIE}"

echo "=== Douban Sync Action Completed ==="
