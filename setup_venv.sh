#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python3"

if [[ ! -x "$VENV_PYTHON" ]]; then
  python3 -m venv "$VENV_DIR"
fi

"$VENV_PYTHON" -m pip install --upgrade pip

# Python 3.12+ venvs may not include setuptools/wheel by default.
# Editable installs for this project require setuptools.build_meta.
if ! "$VENV_PYTHON" -c "import setuptools, wheel" >/dev/null 2>&1; then
  if ! "$VENV_PYTHON" -m pip install --upgrade setuptools wheel; then
    echo "Failed to install required build dependencies: setuptools, wheel." >&2
    echo "Check network access, then rerun: bash setup_venv.sh" >&2
    exit 1
  fi
fi

"$VENV_PYTHON" -m pip install --no-build-isolation -e "$SCRIPT_DIR"
