"""Checker for R005: Validator not using DTO.from_dict() pattern."""

import ast

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.rules import RuleSeverity, Violation


class R005Checker(BaseChecker):
    """Check for validators using DTO.from_dict() pattern."""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        if not node.name.startswith(const.VALIDATOR_PREFIX):
            self.generic_visit(node)
            return

        if self.is_suppressed(node, const.RULE_ID_R005):
            self.generic_visit(node)
            return

        has_payload_param = any(
            argument.arg == const.PARAMETER_PAYLOAD for argument in node.args.args + node.args.kwonlyargs
        )

        if not has_payload_param:
            self.generic_visit(node)
            return

        has_from_dict = self._has_from_dict_call(node)
        has_validation_error = self._has_validation_error(node)

        if not (has_from_dict or has_validation_error):
            file = str(self.file_path)
            message = const.MSG_R005_NO_FROM_DICT.format(name=node.name)
            self.violations.append(
                Violation(
                    rule_id=const.RULE_ID_R005, severity=RuleSeverity.LOW, file=file,
                    line=node.lineno, col=node.col_offset, message=message
                )
            )

        self.generic_visit(node)

    def _has_from_dict_call(self, node: ast.FunctionDef) -> bool:
        """Check if function body calls .from_dict()."""
        for item in ast.walk(node):
            if isinstance(item, ast.Call):
                if isinstance(item.func, ast.Attribute):
                    if item.func.attr == const.METHOD_FROM_DICT:
                        return True
        return False

    def _has_validation_error(self, node: ast.FunctionDef) -> bool:
        """Check if function raises ValidationError."""
        for item in ast.walk(node):
            if isinstance(item, ast.Raise):
                if isinstance(item.exc, ast.Call):
                    if isinstance(item.exc.func, ast.Name):
                        if const.VALIDATION_ERROR_NAME in item.exc.func.id:
                            return True
        return False
