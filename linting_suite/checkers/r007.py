"""Checker for R007: Pytest fixtures defined outside conftest.py."""

import ast

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.inspection import PathClassifier
from linting_suite.rules import RuleSeverity, Violation


class R007Checker(BaseChecker):
    """Check for pytest fixtures defined outside conftest.py."""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions to find pytest fixtures."""
        if not PathClassifier.is_test_file(self.file_path):
            self.generic_visit(node)
            return

        if self.file_path.name == const.BASENAME_CONFTEST:
            self.generic_visit(node)
            return

        for decorator in node.decorator_list:
            if self._is_pytest_fixture_decorator(decorator):
                if self.is_suppressed(node, const.RULE_ID_R007):
                    continue

                file = str(self.file_path)
                message = const.MSG_R007_FIXTURE.format(name=node.name)
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R007, severity=RuleSeverity.MEDIUM, file=file,
                        line=node.lineno, col=node.col_offset, message=message
                    )
                )

        self.generic_visit(node)

    def _is_pytest_fixture_decorator(self, decorator: ast.expr) -> bool:
        """Check if decorator is @pytest.fixture."""
        if isinstance(decorator, ast.Name):
            return decorator.id == const.DECORATOR_FIXTURE
        elif isinstance(decorator, ast.Attribute):
            if decorator.attr == const.DECORATOR_FIXTURE:
                if isinstance(decorator.value, ast.Name):
                    if decorator.value.id == const.MODULE_PYTEST:
                        return True
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id == const.DECORATOR_FIXTURE
            elif isinstance(decorator.func, ast.Attribute):
                if decorator.func.attr == const.DECORATOR_FIXTURE:
                    if isinstance(decorator.func.value, ast.Name):
                        if decorator.func.value.id == const.MODULE_PYTEST:
                            return True
        return False
