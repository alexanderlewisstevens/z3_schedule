#!/usr/bin/env bash
set -euo pipefail

LOG_FILE=".devcontainer/setup.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Running devcontainer setup"

run_as_root() {
  if command -v sudo >/dev/null 2>&1; then
    sudo "$@"
  else
    "$@"
  fi
}

if command -v apt-get >/dev/null 2>&1; then
  run_as_root rm -f /etc/apt/sources.list.d/yarn.list
fi

if ! command -v z3 >/dev/null 2>&1 && command -v apt-get >/dev/null 2>&1; then
  run_as_root apt-get update
  run_as_root apt-get install -y --no-install-recommends z3
fi

if ! python3 -c "import z3" >/dev/null 2>&1; then
  python3 -m pip install --user -r requirements.txt
fi

python3 z3_HW_problem-1.py
