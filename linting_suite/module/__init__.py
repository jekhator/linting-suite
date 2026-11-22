"""AST-based linter for Python DTO discipline and facade-ban enforcement."""

from linting_suite.config import __version__
from linting_suite.linter import DtoStrictLinter, Rule, RuleSeverity

__all__ = ["DtoStrictLinter", "Rule", "RuleSeverity", "__version__"]
