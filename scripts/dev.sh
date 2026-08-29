#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

"$BASE_DIR/.venv/bin/python" -m uvicorn \
	--app-dir "$BASE_DIR" main:app --reload --port 3999