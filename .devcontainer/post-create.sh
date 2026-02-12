#!/usr/bin/env bash
set -euo pipefail

if ! command -v z3 >/dev/null 2>&1 && command -v apt-get >/dev/null 2>&1; then
  if command -v sudo >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y --no-install-recommends z3
  else
    apt-get update
    apt-get install -y --no-install-recommends z3
  fi
fi

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

.venv/bin/python z3_HW_problem-1.py
