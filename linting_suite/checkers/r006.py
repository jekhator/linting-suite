"""Checker for R006: typing.Any in signature."""

import ast

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.inspection import AnnotationInspector, PathClassifier
from linting_suite.rules import RuleSeverity, Violation


class R006Checker(BaseChecker):
    """Check for typing.Any in service-layer function signatures."""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        if not PathClassifier.is_service_path(self.file_path, self.config.r006_paths):
            self.generic_visit(node)
            return

        if self.is_suppressed(node, const.RULE_ID_R006):
            self.generic_visit(node)
            return

        for argument in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            if argument.annotation and AnnotationInspector.contains_any(argument.annotation):
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R006,
                        severity=RuleSeverity.HIGH,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R006_PARAMETER.format(name=node.name),
                    )
                )
                return

        if node.args.vararg and node.args.vararg.annotation:
            if AnnotationInspector.contains_any(node.args.vararg.annotation):
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R006,
                        severity=RuleSeverity.HIGH,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R006_VARARGS.format(name=node.name),
                    )
                )
                return

        if node.args.kwarg and node.args.kwarg.annotation:
            if AnnotationInspector.contains_any(node.args.kwarg.annotation):
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R006,
                        severity=RuleSeverity.HIGH,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R006_KWARGS.format(name=node.name),
                    )
                )
                return

        if node.returns and AnnotationInspector.contains_any(node.returns):
            self.violations.append(
                Violation(
                    rule_id=const.RULE_ID_R006,
                    severity=RuleSeverity.HIGH,
                    file=str(self.file_path),
                    line=node.lineno,
                    col=node.col_offset,
                    message=const.MSG_R006_RETURN.format(name=node.name),
                )
            )

        self.generic_visit(node)
