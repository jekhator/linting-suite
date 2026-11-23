"""Tests that lint reports a file it could not read or parse instead of passing it."""

import subprocess
import sys

from linting_suite.config._config import Config
from linting_suite.config.constants import (
    EXIT_CODE_HIGH_VIOLATION,
    RULE_ID_UNPARSEABLE_FILE,
    RULE_ID_UNREADABLE_FILE,
)
from linting_suite.linter import DtoStrictLinter
from linting_suite.rules import RuleSeverity


class TestLintFailsLoud:
    """An unreadable or unparseable file is a HIGH violation, never clean."""

    def test_syntax_error_file_is_a_high_violation(self, tmp_path):
        """A file that does not parse yields one HIGH violation at the error line."""
        broken = tmp_path / "broken.py"
        broken.write_text("x = 1\ndef foo(:\n")
        linter = DtoStrictLinter(Config())

        violations = linter.lint_file(broken)

        assert len(violations) == 1
        assert violations[0].rule_id == RULE_ID_UNPARSEABLE_FILE
        assert violations[0].severity == RuleSeverity.HIGH
        assert violations[0].file == str(broken)
        assert violations[0].line == 2
        assert linter.get_exit_code(violations) == EXIT_CODE_HIGH_VIOLATION

    def test_undecodable_file_is_a_high_violation(self, tmp_path):
        """A file that is not valid text yields one HIGH violation."""
        binary = tmp_path / "binary.py"
        binary.write_bytes(b"\x80\x81\x82\x83")
        linter = DtoStrictLinter(Config())

        violations = linter.lint_file(binary)

        assert len(violations) == 1
        assert violations[0].rule_id == RULE_ID_UNREADABLE_FILE
        assert violations[0].severity == RuleSeverity.HIGH
        assert linter.get_exit_code(violations) == EXIT_CODE_HIGH_VIOLATION

    def test_directory_scan_reports_the_broken_file(self, tmp_path):
        """A directory scan surfaces the broken file next to the clean one."""
        (tmp_path / "clean.py").write_text("VALUE = 1\n")
        (tmp_path / "broken.py").write_text("x = (\n")
        linter = DtoStrictLinter(Config())

        violations = linter.lint_path(tmp_path)

        assert [v.rule_id for v in violations] == [RULE_ID_UNPARSEABLE_FILE]
        assert violations[0].file.endswith("broken.py")

    def test_rule_can_be_disabled_by_config(self, tmp_path):
        """The usual disabled_rules switch applies to the file-error rules."""
        broken = tmp_path / "broken.py"
        broken.write_text("x = (\n")
        linter = DtoStrictLinter(Config(disabled_rules=[RULE_ID_UNPARSEABLE_FILE]))

        assert linter.lint_file(broken) == []

    def test_baseline_entry_accepts_the_file_error(self, tmp_path):
        """A baselined file error is accepted like any other baselined violation."""
        broken = tmp_path / "broken.py"
        broken.write_text("x = (\n")
        first = DtoStrictLinter(Config()).lint_file(broken)
        baseline = {(first[0].file, first[0].line, first[0].rule_id): "hash"}

        assert DtoStrictLinter(Config(), baseline=baseline).lint_file(broken) == []

    def test_non_python_file_is_still_skipped(self, tmp_path):
        """A file that is not Python source is not this linter's business."""
        notes = tmp_path / "notes.txt"
        notes.write_bytes(b"\x80\x81")

        assert DtoStrictLinter(Config()).lint_file(notes) == []

    def test_cli_exits_non_zero_on_syntax_error(self, tmp_path):
        """The command line fails the gate on a file it cannot parse."""
        broken = tmp_path / "broken.py"
        broken.write_text("def foo(:\n")

        result = subprocess.run(
            [sys.executable, "-m", "linting_suite.module.cli", str(broken)],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
        )

        assert result.returncode == EXIT_CODE_HIGH_VIOLATION
        assert RULE_ID_UNPARSEABLE_FILE in result.stdout
        assert "broken.py" in result.stdout
