# Overview
Tool to upload `.ipa` files to TestFlight.

It's mostly a wrapper for `fastlane pilot upload`. \
This exists as fastlane pilot upload can sometimes randomly fail. This retries it and add some nice logging.

# To do
* auto increase build number
* extract project out to a more generic uploader (this one will contain UCB things: .ipa finder)
* figure out why no fastlane logs (wait, did it succeed quietly??)
* some way of reading changelog from file

# Requirements
* Python 3
* git
* fastlane (`pilot`)

# Project Structure
```text
repo-root/
  pyproject.toml
  README.md
  package-structure.md
  src/
    pyliot/
      __init__.py
      ...module files...
  tests/
    run_all.py
```

# Install
## Install from GitHub
```bash
pip install "pyliot @ git+https://github.com/OWNER/REPO.git"
```

## Session-only install (venv)
```bash
bash setup_venv.sh
```
`setup_venv.sh` creates/uses `.venv/` and installs project dependencies.

# Quick Start
1. Create API key ([See: Creating Your API Key](#creating-your-api-key))
2. Set parameters/environment variables (See: [passing variables](#passing-variables) and [variables docs](#variables))
3. Run uploader
```bash
bash upload_to_testflight.sh
```
`upload_to_testflight.sh` calls `setup_venv.sh` and then runs the uploader entrypoint.

Direct module execution (debugging):
```bash
.venv/bin/python3 -m pyliot.upload_to_testflight_cmd_entry
```

# Validation
```bash
python3 -m py_compile src/pyliot/*.py tests/run_all.py
python3 tests/run_all.py
```

# Variables
These can be passed either as command line arguments or as environment variables.\
CLI arguments override environment variables if both exist.

| CLI Name | ENV Name | Type | Required (Default) | Description |
|-|-|-|-|-|
| `--api-key-issuer-id` | `API_KEY_ISSUER_ID` | `string` | ✅ | Identifies the issuer who created the authentication token.<br>Look for "Issuer ID" on [the App Store Connect API page](https://appstoreconnect.apple.com/access/integrations/api). |
| `--api-key-id`| `API_KEY_ID` | `string` | ✅ | Look for "Key ID" on your key in [the App Store Connect API page](https://appstoreconnect.apple.com/access/integrations/api). |
| `--api-key-content`| `API_KEY_CONTENT` | `string` | ✅ | The raw text contents of your API key (`.p8` contents). |
| `--ipa-path`| `IPA_PATH`| `path`/`string` | ✅ | Path to the .ipa file to upload. |
| `--changelog`| `CHANGELOG` | `string` | ✅ | Release notes text for this TestFlight upload. |
| `--groups`| `GROUPS` | `comma-separated string` | ❌ | Tester groups to distribute to (`groupA,groupB`). If empty, build still goes to internal testers. |
| `--max-upload-attempts`| `MAX_UPLOAD_ATTEMPTS` | `int` | ❌ (10) | Maximum retry attempts for upload. |
| `--attempt-timeout` | `ATTEMPT_TIMEOUT` | `int` | ❌ (600) | Max time each upload attempt can run in seconds. |

# Passing Variables
## Locally (.env file)
Put variables in a `.env` file at project root.\
**Do not commit this file; it contains sensitive values.**

See [example.env](example.env)

## Unity Cloud Build (Environment Variables)
Go to configuration -> Advanced Settings -> Environment variables. \
Important: **some required variables are provided automatically by UCB.**

## Command Line Arguments
You can pass any variable with CLI flags.

Example:
```bash
bash upload_to_testflight.sh \
  --api-key-issuer-id "<issuer-id>" \
  --api-key-id "<key-id>" \
  --api-key-content "<p8-content>" \
  --output-directory "./Builds/iOS" \
  --changelog "Internal QA build" \
  --groups "Internal QA" \
  --max-upload-attempts 10 \
  --attempt-timeout 600
```
# Creating Your API Key
This is how the upload script authenticates with App Store Connect.

Create here: https://appstoreconnect.apple.com/access/integrations/api\
Apple docs: https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api

Once you've created and downloaded it (`.p8`), store it securely.
If you open it in a text editor, it should look like this:
```text
-----BEGIN PRIVATE KEY-----
<key-content>
-----END PRIVATE KEY-----
```
