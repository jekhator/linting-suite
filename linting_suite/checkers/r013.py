"""Checker for R013: Signature grouping (P14 - compact method signatures)."""

import ast

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.rules import RuleSeverity, Violation


class R013Checker(BaseChecker):
    """
    Check compact method signatures per P14 calibration.

    Per 2026-07-23 calibration:
    - Handler methods (log_*, record_*, wrap_*): 2-5 params per line
    - Factory classmethods (@classmethod): NEVER flag (any grouping OK)
    - Short signatures (<=3 params): no enforcement
    """

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions to check signature grouping."""
        if self.is_suppressed(node, const.RULE_ID_R013):
            self.generic_visit(node)
            return

        if node.lineno is None or node.end_lineno is None:
            self.generic_visit(node)
            return

        self._check_signature(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definitions to check signature grouping."""
        if self.is_suppressed(node, const.RULE_ID_R013):
            self.generic_visit(node)
            return

        if node.lineno is None or node.end_lineno is None:
            self.generic_visit(node)
            return

        self._check_signature(node)
        self.generic_visit(node)

    def _check_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Check signature formatting per P14 calibration."""
        parameters_after_self = self._get_params_after_self(node.args)

        if len(parameters_after_self) <= const.R013_MIN_PARAMETERS:
            return

        if node.lineno == node.end_lineno:
            return

        if self._is_classmethod(node):
            return

        if not self._is_handler_method(node.name):
            return

        self._check_handler_signature(node, parameters_after_self)

    def _get_params_after_self(self, args: ast.arguments) -> list[ast.arg]:
        """Extract regular parameters after self/cls (excluding *args, **kwargs)."""
        parameters = []
        if len(args.args) > 0:
            parameters = args.args[1:]
        parameters += args.posonlyargs + args.kwonlyargs
        return parameters

    def _is_classmethod(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Check if function is a classmethod (never flag)."""
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == const.DECORATOR_CLASSMETHOD:
                return True
        return False

    def _is_handler_method(self, method_name: str) -> bool:
        """Check if method is a handler (log_*, record_*, wrap_*)."""
        return (
            method_name.startswith(const.R013_HANDLER_PREFIX_LOG)
            or method_name.startswith(const.R013_HANDLER_PREFIX_RECORD)
            or method_name.startswith(const.R013_HANDLER_PREFIX_WRAP)
        )

    def _check_handler_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef, parameters: list[ast.arg]) -> None:
        """Check handler signature for proper grouping (2-5 per line)."""
        parameter_lines: dict[int, list[str]] = {}
        for parameter in parameters:
            line = parameter.lineno  # type: ignore[union-attr]
            if line not in parameter_lines:
                parameter_lines[line] = []
            parameter_lines[line].append(parameter.arg)

        sorted_lines = sorted(parameter_lines.items())

        for line_number, parameter_names in sorted_lines:
            parameter_count = len(parameter_names)
            if parameter_count > const.R013_MAX_PARAMETERS_PER_LINE:
                file = str(self.file_path)
                message = const.MSG_R013_HANDLER_LINE.format(count=parameter_count)
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R013, severity=RuleSeverity.INFO, file=file,
                        line=line_number, col=0, message=message
                    )
                )
