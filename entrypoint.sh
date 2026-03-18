#!/bin/sh
set -e

echo "=== Douban Sync Action Started ==="
echo "User ID: ${INPUT_ID}"
echo "Output Dir: ${INPUT_DIR}"

# 创建输出目录
mkdir -p "${INPUT_DIR}"

# 运行 Python 脚本（从环境变量读取 Cookie）
python -m src.douban_client \
    "${INPUT_ID}" \
    "${INPUT_DIR}" \
    "${DOUBAN_COOKIE}"

echo "=== Douban Sync Action Completed ==="
