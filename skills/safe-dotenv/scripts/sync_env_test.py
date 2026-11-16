from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from sync_env import sync


class SyncEnvTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp_dir.name)
        self.example = self.directory / ".env.example"
        self.env = self.directory / ".env"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_sync_preserves_values_and_adopts_template_order_comments_and_variables(self) -> None:
        self.example.write_text("# New heading\nSECOND=REDACTED # second setting\nFIRST=REDACTED\n", encoding="utf-8")
        self.env.write_text("FIRST=secret-value\nREMOVED=old-value\nSECOND=another-secret\n", encoding="utf-8")

        sync(self.example)

        self.assertEqual(
            "# New heading\nSECOND=another-secret # second setting\nFIRST=secret-value\n",
            self.env.read_text(encoding="utf-8"),
        )

    def test_sync_creates_missing_env_with_restricted_permissions(self) -> None:
        self.example.write_text("TOKEN=REDACTED\n", encoding="utf-8")

        sync(self.example)

        self.assertEqual("TOKEN=REDACTED\n", self.env.read_text(encoding="utf-8"))
        self.assertEqual(0o600, self.env.stat().st_mode & 0o777)

    def test_sync_supports_dotenv_variants(self) -> None:
        local = self.directory / ".env.local"
        local_example = self.directory / ".env.local.example"
        local_example.write_text("LOCAL_TOKEN=REDACTED\n", encoding="utf-8")
        local.write_text("LOCAL_TOKEN=local-secret\n", encoding="utf-8")

        sync(local_example)

        self.assertEqual("LOCAL_TOKEN=local-secret\n", local.read_text(encoding="utf-8"))

    def test_sync_preserves_quoted_values_and_template_inline_comments(self) -> None:
        self.example.write_text('TOKEN=REDACTED # API token\nURL=REDACTED\n', encoding="utf-8")
        self.env.write_text('TOKEN="secret # value" # private comment\nURL=https://example.com/#path\n', encoding="utf-8")

        sync(self.example)

        self.assertEqual(
            'TOKEN="secret # value" # API token\nURL=https://example.com/#path\n',
            self.env.read_text(encoding="utf-8"),
        )

    def test_sync_preserves_assignment_format_from_example(self) -> None:
        self.example.write_text("export  TOKEN = REDACTED\n", encoding="utf-8")
        self.env.write_text("TOKEN = secret-value\n", encoding="utf-8")

        sync(self.example)

        self.assertEqual("export  TOKEN = secret-value\n", self.env.read_text(encoding="utf-8"))

    def test_cli_rejects_non_env_paths(self) -> None:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("sync_env.py")), str(self.directory / "settings")],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("file name must start with .env", result.stderr)

    def test_bare_keys_remain_unset_and_do_not_discard_assigned_values(self) -> None:
        self.example.write_text("SETTING=template-default\nOTHER=example\n", encoding="utf-8")
        self.env.write_text("SETTING\nOTHER=preserved\n", encoding="utf-8")

        sync(self.example)

        self.assertEqual(
            "SETTING=template-default\nOTHER=preserved\n",
            self.env.read_text(encoding="utf-8"),
        )

    def test_unsupported_syntax_fails_without_overwriting_existing_file(self) -> None:
        self.example.write_text("TOKEN=REDACTED\n", encoding="utf-8")
        self.env.write_text("TOKEN=keep-this\nMULTILINE: unsupported\n", encoding="utf-8")

        with self.assertRaises(ValueError):
            sync(self.example)

        self.assertEqual("TOKEN=keep-this\nMULTILINE: unsupported\n", self.env.read_text(encoding="utf-8"))

    def test_duplicate_template_variable_fails_without_overwriting(self) -> None:
        self.example.write_text("TOKEN=REDACTED\nTOKEN=REDACTED\n", encoding="utf-8")
        self.env.write_text("TOKEN=keep-this\n", encoding="utf-8")

        with self.assertRaises(ValueError):
            sync(self.example)

        self.assertEqual("TOKEN=keep-this\n", self.env.read_text(encoding="utf-8"))

    def test_cli_works_when_skill_is_relocated(self) -> None:
        script = self.directory / "portable-skill" / "scripts" / "sync_env.py"
        script.parent.mkdir(parents=True)
        shutil.copyfile(Path(__file__).with_name("sync_env.py"), script)
        self.example.write_text("TOKEN=REDACTED\n", encoding="utf-8")
        self.env.write_text("TOKEN=fixture-value\n", encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(script), str(self.example)],
            cwd=self.directory,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, result.returncode)
        self.assertEqual("TOKEN=fixture-value\n", self.env.read_text(encoding="utf-8"))
        self.assertNotIn("fixture-value", result.stdout + result.stderr)

    def test_cli_does_not_disclose_dotenv_contents_on_errors(self) -> None:
        self.example.write_text("TOKEN=REDACTED\n", encoding="utf-8")
        original = b"PRIVATE_KEY=fixture-value\nPRIVATE_KEY=other-value\n"
        self.env.write_bytes(original)

        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("sync_env.py")), str(self.example)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertNotIn("PRIVATE_KEY", result.stdout + result.stderr)
        self.assertNotIn("fixture-value", result.stdout + result.stderr)
        self.assertEqual(original, self.env.read_bytes())

        original = b"TOKEN=fixture-value\xff\n"
        self.env.write_bytes(original)
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("sync_env.py")), str(self.example)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertNotIn("fixture-value", result.stdout + result.stderr)
        self.assertNotIn("0xff", result.stdout + result.stderr)
        self.assertEqual(original, self.env.read_bytes())


if __name__ == "__main__":
    unittest.main()
