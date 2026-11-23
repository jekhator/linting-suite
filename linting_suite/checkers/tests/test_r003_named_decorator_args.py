"""Tests for R003 when a dataclass decorator argument is a name, not a literal."""

import ast
import subprocess
import sys
import warnings
from pathlib import Path

from linting_suite.checkers import R003Checker
from linting_suite.config._config import Config
from linting_suite.linter import DtoStrictLinter

NAMED_ARGUMENT_SOURCE = """
from dataclasses import dataclass

FROZEN = True


@dataclass(frozen=FROZEN, slots=True)
class Shape:
    name: str
"""


class TestR003NamedDecoratorArguments:
    """A named decorator argument is reported on, never a crash."""

    def test_named_argument_does_not_touch_removed_ast_node(self, tmp_path):
        """Linting must not reach for ast.NameConstant (deprecated in 3.12, removed in 3.14)."""
        dto_file = tmp_path / "dtos.py"
        dto_file.write_text(NAMED_ARGUMENT_SOURCE)
        linter = DtoStrictLinter(Config())

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            violations = linter.lint_file(dto_file)

        assert isinstance(violations, list)

    def test_named_argument_is_extracted_by_name(self):
        """The keyword value is recorded as the name it refers to."""
        tree = ast.parse(NAMED_ARGUMENT_SOURCE)
        class_node = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef))
        checker = R003Checker(Path("dtos.py"), NAMED_ARGUMENT_SOURCE, Config())

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            kwargs = checker._extract_decorator_kwargs(class_node.decorator_list[0])

        assert kwargs == {"frozen": "FROZEN", "slots": "True"}

    def test_cli_exits_cleanly_on_named_argument(self, tmp_path):
        """The command line reports instead of dying with a traceback."""
        dto_file = tmp_path / "dtos.py"
        dto_file.write_text(NAMED_ARGUMENT_SOURCE)

        result = subprocess.run(
            [
                sys.executable,
                "-W",
                "error::DeprecationWarning",
                "-m",
                "linting_suite.module.cli",
                str(dto_file),
            ],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
        )

        assert "Traceback" not in result.stderr
        assert "NameConstant" not in result.stderr
        assert result.returncode == 0
