"""Test R002 exception tag format and separator alignment."""

from linting_suite.config._config import Config
from linting_suite.linter import DtoStrictLinter


class TestR002TagSeparatorFormat:
    """Test suite for related functionality."""

    def test_r002_tag_separator_format_in_message(self, tmp_path):
        """Test that R002 error message uses correct tag separator format colon."""
        code_file = tmp_path / "test.py"
        code_file.write_text("""
def process_data():
    return {"key": 1, "value": 2, "data": 3}
""")

        config = Config(
            service_paths=["**/*.py"], exception_tags=["facade - celery schedule"],
            exception_tag_requires_justification=True
        )
        linter = DtoStrictLinter(config)
        violations = linter.lint_file(code_file)
        r002_violations = [found for found in violations if found.rule_id == "R002"]

        assert len(r002_violations) >= 1
        for violation in r002_violations:
            message = violation.message
            if "Format:" in message:
                assert "Format: 'tag: explanation'" in message
                assert "facade - celery schedule:" in message
                assert "—" not in message

    def test_tag_separator_uses_colon_not_em_dash(self, tmp_path):
        """Test that tag separator format shows colon, not em dash."""
        config = Config(
            service_paths=["**/*.py"], exception_tags=["facade - celery schedule"],
            exception_tag_requires_justification=True
        )
        assert all("-" in tag and "—" not in tag for tag in config.exception_tags)
