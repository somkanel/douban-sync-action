#!/bin/sh
set -e

echo "=== Douban Sync Action Started ==="

python -m src.douban_client \
  --id "${INPUT_ID}" \
  --type "${INPUT_TYPE}" \
  --format "${INPUT_FORMAT}" \
  --dir "${INPUT_DIR}" \
  --count "${INPUT_COUNT}"

echo "=== Douban Sync Action Completed ==="
