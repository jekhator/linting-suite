"""Checker for R010: Legacy typing aliases for abstract base classes."""

import ast

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.rules import RuleSeverity, Violation


class R010Checker(BaseChecker):
    """Check for legacy typing.* ABCs that should use collections.abc."""

    LEGACY_TO_MODERN = dict(const.R010_LEGACY_TO_MODERN)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit 'from' imports to find typing.* ABC imports."""
        if node.module != const.MODULE_TYPING:
            self.generic_visit(node)
            return

        for alias in node.names:
            imported_name = alias.name
            if imported_name in self.LEGACY_TO_MODERN:
                if self.is_suppressed(node, const.RULE_ID_R010):
                    self.generic_visit(node)
                    return

                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R010,
                        severity=RuleSeverity.MEDIUM,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R010_LEGACY_IMPORT.format(name=imported_name),
                    )
                )

        self.generic_visit(node)
