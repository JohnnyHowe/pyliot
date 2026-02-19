import unittest
from pathlib import Path
from unittest.mock import patch

from pyliot.upload_to_testflight import _build_command, upload_to_testflight


class UploadToTestflightTests(unittest.TestCase):
    def test_build_command_includes_groups_when_provided(self) -> None:
        with patch("pyliot.upload_to_testflight.command_building.resolve_paths"):
            command = _build_command(
                ipa_path=Path("Builds/iOS/build.ipa"),
                api_key_path=Path("AppStoreConnectKey.json"),
                changelog="QA build",
                groups=["Internal QA", "Dev Team"],
            )

        self.assertIn("--groups", command)
        self.assertIn("Internal QA,Dev Team", command)

    def test_upload_retries_and_fails_after_max_attempts(self) -> None:
        with patch("pyliot.upload_to_testflight.APIKey") as mock_api_key, patch(
            "pyliot.upload_to_testflight.run_attempt",
            side_effect=RuntimeError("boom"),
        ) as mock_run_attempt, patch("pyliot.upload_to_testflight.pretty_print"):
            mock_api_key.return_value.file_path = Path("AppStoreConnectKey.json")

            with self.assertRaises(RuntimeError):
                upload_to_testflight(
                    api_key_issuer_id="issuer",
                    api_key_id="keyid",
                    api_key_content="private-key",
                    ipa_path=Path("Builds/iOS/build.ipa"),
                    changelog="notes",
                    max_upload_attempts=3,
                )

        self.assertEqual(mock_run_attempt.call_count, 3)

    def test_upload_returns_on_first_success(self) -> None:
        with patch("pyliot.upload_to_testflight.APIKey") as mock_api_key, patch(
            "pyliot.upload_to_testflight.run_attempt",
            return_value=None,
        ) as mock_run_attempt:
            mock_api_key.return_value.file_path = Path("AppStoreConnectKey.json")

            upload_to_testflight(
                api_key_issuer_id="issuer",
                api_key_id="keyid",
                api_key_content="private-key",
                ipa_path=Path("Builds/iOS/build.ipa"),
                changelog="notes",
                max_upload_attempts=5,
            )

        self.assertEqual(mock_run_attempt.call_count, 1)


if __name__ == "__main__":
    unittest.main()
