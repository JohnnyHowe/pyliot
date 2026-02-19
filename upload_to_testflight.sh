#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python3"

"$SCRIPT_DIR/setup_venv.sh"
"$VENV_PYTHON" -m pyliot.upload_to_testflight_cmd_entry "$@"
