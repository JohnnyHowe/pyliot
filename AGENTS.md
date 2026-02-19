# Repository Guidelines

## Project Structure & Module Organization
Core code lives in `src/pyliot/`. The CLI entry point is `src/pyliot/upload_to_testflight_cmd_entry.py`, which loads parameters and calls the upload flow in `src/pyliot/upload_to_test_flight.py`.

Top-level files:
- `pyproject.toml`: package metadata and dependencies.
- `upload_to_testflight.sh`: local bootstrap + run script (creates/uses `.venv`).
- `example.env`: environment variable template for required secrets and upload settings.
- `README.md`: usage, variables, and validation commands.

## Build, Test, and Development Commands
- `bash upload_to_testflight.sh`: set up `.venv`, install dependencies, and run uploader.
- `.venv/bin/python3 -m pyliot.upload_to_testflight_cmd_entry`: run CLI directly for debugging.
- `python3 -m py_compile src/pyliot/*.py`: quick syntax validation.
- `pip install -e .`: editable local install for iterative development.

If you add tests, place them under `tests/` (README references `tests/run_all.py`).

## Coding Style & Naming Conventions
- Python 3.10+ (`pyproject.toml` requires `>=3.10`).
- Follow existing module naming: `snake_case.py` (example: `upload_parameters.py`).
- Use descriptive function/class names (`UploadParameters`, `run_attempt`).
- Match surrounding file style when editing; current codebase uses both tabs and spaces in different files, so avoid unrelated reformatting.
- Prefer explicit type hints on public functions and parameters.

## Testing Guidelines
No formal test framework is currently configured in-repo. Minimum expectation for changes:
- Run `python3 -m py_compile src/pyliot/*.py` before opening a PR.
- Perform a local CLI smoke test with non-production values via `.env`.
- For new behavior, add focused tests under `tests/` using `test_*.py` naming and document run instructions in README.

## Commit & Pull Request Guidelines
Git history is minimal (currently a single `Initial commit`), so adopt clear, imperative commit messages such as `Add retry logging for pilot upload timeout`.

For PRs:
- Explain what changed and why.
- List validation steps you ran (commands + outcome).
- Link related issues/tasks.
- Include sample CLI invocation or log snippets when behavior/output changes.

## Security & Configuration Tips
Never commit `.env`, API key content, or App Store credentials. Keep secrets in local environment variables or CI/UCB secure settings, and use `example.env` only as a template.
