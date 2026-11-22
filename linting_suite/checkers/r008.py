"""Checker for R008: Bare module-level test function."""

import ast

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.inspection import PathClassifier
from linting_suite.rules import RuleSeverity, Violation


class R008Checker(BaseChecker):
    """Check for bare module-level test functions."""

    def visit_Module(self, node: ast.Module) -> None:
        """Visit module to find top-level test functions."""
        if not PathClassifier.is_test_file(self.file_path):
            return

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if item.name.startswith(const.TEST_FUNCTION_PREFIX):
                    if self.is_suppressed(item, const.RULE_ID_R008):
                        continue

                    file = str(self.file_path)
                    message = const.MSG_R008_TEST_FUNCTION.format(name=item.name)
                    self.violations.append(
                        Violation(
                            rule_id=const.RULE_ID_R008, severity=RuleSeverity.MEDIUM, file=file,
                            line=item.lineno, col=item.col_offset, message=message
                        )
                    )
