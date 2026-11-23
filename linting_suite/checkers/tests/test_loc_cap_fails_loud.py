"""Tests that loc-cap fails loud on a missing path or an unreadable file."""

import subprocess
import sys

import pytest

from linting_suite.config.constants import (
    ERR_LOC_CAP_UNREADABLE_FILE,
    ERR_NONEXISTENT_PATH,
    EXIT_CODE_HIGH_VIOLATION,
    EXIT_CODE_SUCCESS,
)
from linting_suite.loc_cap import LocCap, LocCapReadError


class TestLocCapMissingPath:
    """A path that does not exist is an error, never a silent pass."""

    def test_run_loc_cap_missing_path_exits_non_zero(self, tmp_path, capsys):
        """A missing path returns the high-violation exit code and names the path."""
        missing = str(tmp_path / "does_not_exist")

        exit_code = LocCap.run_loc_cap(missing)

        captured = capsys.readouterr()
        assert exit_code == EXIT_CODE_HIGH_VIOLATION
        assert ERR_NONEXISTENT_PATH.format(path=missing) in captured.err
        assert "within" not in captured.out

    def test_run_loc_cap_missing_path_generate_exits_non_zero(self, tmp_path, capsys):
        """Generating a baseline for a missing path is an error too."""
        missing = str(tmp_path / "does_not_exist")

        exit_code = LocCap.run_loc_cap(missing, generate=True)

        assert exit_code == EXIT_CODE_HIGH_VIOLATION
        assert ERR_NONEXISTENT_PATH.format(path=missing) in capsys.readouterr().err

    def test_unexpanded_brace_path_exits_non_zero(self, tmp_path, capsys):
        """A literal one-item brace path (what the shell leaves behind) fails."""
        (tmp_path / "common").mkdir()
        literal = str(tmp_path / "common" / "{constants}")

        exit_code = LocCap.run_loc_cap(literal)

        assert exit_code == EXIT_CODE_HIGH_VIOLATION
        assert "{constants}" in capsys.readouterr().err

    def test_cli_loc_cap_missing_path_exits_non_zero(self, tmp_path):
        """The loc-cap subcommand exits 1 on a missing path."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "linting_suite.module.cli",
                "loc-cap",
                str(tmp_path / "nope"),
            ],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
        )

        assert result.returncode == EXIT_CODE_HIGH_VIOLATION
        assert "path does not exist" in result.stderr
        assert "within" not in result.stdout

    def test_existing_empty_directory_still_passes(self, tmp_path):
        """An existing directory with no Python files stays a pass."""
        assert LocCap.run_loc_cap(str(tmp_path)) == EXIT_CODE_SUCCESS


class TestLocCapUnreadableFile:
    """A file that cannot be decoded is an error, never zero lines."""

    def test_count_lines_undecodable_file_raises(self, tmp_path):
        """A file that is not UTF-8 raises instead of counting as zero lines."""
        binary_file = tmp_path / "binary.py"
        binary_file.write_bytes(b"\x80\x81\x82\n" * 400)

        with pytest.raises(LocCapReadError) as raised:
            LocCap.count_lines(str(binary_file))

        assert str(raised.value) == ERR_LOC_CAP_UNREADABLE_FILE.format(
            path=str(binary_file)
        )

    def test_count_lines_missing_file_raises(self, tmp_path):
        """A file that cannot be opened raises instead of counting as zero lines."""
        with pytest.raises(LocCapReadError):
            LocCap.count_lines(str(tmp_path / "gone.py"))

    def test_run_loc_cap_undecodable_file_exits_non_zero(self, tmp_path, capsys):
        """An undecodable file fails the gate and is named on stderr."""
        binary_file = tmp_path / "binary.py"
        binary_file.write_bytes(b"\x80\x81\x82\n" * 400)

        exit_code = LocCap.run_loc_cap(str(tmp_path), hard_cap=300, soft_target=200)

        captured = capsys.readouterr()
        assert exit_code == EXIT_CODE_HIGH_VIOLATION
        assert "binary.py" in captured.err
        assert "within" not in captured.out

    def test_run_loc_cap_generate_undecodable_file_exits_non_zero(
        self, tmp_path, capsys
    ):
        """Baseline generation fails on an undecodable file as well."""
        (tmp_path / "binary.py").write_bytes(b"\x80\x81\x82\n")

        exit_code = LocCap.run_loc_cap(str(tmp_path), generate=True)

        assert exit_code == EXIT_CODE_HIGH_VIOLATION
        assert "binary.py" in capsys.readouterr().err
