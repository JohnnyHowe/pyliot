import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from pyliot.upload_parameters import UploadParameters


class UploadParametersTests(unittest.TestCase):
    def _required_env(self) -> dict[str, str]:
        return {
            "API_KEY_ISSUER_ID": "issuer",
            "API_KEY_ID": "keyid",
            "API_KEY_CONTENT": "private-key",
            "IPA_PATH": "Builds/iOS/build.ipa",
            "CHANGELOG": "notes",
        }

    def test_cli_overrides_env_for_max_attempts(self) -> None:
        env = self._required_env()
        env["MAX_UPLOAD_ATTEMPTS"] = "3"

        with patch.dict(os.environ, env, clear=True), patch.object(
            sys, "argv", ["prog", "--max-upload-attempts", "7"]
        ), patch("pyliot.upload_parameters.pretty_print"):
            parameters = UploadParameters()
            parameters.load()

        self.assertEqual(parameters.max_upload_attempts, 7)
        self.assertEqual(parameters.attempt_timeout, 600)
        self.assertEqual(parameters.ipa_path, Path("Builds/iOS/build.ipa"))

    def test_invalid_env_cast_keeps_default_max_attempts(self) -> None:
        env = self._required_env()
        env["MAX_UPLOAD_ATTEMPTS"] = "not-a-number"

        with patch.dict(os.environ, env, clear=True), patch.object(
            sys, "argv", ["prog"]
        ), patch("pyliot.upload_parameters.pretty_print"):
            parameters = UploadParameters()
            parameters.load()

        self.assertEqual(parameters.max_upload_attempts, 10)


if __name__ == "__main__":
    unittest.main()
