"""Checker for R004: Module-level function without exception tag."""

import ast
from pathlib import Path

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.config._config import Config
from linting_suite.inspection import PathClassifier
from linting_suite.rules import RuleSeverity, Violation


class R004Checker(BaseChecker):
    """Check for module-level functions without exception tags (auto-detects class-method wrappers)."""

    def __init__(self, file_path: Path, source: str, config: Config):
        super().__init__(file_path, source, config)
        self.in_service_file = False
        self.in_service_file = PathClassifier.is_service_path(
            file_path, config.service_paths
        )

    def visit_Module(self, node: ast.Module) -> None:
        """Visit module to find top-level function defs."""
        if not self.in_service_file:
            return

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if self.is_suppressed(item, const.RULE_ID_R004):
                    continue
                if not self._has_exception_tag(
                    item
                ) and not self._is_class_method_wrapper(item):
                    self.violations.append(
                        Violation(
                            rule_id=const.RULE_ID_R004,
                            severity=RuleSeverity.HIGH,
                            file=str(self.file_path),
                            line=item.lineno,
                            col=item.col_offset,
                            message=const.MSG_R004_NO_TAG.format(name=item.name),
                        )
                    )

    def _is_class_method_wrapper(self, node: ast.FunctionDef) -> bool:
        """Check if function body delegates to class methods (auto-detected wrapper pattern)."""
        for statement in node.body:
            if isinstance(statement, ast.Return) and statement.value:
                if self._is_method_delegation(statement.value):
                    return True
        return False

    def _is_method_delegation(self, node: ast.expr) -> bool:
        """Check if node is a method call (attribute access followed by call)."""
        if isinstance(node, ast.Call):
            function = node.func
            if isinstance(function, ast.Attribute):
                return True
        return False

    def _has_exception_tag(self, node: ast.FunctionDef) -> bool:
        """Check if function has a documented exception tag."""
        comment = self.get_comment_text(node.lineno)
        for tag in self.config.exception_tags:
            if tag in comment:
                return True

        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            docstring = node.body[0].value.value
            for tag in self.config.exception_tags:
                if tag in docstring:
                    return True

        return False
