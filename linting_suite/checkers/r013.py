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

    def _check_signature(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> None:
        """Check signature formatting per P14 calibration."""
        params_after_self = self._get_params_after_self(node.args)

        if len(params_after_self) <= const.R013_MIN_PARAMETERS:
            return

        if node.lineno == node.end_lineno:
            return

        if self._is_classmethod(node):
            return

        if not self._is_handler_method(node.name):
            return

        self._check_handler_signature(node, params_after_self)

    def _get_params_after_self(self, args: ast.arguments) -> list[ast.arg]:
        """Extract regular parameters after self/cls (excluding *args, **kwargs)."""
        params = []
        if len(args.args) > 0:
            params = args.args[1:]
        params += args.posonlyargs + args.kwonlyargs
        return params

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

    def _check_handler_signature(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, params: list[ast.arg]
    ) -> None:
        """Check handler signature for proper grouping (2-5 per line)."""
        param_lines: dict[int, list[str]] = {}
        for param in params:
            line = param.lineno  # type: ignore[union-attr]
            if line not in param_lines:
                param_lines[line] = []
            param_lines[line].append(param.arg)

        sorted_lines = sorted(param_lines.items())

        for line_num, param_names in sorted_lines:
            param_count = len(param_names)
            if param_count > const.R013_MAX_PARAMETERS_PER_LINE:
                file = str(self.file_path)
                message = const.MSG_R013_HANDLER_LINE.format(count=param_count)
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R013,
                        severity=RuleSeverity.INFO,
                        file=file,
                        line=line_num,
                        col=0,
                        message=message,
                    )
                )
