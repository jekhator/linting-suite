"""Main linter implementation."""

import ast
import hashlib
import json
from pathlib import Path

import linting_suite.config.constants as const
import linting_suite.linter.linter_objects as objs
from linting_suite.checkers import (
    R001Checker,
    R002Checker,
    R003Checker,
    R004Checker,
    R005Checker,
    R006Checker,
    R007Checker,
    R008Checker,
    R009Checker,
    R010Checker,
    R011Checker,
    R012Checker,
    R013Checker,
    R014Checker,
    R015Checker,
)
from linting_suite.config._config import Config
from linting_suite.rules import RuleSeverity, Violation


class DtoStrictLinter:
    """AST-based linter for DTO discipline."""

    def __init__(
        self, config: Config, baseline: dict[tuple[str, int, str], str] | None = None
    ):
        self.config = config
        self.violations: list[Violation] = []
        self.baseline = baseline or {}

    def lint_file(self, file_path: Path) -> list[Violation]:
        """Lint a single Python file."""
        if not file_path.suffix == const.PY_EXTENSION:
            return []

        try:
            source = file_path.read_text()
        except Exception:
            return []

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        violations = []

        for checker_cls in [
            R001Checker,
            R002Checker,
            R003Checker,
            R004Checker,
            R005Checker,
            R006Checker,
            R007Checker,
            R008Checker,
            R009Checker,
            R010Checker,
            R011Checker,
            R012Checker,
            R013Checker,
            R014Checker,
            R015Checker,
        ]:
            checker = checker_cls(file_path, source, self.config)
            checker.visit(tree)
            violations.extend(checker.violations)

        filtered = []
        for violation in violations:
            if self.config.is_rule_enabled(violation.rule_id):
                filtered.append(violation)

        if self.baseline:
            filtered = self._filter_by_baseline(filtered)

        return filtered

    def lint_path(self, path: Path) -> list[Violation]:
        """Lint all Python files in a directory or single file."""
        all_violations = []

        if path.is_file():
            all_violations.extend(self.lint_file(path))
        elif path.is_dir():
            for py_file in path.rglob(const.PY_GLOB):
                all_violations.extend(self.lint_file(py_file))

        filtered = []
        for candidate in all_violations:
            if self.config.is_rule_enabled(candidate.rule_id):
                filtered.append(candidate)

        if self.baseline:
            filtered = self._filter_by_baseline(filtered)

        overridden = []
        for violation in filtered:
            if violation.rule_id in self.config.severity_overrides:
                new_severity = self.config.severity_overrides[violation.rule_id].upper()
                if new_severity in const.VALID_SEVERITY_LEVELS:
                    violation = Violation(
                        rule_id=violation.rule_id,
                        severity=RuleSeverity[new_severity],
                        file=violation.file,
                        line=violation.line,
                        col=violation.col,
                        message=violation.message,
                    )
            overridden.append(violation)

        return overridden

    def _filter_by_baseline(self, violations: list[Violation]) -> list[Violation]:
        """Filter violations by baseline, removing accepted violations by file+line+rule_id."""
        new_violations = []
        for violation in violations:
            key = (violation.file, violation.line, violation.rule_id)
            if key not in self.baseline:
                new_violations.append(violation)
        return new_violations

    @staticmethod
    def _hash_message(message: str) -> str:
        """Hash violation message for baseline comparison."""
        return hashlib.sha256(message.encode()).hexdigest()[:const.MESSAGE_HASH_LENGTH]

    def generate_baseline(self, violations: list[Violation]) -> list[dict]:
        """Generate baseline JSON from violations."""
        baseline_data = []
        for violation in violations:
            message_hash = self._hash_message(violation.message)
            baseline_data.append(
                {
                    const.BASELINE_KEY_FILE: violation.file,
                    const.BASELINE_KEY_LINE: violation.line,
                    const.BASELINE_KEY_RULE_ID: violation.rule_id,
                    const.BASELINE_KEY_MESSAGE_HASH: message_hash,
                }
            )
        return baseline_data

    @staticmethod
    def load_baseline(baseline_path: Path) -> dict[tuple[str, int, str], str]:
        """Load baseline JSON file."""
        try:
            with open(baseline_path, const.FILE_MODE_READ) as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise objs.BaselineLoadError(
                const.ERR_BASELINE_INVALID_JSON.format(path=baseline_path)
            ) from error
        except OSError as error:
            raise objs.BaselineLoadError(
                const.ERR_BASELINE_MISSING.format(path=baseline_path)
            ) from error

        if not isinstance(data, list):
            raise objs.BaselineLoadError(const.ERR_BASELINE_NOT_LIST.format(path=baseline_path))

        baseline = {}
        for index, entry in enumerate(data):
            if not isinstance(entry, dict):
                raise objs.BaselineLoadError(
                    const.ERR_BASELINE_ENTRY_NOT_OBJECT.format(
                        index=index, path=baseline_path
                    )
                )
            for key in const.REQUIRED_BASELINE_KEYS:
                if key not in entry:
                    raise objs.BaselineLoadError(
                        const.ERR_BASELINE_ENTRY_SHAPE.format(
                            index=index, key=key, path=baseline_path
                        )
                    )
            baseline_key = (entry[const.BASELINE_KEY_FILE], entry[const.BASELINE_KEY_LINE], entry[const.BASELINE_KEY_RULE_ID])
            baseline[baseline_key] = entry[const.BASELINE_KEY_MESSAGE_HASH]
        return baseline

    def format_violations(
        self, violations: list[Violation], format_type: str = const.FORMAT_TEXT
    ) -> str:
        """Format violations for output."""
        if format_type == const.FORMAT_GITHUB:
            return const.LINE_SEPARATOR.join(violation.format_github() for violation in violations)
        elif format_type == const.FORMAT_JSON:
            return json.dumps(
                [
                    {
                        const.VIOLATION_KEY_RULE_ID: violation.rule_id,
                        const.VIOLATION_KEY_SEVERITY: violation.severity.value,
                        const.VIOLATION_KEY_FILE: violation.file,
                        const.VIOLATION_KEY_LINE: violation.line,
                        const.VIOLATION_KEY_COL: violation.col,
                        const.VIOLATION_KEY_MESSAGE: violation.message,
                    }
                    for violation in violations
                ],
                indent=const.JSON_INDENT,
            )
        else:
            return const.LINE_SEPARATOR.join(violation.format_text() for violation in violations)

    def get_exit_code(self, violations: list[Violation]) -> int:
        """Determine exit code based on violation severities."""
        if not violations:
            return const.EXIT_CODE_SUCCESS

        has_high = any(violation.severity == RuleSeverity.HIGH for violation in violations)
        has_medium = any(violation.severity == RuleSeverity.MEDIUM for violation in violations)
        has_low = any(violation.severity == RuleSeverity.LOW for violation in violations)
        has_info = any(violation.severity == RuleSeverity.INFO for violation in violations)

        if has_high:
            return const.EXIT_CODE_HIGH_VIOLATION
        elif has_medium:
            return const.EXIT_CODE_MEDIUM_VIOLATION
        elif has_low:
            return const.EXIT_CODE_LOW_VIOLATION
        elif has_info:
            return const.EXIT_CODE_SUCCESS
        else:
            return const.EXIT_CODE_SUCCESS
