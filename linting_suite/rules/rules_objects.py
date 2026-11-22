"""Rule object definitions and violations."""

from dataclasses import dataclass
from enum import Enum

import linting_suite.config.constants as const


class RuleSeverity(Enum):
    """Severity levels for violations."""

    HIGH = const.SEVERITY_HIGH
    MEDIUM = const.SEVERITY_MEDIUM
    LOW = const.SEVERITY_LOW
    INFO = const.SEVERITY_INFO


@dataclass(frozen=True, slots=True)
class Violation:
    """Represents a single linting violation."""

    rule_id: str
    severity: RuleSeverity
    file: str
    line: int
    col: int
    message: str

    def format_text(self) -> str:
        """Format as plain text."""
        return const.TEMPLATE_VIOLATION_TEXT.format(file=self.file, line=self.line, rule_id=self.rule_id, message=self.message)

    def format_github(self) -> str:
        """Format as GitHub Actions annotation."""
        if self.severity == RuleSeverity.HIGH:
            level = const.GITHUB_LEVEL_ERROR
        elif self.severity == RuleSeverity.INFO:
            level = const.GITHUB_LEVEL_NOTICE
        else:
            level = const.GITHUB_LEVEL_WARNING
        return const.TEMPLATE_VIOLATION_GITHUB.format(level=level, file=self.file, line=self.line, col=self.col, message=self.message)


@dataclass(frozen=True, slots=True)
class Rule:
    """Rule definition."""

    id: str
    name: str
    severity: RuleSeverity
    description: str
