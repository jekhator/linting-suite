"""Tests for R002 exemption: dict literals in to_* methods of dataclasses."""

from linting_suite.config._config import Config
from linting_suite.linter import DtoStrictLinter


class TestR002SerializerExemption:
    """Test suite for related functionality."""

    def test_r002_exempt_serializer_methods(self, fixture_dir):
        """Good: dict literals in to_* methods of dataclasses are exempt."""
        config = Config(
            service_paths=[
                "*/**/*.py",
                "tests/fixtures/**/*.py",
            ],
            dto_paths=["**/dtos.py"],
        )
        linter = DtoStrictLinter(config)
        violations = linter.lint_file(fixture_dir / "good" / "r002_good_serializer.py")
        r002_violations = [violation for violation in violations if violation.rule_id == "R002"]
        assert len(r002_violations) == 0, (
            "to_* methods in dataclasses should be exempt from R002"
        )

    def test_r002_flags_non_serializer_in_dataclass(self, fixture_dir):
        """Bad: dict literals in non-to_* methods of dataclasses are still flagged."""
        config = Config(
            service_paths=[
                "*/**/*.py",
                "tests/fixtures/**/*.py",
            ],
            dto_paths=["**/dtos.py"],
        )
        linter = DtoStrictLinter(config)
        violations = linter.lint_file(
            fixture_dir / "bad" / "r002_bad_non_serializer.py"
        )
        r002_violations = [violation for violation in violations if violation.rule_id == "R002"]
        assert len(r002_violations) >= 1, (
            "get_metadata() with inline dict should be flagged"
        )
        assert any("keys" in violation.message for violation in r002_violations), (
            "Violation should mention dict keys"
        )
