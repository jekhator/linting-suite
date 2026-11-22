"""Checker for R011: String literal at raise site."""

import ast

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.inspection import PathClassifier
from linting_suite.rules import RuleSeverity, Violation


class R011Checker(BaseChecker):
    """
    Check for string literals in raise exception arguments.

    Enforces that exception message arguments must be references to ERR_*
    constants (via const.* or similar), never inline string literals or
    f-strings.
    """

    def visit_Raise(self, node: ast.Raise) -> None:
        """Visit raise statements to find string literal messages."""
        if PathClassifier.is_test_file(self.file_path):
            self.generic_visit(node)
            return

        if self._is_constant_module(self.file_path):
            self.generic_visit(node)
            return

        if node.exc is None:
            self.generic_visit(node)
            return

        if not isinstance(node.exc, ast.Call):
            self.generic_visit(node)
            return

        if self.is_suppressed(node, const.RULE_ID_R011):
            self.generic_visit(node)
            return

        has_literal = self._check_for_string_literals(node.exc)
        if has_literal:
            self.violations.append(
                Violation(
                    rule_id=const.RULE_ID_R011,
                    severity=RuleSeverity.HIGH,
                    file=str(self.file_path),
                    line=node.lineno,
                    col=node.col_offset,
                    message=const.MSG_R011_RAISE_LITERAL,
                )
            )

        self.generic_visit(node)

    def _is_constant_module(self, file_path) -> bool:
        """Check if file is a constants module."""
        return (
            file_path.name == const.BASENAME_CONSTANTS
            or file_path.name.endswith(const.BASENAME_CONST_SUFFIX)
            or const.CONSTANTS_PATH_WORD in str(file_path)
        )

    def _check_for_string_literals(self, call_node: ast.Call) -> bool:
        """
        Check if a Call node contains string literal arguments.

        Returns True if any positional or keyword argument is:
        - An ast.Constant with string value
        - An ast.JoinedStr (f-string)
        """
        for argument in call_node.args:
            if self._is_string_literal(argument):
                return True

        for keyword in call_node.keywords:
            if self._is_string_literal(keyword.value):
                return True

        return False

    def _is_string_literal(self, node: ast.expr) -> bool:
        """Check if a node is a string literal or f-string."""
        if isinstance(node, ast.Constant):
            return isinstance(node.value, str)
        if isinstance(node, ast.JoinedStr):
            return True
        return False
